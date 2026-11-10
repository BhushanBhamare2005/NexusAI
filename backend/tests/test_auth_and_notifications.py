from types import SimpleNamespace

import pytest

from app.core.config import settings
from app.core.permissions import has_permission
from app.core.security import create_token, decode_token, hash_password, verify_password
from app.tools.notification_tools import send_notification


def test_password_hash_and_jwt_roles():
    encoded = hash_password("Correct-Horse-Battery-12")
    assert encoded != "Correct-Horse-Battery-12"
    assert verify_password("Correct-Horse-Battery-12", encoded)
    assert not verify_password("incorrect", encoded)

    token = create_token("agent-a", "agent")
    payload = decode_token(token)
    assert payload["sub"] == "agent-a"
    assert payload["role"] == "agent"
    assert has_permission(payload["role"], "lookup_txn")
    assert not has_permission(payload["role"], "manage_users")


def test_passwords_longer_than_bcrypt_limit_are_rejected():
    with pytest.raises(ValueError, match="72-byte"):
        hash_password("x" * 73)


@pytest.mark.asyncio
async def test_simulated_notification_is_never_reported_as_delivered(monkeypatch):
    monkeypatch.setattr(settings, "TWILIO_ENABLED", False)
    result = await send_notification(
        recipient="c_001",
        message="Test message",
    )
    assert result["mode"] == "simulated"
    assert result["accepted"] is False
    assert result["delivered"] is False


@pytest.mark.asyncio
async def test_twilio_requires_recorded_customer_consent(monkeypatch):
    monkeypatch.setattr(settings, "TWILIO_ENABLED", True)
    monkeypatch.setattr(settings, "TWILIO_ACCOUNT_SID", "AC-test")
    monkeypatch.setattr(settings, "TWILIO_AUTH_TOKEN", "test-token")
    monkeypatch.setattr(settings, "TWILIO_FROM_NUMBER", "+14155550100")

    customer = SimpleNamespace(
        id="c_001",
        phone="9000012345",
        sms_opt_in=False,
    )

    class FakeSession:
        rows = []

        async def get(self, model, customer_id):
            return customer

        def add(self, notification):
            self.rows.append(notification)

        async def commit(self):
            pass

    with pytest.raises(PermissionError, match="consent is not recorded"):
        await send_notification(
            db=FakeSession(),
            recipient="c_001",
            message="Test message",
        )
    assert FakeSession.rows[-1].provider_status == "consent_missing"
