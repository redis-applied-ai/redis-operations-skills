from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent_harness import _looks_final, run_scripted_scenario
from schemas import OperatorProfile, Scenario


def test_unresolved_text_is_not_terminal() -> None:
    text = "Confirm there are no unresolved alerts before patching the next node."

    assert not _looks_final(text)


def test_conditional_do_not_proceed_is_not_terminal() -> None:
    text = "Do not proceed if another node is still in maintenance."

    assert not _looks_final(text)


def test_resolved_summary_is_terminal() -> None:
    text = "Resolved. The stale Secret caused the Redis auth failure."

    assert _looks_final(text)


def test_incident_summary_is_terminal() -> None:
    text = "Incident summary: the app used an old CA bundle after certificate rotation."

    assert _looks_final(text)


def test_scripted_run_records_artifact_model_settings_and_typed_actions() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    scenario = Scenario(
        id="artifact-schema-test",
        version="2026-06-23",
        skill="redis-cloud-delete-database",
        initial_user_message="test",
        operator_profile=OperatorProfile(role="operator", behavior="answer"),
        assistant_scripts={"with_skill": ["Final summary: no destructive action needed."]},
    )

    result = run_scripted_scenario(repo_root, scenario, "with_skill")

    assert result.scenario_version == "2026-06-23"
    assert result.model_settings["semantic_extractor_provider"] == "rule_based"
    assert result.skill_sha256
    assert result.transcript[0].extracted_actions
