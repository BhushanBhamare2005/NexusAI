def funnel_series(summary: dict) -> list[dict]:
    return [
        {"stage": "Attempts", "value": summary.get("total", 0)},
        {"stage": "Successful", "value": summary.get("success", 0)},
        {"stage": "Failed", "value": summary.get("failed", 0)},
        {"stage": "Pending", "value": summary.get("pending", 0)},
        {"stage": "Abandoned", "value": summary.get("abandoned", 0)},
    ]
