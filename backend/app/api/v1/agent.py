import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import require
from app.schemas.agent import AgentRunRequest, AgentRunOut
from app.services import agent_service

router = APIRouter(prefix="/agent", tags=["agent"])


@router.get("/evaluation")
async def evaluation(_user: dict = Depends(require("view_evaluation"))) -> dict:
    evaluation_path = Path("evaluation_results.json")
    if not evaluation_path.is_file():
        evaluation_path = Path(__file__).resolve().parents[4] / "evaluation_results.json"
    if not evaluation_path.is_file():
        raise HTTPException(404, "evaluation results not found; run scripts.run_evaluation")
    return json.loads(evaluation_path.read_text(encoding="utf-8"))


@router.post("/run", response_model=AgentRunOut)
async def run(req: AgentRunRequest, _user: dict = Depends(require("lookup_txn"))):
    return await agent_service.run_agent(
        req.message, req.customer_id, req.merchant_id, req.transaction_ref
    )

@router.get("/runs/{run_id}", response_model=AgentRunOut)
async def get_run(
    run_id: str,
    _user: dict = Depends(require("lookup_txn")),
):
    r = await agent_service.get_run(run_id)
    if not r:
        raise HTTPException(404, "run not found")
    return r

@router.get("/runs", response_model=list[AgentRunOut])
async def list_runs(
    limit: int = Query(20, ge=1, le=100),
    _user: dict = Depends(require("lookup_txn")),
):
    return await agent_service.list_runs(limit)
