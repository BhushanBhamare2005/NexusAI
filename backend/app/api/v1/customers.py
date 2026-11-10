import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select

from app.core.security import require
from app.db.session import AsyncSessionLocal
from app.models.customer import Customer
from app.audit.ledger import append as audit_append

router = APIRouter(prefix="/customers", tags=["customers"])


class SmsConsentUpdate(BaseModel):
    sms_opt_in: bool
    consent_source: str = Field(min_length=3, max_length=200)

    @field_validator("consent_source")
    @classmethod
    def consent_source_must_be_nonblank(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("consent source must describe the recorded consent")
        return value


@router.get("")
async def list_customers(
    _manager: dict = Depends(require("manage_customer_consent")),
):
    async with AsyncSessionLocal() as db:
        customers = (
            await db.execute(select(Customer).order_by(Customer.id).limit(500))
        ).scalars().all()
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "phone": customer.phone,
                "smsOptIn": customer.sms_opt_in,
                "consentSource": customer.sms_consent_source,
            }
            for customer in customers
        ]


@router.put("/{customer_id}/sms-consent")
async def update_sms_consent(
    customer_id: str,
    body: SmsConsentUpdate,
    _manager: dict = Depends(require("manage_customer_consent")),
):
    async with AsyncSessionLocal() as db:
        customer = await db.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        customer.sms_opt_in = body.sms_opt_in
        customer.sms_consent_source = body.consent_source.strip()
        await db.commit()
        await audit_append(
            db,
            case_id=f"customer:{customer.id}",
            run_id=f"sms-consent:{uuid.uuid4()}",
            event_type="sms_consent_updated",
            actor=_manager["sub"],
            payload={
                "sms_opt_in": customer.sms_opt_in,
                "consent_source": customer.sms_consent_source,
            },
        )
        return {
            "id": customer.id,
            "smsOptIn": customer.sms_opt_in,
            "consentSource": customer.sms_consent_source,
        }
