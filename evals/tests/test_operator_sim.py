from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from operator_sim import _requests_sensitive_data


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
