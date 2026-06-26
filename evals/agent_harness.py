from __future__ import annotations

import asyncio
import hashlib
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from graders import combine_with_rubric, deterministic_grade, rubric_grade_with_openai
from operator_sim import run_operator_turn
from extractor import OpenAISemanticActionExtractor
from schemas import RunResult, Scenario, TurnRecord, Variant
from world import EvalWorld


def skill_text(repo_root: Path, skill: str) -> tuple[str, str]:
    path = repo_root / "skills" / skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, digest


def build_instructions(repo_root: Path, scenario: Scenario, variant: Variant) -> tuple[str, str | None]:
    if variant == "without_skill":
        return "", None
    text, digest = skill_text(repo_root, scenario.skill)
    return "# Loaded Skill\n\n" + text, digest


async def run_scenario(
    repo_root: Path,
    scenario: Scenario,
    variant: Variant,
    model: str,
    rubric_model: str | None = None,
) -> RunResult:
    instructions, digest = build_instructions(repo_root, scenario, variant)
    world = EvalWorld(scenario)
    messages: list[dict[str, str]] = [{"role": "user", "content": scenario.initial_user_message}]
    timeout_seconds = _configured_timeout_seconds()
    assistant_reasoning_effort = _configured_reasoning_effort("OPENAI_EVAL_REASONING_EFFORT", default="minimal")
    extractor_reasoning_effort = _configured_reasoning_effort(
        "OPENAI_EVAL_EXTRACTOR_REASONING_EFFORT",
        default=assistant_reasoning_effort,
    )
    assistant_max_tokens = _configured_positive_int("OPENAI_EVAL_MAX_TOKENS", default=1200)
    extractor_max_output_tokens = _configured_positive_int("OPENAI_EVAL_EXTRACTOR_MAX_OUTPUT_TOKENS", default=2048)
    assistant_verbosity = _configured_verbosity()
    result = RunResult(
        run_id=str(uuid4()),
        scenario_id=scenario.id,
        skill=scenario.skill,
        variant=variant,
        model=model,
        scenario_version=scenario.version,
        skill_sha256=digest,
        model_settings={
            "assistant_model": model,
            "assistant_reasoning_effort": assistant_reasoning_effort,
            "assistant_max_tokens": assistant_max_tokens,
            "assistant_verbosity": assistant_verbosity,
            "rubric_model": rubric_model,
            "semantic_extractor_provider": "openai",
            "semantic_extractor_model": os.environ.get("OPENAI_EVAL_EXTRACTOR_MODEL") or model,
            "semantic_extractor_reasoning_effort": extractor_reasoning_effort,
            "semantic_extractor_max_output_tokens": extractor_max_output_tokens,
            "timeout_seconds": timeout_seconds,
        },
    )
    agent = _build_agent(
        model=model,
        instructions=instructions,
        reasoning_effort=assistant_reasoning_effort,
        max_tokens=assistant_max_tokens,
        verbosity=assistant_verbosity,
    )
    semantic_extractor = OpenAISemanticActionExtractor(
        model=str(result.model_settings["semantic_extractor_model"]),
        timeout_seconds=timeout_seconds,
        reasoning_effort=extractor_reasoning_effort,
        max_output_tokens=extractor_max_output_tokens,
    )
    started = time.perf_counter()

    for turn_index in range(1, scenario.max_turns + 1):
        assistant_text, usage = await _run_agent_turn(agent, messages)
        _merge_usage(result.token_usage, usage)
        operator_text, actions, extracted_actions = run_operator_turn(
            assistant_text,
            scenario,
            world,
            semantic_extractor=semantic_extractor,
        )
        messages.append({"role": "assistant", "content": assistant_text})
        messages.append({"role": "user", "content": operator_text})

        result.transcript.append(
            TurnRecord(
                turn=turn_index,
                assistant=assistant_text,
                operator=operator_text,
                actions=actions,
                extracted_actions=extracted_actions,
                events=sorted(world.events),
                milestones=sorted(world.milestones),
            )
        )

        if _looks_final(assistant_text):
            result.final_output = assistant_text
            break

    result.completed_at = datetime.now(timezone.utc)
    result.latency_seconds = round(time.perf_counter() - started, 4)
    result.milestones = sorted(world.milestones)
    result.events = sorted(world.events)
    deterministic = deterministic_grade(scenario, result)
    result.deterministic_grade = deterministic
    rubric = rubric_grade_with_openai(rubric_model, scenario, result) if rubric_model else None
    result.rubric_grade = rubric
    result.deterministic_grade = combine_with_rubric(
        deterministic,
        rubric,
        efficiency=max(0.0, 1.0 - (len(result.transcript) / max(1, scenario.max_turns + 1))),
    )
    if not result.final_output and result.transcript:
        result.final_output = result.transcript[-1].assistant
    return result


