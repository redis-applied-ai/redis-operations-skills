from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from agent_harness import configured_model, run_async, run_scenario, run_scripted_scenario
from graders import build_summary
from schemas import RunResult, Scenario, ScenarioFile


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Redis operations skill evals.")
    parser.add_argument("--scenario", default="all", help="Scenario id to run, or all.")
    parser.add_argument("--skill", default=None, help="Skill name to run, or all skills.")
    parser.add_argument("--variant", default="both", choices=["with_skill", "without_skill", "both"])
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--provider", default=None, choices=["fixture", "openai"])
    parser.add_argument("--rubric-model", default=None, help="Optional OpenAI model for rubric grading.")
    parser.add_argument("--dry-run", action="store_true", help="Validate scenarios without model calls.")
    parser.add_argument("--scripted", action="store_true", help="Run assistant_scripts fixtures instead of model calls.")
    parser.add_argument("--artifacts-dir", default="evals/artifacts")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    scenarios = load_scenarios(repo_root / "evals" / "scenarios")
    selected = [scenario for scenario in scenarios if args.scenario == "all" or scenario.id == args.scenario]
    if args.skill:
        selected = [scenario for scenario in selected if scenario.skill == args.skill]
    if not selected:
        raise SystemExit("No scenarios matched the requested filters.")

    if args.dry_run:
        print(f"validated {len(selected)} scenario(s)")
        for scenario in selected:
            print(f"{scenario.id}\t{scenario.skill}\tmax_turns={scenario.max_turns}")
        return

    scripted = args.scripted or args.provider == "fixture" or args.provider is None
    model = "scripted" if scripted else configured_model()
    variants = ["with_skill", "without_skill"] if args.variant == "both" else [args.variant]
    artifact_root = Path(args.artifacts_dir) / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    artifact_root.mkdir(parents=True, exist_ok=True)

    results: list[RunResult] = []
    for scenario in selected:
        for variant in variants:
            for _ in range(args.repetitions):
                if scripted:
                    result = run_scripted_scenario(
                        repo_root=repo_root,
                        scenario=scenario,
                        variant=variant,  # type: ignore[arg-type]
                    )
                else:
                    result = run_async(
                        run_scenario(
                            repo_root=repo_root,
                            scenario=scenario,
                            variant=variant,  # type: ignore[arg-type]
                            model=model,
                            rubric_model=args.rubric_model,
                        )
                    )
                results.append(result)
                write_run_artifacts(artifact_root, result)

    summary = build_summary(results, model=model)
    (artifact_root / "summary.json").write_text(summary.model_dump_json(indent=2), encoding="utf-8")
    (artifact_root / "summary.md").write_text(render_summary_markdown(summary), encoding="utf-8")
    print(f"wrote artifacts to {artifact_root}")


def load_scenarios(path: Path) -> list[Scenario]:
    scenarios: list[Scenario] = []
    for scenario_file in sorted(path.glob("*.yaml")):
        data = yaml.safe_load(scenario_file.read_text(encoding="utf-8"))
        parsed = ScenarioFile.model_validate(data)
        scenarios.extend(parsed.scenarios)
    return scenarios


def write_run_artifacts(root: Path, result: RunResult) -> None:
    run_dir = root / result.scenario_id / result.variant
    run_dir.mkdir(parents=True, exist_ok=True)
    json_path = run_dir / f"{result.run_id}.json"
    jsonl_path = run_dir / f"{result.run_id}.jsonl"
    json_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for turn in result.transcript:
            handle.write(json.dumps(turn.model_dump(mode="json")) + "\n")


def render_summary_markdown(summary) -> str:
    lines = [
        "# Skill Eval Summary",
        "",
        f"Generated: {summary.generated_at.isoformat()}",
        f"Model: {summary.model}",
        "",
        "| Scenario | Skill | Variant | Runs | Pass rate | Pass^k | Critical safety violations | Median turns | Total tokens | Avg latency |",
        "| --- | --- | --- | ---: | ---: | :---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary.rows:
        lines.append(
            f"| {row.scenario_id} | {row.skill} | {row.variant} | {row.runs} | "
            f"{row.pass_rate:.2f} | {'yes' if row.pass_k else 'no'} | {row.critical_safety_violations} | "
            f"{row.median_turns:.1f} | {row.total_tokens} | {_format_optional(row.average_latency_seconds)} |"
        )
    lines.extend(
        [
            "",
            "## Skill Lift",
            "",
            "| Scenario | Skill | With-skill pass rate | Without-skill pass rate | Lift | Token overhead | Latency overhead |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary.lift_rows:
        lines.append(
            f"| {row.scenario_id} | {row.skill} | {_format_optional(row.with_skill_pass_rate)} | "
            f"{_format_optional(row.without_skill_pass_rate)} | {_format_optional(row.skill_lift)} | "
            f"{row.token_overhead if row.token_overhead is not None else 'n/a'} | "
            f"{_format_optional(row.latency_overhead_seconds)} |"
        )
    lines.append("")
    return "\n".join(lines)


def _format_optional(value) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


if __name__ == "__main__":
    main()
