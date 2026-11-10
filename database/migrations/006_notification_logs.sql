CREATE TABLE IF NOT EXISTS notification_logs (
  id VARCHAR PRIMARY KEY,
  case_id VARCHAR,
  customer_id VARCHAR,
  channel VARCHAR NOT NULL,
  recipient VARCHAR NOT NULL,
  message TEXT NOT NULL,
  mode VARCHAR NOT NULL,
  accepted BOOLEAN NOT NULL DEFAULT FALSE,
  delivered BOOLEAN NOT NULL DEFAULT FALSE,
  provider_id VARCHAR,
  provider_status VARCHAR,
  created_at TIMESTAMP DEFAULT NOW()
);
