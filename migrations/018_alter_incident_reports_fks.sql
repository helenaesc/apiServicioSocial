ALTER TABLE incident_reports
ADD CONSTRAINT fk_incident_request FOREIGN KEY (request_id) REFERENCES student_event_requests(id),
ADD CONSTRAINT fk_incident_user FOREIGN KEY (id_user) REFERENCES users(id),
ADD CONSTRAINT fk_incident_reported_by FOREIGN KEY (reported_by_user_id) REFERENCES users(id);