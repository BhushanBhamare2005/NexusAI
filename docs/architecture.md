## Prototype scope
All Paytm payment and refund flows are SIMULATED against seeded data; no real money moves. SMS is simulated by default; optional Twilio delivery requires configured credentials and recorded customer opt-in. Production swaps app/integrations/paytm_mock/ for authorized Paytm Business API adapters behind the same interface.

# Architecture
Customer/Merchant UI → FastAPI → LangGraph orchestrator → specialized nodes → TrustGuard → tool execution → verification → audit ledger.

## Components
- **Frontend:** React + TS + Vite + Tailwind
- **Backend:** FastAPI, async SQLAlchemy, LangGraph
- **DB:** SQLite by default; PostgreSQL is supported by configuration
- **Safety:** TrustGuard risk engine + approval manager + hash-chain audit
- **Revenue Rescue:** recovery engine + followup generator + conversion tracker
- **RAG:** local policy passages with deterministic keyword ranking
