# Evaluation and Prototype Scope

## What works end-to-end

- An 8-step LangGraph resolution cycle investigates a message and returns a case outcome. Gemini is optional; the workflow falls back to rule-based intent and diagnosis.
- Policy passages are retrieved during diagnosis and shown as case evidence; retrieval currently uses deterministic keyword ranking.
- TrustGuard checks refund eligibility, blocks duplicate refunds, and supports approval decisions for protected actions.
- Agent outcomes are written to a hash-chain audit ledger that can be verified through the API.
- Revenue Rescue scans seeded transactions for opportunities and records simulated follow-ups.
- A 200-case evaluation script measures intent matches and verified outcomes and writes `evaluation_results.json` for the dashboard chart.

## Known limitations (prototype scope)

| Area | Current implementation |
|---|---|
| AI model | Gemini LLM with rule fallback; an API key is required for LLM responses. |
| Payments | Provider interface with seeded-data mock adapter; no real payment or refund is made. |
| Messaging | Twilio adapter is opt-in; disabled configuration uses a persisted simulated/not-sent log that appears in Evidence Center. Actual delivery requires valid account credentials and recorded customer SMS consent. |
| Auth | Persisted local accounts with bcrypt password hashes, JWTs, manager bootstrap, account creation, and API role checks. Configure a stable JWT secret for multi-process deployments. |
| DB | SQLite by default; PostgreSQL is supported by configuration. |
| Observability | HTTP request/status/latency and LLM success/fallback counters are exposed to managers; no external monitoring provider is configured. |

## Measured

- Intent accuracy and verified resolution rate: run `python -m scripts.run_evaluation` to measure the current seeded dataset. These scripted scenarios are not a representative production benchmark.
- Latest seeded run: 100.0% intent match and 22.0% verified outcomes (44/200); simulated notifications are correctly counted as unverified, not as completed deliveries.
- Duplicate refund prevention: 100% in `test_trustguard.py`.
- API smoke tests: passing for the simulated API workflows.
