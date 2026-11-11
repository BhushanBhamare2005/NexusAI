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
