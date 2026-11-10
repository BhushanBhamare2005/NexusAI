from app.agents.state.agent_state import AgentState

async def context_node(state: AgentState) -> AgentState:
    state.setdefault("tool_calls", [])
    state.setdefault("tool_results", [])
    state["step_index"] = 1
    return state
