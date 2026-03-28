CREATE TABLE pass_sessions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  request_id BIGINT NOT NULL,
  qr_token_hash VARCHAR(255) NOT NULL,
  status ENUM('ACTIVE','USED','EXPIRED','REVOKED') NOT NULL DEFAULT 'ACTIVE',
  issued_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at DATETIME NOT NULL,
  used_at DATETIME NULL,
  revoked_at DATETIME NULL,
  refresh_count INT NOT NULL DEFAULT 0,
  UNIQUE KEY uk_pass_token_hash (qr_token_hash),
  KEY idx_pass_request (request_id),
  CONSTRAINT fk_pass_request FOREIGN KEY (request_id) REFERENCES student_event_requests(id)
);