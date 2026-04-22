CREATE TABLE registration_audit_log (
  id BIGINT NOT NULL AUTO_INCREMENT,
  registration_id BIGINT NOT NULL,
  event_id BIGINT NOT NULL,
  id_user BIGINT NOT NULL,
  action_type VARCHAR(50) NOT NULL,
  old_status VARCHAR(30) DEFAULT NULL,
  new_status VARCHAR(30) DEFAULT NULL,
  actor_type VARCHAR(30) NOT NULL,
  actor_admin_user_id BIGINT DEFAULT NULL,
  reason VARCHAR(255) DEFAULT NULL,
  snapshot_json JSON DEFAULT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);