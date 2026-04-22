ALTER TABLE registration_audit_log
  ADD KEY idx_reg_audit_registration (registration_id),
  ADD KEY idx_reg_audit_event (event_id),
  ADD KEY idx_reg_audit_user (id_user),
  ADD KEY idx_reg_audit_actor_admin (actor_admin_user_id),
  ADD KEY idx_reg_audit_created_at (created_at);

ALTER TABLE registrations
  ADD KEY idx_reg_event_user_status (event_id, id_user, status),
  ADD KEY idx_reg_request (request_id),
  ADD KEY idx_reg_accepted_at (accepted_at);

ALTER TABLE student_event_requests
  ADD KEY idx_request_status_event (status, event_id),
  ADD KEY idx_request_access_enabled_at (access_enabled_at),
  ADD KEY idx_request_registered_at (registered_at);

ALTER TABLE admin_users
  ADD KEY idx_admin_users_role_status (role, status);