from sqlalchemy import select
from app.repositories.base_repo import BaseRepo
from app.models.approval import Approval

class ApprovalRepo(BaseRepo[Approval]):
    model = Approval
    async def pending(self):
        res = await self.db.execute(select(Approval).where(Approval.status == "pending"))
        return res.scalars().all()
