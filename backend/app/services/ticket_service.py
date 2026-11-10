from app.db.session import AsyncSessionLocal
from app.repositories.ticket_repo import TicketRepo

async def by_run(run_id: str):
    async with AsyncSessionLocal() as db:
        return await TicketRepo(db).by_run(run_id)
