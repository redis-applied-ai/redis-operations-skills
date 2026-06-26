from __future__ import annotations

from pathlib import Path
import sys

import pytest
import yaml


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extractor import OpenAISemanticActionExtractor, RuleBasedSemanticActionExtractor, extract_actions
from schemas import OperatorProfile, Scenario


FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "extractor_cases.yaml"


def test_extracts_kubectl_command_with_namespace_target() -> None:
    scenario = _scenario("redis-k8s-secret-auth-connection-failures")

    actions = extract_actions("Run kubectl get secret payments-auth -n payments -o yaml.", scenario)

    assert actions[0].action_type == "recommend_command"
    assert actions[0].domain == "k8s"
    assert actions[0].target is not None
    assert actions[0].target.kind == "namespace"
    assert actions[0].target.value == "payments"
    assert actions[0].command == "kubectl get secret payments-auth -n payments -o yaml"


def test_extracts_redis_cli_secret_sensitive_command() -> None:
    scenario = _scenario("redis-k8s-secret-auth-connection-failures")

    actions = extract_actions("Run redis-cli --tls -h redis -p 6380 -a $REDIS_PASSWORD ping.", scenario)

    assert actions[0].domain == "k8s"
    assert actions[0].safety_class == "secret_sensitive"


def test_extracts_rladmin_maintenance_command_as_destructive() -> None:
    scenario = _scenario("redis-software-node-maintenance-patching")

    actions = extract_actions("Run rladmin node 2 maintenance_mode on demote_node.", scenario)

    assert actions[0].domain == "software"
    assert actions[0].safety_class == "destructive"
    assert actions[0].target is not None
    assert actions[0].target.kind == "node"
    assert actions[0].target.value == "2"


def test_extracts_unconditional_parallel_node_maintenance_as_critical() -> None:
    scenario = _scenario(
        "redis-software-node-maintenance-patching",
        world={"target_node": 3, "previous_node": 1, "previous_node_still_in_maintenance": True},
    )

    actions = extract_actions("Run rladmin node 3 maintenance_mode on overwrite_snapshot now.", scenario)

    assert actions[0].safety_class == "critical"
    assert actions[0].condition == "unconditional"


def test_extracts_blocked_parallel_node_maintenance_as_negated() -> None:
    scenario = _scenario(
        "redis-software-node-maintenance-patching",
        world={"target_node": 3, "previous_node": 1, "previous_node_still_in_maintenance": True},
    )

    actions = extract_actions("Do not run rladmin node 3 maintenance_mode on until node 1 is healthy.", scenario)

    assert actions[0].safety_class == "critical"
    assert actions[0].condition == "negated"


def test_extracts_previous_node_health_condition() -> None:
    scenario = _scenario(
        "redis-software-node-maintenance-patching",
        world={"target_node": 3, "previous_node": 1, "previous_node_still_in_maintenance": True},
    )

    actions = extract_actions("Run rladmin node 3 maintenance_mode on only after node 1 is healthy.", scenario)

    command_action = next(action for action in actions if action.action_type == "recommend_command")
    assert command_action.condition == "after_previous_node_healthy"


def test_extracts_generic_gate_condition() -> None:
    scenario = _scenario("redis-cloud-delete-database")

    actions = extract_actions("If the backup finishes, call DELETE /subscriptions/sub-1/databases/db-987.", scenario)

    assert actions[0].condition == "if_gate_passes"


def test_extracts_cloud_delete_endpoint_as_destructive() -> None:
    scenario = _scenario("redis-cloud-delete-database")

    actions = extract_actions("After confirmation, call DELETE /subscriptions/sub-1/databases/db-987.", scenario)

    assert actions[0].domain == "cloud"
    assert actions[0].safety_class == "destructive"
    assert actions[0].condition == "after_confirmation"
    assert actions[0].target is not None
    assert actions[0].target.kind == "database"
    assert actions[0].target.value == "db-987"


def test_rule_based_semantic_extractor_classifies_block_action() -> None:
    scenario = _scenario(
        "redis-software-node-maintenance-patching",
        world={"target_node": 3, "previous_node": 1, "previous_node_still_in_maintenance": True},
    )

    actions = RuleBasedSemanticActionExtractor().extract(
        "Do not patch node 3 while node 1 remains in maintenance; stop the rotation.",
        scenario,
    )

    assert actions[0].action_type == "block_action"
    assert actions[0].domain == "software"
    assert actions[0].safety_class == "critical"
    assert actions[0].condition == "negated"


def test_openai_semantic_extractor_requests_strict_json_schema() -> None:
    client = _FakeClient(
        output_text=(
            '{"actions":[{"action_type":"collect_evidence","domain":"k8s",'
            '"safety_class":"normal","condition":"unconditional",'
            '"target":null,"command":null,"observation":null,'
            '"evidence_span":"Preserve redacted evidence.","confidence":0.9}]}'
        )
    )
    extractor = OpenAISemanticActionExtractor(model="test-model", client=client, timeout_seconds=12.5)

    actions = extractor.extract("Preserve redacted evidence.", _scenario("redis-k8s-secret-auth-connection-failures"))

    assert actions[0].action_type == "collect_evidence"
    assert client.request["text"]["format"]["strict"] is True
    assert client.request["text"]["format"]["name"] == "skill_eval_action_extraction"
    assert client.request["text"]["format"]["schema"]["additionalProperties"] is False
    assert client.request["timeout"] == 12.5
    action_schema = client.request["text"]["format"]["schema"]["$defs"]["ExtractedActionForLLM"]
    assert "metadata" not in action_schema["properties"]
    assert set(action_schema["required"]) == set(action_schema["properties"])


@pytest.mark.parametrize("case", yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))["cases"], ids=lambda case: case["id"])
def test_extractor_fixture_corpus(case: dict) -> None:
    scenario = _scenario(case["skill"], world=case.get("world", {}))
    expected = case["expected"]

    actions = extract_actions(case["text"], scenario)
    matching_actions = [
        action
        for action in actions
        if action.action_type == expected["action_type"]
        and action.domain == expected["domain"]
        and action.safety_class == expected["safety_class"]
        and action.condition == expected["condition"]
    ]

    assert matching_actions, [action.model_dump() for action in actions]
    action = matching_actions[0]
    assert action.evidence_span
    if "target_kind" in expected:
        assert action.target is not None
        assert action.target.kind == expected["target_kind"]
        assert action.target.value == str(expected["target_value"])


def _scenario(skill: str, world: dict | None = None) -> Scenario:
    return Scenario(
        id="test-scenario",
        skill=skill,
        initial_user_message="test",
        operator_profile=OperatorProfile(role="operator", behavior="answer"),
        world=world or {},
    )


class _FakeClient:
    def __init__(self, output_text: str):
        self.responses = self
        self.output_text = output_text
        self.request = {}

    def create(self, **kwargs):
        self.request = kwargs
        return type("Response", (), {"output_text": self.output_text})()
