from .client import PaytmMockClient

async def lookup_payment(client: PaytmMockClient, txn_ref: str):
    txn = await client.get_transaction(txn_ref)
    if not txn:
        return None
    return {
        "txn_ref": txn.txn_ref,
        "customer_id": txn.customer_id,
        "merchant_id": txn.merchant_id,
        "amount": txn.amount,
        "status": txn.status,
        "upi_ref": txn.upi_ref,
        "settlement_id": txn.settlement_id,
    }
