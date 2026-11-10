from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from .config import settings
from .permissions import has_permission

bearer_scheme = HTTPBearer(auto_error=False)

def hash_password(p: str) -> str:
    if len(p.encode("utf-8")) > 72:
        raise ValueError("password exceeds bcrypt's 72-byte limit")
    return bcrypt.hashpw(p.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(p: str, h: str) -> bool:
    if len(p.encode("utf-8")) > 72:
        return False
    return bcrypt.checkpw(p.encode("utf-8"), h.encode("utf-8"))

def create_token(sub: str, role: str) -> str:
    payload = {
        "sub": sub,
        "role": role,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.JWT_ACCESS_TOKEN_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


async def current_user(
    cred: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> dict:
    if cred is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(cred.credentials)
    except JWTError as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    if not payload.get("sub") or not payload.get("role"):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    from app.services.user_service import get_active_user

    user = await get_active_user(payload["sub"])
    if not user or user.role != payload["role"]:
        raise HTTPException(
            status_code=401,
            detail="User account is inactive or token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"sub": user.username, "role": user.role}


def require(action: str):
    async def dependency(user: dict = Depends(current_user)) -> dict:
        if not has_permission(user["role"], action):
            raise HTTPException(status_code=403, detail="Permission denied")
        return user

    return dependency
