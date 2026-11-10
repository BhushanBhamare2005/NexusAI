import uuid
from datetime import datetime
from app.db.session import AsyncSessionLocal
from app.agents.graph import get_graph
from app.agents.nodes.execution_node import execution_node
from app.agents.nodes.response_node import response_node
from app.agents.nodes.verification_node import verification_node
from app.models.agent_run import AgentRun
from app.audit.ledger import append as audit_append
from sqlalchemy import select

async def run_agent(message: str, customer_id: str | None = None,
                    merchant_id: str | None = None, transaction_ref: str | None = None) -> dict:
    run_id = str(uuid.uuid4())
    case_id = f"case_{run_id[:8]}"

    initial = {
        "run_id": run_id,
        "case_id": case_id,
        "user_message": message,
        "customer_id": customer_id,
        "merchant_id": merchant_id,
        "transaction_ref": transaction_ref,
        "tool_calls": [],
        "tool_results": [],
        "status": "running",
    }

    graph = get_graph()
    final_state = await graph.ainvoke(initial)

    async with AsyncSessionLocal() as db:
        run = AgentRun(
            id=run_id,
            case_id=case_id,
            status=final_state.get("status", "failed"),
            intent=final_state.get("intent"),
            root_cause=final_state.get("diagnosis"),
            selected_action=final_state.get("selected_action"),
            risk_level=final_state.get("risk_level"),
            steps=_build_steps(final_state),
            tool_calls=final_state.get("tool_calls", []),
            state_data=final_state,
            final_response=final_state.get("final_response"),
        )
        db.add(run)
        await db.commit()

        await audit_append(db, case_id, run_id, "agent_run_completed",
                          payload={"status": run.status, "intent": run.intent})

        created_at = run.created_at
        updated_at = run.updated_at

    return _serialize(final_state, run_id, case_id, created_at, updated_at)

def _build_steps(state: dict) -> list[dict]:
    labels = ["Understand", "Investigate", "Diagnose", "Decide",
              "Execute", "Verify", "Deliver", "Escalate"]
    current = state.get("step_index", 1)
    steps = []
    for i, label in enumerate(labels, start=1):
        status = "done" if i <= current else "pending"
        if i == 4 and state.get("needs_approval"):
            status = "done"
        steps.append({"step": i, "name": label, "status": status})
    return steps

def _serialize(
    state: dict,
    run_id: str,
    case_id: str,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
) -> dict:
    now = datetime.utcnow()
    return {
        "runId": run_id,
        "caseId": case_id,
        "status": state.get("status", "failed"),
        "intent": state.get("intent"),
        "rootCause": state.get("diagnosis"),
        "selectedAction": state.get("selected_action"),
        "riskLevel": state.get("risk_level"),
        "steps": _build_steps(state),
        "toolCalls": state.get("tool_calls", []),
        "finalResponse": state.get("final_response"),
        "knowledgeEvidence": state.get("knowledge_evidence", []),
        "verified": (state.get("verification") or {}).get("verified", False),
        "createdAt": (created_at or now).isoformat(),
        "updatedAt": (updated_at or now).isoformat(),
    }


