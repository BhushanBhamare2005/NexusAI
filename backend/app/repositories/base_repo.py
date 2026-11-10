from typing import Generic, TypeVar, Type, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base

M = TypeVar("M", bound=Base)

class BaseRepo(Generic[M]):
    model: Type[M]
    def __init__(self, db: AsyncSession):
        self.db = db
    async def add(self, obj: M) -> M:
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    async def get(self, pk: str) -> M | None:
        return await self.db.get(self.model, pk)
    async def all(self, limit: int = 100) -> Sequence[M]:
        result = await self.db.execute(select(self.model).limit(limit))
        return result.scalars().all()
