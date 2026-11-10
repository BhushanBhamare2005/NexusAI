import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audit_event import AuditEvent
from app.audit.hash_chain import compute_hash

GENESIS = "0" * 64

async def append(
    db: AsyncSession,
    case_id: str,
    run_id: str,
    event_type: str,
    actor: str = "nexus-agent",
    payload: dict | None = None,
) -> AuditEvent:
    payload = payload or {}
    last = (await db.execute(
        select(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(1)
    )).scalar_one_or_none()
    prev = last.hash if last else GENESIS
    event_time = datetime.utcnow()
    body = {
        "case_id": case_id,
        "run_id": run_id,
        "event_type": event_type,
        "actor": actor,
        "payload": payload,
        "ts": event_time.isoformat(),
    }
    ev = AuditEvent(
        id=str(uuid.uuid4()),
        case_id=case_id,
        run_id=run_id,
        event_type=event_type,
        actor=actor,
        payload=payload,
        prev_hash=prev,
        hash=compute_hash(prev, body),
        timestamp=event_time,
    )
    db.add(ev)
    await db.commit()
    await db.refresh(ev)
    return ev

async def verify(db: AsyncSession) -> dict:
    res = await db.execute(select(AuditEvent).order_by(AuditEvent.timestamp.asc()))
    events = res.scalars().all()
    prev = GENESIS
    for ev in events:
        body = {
            "case_id": ev.case_id,
            "run_id": ev.run_id,
            "event_type": ev.event_type,
            "actor": ev.actor,
            "payload": ev.payload,
            "ts": ev.timestamp.isoformat(),
        }
        expected_hash = compute_hash(prev, body)
        if ev.prev_hash != prev or ev.hash != expected_hash:
            return {"valid": False, "checkedEvents": len(events), "brokenAt": ev.id}
        prev = ev.hash
    return {"valid": True, "checkedEvents": len(events), "brokenAt": None}
