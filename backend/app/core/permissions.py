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

DASHBOARD_ROUTES = {
    "manager": ("/trustguard", "manage_users"),
    "senior_agent": ("/revenue", "view_revenue"),
    "agent": ("/agent", "lookup_txn"),
}


def has_permission(role: str, action: str) -> bool:
    allowed = ROLE_PERMISSIONS.get(role, set())
    return "*" in allowed or action in allowed


def available_dashboards(role: str) -> list[dict[str, str]]:
    return [
        {"role": dashboard_role, "path": path}
        for dashboard_role, (path, permission) in DASHBOARD_ROUTES.items()
        if has_permission(role, permission)
    ]
