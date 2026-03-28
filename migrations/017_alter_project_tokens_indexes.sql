ALTER TABLE project_tokens
ADD KEY idx_project_tokens_status (event_project_id, status),
ADD KEY idx_project_tokens_reserved_until (reserved_until),
ADD KEY idx_project_tokens_used_request (used_by_request_id),
ADD KEY idx_project_tokens_reserved_request (reserved_by_request_id);