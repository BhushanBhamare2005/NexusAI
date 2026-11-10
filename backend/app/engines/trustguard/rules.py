"""TrustGuard rules return a risk level and explanatory reason."""
from typing import Any

def rule_duplicate_refund(eligibility: dict[str, Any]) -> tuple[str, str] | None:
    if eligibility.get("reason") == "refund_already_exists":
        return (
            "blocked",
            f"Duplicate refund detected (existing: {eligibility.get('existing_refund_id')})",
        )
    return None


def rule_ineligible_refund(eligibility: dict[str, Any]) -> tuple[str, str] | None:
    if eligibility.get("eligible") is False:
        return ("blocked", f"Refund is not eligible: {eligibility.get('reason', 'unknown')}")
    return None


def rule_high_value(
    amount: float, threshold: float = 10000.0
) -> tuple[str, str] | None:
    if amount >= threshold:
        return (
            "approval_needed",
            f"High-value transaction ₹{amount} requires approval",
        )
    return None


def assess_refund(ctx: dict[str, Any]) -> list[tuple[str, str]]:
    eligibility = ctx.get("eligibility", {})
    txn = ctx.get("txn", {})
    results = [
        rule_duplicate_refund(eligibility),
        rule_ineligible_refund(eligibility),
        rule_high_value(float(txn.get("amount") or 0)),
    ]
    return [result for result in results if result]
