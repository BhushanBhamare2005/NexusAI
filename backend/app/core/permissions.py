ROLE_PERMISSIONS = {
    "agent": {
        "lookup_txn",
        "create_ticket",
        "send_notification",
        "view_evaluation",
    },
    "senior_agent": {
        "lookup_txn",
        "create_ticket",
        "send_notification",
        "check_refund_eligibility",
        "initiate_refund",
        "view_revenue",
        "view_audit",
        "view_evaluation",
        "view_notifications",
    },
    "manager": {"*"},
    "customer": {"lookup_txn"},
}

def has_permission(role: str, action: str) -> bool:
    allowed = ROLE_PERMISSIONS.get(role, set())
    return "*" in allowed or action in allowed
