# Paytm NEXUS AI

**Autonomous Business Resolution & Recovery Teammate**
*From Customer Intent to Verified Business Outcome.*

NEXUS is an AI teammate that investigates payment issues, executes safe actions via tools, verifies outcomes, and produces a tamper-evident resolution ledger.

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
Copy-Item .env.example .env        # Windows PowerShell
# cp .env.example .env             # macOS/Linux
# Set unique NEXUS_BOOTSTRAP_USERNAME and NEXUS_BOOTSTRAP_PASSWORD values
# (minimum 12 characters) in .env before first startup.
python -m scripts.seed_db
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173 and sign in with the bootstrap manager account.
The first manager is created only when the user table is empty. Managers can
create agent accounts from TrustGuard.

API docs: http://localhost:8000/docs

### Vercel deployment

The frontend and FastAPI backend are deployed as separate Vercel projects. Set
`DATABASE_URL`, `JWT_SECRET`, `NEXUS_BOOTSTRAP_USERNAME`,
`NEXUS_BOOTSTRAP_PASSWORD`, and `CORS_ORIGINS` in the backend project's
Production environment. Set `VITE_API_URL` in the frontend project's Production
environment to the backend deployment URL, then redeploy both projects.
`GEMINI_API_KEY` is optional; without it, the rule-based fallback is used.
The backend runtime dependencies are in `backend/requirements.txt`;
`requirements-dev.txt` adds test tools, and `requirements-optional.txt` contains
the heavyweight optional analytics and embedding packages.

### Optional integrations

- **Gemini:** set `GEMINI_API_KEY` to enable LLM intent/diagnosis/responses;
  deterministic rules and policy retrieval remain available without it.
- **Twilio:** configure `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`,
  `TWILIO_FROM_NUMBER`, and `TWILIO_ENABLED=true`. SMS is sent only to a customer
  with recorded opt-in consent; otherwise notifications stay simulated/not sent.
- **Payments:** `PaymentProvider` currently selects the local seeded-data mock.
  Add an authorized provider adapter and credentials before handling any real
  transactions; live Paytm operations are not enabled.
- **JWT:** configure a stable, random `JWT_SECRET` in deployments. Without an
  environment value, a random process-local key is generated.

The project logs HTTP requests and exposes manager-only metrics at
`/api/v1/health/metrics`.

### Docker Compose

Before `docker compose up --build`, set `POSTGRES_PASSWORD`, `JWT_SECRET`,
`NEXUS_BOOTSTRAP_USERNAME`, and `NEXUS_BOOTSTRAP_PASSWORD` in the environment
or in a root-level `.env` file. Use URL-safe database-password characters and
a random 32+ character JWT secret.

## Screens
1. **Command Center** — live cases, KPIs
2. **AI Teammate Workspace** — chat + 8-step execution timeline
3. **Transaction Intelligence** — investigate txn evidence
4. **TrustGuard** — risk levels, approvals, duplicate-refund prevention
5. **Revenue Rescue** — recoverable failed payments
6. **Evidence Center** — hash-chained audit ledger

## Disclaimer
All Paytm APIs are **simulated**. No real financial operations occur.
