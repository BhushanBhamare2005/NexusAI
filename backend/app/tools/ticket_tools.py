import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket

async def create_ticket(
    db: AsyncSession,
    case_id: str,
    run_id: str,
    subject: str,
    description: str = "",
    priority: str = "medium",
) -> dict:
    t = Ticket(
        id=str(uuid.uuid4()),
        case_id=case_id,
        run_id=run_id,
        subject=subject,
        description=description,
        priority=priority,
    )
    db.add(t)
    await db.commit()
    return {"ticket_id": t.id, "status": t.status, "priority": t.priority}
