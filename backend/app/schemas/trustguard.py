from datetime import datetime
from pydantic import Field
from app.schemas.agent import CamelModel


class ApprovalOut(CamelModel):
    id: str
    case_id: str
    run_id: str
    action: str
    requested_by: str
    reason: str
    risk_level: str
    status: str
    created_at: datetime
    decided_at: datetime | None = None
    decided_by: str | None = None


class ApprovalDecision(CamelModel):
    decision: str = Field(pattern="^(approved|rejected)$")
    decided_by: str = "reviewer"
