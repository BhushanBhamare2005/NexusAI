"""Simulated provider adapter. Reads seeded records; it never contacts Paytm."""
import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.transaction_repo import TransactionRepo
from app.repositories.refund_repo import RefundRepo
from app.models.refund import Refund
from app.integrations.paytm_mock.refund_api import check_refund_eligibility

class PaytmMockClient:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.txns = TransactionRepo(db)
        self.refunds = RefundRepo(db)

    async def get_transaction(self, txn_ref: str):
        return await self.txns.by_ref(txn_ref)

    async def get_settlement(self, settlement_id: str):
        # Simulated settlement lookup
        if not settlement_id:
            return None
        return {"settlement_id": settlement_id, "status": "processing"}

    async def existing_refunds(self, txn_id: str):
        return await self.refunds.by_transaction(txn_id)

    async def check_refund_eligibility(self, txn_ref: str) -> dict:
        return await check_refund_eligibility(self, txn_ref)

    async def initiate_refund(self, txn_ref: str, reason: str) -> dict:
        eligibility = await self.check_refund_eligibility(txn_ref)
        if not eligibility.get("eligible"):
            return {"initiated": False, **eligibility}
        txn = await self.get_transaction(txn_ref)
        if not txn:
            return {"initiated": False, "reason": "transaction_not_found"}
        refund = Refund(
            id=str(uuid.uuid4()),
            transaction_id=txn.id,
            amount=txn.amount,
            reason=reason,
            status="initiated",
        )
        self.db.add(refund)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            existing = await self.existing_refunds(txn.id)
            if existing:
                return {
                    "initiated": False,
                    "eligible": False,
                    "reason": "refund_already_exists",
                    "existing_refund_id": existing[0].id,
                }
            raise
        return {"initiated": True, "refund_id": refund.id, "amount": txn.amount}
