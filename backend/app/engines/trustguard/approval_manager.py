import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.approval import Approval
from app.repositories.approval_repo import ApprovalRepo

async def request_approval(
    db: AsyncSession,
    case_id: str,
    run_id: str,
    action: str,
    reason: str,
    risk_level: str = "approval_needed",
) -> Approval:
    a = Approval(
        id=str(uuid.uuid4()),
        case_id=case_id,
        run_id=run_id,
        action=action,
        reason=reason,
        risk_level=risk_level,
        status="pending",
    )
    db.add(a)
    await db.commit()
    await db.refresh(a)
    return a

async def decide(db: AsyncSession, approval_id: str, decision: str, decided_by: str = "reviewer") -> Approval | None:
    repo = ApprovalRepo(db)
    a = await repo.get(approval_id)
    if not a:
        return None
    if a.status != "pending":
        raise ValueError("approval_already_decided")
    a.status = decision
    a.decided_by = decided_by
    a.decided_at = datetime.utcnow()
    await db.commit()
    await db.refresh(a)
    return a
