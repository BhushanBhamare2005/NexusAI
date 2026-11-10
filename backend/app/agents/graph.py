from langgraph.graph import StateGraph, END
from app.agents.state.agent_state import AgentState
from app.agents.nodes.intent_node import intent_node
from app.agents.nodes.context_node import context_node
from app.agents.nodes.investigation_node import investigation_node
from app.agents.nodes.diagnosis_node import diagnosis_node
from app.agents.nodes.planning_node import planning_node
from app.agents.nodes.risk_node import risk_node
from app.agents.nodes.approval_node import approval_node
from app.agents.nodes.execution_node import execution_node
from app.agents.nodes.verification_node import verification_node
from app.agents.nodes.response_node import response_node
from app.agents.nodes.escalation_node import escalation_node
from app.agents.edges.routing import route_after_risk, route_after_approval

def build_graph():
    g = StateGraph(AgentState)
    g.add_node("intent_step", intent_node)
    g.add_node("context_step", context_node)
    g.add_node("investigation_step", investigation_node)
    g.add_node("diagnosis_step", diagnosis_node)
    g.add_node("planning_step", planning_node)
    g.add_node("risk_step", risk_node)
    g.add_node("approval_step", approval_node)
    g.add_node("execution_step", execution_node)
    g.add_node("verification_step", verification_node)
    g.add_node("response_step", response_node)
    g.add_node("escalation_step", escalation_node)

    g.set_entry_point("intent_step")
    g.add_edge("intent_step", "context_step")
    g.add_edge("context_step", "investigation_step")
    g.add_edge("investigation_step", "diagnosis_step")
    g.add_edge("diagnosis_step", "planning_step")
    g.add_edge("planning_step", "risk_step")

    g.add_conditional_edges("risk_step", route_after_risk, {
        "execution": "execution_step",
        "approval": "approval_step",
        "escalation": "escalation_step",
    })
    g.add_conditional_edges("approval_step", route_after_approval, {
        "execution": "execution_step",
        "response": "response_step",
    })
    g.add_edge("execution_step", "verification_step")
    g.add_edge("verification_step", "response_step")
    g.add_edge("response_step", END)
    g.add_edge("escalation_step", END)
    return g.compile()

_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
