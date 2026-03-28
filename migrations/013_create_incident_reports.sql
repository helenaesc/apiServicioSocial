CREATE TABLE incident_reports (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  event_id BIGINT NOT NULL,
  request_id BIGINT NULL,
  id_user BIGINT NULL,
  reported_by_user_id BIGINT NULL,
  type VARCHAR(40) NOT NULL,
  severity ENUM('LOW','MEDIUM','HIGH') NOT NULL DEFAULT 'MEDIUM',
  status ENUM('OPEN','IN_PROGRESS','RESOLVED','DISMISSED') NOT NULL DEFAULT 'OPEN',
  description VARCHAR(255) NULL,
  resolution_notes VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  resolved_at DATETIME NULL,
  KEY idx_incident_event (event_id),
  CONSTRAINT fk_incident_event FOREIGN KEY (event_id) REFERENCES events(id)
);