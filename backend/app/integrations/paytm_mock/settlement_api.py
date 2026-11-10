from .client import PaytmMockClient

async def settlement_status(client: PaytmMockClient, settlement_id: str):
    return await client.get_settlement(settlement_id)