async def resume_approved_run(run_id: str) -> dict | None:
    async with AsyncSessionLocal() as db:
        run = await db.get(AgentRun, run_id)
        if not run:
            return None
        state = dict(run.state_data or {})

    if not state:
        raise RuntimeError(f"Approval run {run_id} has no saved agent state")

    state["status"] = "running"
    state["needs_approval"] = False
    await execution_node(state)
    await verification_node(state)
    await response_node(state)

    async with AsyncSessionLocal() as db:
        run = await db.get(AgentRun, run_id)
        if not run:
            return None
        run.status = state.get("status", "failed")
        run.steps = _build_steps(state)
        run.tool_calls = state.get("tool_calls", [])
        run.state_data = state
        run.final_response = state.get("final_response")
        run.updated_at = datetime.utcnow()
        await db.commit()
        await audit_append(
            db,
            run.case_id,
            run_id,
            "approval_resolved",
            payload={"status": run.status},
        )
        return {
            "runId": run.id,
            "caseId": run.case_id,
            "status": run.status,
            "intent": run.intent,
            "rootCause": run.root_cause,
            "selectedAction": run.selected_action,
            "riskLevel": run.risk_level,
            "steps": run.steps or [],
            "toolCalls": run.tool_calls or [],
            "finalResponse": run.final_response,
            "knowledgeEvidence": (run.state_data or {}).get("knowledge_evidence", []),
            "verified": (run.state_data or {}).get("verification", {}).get("verified", False),
            "createdAt": run.created_at.isoformat(),
            "updatedAt": run.updated_at.isoformat(),
        }


async def reject_approval_run(run_id: str) -> dict | None:
    async with AsyncSessionLocal() as db:
        run = await db.get(AgentRun, run_id)
        if not run:
            return None
        state = dict(run.state_data or {})
        state["status"] = "escalated"
        state["final_response"] = (
            f"Approval was rejected. Case reference: {run.case_id}."
        )
        run.status = "escalated"
        run.state_data = state
        run.final_response = state["final_response"]
        run.updated_at = datetime.utcnow()
        run.steps = _build_steps({**state, "step_index": 8})
        await db.commit()
        await audit_append(
            db,
            run.case_id,
            run_id,
            "approval_rejected",
            payload={"status": run.status},
        )
        return {
            "runId": run.id,
            "caseId": run.case_id,
            "status": run.status,
            "intent": run.intent,
            "rootCause": run.root_cause,
            "selectedAction": run.selected_action,
            "riskLevel": run.risk_level,
            "steps": run.steps or [],
            "toolCalls": run.tool_calls or [],
            "finalResponse": run.final_response,
            "knowledgeEvidence": (run.state_data or {}).get("knowledge_evidence", []),
            "verified": (run.state_data or {}).get("verification", {}).get("verified", False),
            "createdAt": run.created_at.isoformat(),
            "updatedAt": run.updated_at.isoformat(),
        }

async def get_run(run_id: str) -> dict | None:
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(AgentRun).where(AgentRun.id == run_id))
        run = res.scalar_one_or_none()
        if not run:
            return None
        return {
            "runId": run.id,
            "caseId": run.case_id,
            "status": run.status,
            "intent": run.intent,
            "rootCause": run.root_cause,
            "selectedAction": run.selected_action,
            "riskLevel": run.risk_level,
            "steps": run.steps or [],
            "toolCalls": run.tool_calls or [],
            "finalResponse": run.final_response,
            "knowledgeEvidence": (run.state_data or {}).get("knowledge_evidence", []),
            "verified": (run.state_data or {}).get("verification", {}).get("verified", False),
            "createdAt": run.created_at.isoformat(),
            "updatedAt": run.updated_at.isoformat(),
        }

async def list_runs(limit: int = 20) -> list[dict]:
    async with AsyncSessionLocal() as db:
        res = await db.execute(
            select(AgentRun).order_by(AgentRun.created_at.desc()).limit(limit)
        )
        runs = res.scalars().all()
        return [{
            "runId": r.id,
            "caseId": r.case_id,
            "status": r.status,
            "intent": r.intent,
            "rootCause": r.root_cause,
            "selectedAction": r.selected_action,
            "riskLevel": r.risk_level,
            "steps": r.steps or [],
            "toolCalls": r.tool_calls or [],
            "finalResponse": r.final_response,
            "knowledgeEvidence": (r.state_data or {}).get("knowledge_evidence", []),
            "verified": (r.state_data or {}).get("verification", {}).get("verified", False),
            "createdAt": r.created_at.isoformat(),
            "updatedAt": r.updated_at.isoformat(),
        } for r in runs]
