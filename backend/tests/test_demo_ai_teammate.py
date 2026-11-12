from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.agents import llm
from app.core.config import settings
from app.core.security import current_user
from app.main import app


@pytest.mark.asyncio
async def test_demo_ai_teammate_uses_gemini_and_limits_access(monkeypatch):
    gemini = AsyncMock(return_value="Check the payment reference and settlement status.")
    monkeypatch.setattr("app.api.v1.demo.llm_text", gemini)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test-key")
    monkeypatch.setitem(
        app.dependency_overrides,
        current_user,
        lambda: {"sub": "demo-agent", "role": "demo_agent"},
    )

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/demo/ai-teammate",
                json={"message": "My payment is delayed"},
            )

        assert response.status_code == 200
        assert response.json() == {
            "answer": "Check the payment reference and settlement status."
        }
        assert "My payment is delayed" in gemini.await_args.args[0]
    finally:
        app.dependency_overrides.pop(current_user, None)


@pytest.mark.asyncio
async def test_demo_ai_teammate_rejects_operational_role(monkeypatch):
    gemini = AsyncMock(return_value="This must not be called.")
    monkeypatch.setattr("app.api.v1.demo.llm_text", gemini)
    monkeypatch.setitem(
        app.dependency_overrides,
        current_user,
        lambda: {"sub": "agent", "role": "agent"},
    )

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/demo/ai-teammate",
                json={"message": "My payment is delayed"},
            )

        assert response.status_code == 403
        gemini.assert_not_awaited()
    finally:
        app.dependency_overrides.pop(current_user, None)


@pytest.mark.asyncio
async def test_demo_ai_teammate_reports_missing_gemini_configuration(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setitem(
        app.dependency_overrides,
        current_user,
        lambda: {"sub": "demo-agent", "role": "demo_agent"},
    )

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/demo/ai-teammate",
                json={"message": "What should I check?"},
            )

        assert response.status_code == 503
        assert "GEMINI_API_KEY" in response.json()["detail"]
    finally:
        app.dependency_overrides.pop(current_user, None)


@pytest.mark.asyncio
async def test_llm_text_requires_gemini_api_key(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")

    with pytest.raises(llm.LLMConfigurationError):
        await llm.llm_text("Question")
