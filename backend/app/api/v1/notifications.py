from fastapi import APIRouter, Depends, Query

from app.core.security import require
from app.services.notification_service import recent

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
async def notification_history(
    limit: int = Query(20, ge=1, le=100),
    _user: dict = Depends(require("view_notifications")),
):
    return await recent(limit)
