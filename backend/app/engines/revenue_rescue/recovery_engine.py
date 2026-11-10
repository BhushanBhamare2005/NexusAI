import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.recovery_opportunity import RecoveryOpportunity
from app.repositories.transaction_repo import TransactionRepo

async def find_opportunities(db: AsyncSession, merchant_id: str) -> list[RecoveryOpportunity]:
    repo = TransactionRepo(db)
    txns = await repo.by_merchant(merchant_id)
    existing_result = await db.execute(
        select(RecoveryOpportunity.transaction_id).where(
            RecoveryOpportunity.merchant_id == merchant_id
        )
    )
    existing_transaction_ids = set(existing_result.scalars().all())
    created = []
    for t in txns:
        if t.status not in ("failed", "abandoned", "pending"):
            continue
        if t.amount <= 0 or t.id in existing_transaction_ids:
            continue
        opp = RecoveryOpportunity(
            id=str(uuid.uuid4()),
            merchant_id=merchant_id,
            transaction_id=t.id,
            txn_ref=t.txn_ref,
            amount=t.amount,
            reason=t.status,
            root_cause=t.root_cause or "unknown",
            recoverable=True,
            recommended_action=_recommend(t),
            conversion_status="not_contacted",
        )
        db.add(opp)
        created.append(opp)
        existing_transaction_ids.add(t.id)
    await db.commit()
    return created

def _recommend(t) -> str:
    if t.status == "failed":
        return "Retry payment via alternate method"
    if t.status == "pending":
        return "Wait for settlement; send status update"
    return "Send recovery link via SMS/WhatsApp"
