from datetime import datetime

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def now() -> datetime:
    return datetime.utcnow()
