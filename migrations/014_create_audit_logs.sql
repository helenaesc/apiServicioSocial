CREATE TABLE audit_logs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  event_id BIGINT NULL,
  actor_role VARCHAR(20) NOT NULL,
  actor_identifier VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50) NOT NULL,
  entity_id BIGINT NOT NULL,
  action VARCHAR(50) NOT NULL,
  reason VARCHAR(255) NULL,
  old_values_json JSON NULL,
  new_values_json JSON NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_audit_event (event_id),
  KEY idx_audit_entity (entity_type, entity_id)
);