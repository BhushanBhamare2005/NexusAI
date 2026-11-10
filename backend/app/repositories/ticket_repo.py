from sqlalchemy import select
from app.repositories.base_repo import BaseRepo
from app.models.ticket import Ticket

class TicketRepo(BaseRepo[Ticket]):
    model = Ticket
    async def by_run(self, run_id: str):
        res = await self.db.execute(select(Ticket).where(Ticket.run_id == run_id))
        return res.scalars().all()
