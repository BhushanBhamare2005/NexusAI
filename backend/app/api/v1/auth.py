from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

from app.core.permissions import DASHBOARD_ROUTES, available_dashboards, has_permission
from app.core.security import create_token, current_user, require
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=72)


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=12, max_length=72)
    role: Literal["agent", "senior_agent", "manager"]

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("password exceeds bcrypt's 72-byte limit")
        return value


class UserUpdateRequest(BaseModel):
    role: Literal["agent", "senior_agent", "manager"] | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def require_update(self):
        if self.role is None and self.is_active is None:
            raise ValueError("At least one of role or is_active must be provided")
        return self


def _user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
    }


def _history_payload(entry):
    return {
        "id": entry.id,
        "target_user_id": entry.target_user_id,
        "target_username": entry.target_username,
        "actor_username": entry.actor_username,
        "action": entry.action,
        "previous_role": entry.previous_role,
        "new_role": entry.new_role,
        "previous_active": entry.previous_active,
        "new_active": entry.new_active,
        "created_at": entry.created_at,
    }


@router.post("/login")
async def login(request: LoginRequest):
    user = await user_service.authenticate(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token(user.username, user.role)
    return {
        "token": token,
        "role": user.role,
        "user": {"username": user.username, "role": user.role},
    }


@router.get("/me")
async def me(user: dict = Depends(current_user)):
    return {"username": user["sub"], "role": user["role"]}


@router.get("/dashboards")
async def dashboards(user: dict = Depends(current_user)):
    return available_dashboards(user["role"])


@router.get("/dashboards/{role}")
async def dashboard_for_role(role: str, user: dict = Depends(current_user)):
    dashboard = DASHBOARD_ROUTES.get(role)
    if dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    path, permission = dashboard
    if not has_permission(user["role"], permission):
        raise HTTPException(status_code=403, detail="Dashboard access denied")
    return {"role": role, "path": path}


@router.get("/users")
async def list_accounts(_manager: dict = Depends(require("manage_users"))):
    return [_user_payload(user) for user in await user_service.list_users()]


@router.post("/users", status_code=201)
async def create_account(
    request: UserCreateRequest,
    manager: dict = Depends(require("manage_users")),
):
    try:
        user = await user_service.create_user(
            request.username,
            request.password,
            request.role,
            manager["sub"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _user_payload(user)


@router.patch("/users/{user_id}")
async def update_account(
    user_id: str,
    request: UserUpdateRequest,
    manager: dict = Depends(require("manage_users")),
):
    try:
        user = await user_service.update_user(
            user_id=user_id,
            actor=manager["sub"],
            role=request.role,
            is_active=request.is_active,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _user_payload(user)


@router.get("/role-history")
async def role_history(_manager: dict = Depends(require("manage_users"))):
    return [_history_payload(entry) for entry in await user_service.list_role_history()]
