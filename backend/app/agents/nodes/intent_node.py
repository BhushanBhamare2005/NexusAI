import re
from app.agents.state.agent_state import AgentState
from app.agents.llm import format_prompt, llm_json
from app.agents.prompts.intent_prompt import INTENT_PROMPT

async def intent_node(state: AgentState) -> AgentState:
    msg = state.get("user_message", "")
    parsed = await llm_json(format_prompt(INTENT_PROMPT, message=msg))
    if parsed and parsed.get("intent"):
        intent = parsed["intent"]
        entities = parsed.get("entities", {})
        if not isinstance(entities, dict):
            entities = {}
    else:
        lowered = msg.lower()
        if "refund" in lowered and any(k in lowered for k in ("duplicate", "already")):
            intent = "duplicate_refund_concern"
        elif any(k in lowered for k in ("refund", "paise wapas", "money back")):
            intent = "refund_request"
        elif any(k in lowered for k in ("pending", "nahi mila", "not received", "kat gaye")):
            intent = "payment_status_mismatch"
        elif any(k in lowered for k in ("settlement", "settle")):
            intent = "settlement_delay"
        elif any(k in lowered for k in ("recover", "retry", "failed payment")):
            intent = "revenue_recovery"
        else:
            intent = "general_question"

        entities: dict[str, str | float] = {}
        m = re.search(r"₹?\s?(\d{2,7})", msg)
        if m:
            entities["amount"] = float(m.group(1))

    transaction_ref = state.get("transaction_ref")
    if not transaction_ref:
        ref_match = re.search(r"\bTXN[A-Z0-9_-]*\d[A-Z0-9_-]*\b", msg, re.IGNORECASE)
        transaction_ref = ref_match.group(0) if ref_match else None
    if transaction_ref:
        entities["txn_ref"] = transaction_ref

    state["intent"] = intent
    state["entities"] = entities
    state["step_index"] = 1
    return state
