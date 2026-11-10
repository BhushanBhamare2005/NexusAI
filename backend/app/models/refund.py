from datetime import datetime
from sqlalchemy import String, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Refund(Base):
    __tablename__ = "refunds"
    __table_args__ = (
        UniqueConstraint("transaction_id", name="uq_refunds_transaction_id"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    transaction_id: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="initiated")
    reason: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
