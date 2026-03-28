ALTER TABLE pass_sessions
ADD KEY idx_pass_request_status (request_id, status),
ADD KEY idx_pass_expires_at (expires_at);
