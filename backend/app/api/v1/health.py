from fastapi import APIRouter, Depends
from app.core.security import require

router = APIRouter(prefix="/health", tags=["health"])
_request_metrics = {"total": 0, "errors": 0, "duration_ms_total": 0.0, "status_codes": {}}

@router.get("")
async def health():
    return {"status": "ok", "service": "paytm-nexus-ai"}


@router.get("/metrics")
async def metrics(_user: dict = Depends(require("view_health"))):
    from app.agents.llm import LLM_METRICS

    return {
        "http": {
            **_request_metrics,
            "status_codes": dict(_request_metrics["status_codes"]),
        },
        "llm": dict(LLM_METRICS),
    }


def record_request(status_code: int, duration_ms: float) -> None:
    _request_metrics["total"] += 1
    _request_metrics["duration_ms_total"] += duration_ms
    code = str(status_code)
    _request_metrics["status_codes"][code] = (
        _request_metrics["status_codes"].get(code, 0) + 1
    )
    if status_code >= 500:
        _request_metrics["errors"] += 1
