"""Simulated inbound webhooks for demo. Not exposed to external parties."""
from datetime import datetime

def parse_webhook(payload: dict) -> dict:
    return {
        "received_at": datetime.utcnow().isoformat(),
        "event": payload.get("event", "unknown"),
        "data": payload.get("data", {}),
    }
