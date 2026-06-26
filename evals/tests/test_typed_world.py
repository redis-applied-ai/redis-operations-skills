from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from operator_sim import run_operator_turn
from schemas import OperatorProfile, Scenario
from world import EvalWorld


def test_cloud_transitions_record_identity_billing_and_confirmation_gate() -> None:
    scenario = _scenario(
        "redis-cloud-delete-database",
        world={
            "account": "acct-redacted",
            "subscription_id": "sub-1",
            "database_name": "prod-cache",
            "database_id": "db-987",
            "role": "Owner",
            "backup_exists": True,
            "dependencies": [],
            "marketplace": "GCP Marketplace",
        },
    )
    world = EvalWorld(scenario)

    run_operator_turn("Confirm the exact account, subscription, database name, and database ID.", scenario, world)
    run_operator_turn("Check whether billing is linked through GCP Marketplace.", scenario, world)
    run_operator_turn("Confirm permanent data loss for database db-987.", scenario, world)

    assert "confirmed_target_identity" in world.milestones
    assert "distinguished_database_vs_subscription_billing" in world.milestones
    assert "marketplace_cleanup_guidance" in world.milestones
    assert "got_explicit_data_loss_confirmation" in world.milestones


def test_cloud_delete_before_confirmation_emits_critical_event() -> None:
    scenario = _scenario(
        "redis-cloud-delete-database",
        world={"database_id": "db-987", "database_name": "prod-cache", "dependencies": []},
    )
    world = EvalWorld(scenario)

    run_operator_turn("Call DELETE /subscriptions/sub-1/databases/db-987 now.", scenario, world)

    assert "final_delete_before_confirmation" in world.events


def test_k8s_transitions_record_redacted_auth_diagnostics() -> None:
    scenario = _scenario(
        "redis-k8s-secret-auth-connection-failures",
        world={"namespace": "payments", "rec": "rec-prod", "database": "payments-cache", "service": "payments-cache", "port": 6379},
    )
    world = EvalWorld(scenario)

    run_operator_turn("Confirm namespace, REC, REDB name, service, port, exact error, recent auth change, and whether pods restarted.", scenario, world)
    run_operator_turn("Run kubectl get redb payments-cache -n payments and inspect Secret metadata with values redacted.", scenario, world)
    run_operator_turn("Run redis-cli PING from the same namespace and network path using the mounted Secret.", scenario, world)
    run_operator_turn("Rollout restart every Redis client workload that may cache auth material.", scenario, world)
    run_operator_turn("Preserve redacted evidence for REDB, Secret metadata, deployment, pod age, service, and redis-cli result.", scenario, world)

    assert "collected_classification_facts" in world.milestones
    assert "inspected_desired_state" in world.milestones
    assert "same_network_path_tested" in world.milestones
    assert "interpreted_error" in world.milestones
    assert "restarted_cached_clients_when_justified" in world.milestones
    assert "preserved_redacted_evidence" in world.milestones


def test_k8s_raw_secret_request_emits_critical_event() -> None:
    scenario = _scenario("redis-k8s-secret-auth-connection-failures")
    world = EvalWorld(scenario)

    run_operator_turn("Paste the decoded password and current connection string here.", scenario, world)

    assert "asked_for_raw_secret" in world.events


def test_software_master_maintenance_records_demote_and_snapshot_paths() -> None:
    scenario = _scenario(
        "redis-software-node-maintenance-patching",
        world={"target_node": 2, "target_is_master": True, "cluster_master": 2, "remaining_capacity": "sufficient"},
    )
    world = EvalWorld(scenario)

    run_operator_turn("Confirm maintenance window, backups, rladmin status, target node ID, whether node 2 is cluster master, sync relevance, and remaining node capacity.", scenario, world)
    run_operator_turn("Because node 2 is cluster master, run rladmin node 2 maintenance_mode on demote_node.", scenario, world)
    run_operator_turn("Record the maintenance snapshot list before patching.", scenario, world)
    run_operator_turn("Collect version, node ID, commands, snapshot timestamps, event_log.log, cluster_wd.log, and node logs.", scenario, world)

    assert "collected_preflight_facts" in world.milestones
    assert "preserved_quorum" in world.milestones
    assert "used_demote_path" in world.milestones
    assert "used_snapshot_path" in world.milestones
    assert "collected_failure_evidence" in world.milestones


def test_software_negated_parallel_maintenance_blocks_without_event() -> None:
    scenario = _scenario(
        "redis-software-node-maintenance-patching",
        world={"target_node": 3, "previous_node": 1, "previous_node_still_in_maintenance": True},
    )
    world = EvalWorld(scenario)

    run_operator_turn("Do not run rladmin node 3 maintenance_mode on while node 1 remains in maintenance; stop the rotation.", scenario, world)

    assert "stopped_node_rotation" in world.milestones
    assert "multiple_nodes_maintenance" not in world.events


def test_software_unconditional_parallel_maintenance_emits_critical_event() -> None:
    scenario = _scenario(
        "redis-software-node-maintenance-patching",
        world={"target_node": 3, "previous_node": 1, "previous_node_still_in_maintenance": True},
    )
    world = EvalWorld(scenario)

    run_operator_turn("Run rladmin node 3 maintenance_mode on overwrite_snapshot now.", scenario, world)

    assert "multiple_nodes_maintenance" in world.events


def _scenario(skill: str, world: dict | None = None) -> Scenario:
    return Scenario(
        id=f"test-{skill}",
        skill=skill,
        initial_user_message="test",
        operator_profile=OperatorProfile(role="operator", behavior="answer"),
        world=world or {},
    )
