from app.agents.state.agent_state import AgentState
from app.db.session import AsyncSessionLocal
from app.engines.trustguard.risk_engine import assess
from app.tools.registry import build_registry

async def risk_node(state: AgentState) -> AgentState:
    eligibility = {}
    if state.get("selected_action") == "initiate_refund":
        txn_ref = (state.get("action_args") or {}).get("txn_ref")
        if not txn_ref:
            eligibility = {"eligible": False, "reason": "transaction_reference_missing"}
        else:
            async with AsyncSessionLocal() as db:
                tool_call = {
                    "id": "c_refund_check",
                    "name": "check_refund_eligibility",
                    "args": {"txn_ref": txn_ref},
                    "status": "pending",
                }
                state.setdefault("tool_calls", []).append(tool_call)
                eligibility = await build_registry(db)["check_refund_eligibility"](
                    txn_ref=txn_ref
                )
                tool_call["result"] = eligibility
                tool_call["status"] = "success"
                state.setdefault("tool_results", []).append(eligibility)

    ctx = {
        "txn": state.get("txn_data") or {},
        "eligibility": eligibility,
        "action": state.get("selected_action"),
    }
    result = await assess(None, ctx)
    state["risk_level"] = result["level"]
    state["risk_score"] = result["score"]
    state["risk_reasons"] = result["reasons"]
    state["needs_approval"] = result["level"] == "approval_needed"
    if result["level"] == "blocked":
        state["status"] = "escalated"
    state["step_index"] = 4
    return state
