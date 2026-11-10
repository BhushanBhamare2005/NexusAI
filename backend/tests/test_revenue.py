from app.engines.revenue_rescue.followup_generator import generate_message

class _Opp:
    amount = 500
    txn_ref = "TXN123"
    id = "abcdef12345"

def test_generate_message():
    msg = generate_message(_Opp())
    assert "₹500" in msg
    assert "TXN123" in msg
