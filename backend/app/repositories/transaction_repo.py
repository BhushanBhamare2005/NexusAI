from sqlalchemy import select, or_
from app.repositories.base_repo import BaseRepo
from app.models.transaction import Transaction

class TransactionRepo(BaseRepo[Transaction]):
    model = Transaction
    async def search(self, q: str | None, status: str | None, merchant_id: str | None,
                     customer_id: str | None, limit: int = 50):
        stmt = select(Transaction)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(or_(
                Transaction.txn_ref.ilike(like),
                Transaction.upi_ref.ilike(like),
                Transaction.customer_id.ilike(like),
                Transaction.merchant_id.ilike(like),
            ))
        if status:
            stmt = stmt.where(Transaction.status == status)
        if merchant_id:
            stmt = stmt.where(Transaction.merchant_id == merchant_id)
        if customer_id:
            stmt = stmt.where(Transaction.customer_id == customer_id)
        stmt = stmt.order_by(Transaction.created_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return res.scalars().all()
    async def by_ref(self, txn_ref: str) -> Transaction | None:
        res = await self.db.execute(select(Transaction).where(Transaction.txn_ref == txn_ref))
        return res.scalar_one_or_none()
    async def by_merchant(self, merchant_id: str, limit: int = 500):
        res = await self.db.execute(
            select(Transaction).where(Transaction.merchant_id == merchant_id).limit(limit)
        )
        return res.scalars().all()
