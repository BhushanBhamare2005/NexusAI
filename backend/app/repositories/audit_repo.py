from sqlalchemy import select
from app.repositories.base_repo import BaseRepo
from app.models.audit_event import AuditEvent

class AuditRepo(BaseRepo[AuditEvent]):
    model = AuditEvent
    async def all_ordered(self):
        res = await self.db.execute(select(AuditEvent).order_by(AuditEvent.timestamp.asc()))
        return res.scalars().all()
    async def by_case(self, case_id: str):
        res = await self.db.execute(
            select(AuditEvent).where(AuditEvent.case_id == case_id).order_by(AuditEvent.timestamp.asc())
        )
        return res.scalars().all()
    async def last(self):
        res = await self.db.execute(
            select(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(1)
        )
        return res.scalar_one_or_none()
