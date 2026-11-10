from fastapi import APIRouter, Depends, HTTPException
from app.core.security import require
from app.schemas.transaction import TransactionOut
from app.services import transaction_service

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("", response_model=list[TransactionOut])
async def search(q: str | None = None, status: str | None = None,
                 merchantId: str | None = None, customerId: str | None = None,
                 limit: int = 50,
                 _user: dict = Depends(require("lookup_txn"))):
    return await transaction_service.search(q, status, merchantId, customerId, limit)

@router.get("/{txn_id}", response_model=TransactionOut)
async def get(txn_id: str, _user: dict = Depends(require("lookup_txn"))):
    t = await transaction_service.get(txn_id)
    if not t:
        raise HTTPException(404, "not found")
    return t
