import logging

import httpx

from app.agents.state.agent_state import AgentState
from app.tools.registry import build_registry
from app.db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def _notify(registry, **kwargs) -> dict:
    try:
        return await registry["send_notification"](**kwargs)
    except (ValueError, PermissionError, RuntimeError, httpx.HTTPError) as exc:
        logger.warning("Notification was not sent: %s", exc)
        return {
            "mode": "twilio",
            "delivered": False,
            "error": str(exc),
        }


async def execution_node(state: AgentState) -> AgentState:
    if state.get("status") == "awaiting_approval":
        return state

    action = state["selected_action"]
    async with AsyncSessionLocal() as db:
        registry = build_registry(db)

        if action == "create_investigation_ticket":
            call = {"id": "c_ticket", "name": "create_ticket", "args": {}, "status": "pending"}
            state["tool_calls"].append(call)
            result = await registry["create_ticket"](
                case_id=state["case_id"],
                run_id=state["run_id"],
                subject=f"Investigate {state.get('diagnosis','')}",
                description=state.get("user_message", ""),
                priority="high",
            )
            call["status"] = "success"
            call["result"] = result
            state["tool_results"].append(result)

            n = {"id": "c_notify", "name": "send_notification", "args": {}, "status": "pending"}
            state["tool_calls"].append(n)
            nr = await _notify(registry,
                channel="sms",
                recipient=state.get("customer_id") or "customer",
                message="Your payment issue has been logged and is being investigated.",
                case_id=state["case_id"],
            )
            n["status"] = (
                "success" if nr.get("accepted") or nr.get("delivered") else "error"
            )
            n["result"] = nr
            n["error"] = nr.get("error")
            state["tool_results"].append(nr)

        elif action == "initiate_refund":
            txn_ref = (state.get("action_args") or {}).get("txn_ref")
            call = {
                "id": "c_refund",
                "name": "initiate_refund",
                "args": {"txn_ref": txn_ref},
                "status": "pending",
            }
            state["tool_calls"].append(call)
            result = (
                await registry["initiate_refund"](txn_ref=txn_ref)
                if txn_ref
                else {"initiated": False, "reason": "transaction_reference_missing"}
            )
            call["status"] = "success" if result.get("initiated") else "error"
            call["result"] = result
            state["tool_results"].append(result)
            if not result.get("initiated"):
                state["status"] = "escalated"
                state["risk_level"] = "blocked"
                state["risk_reasons"] = [
                    f"Refund was not initiated: {result.get('reason', 'eligibility changed')}"
                ]

        elif action == "send_status_update":
            n = {"id": "c_status", "name": "send_notification", "args": {}, "status": "pending"}
            state["tool_calls"].append(n)
            nr = await _notify(registry,
                channel="sms",
                recipient=state.get("customer_id") or "customer",
                message="Your payment succeeded. Settlement may take up to 24 hours.",
                case_id=state["case_id"],
            )
            n["status"] = (
                "success" if nr.get("accepted") or nr.get("delivered") else "error"
            )
            n["result"] = nr
            n["error"] = nr.get("error")
            state["tool_results"].append(nr)
        elif action == "answer_from_knowledge":
            state["tool_results"].append(
                {
                    "knowledge_evidence": state.get("knowledge_evidence", []),
                    "source": "local knowledge base",
                }
            )
        else:
            raise ValueError(f"Unsupported agent action: {action}")

    state["step_index"] = 5
    return state