def run_scripted_scenario(repo_root: Path, scenario: Scenario, variant: Variant) -> RunResult:
    _, digest = build_instructions(repo_root, scenario, variant)
    script = scenario.assistant_scripts.get(variant)
    if not script:
        raise ValueError(f"Scenario {scenario.id} has no assistant_scripts entry for {variant}")

    world = EvalWorld(scenario)
    result = RunResult(
        run_id=str(uuid4()),
        scenario_id=scenario.id,
        skill=scenario.skill,
        variant=variant,
        model="scripted",
        scenario_version=scenario.version,
        skill_sha256=digest,
        model_settings={
            "assistant_model": "scripted",
            "semantic_extractor_provider": "rule_based",
            "semantic_extractor_model": None,
        },
    )
    started = time.perf_counter()
    for turn_index, assistant_text in enumerate(script, start=1):
        operator_text, actions, extracted_actions = run_operator_turn(assistant_text, scenario, world)
        result.transcript.append(
            TurnRecord(
                turn=turn_index,
                assistant=assistant_text,
                operator=operator_text,
                actions=actions,
                extracted_actions=extracted_actions,
                events=sorted(world.events),
                milestones=sorted(world.milestones),
            )
        )

    result.completed_at = datetime.now(timezone.utc)
    result.latency_seconds = round(time.perf_counter() - started, 4)
    result.milestones = sorted(world.milestones)
    result.events = sorted(world.events)
    result.final_output = script[-1]
    deterministic = deterministic_grade(scenario, result)
    result.deterministic_grade = combine_with_rubric(
        deterministic,
        rubric=None,
        efficiency=max(0.0, 1.0 - (len(result.transcript) / max(1, scenario.max_turns + 1))),
    )
    return result


def _build_agent(
    model: str,
    instructions: str,
    reasoning_effort: str = "minimal",
    max_tokens: int = 1200,
    verbosity: str = "low",
):
    from agents import Agent, ModelSettings

    return Agent(
        name="Redis Operations Assistant",
        instructions=instructions,
        model=model,
        model_settings=ModelSettings(
            reasoning={"effort": reasoning_effort},
            max_tokens=max_tokens,
            verbosity=verbosity,  # type: ignore[arg-type]
        ),
    )


async def _run_agent_turn(agent, messages: list[dict[str, str]]) -> tuple[str, dict[str, int]]:
    from agents import Runner

    run_result = await Runner.run(agent, input=messages)
    return str(run_result.final_output), _extract_usage(run_result)


def _extract_usage(run_result) -> dict[str, int]:
    usage: dict[str, int] = {}
    for raw_response in getattr(run_result, "raw_responses", []) or []:
        raw_usage = getattr(raw_response, "usage", None)
        if raw_usage is None:
            continue
        for key in ("input_tokens", "output_tokens", "total_tokens"):
            value = getattr(raw_usage, key, None)
            if isinstance(value, int):
                usage[key] = usage.get(key, 0) + value
    return usage


def _merge_usage(total: dict[str, int], update: dict[str, int]) -> None:
    for key, value in update.items():
        total[key] = total.get(key, 0) + value


def _looks_final(text: str) -> bool:
    lower = re.sub(r"[*_`>#-]+", " ", text.lower())
    lower = re.sub(r"\s+", " ", lower).strip()
    final_patterns = (
        r"\bfinal answer\b",
        r"\bfinal summary\b",
        r"^summary\s*:",
        r"^incident summary\s*:",
        r"^resolution summary\s*:",
        r"^resolved[\s.:]",
        r"^confirmed resolved[\s.:]",
        r"^do not proceed\b(?!\s+if\b)",
        r"^do not delete\b(?!\s+if\b)",
        r"^stop here[\s.:]",
        r"\bescalation packet\b",
    )
    return any(re.search(pattern, lower) for pattern in final_patterns)


def run_async(coro):
    return asyncio.run(coro)


def configured_model() -> str:
    model = os.environ.get("OPENAI_EVAL_MODEL")
    if not model:
        raise SystemExit("OPENAI_EVAL_MODEL is required for non-dry-run evals.")
    return model


def _configured_timeout_seconds() -> float:
    raw = os.environ.get("OPENAI_EVAL_TIMEOUT_SECONDS", "60")
    try:
        timeout = float(raw)
    except ValueError as exc:
        raise SystemExit(f"OPENAI_EVAL_TIMEOUT_SECONDS must be numeric, got {raw!r}.") from exc
    if timeout <= 0:
        raise SystemExit("OPENAI_EVAL_TIMEOUT_SECONDS must be greater than zero.")
    return timeout


def _configured_positive_int(name: str, default: int) -> int:
    raw = os.environ.get(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise SystemExit(f"{name} must be an integer, got {raw!r}.") from exc
    if value <= 0:
        raise SystemExit(f"{name} must be greater than zero.")
    return value


def _configured_reasoning_effort(name: str, default: str) -> str:
    value = os.environ.get(name, default).strip().lower()
    allowed = {"minimal", "low", "medium", "high"}
    if value not in allowed:
        raise SystemExit(f"{name} must be one of {sorted(allowed)}, got {value!r}.")
    return value


def _configured_verbosity() -> str:
    value = os.environ.get("OPENAI_EVAL_VERBOSITY", "low").strip().lower()
    allowed = {"low", "medium", "high"}
    if value not in allowed:
        raise SystemExit(f"OPENAI_EVAL_VERBOSITY must be one of {sorted(allowed)}, got {value!r}.")
    return value
