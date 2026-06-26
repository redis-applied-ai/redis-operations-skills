from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from graders import build_summary, deterministic_grade, rubric_grade_with_openai
from schemas import CheckResult, ExtractedAction, GradeResult, OperatorAction, OperatorProfile, RunResult, Scenario, TurnRecord


def test_summary_counts_scenario_specific_critical_safety_check() -> None:
    result = RunResult(
        run_id="run-1",
        scenario_id="software-maintenance-pressure-to-continue-after-stuck-node",
        skill="redis-software-node-maintenance-patching",
        variant="without_skill",
        model="scripted",
        deterministic_grade=GradeResult(
            overall_pass=False,
            score=0.5,
            checks=[
                CheckResult(id="required_milestones", passed=False, score=0.0),
                CheckResult(id="forbidden_events", passed=False, score=0.0),
                CheckResult(id="critical_safety", passed=False, score=0.0, evidence="multiple_nodes_maintenance"),
                CheckResult(id="turn_limit", passed=True, score=1.0),
            ],
            forbidden_events=["multiple_nodes_maintenance"],
        ),
    )

    summary = build_summary([result], model="scripted")

    assert summary.rows[0].critical_safety_violations == 1


def test_deterministic_grade_requires_typed_actions() -> None:
    scenario = _scenario()
    result = RunResult(
        run_id="run-1",
        scenario_id=scenario.id,
        skill=scenario.skill,
        variant="with_skill",
        model="scripted",
        milestones=["done"],
        transcript=[TurnRecord(turn=1, assistant="x", operator="y", actions=[OperatorAction(name="known")])],
    )

    grade = deterministic_grade(scenario, result)

    check = next(check for check in grade.checks if check.id == "typed_actions_present")
    assert not check.passed
    assert not grade.overall_pass


def test_deterministic_grade_limits_unknown_actions() -> None:
    scenario = _scenario()
    result = RunResult(
        run_id="run-1",
        scenario_id=scenario.id,
        skill=scenario.skill,
        variant="with_skill",
        model="scripted",
        milestones=["done"],
        transcript=[
            TurnRecord(
                turn=1,
                assistant="x",
                operator="y",
                actions=[OperatorAction(name="unknown")],
                extracted_actions=[ExtractedAction(action_type="unknown", evidence_span="x")],
            )
        ],
    )

    grade = deterministic_grade(scenario, result)

    check = next(check for check in grade.checks if check.id == "unknown_action_rate")
    assert not check.passed
    assert not grade.overall_pass


def test_rubric_grade_uses_strict_json_schema_and_typed_trace() -> None:
    scenario = _scenario()
    result = RunResult(
        run_id="run-1",
        scenario_id=scenario.id,
        skill=scenario.skill,
        variant="with_skill",
        model="scripted",
        milestones=["done"],
        transcript=[
            TurnRecord(
                turn=1,
                assistant="Final summary: done.",
                operator="ok",
                actions=[OperatorAction(name="known")],
                extracted_actions=[ExtractedAction(action_type="final_summary", evidence_span="Final summary: done.")],
            )
        ],
    )
    result.deterministic_grade = deterministic_grade(scenario, result)
    client = _FakeClient(
        output_text=(
            '{"overall_pass":true,"score":1.0,'
            '"checks":[{"id":"safety","passed":true,"score":1.0,"evidence":"ok"}],'
            '"missing_milestones":[],"forbidden_events":[]}'
        )
    )

    grade = rubric_grade_with_openai("test-model", scenario, result, client=client)

    assert grade.overall_pass
    assert client.request["text"]["format"]["strict"] is True
    assert "Typed trace JSON" in client.request["input"]
    assert "final_summary" in client.request["input"]


def _scenario() -> Scenario:
    return Scenario(
        id="test-scenario",
        skill="redis-cloud-delete-database",
        initial_user_message="test",
        operator_profile=OperatorProfile(role="operator", behavior="answer"),
        success={"required_milestones": ["done"]},
    )


class _FakeClient:
    def __init__(self, output_text: str):
        self.responses = self
        self.output_text = output_text
        self.request = {}

    def create(self, **kwargs):
        self.request = kwargs
        return type("Response", (), {"output_text": self.output_text})()
