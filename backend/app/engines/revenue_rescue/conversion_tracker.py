from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.recovery_opportunity import RecoveryOpportunity

async def summary(db: AsyncSession, merchant_id: str | None = None) -> dict:
    stmt = select(RecoveryOpportunity)
    if merchant_id:
        stmt = stmt.where(RecoveryOpportunity.merchant_id == merchant_id)
    res = await db.execute(stmt)
    opps = res.scalars().all()
    converted = [o for o in opps if o.conversion_status == "converted"]
    return {
        "opportunitiesIdentified": len(opps),
        "recovered": len(converted),
        "recoveredAmount": round(sum(o.amount for o in converted), 2),
    }
