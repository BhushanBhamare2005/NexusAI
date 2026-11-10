DIAGNOSIS_PROMPT = """Given transaction data and a user complaint, identify the ROOT CAUSE.
Return ONLY JSON: {"root_cause": "...", "confidence": 0.0-1.0, "evidence": {...}}

Transaction: {txn}
Complaint: {message}
Relevant policy knowledge: {knowledge}
"""
