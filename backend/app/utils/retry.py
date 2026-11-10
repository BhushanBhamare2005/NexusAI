import asyncio
from typing import Callable, Awaitable, TypeVar

T = TypeVar("T")

async def safe_retry(fn: Callable[[], Awaitable[T]], attempts: int = 2, delay: float = 0.3) -> T:
    last: Exception | None = None
    for _ in range(attempts):
        try:
            return await fn()
        except Exception as e:
            last = e
            await asyncio.sleep(delay)
    assert last is not None
    raise last
