ALTER TABLE registration_audit_log
  ADD CONSTRAINT fk_reg_audit_registration
    FOREIGN KEY (registration_id) REFERENCES registrations(id),
  ADD CONSTRAINT fk_reg_audit_event
    FOREIGN KEY (event_id) REFERENCES events(id),
  ADD CONSTRAINT fk_reg_audit_user
    FOREIGN KEY (id_user) REFERENCES users(id),
  ADD CONSTRAINT fk_reg_audit_actor_admin
    FOREIGN KEY (actor_admin_user_id) REFERENCES admin_users(id);