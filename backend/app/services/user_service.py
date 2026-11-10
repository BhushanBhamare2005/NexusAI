import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, verify_password
from app.db.session import AsyncSessionLocal
from app.models.user import User


async def authenticate(username: str, password: str) -> User | None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.username == username, User.is_active.is_(True))
        )
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.password_hash):
            return None
        return user


async def get_active_user(username: str) -> User | None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.username == username, User.is_active.is_(True))
        )
        return result.scalar_one_or_none()


async def create_user(username: str, password: str, role: str) -> User:
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User.id).where(User.username == username))
        if result.scalar_one_or_none():
            raise ValueError("username_already_exists")
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            password_hash=hash_password(password),
            role=role,
        )
        db.add(user)
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            raise ValueError("username_already_exists") from exc
        await db.refresh(user)
        return user


async def ensure_bootstrap_admin(username: str, password: str) -> None:
    if bool(username) != bool(password):
        raise ValueError(
            "both NEXUS_BOOTSTRAP_USERNAME and NEXUS_BOOTSTRAP_PASSWORD must be set"
        )
    if password and (
        len(password.encode("utf-8")) < 12 or len(password.encode("utf-8")) > 72
    ):
        raise ValueError("bootstrap password must be between 12 and 72 UTF-8 bytes")
    if username and not username.replace("_", "").replace("-", "").replace(".", "").isalnum():
        raise ValueError("bootstrap username may contain only letters, numbers, ., _, and -")
    async with AsyncSessionLocal() as db:
        user_count = await db.scalar(select(User.id).limit(1))
        if user_count is not None:
            return
        if not username:
            raise RuntimeError(
                "No user accounts exist. Configure NEXUS_BOOTSTRAP_USERNAME and "
                "NEXUS_BOOTSTRAP_PASSWORD to create the initial manager account."
            )
        db.add(
            User(
                id=str(uuid.uuid4()),
                username=username,
                password_hash=hash_password(password),
                role="manager",
            )
        )
        await db.commit()
