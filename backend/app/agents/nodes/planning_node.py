from app.agents.state.agent_state import AgentState

async def planning_node(state: AgentState) -> AgentState:
    txn = state.get("txn_data") or {}
    status = txn.get("status")
    intent = state.get("intent")

    if intent == "general_question" and state.get("knowledge_evidence"):
        action = "answer_from_knowledge"
    elif intent == "refund_request" and status == "failed":
        action = "initiate_refund"
    elif intent == "duplicate_refund_concern":
        action = "create_investigation_ticket"
    elif status in ("pending", None) or not txn.get("found"):
        action = "create_investigation_ticket"
    elif status == "success":
        action = "send_status_update"
    else:
        action = "create_investigation_ticket"

    state["selected_action"] = action
    state["action_args"] = {
        "txn_ref": (state.get("entities") or {}).get("txn_ref")
        or state.get("transaction_ref"),
        "reason": state.get("diagnosis"),
    }
    state["step_index"] = 4
    return state
