ALTER TABLE audit_events ADD COLUMN IF NOT EXISTS chain_seq SERIAL;
CREATE INDEX IF NOT EXISTS idx_audit_case ON audit_events(case_id);
