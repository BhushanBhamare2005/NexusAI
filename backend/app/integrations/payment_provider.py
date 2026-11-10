from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class PaymentProvider(Protocol):
    async def get_transaction(self, txn_ref: str): ...

    async def get_settlement(self, settlement_id: str): ...

    async def existing_refunds(self, txn_id: str): ...

    async def check_refund_eligibility(self, txn_ref: str) -> dict: ...

    async def initiate_refund(self, txn_ref: str, reason: str) -> dict: ...


def get_payment_provider(db: AsyncSession) -> PaymentProvider:
    from app.integrations.paytm_mock.client import PaytmMockClient

    return PaytmMockClient(db)
