from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RoleAssignmentHistory(Base):
    __tablename__ = "role_assignment_history"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    target_user_id: Mapped[str] = mapped_column(String, index=True)
    target_username: Mapped[str] = mapped_column(String, index=True)
    actor_username: Mapped[str] = mapped_column(String, index=True)
    action: Mapped[str] = mapped_column(String)
    previous_role: Mapped[str | None] = mapped_column(String, nullable=True)
    new_role: Mapped[str | None] = mapped_column(String, nullable=True)
    previous_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    new_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
