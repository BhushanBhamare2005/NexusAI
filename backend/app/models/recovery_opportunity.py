from datetime import datetime
from sqlalchemy import String, DateTime, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class RecoveryOpportunity(Base):
    __tablename__ = "recovery_opportunities"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    merchant_id: Mapped[str] = mapped_column(String, index=True)
    transaction_id: Mapped[str] = mapped_column(String, index=True)
    txn_ref: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    reason: Mapped[str] = mapped_column(String)
    root_cause: Mapped[str] = mapped_column(String)
    recoverable: Mapped[bool] = mapped_column(Boolean, default=True)
    recommended_action: Mapped[str] = mapped_column(String)
    followup_message: Mapped[str | None] = mapped_column(String, nullable=True)
    conversion_status: Mapped[str] = mapped_column(String, default="not_contacted")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
