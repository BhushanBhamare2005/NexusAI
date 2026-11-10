import pytest
from unittest.mock import AsyncMock
from app.agents.graph import build_graph
from app.agents.nodes import diagnosis_node as diagnosis_module
from app.agents.nodes.diagnosis_node import diagnosis_node
from app.agents.nodes.planning_node import planning_node

def test_graph_compiles():
    g = build_graph()
    assert g is not None
    assert hasattr(g, "ainvoke")


@pytest.mark.asyncio
async def test_general_question_uses_retrieved_policy(monkeypatch):
    monkeypatch.setattr(
        diagnosis_module,
        "llm_json",
        AsyncMock(return_value=None),
    )
    state = {
        "intent": "general_question",
        "user_message": "Can you explain bank payment status guidelines?",
        "txn_data": None,
    }

    await diagnosis_node(state)
    await planning_node(state)

    assert state["knowledge_evidence"]
    assert state["selected_action"] == "answer_from_knowledge"
