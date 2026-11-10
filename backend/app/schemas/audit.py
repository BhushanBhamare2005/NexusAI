from datetime import datetime
from app.schemas.agent import CamelModel


class AuditEventOut(CamelModel):
    id: str
    case_id: str
    run_id: str
    event_type: str
    actor: str
    payload: dict
    prev_hash: str
    hash: str
    timestamp: datetime


class LedgerVerification(CamelModel):
    valid: bool
    checked_events: int
    broken_at: str | None = None
