from app.agents.state.agent_state import AgentState
from app.repositories.ticket_repo import TicketRepo
from app.models.refund import Refund
from app.db.session import AsyncSessionLocal

async def verification_node(state: AgentState) -> AgentState:
    if state.get("status") == "awaiting_approval":
        state["verification"] = {"verified": False, "reason": "pending_approval"}
        return state

    action = state["selected_action"]
    verified = False
    details = {}

    async with AsyncSessionLocal() as db:
        if action == "create_investigation_ticket":
            tickets = await TicketRepo(db).by_run(state["run_id"])
            verified = len(tickets) > 0
            details = {"ticket_count": len(tickets), "ticket_id": tickets[0].id if tickets else None}
        elif action == "initiate_refund":
            refund_call = next(
                (
                    call
                    for call in reversed(state.get("tool_calls", []))
                    if call.get("name") == "initiate_refund"
                ),
                {},
            )
            refund_id = (refund_call.get("result") or {}).get("refund_id")
            refund = await db.get(Refund, refund_id) if refund_id else None
            verified = refund is not None
            details = {"refund_id": refund_id, "refund_status": refund.status if refund else None}
        elif action == "answer_from_knowledge":
            verified = bool(state.get("knowledge_evidence"))
            details = {
                "type": "knowledge_base",
                "passages": len(state.get("knowledge_evidence", [])),
            }
        else:
            notification = next(
                (
                    call
                    for call in reversed(state.get("tool_calls", []))
                    if call.get("name") == "send_notification"
                ),
                {},
            )
            result = notification.get("result") or {}
            verified = result.get("delivered", False)
            details = {
                "type": "notification",
                "mode": result.get("mode"),
                "delivered": verified,
            }

    state["verification"] = {"verified": verified, "details": details}
    state["step_index"] = 6
    return state
