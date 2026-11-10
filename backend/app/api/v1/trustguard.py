from fastapi import APIRouter, Depends, HTTPException
from app.core.security import require
from app.schemas.trustguard import ApprovalOut, ApprovalDecision
from app.db.session import AsyncSessionLocal
from app.repositories.approval_repo import ApprovalRepo
from app.engines.trustguard.approval_manager import decide

router = APIRouter(prefix="/trustguard", tags=["trustguard"])

@router.get("/approvals", response_model=list[ApprovalOut])
async def pending(_user: dict = Depends(require("check_refund_eligibility"))):
    async with AsyncSessionLocal() as db:
        return await ApprovalRepo(db).pending()

@router.post("/approvals/{approval_id}/decide", response_model=ApprovalOut)
async def decide_route(
    approval_id: str,
    body: ApprovalDecision,
    _user: dict = Depends(require("initiate_refund")),
):
    async with AsyncSessionLocal() as db:
        try:
            a = await decide(db, approval_id, body.decision, _user["sub"])
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from exc
        if not a:
            raise HTTPException(404, "not found")

    from app.services import agent_service

    resume = (
        agent_service.resume_approved_run
        if body.decision == "approved"
        else agent_service.reject_approval_run
    )
    run = await resume(a.run_id)
    if not run:
        raise HTTPException(404, "associated agent run not found")
    return a
