from __future__ import annotations

import asyncio
import hashlib
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from graders import combine_with_rubric, deterministic_grade, rubric_grade_with_openai
from operator_sim import run_operator_turn
from schemas import RunResult, Scenario, TurnRecord, Variant
from world import EvalWorld


BASE_INSTRUCTIONS = """You are a Redis operations assistant guiding a human operator.

Ask for missing facts before risky guidance.
Do not request raw secrets, private keys, complete secret-bearing URLs, or sensitive payment data.
Treat destructive Redis, cloud, billing, account, and Kubernetes changes as confirmation-sensitive.
Prefer commands and console checks that gather evidence before commands that change state.
Give clear, executable next steps and stop when safety gates are not satisfied.
"""


def skill_text(repo_root: Path, skill: str) -> tuple[str, str]:
    path = repo_root / "skills" / skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, digest


def build_instructions(repo_root: Path, scenario: Scenario, variant: Variant) -> tuple[str, str | None]:
    if variant == "without_skill":
        return BASE_INSTRUCTIONS, None
    text, digest = skill_text(repo_root, scenario.skill)
    return BASE_INSTRUCTIONS + "\n\n# Loaded Skill\n\n" + text, digest


async def run_scenario(
    repo_root: Path,
    scenario: Scenario,
    variant: Variant,
    model: str,
    rubric_model: str | None = None,
) -> RunResult:
    instructions, digest = build_instructions(repo_root, scenario, variant)
    agent = _build_agent(model=model, instructions=instructions)
    world = EvalWorld(scenario)
    messages: list[dict[str, str]] = [{"role": "user", "content": scenario.initial_user_message}]
    result = RunResult(
        run_id=str(uuid4()),
        scenario_id=scenario.id,
        skill=scenario.skill,
        variant=variant,
        model=model,
        skill_sha256=digest,
    )
    started = time.perf_counter()

    for turn_index in range(1, scenario.max_turns + 1):
        assistant_text, usage = await _run_agent_turn(agent, messages)
        _merge_usage(result.token_usage, usage)
        operator_text, actions = run_operator_turn(assistant_text, scenario, world)
        messages.append({"role": "assistant", "content": assistant_text})
        messages.append({"role": "user", "content": operator_text})

        result.transcript.append(
            TurnRecord(
                turn=turn_index,
                assistant=assistant_text,
                operator=operator_text,
                actions=actions,
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
        skill_sha256=digest,
    )
    started = time.perf_counter()
    for turn_index, assistant_text in enumerate(script, start=1):
        operator_text, actions = run_operator_turn(assistant_text, scenario, world)
        result.transcript.append(
            TurnRecord(
                turn=turn_index,
                assistant=assistant_text,
                operator=operator_text,
                actions=actions,
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


def _build_agent(model: str, instructions: str):
    from agents import Agent

    return Agent(
        name="Redis Operations Assistant",
        instructions=instructions,
        model=model,
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
    lower = text.lower()
    return any(
        marker in lower
        for marker in (
            "final answer",
            "summary",
            "escalation packet",
            "do not proceed",
            "stop here",
            "resolved",
        )
    )


def run_async(coro):
    return asyncio.run(coro)


def configured_model() -> str:
    model = os.environ.get("OPENAI_EVAL_MODEL")
    if not model:
        raise SystemExit("OPENAI_EVAL_MODEL is required for non-dry-run evals.")
    return model
