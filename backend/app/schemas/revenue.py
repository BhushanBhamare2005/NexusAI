from datetime import datetime
from app.schemas.agent import CamelModel


class RevenueSummary(CamelModel):
    total_attempts: int
    successful: int
    failed: int
    pending: int
    abandoned: int
    opportunities_identified: int
    recovered: int
    recovered_amount: float


class RecoveryOpportunityOut(CamelModel):
    id: str
    merchant_id: str
    transaction_id: str
    txn_ref: str
    amount: float
    reason: str
    root_cause: str
    recoverable: bool
    recommended_action: str
    followup_message: str | None = None
    conversion_status: str
    created_at: datetime
    notification_mode: str | None = None
    notification_status: str | None = None
    notification_error: str | None = None
