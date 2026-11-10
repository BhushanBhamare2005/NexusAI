def group_by_root_cause(opportunities: list) -> dict[str, list]:
    groups: dict[str, list] = {}
    for o in opportunities:
        groups.setdefault(o.root_cause or "unknown", []).append(o)
    return groups
