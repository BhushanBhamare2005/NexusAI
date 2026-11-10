# API Reference

## Agent
- `POST /api/v1/agent/run` → run NEXUS on a message
- `GET /api/v1/agent/runs/{runId}`
- `GET /api/v1/agent/runs?limit=20`

## Transactions
- `GET /api/v1/transactions?q=&status=&merchantId=&customerId=`
- `GET /api/v1/transactions/{id}`

## TrustGuard
- `GET /api/v1/trustguard/approvals`
- `POST /api/v1/trustguard/approvals/{id}/decide`

## Revenue
- `GET /api/v1/revenue/summary?merchantId=`
- `GET /api/v1/revenue/opportunities?merchantId=`
- `POST /api/v1/revenue/opportunities/scan?merchantId=`
- `POST /api/v1/revenue/opportunities/{id}/followup`

## Audit
- `GET /api/v1/audit/events?caseId=`
- `GET /api/v1/audit/verify`
