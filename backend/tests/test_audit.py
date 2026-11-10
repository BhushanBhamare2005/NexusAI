from app.audit.hash_chain import compute_hash

def test_hash_chain_deterministic():
    h1 = compute_hash("0" * 64, {"a": 1})
    h2 = compute_hash("0" * 64, {"a": 1})
    assert h1 == h2
    assert len(h1) == 64

def test_hash_changes_with_payload():
    h1 = compute_hash("0" * 64, {"a": 1})
    h2 = compute_hash("0" * 64, {"a": 2})
    assert h1 != h2
