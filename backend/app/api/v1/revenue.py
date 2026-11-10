import logging

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.schemas.revenue import RevenueSummary, RecoveryOpportunityOut
from app.db.session import AsyncSessionLocal
from app.models.recovery_opportunity import RecoveryOpportunity
from app.models.transaction import Transaction
from app.models.customer import Customer
from app.engines.revenue_rescue.recovery_engine import find_opportunities
from app.engines.revenue_rescue.conversion_tracker import summary as conv_summary
from app.engines.revenue_rescue.followup_generator import generate_message
from app.tools.notification_tools import send_notification
from app.core.security import require

router = APIRouter(prefix="/revenue", tags=["revenue"])
logger = logging.getLogger(__name__)

@router.get("/summary", response_model=RevenueSummary)
async def summary(
    merchantId: str | None = None,
    _user: dict = Depends(require("view_revenue")),
):
    async with AsyncSessionLocal() as db:
        stmt = select(Transaction)
        if merchantId:
            stmt = stmt.where(Transaction.merchant_id == merchantId)
        res = await db.execute(stmt)
        txns = res.scalars().all()
        counts = {"success": 0, "failed": 0, "pending": 0, "abandoned": 0}
        for t in txns:
            if t.status in counts:
                counts[t.status] += 1
        conv = await conv_summary(db, merchantId)
        return {
            "totalAttempts": len(txns),
            "successful": counts["success"],
            "failed": counts["failed"],
            "pending": counts["pending"],
            "abandoned": counts["abandoned"],
            "opportunitiesIdentified": conv["opportunitiesIdentified"],
            "recovered": conv["recovered"],
            "recoveredAmount": conv["recoveredAmount"],
        }

@router.get("/opportunities", response_model=list[RecoveryOpportunityOut])
async def list_opps(
    merchantId: str | None = None,
    _user: dict = Depends(require("view_revenue")),
):
    async with AsyncSessionLocal() as db:
        stmt = select(RecoveryOpportunity)
        if merchantId:
            stmt = stmt.where(RecoveryOpportunity.merchant_id == merchantId)
        res = await db.execute(stmt.limit(200))
        return res.scalars().all()

@router.post("/opportunities/scan")
async def scan(
    merchantId: str,
    _user: dict = Depends(require("manage_revenue")),
):
    async with AsyncSessionLocal() as db:
        created = await find_opportunities(db, merchantId)
        return {"created": len(created)}

@router.post("/opportunities/{opp_id}/followup", response_model=RecoveryOpportunityOut)
async def followup(
    opp_id: str,
    _user: dict = Depends(require("send_notification")),
):
    async with AsyncSessionLocal() as db:
        o = await db.get(RecoveryOpportunity, opp_id)
        if not o:
            from fastapi import HTTPException
            raise HTTPException(404, "not found")
        if o.conversion_status != "not_contacted":
            from fastapi import HTTPException
            raise HTTPException(409, "follow-up has already been sent")
        o.followup_message = generate_message(o)
        txn = await db.get(Transaction, o.transaction_id)
        customer = await db.get(Customer, txn.customer_id) if txn else None
        try:
            notification = await send_notification(
                db=db,
                channel="sms",
                recipient=customer.id if customer else "customer",
                message=o.followup_message,
            )
        except (ValueError, PermissionError, RuntimeError, httpx.HTTPError) as exc:
            logger.warning("Revenue follow-up was not sent: %s", exc)
            notification = {
                "mode": "twilio",
                "accepted": False,
                "delivered": False,
                "status": "failed",
                "error": str(exc),
            }
        o.conversion_status = (
            "contacted"
            if notification.get("accepted") or notification.get("delivered")
            else "not_contacted"
        )
        await db.commit()
        await db.refresh(o)
        response = RecoveryOpportunityOut.model_validate(o).model_dump(by_alias=True)
        response["notificationMode"] = notification.get("mode")
        response["notificationStatus"] = notification.get("status")
        response["notificationError"] = notification.get("error")
        return response
