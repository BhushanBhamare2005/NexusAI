from app.audit.ledger import verify as verify_ledger

async def verify():
    from app.db.session import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        return await verify_ledger(db)
