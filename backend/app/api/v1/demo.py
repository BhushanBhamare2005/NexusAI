from fastapi import APIRouter, Depends

from app.core.security import require

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/overview")
async def overview(_user: dict = Depends(require("view_demo"))):
    return {
        "label": "Synthetic demonstration data",
        "notice": "This sandbox contains no production merchant or customer records.",
        "metrics": [
            {"label": "Transactions reviewed", "value": 128},
            {"label": "Cases resolved", "value": 94},
            {"label": "Escalations pending", "value": 7},
        ],
        "recent_cases": [
            {
                "id": "DEMO-1001",
                "issue": "Delayed payment confirmation",
                "status": "Resolved",
            },
            {
                "id": "DEMO-1002",
                "issue": "Duplicate notification",
                "status": "Under review",
            },
            {
                "id": "DEMO-1003",
                "issue": "Refund status inquiry",
                "status": "Resolved",
            },
        ],
    }
