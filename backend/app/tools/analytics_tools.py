from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.transaction_repo import TransactionRepo

async def merchant_metrics(db: AsyncSession, merchant_id: str) -> dict:
    repo = TransactionRepo(db)
    txns = await repo.by_merchant(merchant_id)
    total = len(txns)
    by_status = {}
    for t in txns:
        by_status[t.status] = by_status.get(t.status, 0) + 1
    return {
        "merchant_id": merchant_id,
        "total_attempts": total,
        "by_status": by_status,
        "success_rate": round(by_status.get("success", 0) / total, 3) if total else 0,
    }
