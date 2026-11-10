from sqlalchemy.ext.asyncio import AsyncSession
from app.engines.trustguard.rules import assess_refund

async def assess(db: AsyncSession, ctx: dict) -> dict:
    del db
    reasons = []
    level = "safe"
    rank = {"safe": 0, "approval_needed": 1, "blocked": 2}

    results = (
        assess_refund(ctx)
        if ctx.get("action", "initiate_refund") == "initiate_refund"
        else []
    )
    for risk_level, reason in results:
        reasons.append(reason)
        if rank[risk_level] > rank[level]:
            level = risk_level

    score = {"safe": 10, "approval_needed": 55, "blocked": 95}[level]
    return {"level": level, "score": score, "reasons": reasons}
