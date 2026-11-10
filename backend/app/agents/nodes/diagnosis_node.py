from app.agents.state.agent_state import AgentState
from app.agents.llm import format_prompt, llm_json
from app.agents.prompts.diagnosis_prompt import DIAGNOSIS_PROMPT
from app.rag.retriever import retrieve

async def diagnosis_node(state: AgentState) -> AgentState:
    txn = state.get("txn_data") or {}
    status = txn.get("status")
    knowledge = retrieve(
        f"{state.get('user_message', '')} {status or ''} refund payment settlement"
    )
    state["knowledge_evidence"] = knowledge

    parsed = None
    if txn.get("found") or state.get("intent") == "general_question":
        parsed = await llm_json(
            format_prompt(
                DIAGNOSIS_PROMPT,
                txn=txn,
                message=state.get("user_message", ""),
                knowledge="\n".join(knowledge)
                if knowledge
                else "No relevant knowledge-base passages were retrieved.",
            )
        )

    if parsed and parsed.get("root_cause"):
        diagnosis = parsed["root_cause"]
    elif state.get("intent") == "general_question" and knowledge:
        diagnosis = knowledge[0][:600]
    elif not txn.get("found"):
        diagnosis = "Transaction not found in system"
    elif status == "pending":
        diagnosis = "Payment pending — settlement in progress"
    elif status == "failed":
        diagnosis = "Payment failed at bank/UPI layer"
    elif status == "success":
        diagnosis = "Payment succeeded — settlement may be delayed"
    elif status == "refunded":
        diagnosis = "Refund already processed"
    else:
        diagnosis = f"Unknown state: {status}"

    state["diagnosis"] = diagnosis
    state["step_index"] = 3
    return state
