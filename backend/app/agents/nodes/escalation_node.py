from app.agents.state.agent_state import AgentState

async def escalation_node(state: AgentState) -> AgentState:
    state["status"] = "escalated"
    state["final_response"] = (
        f"I've escalated this case to a human specialist. "
        f"Your case reference: {state['case_id']}. "
        f"We'll contact you shortly."
    )
    state["step_index"] = 8
    return state
