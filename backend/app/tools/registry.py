"""Central tool registry — only registered tools may be invoked by the agent."""
from typing import Callable, Awaitable, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.tools import (
    transaction_tools, refund_tools, ticket_tools, notification_tools, analytics_tools,
)

ToolFn = Callable[..., Awaitable[dict[str, Any]]]

def build_registry(db: AsyncSession) -> dict[str, ToolFn]:
    return {
        "lookup_txn": lambda **kw: transaction_tools.lookup_txn(db, **kw),
        "get_settlement": lambda **kw: transaction_tools.get_settlement(db, **kw),
        "check_refund_eligibility": lambda **kw: refund_tools.check_refund_eligibility(db, **kw),
        "initiate_refund": lambda **kw: refund_tools.initiate_refund(db, **kw),
        "create_ticket": lambda **kw: ticket_tools.create_ticket(db, **kw),
        "send_notification": lambda **kw: notification_tools.send_notification(db, **kw),
        "merchant_metrics": lambda **kw: analytics_tools.merchant_metrics(db, **kw),
    }
