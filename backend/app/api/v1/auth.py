from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

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


@router.post("/users", status_code=201)
async def create_account(
    request: UserCreateRequest,
    _manager: dict = Depends(require("manage_users")),
):
    try:
        user = await user_service.create_user(
            request.username,
            request.password,
            request.role,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"username": user.username, "role": user.role}
