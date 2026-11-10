def generate_message(opportunity) -> str:
    return (
        f"Namaste! Your payment of ₹{opportunity.amount:.0f} for "
        f"{opportunity.txn_ref} could not complete. Please revisit the merchant's "
        "official payment page if you would like to try again."
    )
