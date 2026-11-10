from app.db.session import AsyncSessionLocal
from app.repositories.transaction_repo import TransactionRepo

async def search(q=None, status=None, merchant_id=None, customer_id=None, limit=50):
    async with AsyncSessionLocal() as db:
        return await TransactionRepo(db).search(q, status, merchant_id, customer_id, limit)

async def get(txn_id: str):
    async with AsyncSessionLocal() as db:
        return await TransactionRepo(db).get(txn_id)
