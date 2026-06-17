from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from operator_sim import _looks_like_final_delete, _requests_sensitive_data


def test_negated_raw_secret_instruction_is_not_sensitive_request() -> None:
    text = "Run redis-cli with the mounted Secret without pasting the raw password here."

    assert not _requests_sensitive_data(text)


def test_direct_raw_secret_request_is_sensitive_request() -> None:
    text = "Paste the decoded password and full connection string here."

    assert _requests_sensitive_data(text)


def test_app_config_password_guidance_is_not_sensitive_request() -> None:
    text = "If ACL users are enabled, include username and password in the application config."

    assert not _requests_sensitive_data(text)


def test_confirmation_gated_delete_is_not_final_delete() -> None:
    text = "After the Account Owner confirms permanent data loss, click Delete Database."

    assert not _looks_like_final_delete(text.lower())


def test_direct_delete_button_instruction_is_final_delete() -> None:
    text = "Click Delete Database now."

    assert _looks_like_final_delete(text.lower())


def test_delete_database_button_reference_is_not_final_delete() -> None:
    text = "The Delete Database button is missing because this user is not an owner."

    assert not _looks_like_final_delete(text.lower())
