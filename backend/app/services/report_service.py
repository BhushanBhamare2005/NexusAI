from app.db.session import AsyncSessionLocal
from app.repositories.audit_repo import AuditRepo

async def case_report(case_id: str) -> dict:
    async with AsyncSessionLocal() as db:
        events = await AuditRepo(db).by_case(case_id)
        return {
            "case_id": case_id,
            "event_count": len(events),
            "events": [{
                "type": e.event_type,
                "actor": e.actor,
                "at": e.timestamp.isoformat(),
                "payload": e.payload,
            } for e in events],
        }
