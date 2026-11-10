RESPONSE_PROMPT = """Craft a customer-facing resolution message (max 3 sentences).
Be honest: if only a ticket was created, say the case is tracked — do not claim the payment is resolved.
Include the case reference and next step.

Context:
- Intent: {intent}
- Diagnosis: {diagnosis}
- Action taken: {action}
- Tool results: {results}
- Outcome verified: {verified}
- Case ID: {case_id}

Do not claim an action or delivery completed unless Outcome verified is true.
Return ONLY JSON: {"response": "..."}
"""
