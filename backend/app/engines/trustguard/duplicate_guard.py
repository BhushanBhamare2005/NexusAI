from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.refund_repo import RefundRepo

async def is_duplicate_refund(db: AsyncSession, txn_id: str) -> tuple[bool, str | None]:
    repo = RefundRepo(db)
    existing = await repo.by_transaction(txn_id)
    if existing:
        return True, existing[0].id
    return False, None
