from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


Variant = Literal["with_skill", "without_skill"]
ActionType = Literal[
    "ask_observation",
    "recommend_command",
    "block_action",
    "collect_evidence",
    "request_confirmation",
    "final_summary",
    "unknown",
]
ActionCondition = Literal[
    "unconditional",
    "negated",
    "if_gate_passes",
    "after_confirmation",
    "after_previous_node_healthy",
    "unknown",
]
ActionDomain = Literal["cloud", "k8s", "software", "general"]
SafetyClass = Literal["normal", "destructive", "secret_sensitive", "critical"]


class TargetRef(BaseModel):
    kind: str
    value: str


class ExtractedAction(BaseModel):
    action_type: ActionType
    domain: ActionDomain = "general"
    safety_class: SafetyClass = "normal"
    condition: ActionCondition = "unknown"
    target: TargetRef | None = None
    command: str | None = None
    observation: str | None = None
    evidence_span: str
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ActionExtractionResult(BaseModel):
    actions: list[ExtractedAction] = Field(default_factory=list)


class ActionMatch(BaseModel):
    action_type: ActionType | None = None
    domain: ActionDomain | None = None
    safety_class: SafetyClass | None = None
    condition: ActionCondition | None = None
    target_kind: str | None = None
    target_value: str | None = None
    command: str | None = None
    observation: str | None = None


class TransitionRule(BaseModel):
    id: str
    match: ActionMatch
    response: str
    milestones: list[str] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)
    terminal: bool = False


class OperatorProfile(BaseModel):
    role: str
    behavior: str


class SuccessCriteria(BaseModel):
    required_milestones: list[str] = Field(default_factory=list)
    forbidden_events: list[str] = Field(default_factory=list)
    critical_events: list[str] = Field(default_factory=list)


class Scenario(BaseModel):
    id: str
    version: str = "1"
    skill: str
    initial_user_message: str
    tags: list[str] = Field(default_factory=list)
    operator_profile: OperatorProfile
    world: dict[str, Any] = Field(default_factory=dict)
    transitions: list[TransitionRule] = Field(default_factory=list)
    allowed_actions: list[str] = Field(default_factory=list)
    success: SuccessCriteria = Field(default_factory=SuccessCriteria)
    assistant_scripts: dict[str, list[str]] = Field(default_factory=dict)
    max_turns: int = 12


class ScenarioFile(BaseModel):
    scenarios: list[Scenario]


class OperatorAction(BaseModel):
    name: str
    reason: str = ""
    destructive: bool = False


class TurnRecord(BaseModel):
    turn: int
    assistant: str
    operator: str
    actions: list[OperatorAction] = Field(default_factory=list)
    extracted_actions: list[ExtractedAction] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)
    milestones: list[str] = Field(default_factory=list)


class CheckResult(BaseModel):
    id: str
    passed: bool
    score: float
    evidence: str = ""


class GradeResult(BaseModel):
    overall_pass: bool
    score: float
    checks: list[CheckResult]
    missing_milestones: list[str] = Field(default_factory=list)
    forbidden_events: list[str] = Field(default_factory=list)


class RunResult(BaseModel):
    run_id: str
    scenario_id: str
    skill: str
    variant: Variant
    model: str | None
    scenario_version: str = "1"
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    skill_sha256: str | None = None
    model_settings: dict[str, Any] = Field(default_factory=dict)
    transcript: list[TurnRecord] = Field(default_factory=list)
    final_output: str = ""
    milestones: list[str] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)
    deterministic_grade: GradeResult | None = None
    rubric_grade: GradeResult | None = None
    token_usage: dict[str, Any] = Field(default_factory=dict)
    latency_seconds: float | None = None


class SummaryRow(BaseModel):
    scenario_id: str
    skill: str
    variant: Variant
    runs: int
    passes: int
    pass_rate: float
    pass_k: bool
    critical_safety_violations: int
    median_turns: float
    total_tokens: int = 0
    average_latency_seconds: float | None = None


class SkillLiftRow(BaseModel):
    scenario_id: str
    skill: str
    with_skill_pass_rate: float | None
    without_skill_pass_rate: float | None
    skill_lift: float | None
    token_overhead: int | None
    latency_overhead_seconds: float | None


class Summary(BaseModel):
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model: str | None
    rows: list[SummaryRow]
    lift_rows: list[SkillLiftRow] = Field(default_factory=list)
