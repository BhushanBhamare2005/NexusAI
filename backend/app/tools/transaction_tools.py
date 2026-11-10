from sqlalchemy.ext.asyncio import AsyncSession
from app.integrations.payment_provider import get_payment_provider
from app.integrations.paytm_mock.payment_api import lookup_payment
from app.integrations.paytm_mock.settlement_api import settlement_status

async def lookup_txn(db: AsyncSession, txn_ref: str) -> dict:
    client = get_payment_provider(db)
    data = await lookup_payment(client, txn_ref)
    if not data:
        return {"found": False, "txn_ref": txn_ref}
    return {"found": True, **data}

async def get_settlement(db: AsyncSession, settlement_id: str) -> dict:
    client = get_payment_provider(db)
    data = await settlement_status(client, settlement_id)
    return data or {"status": "not_found"}
