ALTER TABLE pass_sessions
  ADD KEY idx_pass_status_expires (status, expires_at),
  ADD KEY idx_pass_request_issued (request_id, issued_at);