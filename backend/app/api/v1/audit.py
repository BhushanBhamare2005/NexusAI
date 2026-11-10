from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.schemas.audit import AuditEventOut, LedgerVerification
from app.db.session import AsyncSessionLocal
from app.models.audit_event import AuditEvent
from app.audit.ledger import verify as verify_ledger
from app.core.security import require

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/events", response_model=list[AuditEventOut])
async def events(
    caseId: str | None = None,
    _user: dict = Depends(require("view_audit")),
):
    async with AsyncSessionLocal() as db:
        stmt = select(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(200)
        if caseId:
            stmt = select(AuditEvent).where(AuditEvent.case_id == caseId).order_by(AuditEvent.timestamp.asc())
        res = await db.execute(stmt)
        return res.scalars().all()

@router.get("/verify", response_model=LedgerVerification)
async def verify(_user: dict = Depends(require("view_audit"))):
    async with AsyncSessionLocal() as db:
        return await verify_ledger(db)
