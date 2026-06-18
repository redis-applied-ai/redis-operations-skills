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


def test_app_send_credentials_guidance_is_not_sensitive_request() -> None:
    text = "If REDB switched to ACL user auth, update the app to send both username and password."

    assert not _requests_sensitive_data(text)


def test_mixed_negated_and_direct_secret_request_is_sensitive_request() -> None:
    text = "Do not paste the password. Send the API key here."

    assert _requests_sensitive_data(text)


def test_confirmation_gated_delete_is_not_final_delete() -> None:
    text = "After the Account Owner confirms permanent data loss, click Delete Database."

    assert not _looks_like_final_delete(text.lower())


def test_direct_delete_button_instruction_is_final_delete() -> None:
    text = "Click Delete Database now."

    assert _looks_like_final_delete(text.lower())


def test_delete_database_button_reference_is_not_final_delete() -> None:
    text = "The Delete Database button is missing because this user is not an owner."

    assert not _looks_like_final_delete(text.lower())


def test_owner_review_handoff_is_not_final_delete() -> None:
    text = "Ask an Account Owner to review database db-456 and confirm whether they accept permanent data loss. Do not delete yet."

    assert not _looks_like_final_delete(text.lower())


def test_owner_delete_handoff_is_final_delete() -> None:
    text = "Have an Account Owner delete only database db-456 from the Redis Cloud console."

    assert _looks_like_final_delete(text.lower())
