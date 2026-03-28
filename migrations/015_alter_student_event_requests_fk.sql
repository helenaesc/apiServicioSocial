ALTER TABLE student_event_requests
ADD CONSTRAINT fk_request_validated_by_user
FOREIGN KEY (validated_by_user_id) REFERENCES users(id);
