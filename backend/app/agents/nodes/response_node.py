from app.agents.state.agent_state import AgentState
from app.agents.llm import format_prompt, llm_json
from app.agents.prompts.response_prompt import RESPONSE_PROMPT

async def response_node(state: AgentState) -> AgentState:
    if state.get("status") == "awaiting_approval":
        state["final_response"] = (
            f"Your case {state['case_id']} requires human approval before proceeding. "
            f"Reason: {'; '.join(state.get('risk_reasons') or [])}. "
            f"A specialist will review shortly."
        )
        return state

    diagnosis = state.get("diagnosis", "")
    action = state.get("selected_action", "")
    verified = (state.get("verification") or {}).get("verified", False)
    ref = state["case_id"][:8]

    parsed = await llm_json(
        format_prompt(
            RESPONSE_PROMPT,
            intent=state.get("intent"),
            diagnosis=diagnosis,
            action=action,
            results=state.get("tool_results"),
            verified=verified,
            case_id=ref,
        )
    )
    if parsed and parsed.get("response"):
        msg = parsed["response"]
    elif state.get("status") == "escalated":
        msg = (
            f"No refund was initiated. {diagnosis}. "
            f"Case reference: {ref}. A specialist will review this case."
        )
    elif action == "create_investigation_ticket":
        msg = (
            f"Your transaction has been identified. {diagnosis}. "
            f"I've created investigation case {ref} with transaction evidence attached. "
            f"No duplicate refund or payment has been initiated. "
            f"The case is now being tracked until the outcome is confirmed."
        )
    elif action == "initiate_refund":
        msg = (
            f"Refund has been initiated for your transaction. {diagnosis}. "
            f"Case reference: {ref}. Refunds typically reflect in 3–5 business days."
        )
    elif action == "send_status_update":
        if verified:
            msg = f"{diagnosis}. Case reference: {ref}. No further action needed."
        else:
            msg = (
                f"{diagnosis}. Case reference: {ref}. "
                "The notification could not be delivered; no update was sent."
            )
    elif action == "answer_from_knowledge":
        msg = f"{diagnosis} Case reference: {ref}."
    else:
        msg = f"Case {ref} has been created. {diagnosis}. We'll follow up shortly."

    if not verified and "(Note: verification pending.)" not in msg:
        msg += " (Note: verification pending.)"

    state["final_response"] = msg
    state["status"] = "resolved" if verified else "failed"
    state["step_index"] = 7
    return state
