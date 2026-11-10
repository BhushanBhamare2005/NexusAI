from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import PaytmMockClient

async def check_refund_eligibility(client: PaytmMockClient, txn_ref: str):
    txn = await client.get_transaction(txn_ref)
    if not txn:
        return {"eligible": False, "reason": "transaction_not_found"}
    existing = await client.existing_refunds(txn.id)
    if existing:
        return {"eligible": False, "reason": "refund_already_exists",
                "existing_refund_id": existing[0].id}
    if txn.status == "refunded":
        return {"eligible": False, "reason": "already_refunded"}
    if txn.status != "failed":
        return {"eligible": False, "reason": "transaction_status_not_refundable"}
    return {"eligible": True, "reason": "ok"}
