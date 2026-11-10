from app.repositories.transaction_repo import TransactionRepo

def test_repo_has_search():
    assert hasattr(TransactionRepo, "search")
    assert hasattr(TransactionRepo, "by_ref")
