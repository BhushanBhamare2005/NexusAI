import re

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.notification_log import NotificationLog


async def recent(limit: int = 20) -> list[dict]:
    async with AsyncSessionLocal() as db:
        rows = (
            await db.execute(
                select(NotificationLog)
                .order_by(NotificationLog.created_at.desc())
                .limit(limit)
            )
        ).scalars().all()
        return [
            {
                "id": row.id,
                "caseId": row.case_id,
                "customerId": row.customer_id,
                "channel": row.channel,
                "recipient": (
                    f"customer:{row.customer_id}"
                    if row.customer_id
                    else _masked_phone(row.recipient)
                ),
                "message": row.message,
                "mode": row.mode,
                "accepted": row.accepted,
                "delivered": row.delivered,
                "providerStatus": row.provider_status,
                "createdAt": row.created_at.isoformat(),
            }
            for row in rows
        ]


def _masked_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    return f"***{digits[-4:]}" if len(digits) >= 4 else "unresolved"
