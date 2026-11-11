import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.security import create_token, current_user, hash_password
from app.main import app
from app.models.role_assignment_history import RoleAssignmentHistory
from app.models.user import User
from app.services import user_service


@pytest.mark.asyncio
async def test_role_management_and_dashboard_access_are_server_authorized(
    tmp_path, monkeypatch
):
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'rbac.db'}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(user_service, "AsyncSessionLocal", session_factory)
    async with engine.begin() as conn:
        await conn.run_sync(User.__table__.create)
        await conn.run_sync(RoleAssignmentHistory.__table__.create)
    async with session_factory() as db:
        db.add_all(
            [
                User(
                    id="manager-id",
                    username="manager",
                    password_hash=hash_password("manager-password"),
                    role="manager",
                    is_active=True,
                ),
                User(
                    id="agent-id",
                    username="agent",
                    password_hash=hash_password("agent-password"),
                    role="agent",
                    is_active=True,
                ),
            ]
        )
        await db.commit()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/auth/users")
        assert response.status_code == 401

    app.dependency_overrides[current_user] = lambda: {
        "sub": "manager",
        "role": "manager",
    }
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/auth/users")
            assert response.status_code == 200
            assert {user["username"] for user in response.json()} == {
                "manager",
                "agent",
            }
            assert "password_hash" not in response.json()[0]

            response = await client.get("/api/v1/auth/dashboards")
            assert response.status_code == 200
            assert {item["role"] for item in response.json()} == {
                "manager",
                "senior_agent",
                "agent",
            }

            response = await client.get("/api/v1/auth/dashboards/agent")
            assert response.status_code == 200
            assert response.json()["path"] == "/agent"

            response = await client.patch(
                "/api/v1/auth/users/agent-id",
                json={"role": "senior_agent"},
            )
            assert response.status_code == 200
            assert response.json()["role"] == "senior_agent"
            with pytest.raises(HTTPException) as exc_info:
                await current_user(
                    credentials(
                        create_token("agent", "agent")
                    )
                )
            assert exc_info.value.status_code == 401

            response = await client.get("/api/v1/auth/role-history")
            assert response.status_code == 200
            assert response.json()[0]["actor_username"] == "manager"
            assert response.json()[0]["previous_role"] == "agent"
            assert response.json()[0]["new_role"] == "senior_agent"

            response = await client.post(
                "/api/v1/auth/users",
                json={
                    "username": "new-agent",
                    "password": "Temporary-Password-123",
                    "role": "agent",
                },
            )
            assert response.status_code == 201
            assert response.json()["role"] == "agent"
            assert "password_hash" not in response.json()
            created_user_id = response.json()["id"]

            response = await client.get("/api/v1/auth/role-history")
            assert response.status_code == 200
            assert any(
                entry["action"] == "account_created"
                and entry["target_username"] == "new-agent"
                for entry in response.json()
            )

            response = await client.patch(
                f"/api/v1/auth/users/{created_user_id}",
                json={"is_active": False},
            )
            assert response.status_code == 200
            assert response.json()["is_active"] is False
            with pytest.raises(HTTPException) as exc_info:
                await current_user(
                    credentials(
                        create_token("new-agent", "agent")
                    )
                )
            assert exc_info.value.status_code == 401
            response = await client.get("/api/v1/auth/role-history")
            assert any(
                entry["target_user_id"] == created_user_id
                and entry["previous_active"] is True
                and entry["new_active"] is False
                for entry in response.json()
            )

            response = await client.post(
                "/api/v1/auth/users",
                json={
                    "username": "demo-manager",
                    "password": "Demo-Manager-Password-123",
                    "role": "demo_manager",
                },
            )
            assert response.status_code == 201
            assert response.json()["is_demo"] is True
            demo_user_id = response.json()["id"]

            response = await client.patch(
                f"/api/v1/auth/users/{demo_user_id}",
                json={"role": "manager"},
            )
            assert response.status_code == 409
            assert response.json()["detail"] == "demo_account_role_is_restricted"

            response = await client.patch(
                "/api/v1/auth/users/manager-id",
                json={"is_active": False},
            )
            assert response.status_code == 409
            assert response.json()["detail"] == "cannot_remove_last_active_manager"

        app.dependency_overrides[current_user] = lambda: {
            "sub": "demo-manager",
            "role": "demo_manager",
        }
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/auth/dashboards")
            assert response.status_code == 200
            assert response.json() == [
                {"role": "demo_manager", "path": "/demo"}
            ]

            response = await client.get("/api/v1/demo/overview")
            assert response.status_code == 200
            assert response.json()["label"] == "Synthetic demonstration data"
            assert all(
                item["id"].startswith("DEMO-")
                for item in response.json()["recent_cases"]
            )

            response = await client.get("/api/v1/auth/users")
            assert response.status_code == 403

            response = await client.get("/api/v1/auth/dashboards/manager")
            assert response.status_code == 403

            response = await client.get("/api/v1/transactions")
            assert response.status_code == 403

        app.dependency_overrides[current_user] = lambda: {
            "sub": "senior",
            "role": "senior_agent",
        }
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/auth/dashboards")
            assert response.status_code == 200
            assert {item["role"] for item in response.json()} == {
                "senior_agent",
                "agent",
            }

            response = await client.get("/api/v1/auth/dashboards/manager")
            assert response.status_code == 403

        app.dependency_overrides[current_user] = lambda: {
            "sub": "agent",
            "role": "agent",
        }
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/auth/users")
            assert response.status_code == 403

            response = await client.get("/api/v1/auth/dashboards")
            assert response.status_code == 200
            assert [item["role"] for item in response.json()] == ["agent"]

            response = await client.get("/api/v1/auth/dashboards/manager")
            assert response.status_code == 403

            response = await client.patch(
                "/api/v1/auth/users/manager-id",
                json={"role": "agent"},
            )
            assert response.status_code == 403

        async with session_factory() as db:
            history = (
                await db.execute(select(RoleAssignmentHistory))
            ).scalars().all()
            assert len(history) == 4
    finally:
        app.dependency_overrides.pop(current_user, None)
        await engine.dispose()


def credentials(token: str):
    from fastapi.security import HTTPAuthorizationCredentials

    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
