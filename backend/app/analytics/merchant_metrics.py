from collections import Counter
from app.repositories.transaction_repo import TransactionRepo

async def compute(db, merchant_id: str) -> dict:
    repo = TransactionRepo(db)
    txns = await repo.by_merchant(merchant_id)
    counts = Counter(t.status for t in txns)
    total = len(txns)
    return {
        "merchant_id": merchant_id,
        "total": total,
        "success": counts.get("success", 0),
        "failed": counts.get("failed", 0),
        "pending": counts.get("pending", 0),
        "abandoned": counts.get("abandoned", 0),
        "success_rate": round(counts.get("success", 0) / total, 3) if total else 0.0,
    }
