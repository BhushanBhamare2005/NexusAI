from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.security import current_user
from app.main import app


async def _dashboard_for_role(role: str):
    app.dependency_overrides[current_user] = lambda: {
        "sub": f"existing-{role}",
        "role": role,
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        return await client.get("/api/v1/demo/dashboard")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("role", "scope"),
    [
        ("demo_manager", "team"),
        ("demo_senior_agent", "assigned_team"),
        ("demo_agent", "personal"),
    ],
)
async def test_demo_dashboard_returns_role_scoped_synthetic_data(role, scope):
    try:
        response = await _dashboard_for_role(role)
    finally:
        app.dependency_overrides.pop(current_user, None)

    assert response.status_code == 200
    data = response.json()
    assert data["scope"] == scope
    assert "fictional" in data["notice"].lower()
    assert len(data["metrics"]) == 4
    assert data["tasks"]
    assert data["productivity"]
    assert data["task_analytics"]
    assert data["reports"]


@pytest.mark.asyncio
async def test_demo_manager_sees_complete_synthetic_team():
    try:
        response = await _dashboard_for_role("demo_manager")
    finally:
        app.dependency_overrides.pop(current_user, None)

    data = response.json()
    assert len(data["team_members"]) == 8
    assert sum(member["role"] == "Agent" for member in data["team_members"]) == 6
    assert sum(member["role"] == "Senior Agent" for member in data["team_members"]) == 2
    assert len(data["tasks"]) == 12


@pytest.mark.asyncio
async def test_demo_senior_agent_sees_only_assigned_team_data():
    try:
        response = await _dashboard_for_role("demo_senior_agent")
    finally:
        app.dependency_overrides.pop(current_user, None)

    data = response.json()
    assert data["profile"]["name"] == "Sofia Chen"
    assert {member["name"] for member in data["team_members"]} == {
        "Maya Patel",
        "Liam Brooks",
        "Zoe Carter",
    }
    assert {task["assignee"] for task in data["tasks"]} == {
        "Maya Patel",
        "Liam Brooks",
        "Zoe Carter",
    }
    assert all(
        "Arjun Mehta" not in activity["text"]
        and "Elena Torres" not in activity["text"]
        and "Theo Kim" not in activity["text"]
        and "Noah Reed" not in activity["text"]
        for activity in data["activities"]
    )


@pytest.mark.asyncio
async def test_demo_agent_sees_only_personal_synthetic_data():
    try:
        response = await _dashboard_for_role("demo_agent")
    finally:
        app.dependency_overrides.pop(current_user, None)

    data = response.json()
    assert data["profile"] == {"name": "Maya Patel", "title": "Agent"}
    assert data["team_members"] == []
    assert all(task["assignee"] == "Maya Patel" for task in data["tasks"])
    assert all("Maya Patel" in activity["text"] for activity in data["activities"])
    assert all(
        name not in str(data)
        for name in (
            "Sofia Chen",
            "Liam Brooks",
            "Zoe Carter",
            "Arjun Mehta",
            "Elena Torres",
            "Theo Kim",
            "Noah Reed",
        )
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["agent", "senior_agent", "manager"])
async def test_operational_roles_cannot_access_demo_dashboard(role):
    try:
        response = await _dashboard_for_role(role)
    finally:
        app.dependency_overrides.pop(current_user, None)

    assert response.status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "role", ["demo_manager", "demo_senior_agent", "demo_agent"]
)
async def test_all_demo_roles_retain_existing_ai_teammate_access(role, monkeypatch):
    responder = AsyncMock(return_value="A synthetic guidance response.")
    monkeypatch.setattr("app.api.v1.demo.llm_text", responder)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test-key")
    app.dependency_overrides[current_user] = lambda: {
        "sub": f"existing-{role}",
        "role": role,
    }

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/demo/ai-teammate",
                json={"message": "How can I review a delayed payment?"},
            )
    finally:
        app.dependency_overrides.pop(current_user, None)

    assert response.status_code == 200
    assert response.json() == {"answer": "A synthetic guidance response."}
    responder.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "role", ["demo_manager", "demo_senior_agent", "demo_agent"]
)
async def test_demo_roles_cannot_access_production_user_records(role):
    app.dependency_overrides[current_user] = lambda: {
        "sub": f"existing-{role}",
        "role": role,
    }
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/auth/users")
    finally:
        app.dependency_overrides.pop(current_user, None)

    assert response.status_code == 403
