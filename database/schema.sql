CREATE TABLE IF NOT EXISTS merchants (
  id VARCHAR PRIMARY KEY,
  name VARCHAR NOT NULL,
  upi_id VARCHAR NOT NULL,
  language VARCHAR DEFAULT 'en',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customers (
  id VARCHAR PRIMARY KEY,
  name VARCHAR NOT NULL,
  phone VARCHAR NOT NULL,
  sms_opt_in BOOLEAN NOT NULL DEFAULT FALSE,
  sms_consent_source VARCHAR,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transactions (
  id VARCHAR PRIMARY KEY,
  txn_ref VARCHAR NOT NULL,
  customer_id VARCHAR NOT NULL,
  merchant_id VARCHAR NOT NULL,
  amount DOUBLE PRECISION NOT NULL,
  currency VARCHAR DEFAULT 'INR',
  status VARCHAR NOT NULL,
  method VARCHAR NOT NULL,
  upi_ref VARCHAR,
  settlement_id VARCHAR,
  root_cause VARCHAR,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_txn_ref ON transactions(txn_ref);
CREATE INDEX IF NOT EXISTS idx_txn_merchant ON transactions(merchant_id);

CREATE TABLE IF NOT EXISTS refunds (
  id VARCHAR PRIMARY KEY,
  transaction_id VARCHAR NOT NULL UNIQUE,
  amount DOUBLE PRECISION NOT NULL,
  status VARCHAR DEFAULT 'initiated',
  reason VARCHAR DEFAULT '',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tickets (
  id VARCHAR PRIMARY KEY,
  case_id VARCHAR NOT NULL,
  run_id VARCHAR NOT NULL,
  subject VARCHAR NOT NULL,
  description VARCHAR DEFAULT '',
  priority VARCHAR DEFAULT 'medium',
  status VARCHAR DEFAULT 'open',
  assignee VARCHAR DEFAULT 'investigation-team',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS approvals (
  id VARCHAR PRIMARY KEY,
  case_id VARCHAR NOT NULL,
  run_id VARCHAR NOT NULL,
  action VARCHAR NOT NULL,
  requested_by VARCHAR DEFAULT 'nexus-agent',
  reason VARCHAR DEFAULT '',
  risk_level VARCHAR DEFAULT 'approval_needed',
  status VARCHAR DEFAULT 'pending',
  decided_by VARCHAR,
  created_at TIMESTAMP DEFAULT NOW(),
  decided_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_runs (
  id VARCHAR PRIMARY KEY,
  case_id VARCHAR NOT NULL,
  status VARCHAR DEFAULT 'running',
  intent VARCHAR,
  root_cause VARCHAR,
  selected_action VARCHAR,
  risk_level VARCHAR,
  steps JSONB DEFAULT '[]'::jsonb,
  tool_calls JSONB DEFAULT '[]'::jsonb,
  state_data JSONB DEFAULT '{}'::jsonb,
  final_response VARCHAR,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
  id VARCHAR PRIMARY KEY,
  case_id VARCHAR NOT NULL,
  run_id VARCHAR NOT NULL,
  event_type VARCHAR NOT NULL,
  actor VARCHAR NOT NULL,
  payload JSONB DEFAULT '{}'::jsonb,
  prev_hash VARCHAR NOT NULL,
  hash VARCHAR NOT NULL,
  timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS recovery_opportunities (
  id VARCHAR PRIMARY KEY,
  merchant_id VARCHAR NOT NULL,
  transaction_id VARCHAR NOT NULL,
  txn_ref VARCHAR NOT NULL,
  amount DOUBLE PRECISION NOT NULL,
  reason VARCHAR NOT NULL,
  root_cause VARCHAR NOT NULL,
  recoverable BOOLEAN DEFAULT TRUE,
  recommended_action VARCHAR NOT NULL,
  followup_message VARCHAR,
  conversion_status VARCHAR DEFAULT 'not_contacted',
  created_at TIMESTAMP DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS role_assignment_history (
  id VARCHAR PRIMARY KEY,
  target_user_id VARCHAR NOT NULL,
  target_username VARCHAR NOT NULL,
  actor_username VARCHAR NOT NULL,
  action VARCHAR NOT NULL,
  previous_role VARCHAR,
  new_role VARCHAR,
  previous_active BOOLEAN,
  new_active BOOLEAN,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_role_history_target_user
  ON role_assignment_history (target_user_id);
CREATE INDEX IF NOT EXISTS idx_role_history_target_username
  ON role_assignment_history (target_username);
CREATE INDEX IF NOT EXISTS idx_role_history_actor_username
  ON role_assignment_history (actor_username);
