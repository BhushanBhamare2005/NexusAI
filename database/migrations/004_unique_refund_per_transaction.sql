CREATE UNIQUE INDEX IF NOT EXISTS uq_refunds_transaction_id
  ON refunds(transaction_id);
