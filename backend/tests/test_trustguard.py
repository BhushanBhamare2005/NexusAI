from app.engines.trustguard.risk_engine import assess
import pytest

@pytest.mark.asyncio
async def test_duplicate_refund_blocked():
    ctx = {"txn": {"status": "failed", "amount": 500},
           "eligibility": {"reason": "refund_already_exists", "existing_refund_id": "r1"}}
    result = await assess(None, ctx)
    assert result["level"] == "blocked"

@pytest.mark.asyncio
async def test_high_value_requires_approval():
    ctx = {"txn": {"status": "failed", "amount": 15000}, "eligibility": {"reason": "ok"}}
    result = await assess(None, ctx)
    assert result["level"] == "approval_needed"
