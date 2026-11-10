from datetime import datetime
from app.schemas.agent import CamelModel


class TransactionOut(CamelModel):
    id: str
    txn_ref: str
    customer_id: str
    merchant_id: str
    amount: float
    currency: str
    status: str
    method: str
    upi_ref: str | None = None
    settlement_id: str | None = None
    root_cause: str | None = None
    created_at: datetime
    updated_at: datetime
