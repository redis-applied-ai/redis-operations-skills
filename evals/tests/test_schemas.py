from __future__ import annotations

from pathlib import Path
import sys

import pytest
from pydantic import ValidationError


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from schemas import (
    ActionExtractionLLMResult,
    ActionExtractionResult,
    ActionMatch,
    ExtractedAction,
    TargetRef,
    TransitionRule,
    strict_json_schema,
)


def test_extracted_action_requires_known_action_type() -> None:
    with pytest.raises(ValidationError):
        ExtractedAction(action_type="literal_match", evidence_span="unsafe text")


def test_extracted_action_confidence_is_bounded() -> None:
    with pytest.raises(ValidationError):
        ExtractedAction(
            action_type="block_action",
            target=TargetRef(kind="node", value="3"),
            evidence_span="node 3 is blocked",
            confidence=1.2,
        )


def test_transition_rule_requires_valid_condition() -> None:
    with pytest.raises(ValidationError):
        TransitionRule(
            id="unsafe-node-rotation",
            match=ActionMatch(action_type="recommend_command", condition="after_magic"),
            response="blocked",
        )


def test_transition_rule_accepts_typed_match() -> None:
    rule = TransitionRule(
        id="block-node-rotation",
        match=ActionMatch(
            action_type="block_action",
            domain="software",
            target_kind="node",
            target_value="3",
            condition="after_previous_node_healthy",
        ),
        response="Node 3 is blocked until node 1 is healthy.",
        milestones=["stopped_node_rotation"],
    )

    assert rule.match.action_type == "block_action"
    assert rule.milestones == ["stopped_node_rotation"]


def test_action_extraction_result_accepts_typed_actions() -> None:
    result = ActionExtractionResult(
        actions=[
            ExtractedAction(
                action_type="collect_evidence",
                evidence_span="Preserve redacted logs.",
            )
        ]
    )

    assert result.actions[0].action_type == "collect_evidence"


def test_strict_json_schema_disallows_additional_properties_recursively() -> None:
    schema = strict_json_schema(ActionExtractionLLMResult)

    assert schema["additionalProperties"] is False
    assert schema["required"] == ["actions"]
    assert "default" not in schema["properties"]["actions"]
    assert schema["$defs"]["ExtractedActionForLLM"]["additionalProperties"] is False
    assert set(schema["$defs"]["ExtractedActionForLLM"]["required"]) == set(
        schema["$defs"]["ExtractedActionForLLM"]["properties"]
    )
    assert "metadata" not in schema["$defs"]["ExtractedActionForLLM"]["properties"]
    assert schema["$defs"]["TargetRef"]["additionalProperties"] is False
