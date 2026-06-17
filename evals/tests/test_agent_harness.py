from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent_harness import _looks_final


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
