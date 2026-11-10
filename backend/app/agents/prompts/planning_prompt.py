PLANNING_PROMPT = """Given the diagnosis and intent, pick ONE safe action:
- create_investigation_ticket (when status=pending or unknown)
- initiate_refund (only if status=failed and no existing refund)
- send_status_update (when status=success)
- escalate_to_human (when uncertain)

Return ONLY JSON: {"action": "...", "args": {...}, "reasoning": "..."}

Intent: {intent}
Root cause: {diagnosis}
Transaction: {txn}
"""
