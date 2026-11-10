from app.agents.state.agent_state import AgentState
from app.engines.trustguard.approval_manager import request_approval
from app.db.session import AsyncSessionLocal

async def approval_node(state: AgentState) -> AgentState:
    if not state.get("needs_approval"):
        return state
    async with AsyncSessionLocal() as db:
        a = await request_approval(
            db,
            case_id=state["case_id"],
            run_id=state["run_id"],
            action=state["selected_action"],
            reason="; ".join(state.get("risk_reasons") or ["risk flagged"]),
            risk_level=state["risk_level"],
        )
        state["approval_id"] = a.id
    state["status"] = "awaiting_approval"
    return state
