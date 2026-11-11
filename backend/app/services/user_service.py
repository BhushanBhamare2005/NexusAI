import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, verify_password
from app.db.session import AsyncSessionLocal
from app.models.role_assignment_history import RoleAssignmentHistory
from app.models.user import User

SUPPORTED_ROLES = {"agent", "senior_agent", "manager"}


def _record_assignment(
    *,
    user: User,
    actor: str,
    action: str,
    previous_role: str | None,
    new_role: str | None,
    previous_active: bool | None,
    new_active: bool | None,
) -> RoleAssignmentHistory:
    return RoleAssignmentHistory(
        id=str(uuid.uuid4()),
        target_user_id=user.id,
        target_username=user.username,
        actor_username=actor,
        action=action,
        previous_role=previous_role,
        new_role=new_role,
        previous_active=previous_active,
        new_active=new_active,
    )


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


async def list_users() -> list[User]:
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).order_by(User.created_at, User.username))
        return list(result.scalars().all())


async def list_role_history(limit: int = 200) -> list[RoleAssignmentHistory]:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(RoleAssignmentHistory)
            .order_by(RoleAssignmentHistory.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())


async def create_user(
    username: str,
    password: str,
    role: str,
    actor: str,
) -> User:
    if role not in SUPPORTED_ROLES:
        raise ValueError("unsupported_role")
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
        db.add(
            _record_assignment(
                user=user,
                actor=actor,
                action="account_created",
                previous_role=None,
                new_role=role,
                previous_active=None,
                new_active=True,
            )
        )
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            raise ValueError("username_already_exists") from exc
        await db.refresh(user)
        return user


async def update_user(
    *,
    user_id: str,
    actor: str,
    role: str | None = None,
    is_active: bool | None = None,
) -> User:
    if role is not None and role not in SUPPORTED_ROLES:
        raise ValueError("unsupported_role")
    if role is None and is_active is None:
        raise ValueError("no_changes_requested")

    async with AsyncSessionLocal() as db:
        async with db.begin():
            result = await db.execute(
                select(User)
                .where(User.role == "manager", User.is_active.is_(True))
                .with_for_update()
            )
            active_managers = list(result.scalars().all())
            result = await db.execute(
                select(User).where(User.id == user_id).with_for_update()
            )
            user = result.scalar_one_or_none()
            if user is None:
                raise LookupError("user_not_found")

            next_role = role if role is not None else user.role
            next_active = is_active if is_active is not None else user.is_active
            removes_manager = (
                user.role == "manager"
                and user.is_active
                and (next_role != "manager" or not next_active)
            )
            if removes_manager and len(active_managers) <= 1:
                raise ValueError("cannot_remove_last_active_manager")
            if removes_manager and user.username == actor:
                raise ValueError("cannot_change_own_manager_access")
            if next_role == user.role and next_active == user.is_active:
                return user

            previous_role = user.role
            previous_active = user.is_active
            user.role = next_role
            user.is_active = next_active
            db.add(
                _record_assignment(
                    user=user,
                    actor=actor,
                    action="user_updated",
                    previous_role=previous_role,
                    new_role=next_role,
                    previous_active=previous_active,
                    new_active=next_active,
                )
            )
            await db.flush()
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
