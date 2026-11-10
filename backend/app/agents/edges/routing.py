from app.agents.state.agent_state import AgentState

def route_after_risk(state: AgentState) -> str:
    if state.get("risk_level") == "blocked":
        return "escalation"
    if state.get("needs_approval"):
        return "approval"
    return "execution"

def route_after_approval(state: AgentState) -> str:
    if state.get("status") == "awaiting_approval":
        return "response"
    return "execution"
