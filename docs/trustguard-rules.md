# TrustGuard Rules
| Rule | Trigger | Level |
|---|---|---|
| Duplicate refund | existing_refund_id present | blocked |
| Already refunded | status == refunded | blocked |
| Pending txn | status == pending | approval_needed |
| High value | amount >= 10000 | approval_needed |
```

---

# Final Bootstrap Sequence

```bash
# 1. Root
mkdir paytm-nexus-ai && cd paytm-nexus-ai

# 2. Backend
mkdir -p backend/app/{core,api/v1,agents/{state,nodes,edges,prompts},tools,services,engines/{trustguard,revenue_rescue},rag,models,schemas,repositories,db,audit,integrations/paytm_mock,analytics,utils}
mkdir -p backend/{knowledge_base,scripts,tests}
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Start Postgres (docker or local), then:
python -m scripts.seed_db
uvicorn app.main:app --reload
# Open http://localhost:8000/docs

# 3. Frontend (new terminal)
cd ../frontend
npm install
cp .env.example .env
npm run dev
# Open http://localhost:5173
