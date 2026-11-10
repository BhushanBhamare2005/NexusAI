from sqlalchemy.ext.asyncio import AsyncSession
from app.integrations.payment_provider import get_payment_provider

async def check_refund_eligibility(db: AsyncSession, txn_ref: str) -> dict:
    provider = get_payment_provider(db)
    return await provider.check_refund_eligibility(txn_ref)

async def initiate_refund(db: AsyncSession, txn_ref: str, reason: str = "customer_request") -> dict:
    provider = get_payment_provider(db)
    return await provider.initiate_refund(txn_ref, reason)
