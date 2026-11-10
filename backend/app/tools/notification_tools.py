"""Notification provider with opt-in Twilio delivery and safe simulation mode."""
from datetime import datetime, timezone
import re
import uuid

import httpx
from app.core.config import settings
from app.models.customer import Customer
from app.models.notification_log import NotificationLog


async def send_notification(
    db=None, channel: str = "sms", recipient: str = "customer",
    message: str = "", case_id: str | None = None,
) -> dict:
    phone = recipient
    customer = (
        await db.get(Customer, recipient)
        if db is not None and not recipient.startswith("+")
        else None
    )
    if customer:
        phone = customer.phone
    phone = f"+91{phone}" if re.fullmatch(r"\d{10}", phone) else phone
    record = {
        "id": str(uuid.uuid4()),
        "channel": channel,
        "recipient": phone,
        "customer_id": customer.id if customer else None,
        "case_id": case_id,
        "sent_at": datetime.now(timezone.utc).isoformat(),
    }
    notification_ref = f"customer:{customer.id}" if customer else "unresolved"

    if settings.TWILIO_ENABLED:
        if channel != "sms":
            raise ValueError(f"Unsupported Twilio channel: {channel}")
        if not all(
            (
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN,
                settings.TWILIO_FROM_NUMBER,
            )
        ):
            raise RuntimeError("Twilio is enabled but its credentials are incomplete")
        if not re.fullmatch(r"\+[1-9]\d{7,14}", phone):
            raise ValueError("A valid customer phone number is required for Twilio SMS")
        if not customer or not customer.sms_opt_in:
            await _persist(
                db,
                record,
                message,
                mode="twilio",
                accepted=False,
                delivered=False,
                provider_status="consent_missing",
            )
            raise PermissionError(
                "SMS was not sent: customer consent is not recorded"
            )
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/"
                    f"{settings.TWILIO_ACCOUNT_SID}/Messages.json",
                    auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
                    data={
                        "To": phone,
                        "From": settings.TWILIO_FROM_NUMBER,
                        "Body": message,
                    },
                )
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPStatusError as exc:
            await _persist(
                db,
                record,
                message,
                mode="twilio",
                accepted=False,
                delivered=False,
                provider_status=f"http_{exc.response.status_code}",
            )
            raise
        except httpx.RequestError:
            await _persist(
                db,
                record,
                message,
                mode="twilio",
                accepted=False,
                delivered=False,
                provider_status="provider_unreachable",
            )
            raise
        result = {
            "id": record["id"],
            "channel": channel,
            "recipient": notification_ref,
            "case_id": case_id,
            "sent_at": record["sent_at"],
            "mode": "twilio",
            "accepted": payload.get("status")
            in {"accepted", "queued", "sending", "sent", "delivered"},
            "delivered": payload.get("status") == "delivered",
            "notification_id": payload.get("sid"),
            "status": payload.get("status"),
        }
        await _persist(
            db,
            record,
            message,
            mode="twilio",
            accepted=result["accepted"],
            delivered=result["delivered"],
            provider_id=result["notification_id"],
            provider_status=result["status"],
        )
        return result

    result = {
        "id": record["id"],
        "channel": channel,
        "recipient": notification_ref,
        "case_id": case_id,
        "sent_at": record["sent_at"],
        "mode": "simulated",
        "accepted": False,
        "delivered": False,
        "notification_id": f"ntf_{record['id'][:8]}",
        "message": message,
    }
    await _persist(
        db,
        record,
        message,
        mode="simulated",
        accepted=False,
        delivered=False,
        provider_id=result["notification_id"],
        provider_status="not_sent",
    )
    return {key: value for key, value in result.items() if key != "message"}


async def _persist(
    db,
    record: dict,
    message: str,
    mode: str,
    accepted: bool,
    delivered: bool,
    provider_id: str | None = None,
    provider_status: str | None = None,
) -> None:
    if db is None:
        return
    db.add(
        NotificationLog(
            id=record["id"],
            case_id=record["case_id"],
            customer_id=record["customer_id"],
            channel=record["channel"],
            recipient=record["recipient"],
            message=message,
            mode=mode,
            accepted=accepted,
            delivered=delivered,
            provider_id=provider_id,
            provider_status=provider_status,
        )
    )
    await db.commit()
