from app.agents.state.agent_state import AgentState
from app.tools.registry import build_registry
from app.db.session import AsyncSessionLocal

async def investigation_node(state: AgentState) -> AgentState:
    ref = (state.get("entities") or {}).get("txn_ref") or state.get("transaction_ref")
    if not ref:
        state["txn_data"] = None
        state["step_index"] = 2
        return state

    async with AsyncSessionLocal() as db:
        registry = build_registry(db)
        call = {"id": "c1", "name": "lookup_txn", "args": {"txn_ref": ref}, "status": "pending"}
        state["tool_calls"].append(call)
        result = await registry["lookup_txn"](txn_ref=ref)
        call["status"] = "success"
        call["result"] = result
        state["tool_results"].append(result)
        state["txn_data"] = result
        state["customer_id"] = state.get("customer_id") or result.get("customer_id")
        state["merchant_id"] = state.get("merchant_id") or result.get("merchant_id")

    state["step_index"] = 2
    return state
