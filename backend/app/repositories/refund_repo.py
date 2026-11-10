from sqlalchemy import select
from app.repositories.base_repo import BaseRepo
from app.models.refund import Refund

class RefundRepo(BaseRepo[Refund]):
    model = Refund
    async def by_transaction(self, txn_id: str):
        res = await self.db.execute(select(Refund).where(Refund.transaction_id == txn_id))
        return res.scalars().all()
