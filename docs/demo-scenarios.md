# Demo Scenarios

## Scenario 1 — Payment dispute
1. Seed DB (`python -m scripts.seed_db`)
2. Open AgentWorkspace, message: "Maine ₹2500 pay kiye, merchant ko nahi mila. TXN100000"
3. Observe timeline: intent → investigate → diagnose (pending) → plan (ticket) → execute → verify → resolved
4. Open Audit page: hash chain intact

## Scenario 2 — Duplicate refund prevention
1. Create a failed transaction; manually insert a refund row
2. Request refund via agent → TrustGuard blocks
3. Show TrustGuard screen: risk_level = blocked

## Scenario 3 — Revenue rescue
1. `POST /api/v1/revenue/opportunities/scan?merchantId=m_001`
2. Open Revenue page: recoverable opportunities appear
3. Trigger follow-up → status changes to `contacted`
