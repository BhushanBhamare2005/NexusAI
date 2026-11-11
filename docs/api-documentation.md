# API Reference

## Authentication and role management
- `POST /api/v1/auth/login` → exchange username/password for an expiring bearer token
- `GET /api/v1/auth/me` → return the active user's database-backed identity and role
- `GET /api/v1/auth/dashboards` → list dashboards authorized for the current role
- `GET /api/v1/auth/dashboards/{role}` → server-authorize a dashboard selection
- `GET /api/v1/auth/users` → list accounts (manager only)
- `POST /api/v1/auth/users` → create an account (manager only)
- `PATCH /api/v1/auth/users/{user_id}` → change role or active status (manager only)
- `GET /api/v1/auth/role-history` → list account creation and role/active-status history (manager only)

Role and active-status changes are stored in the production `users` table. The
backend checks the active database account against the JWT on each protected
request, so changing a role or deactivating an account invalidates its old
token. The API prevents removing the last active manager. Role assignment
history is stored separately in `role_assignment_history`; no password hashes
or secrets are included in these records.

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
