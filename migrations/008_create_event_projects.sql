CREATE TABLE event_projects (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  event_id BIGINT NOT NULL,
  project_id INT NOT NULL,
  slots_total INT NOT NULL DEFAULT 0,
  status ENUM('ACTIVE','HIDDEN','CLOSED') NOT NULL DEFAULT 'ACTIVE',
  notes VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_event_project (event_id, project_id),
  CONSTRAINT fk_event_projects_event FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_event_projects_project FOREIGN KEY (project_id) REFERENCES project(id)
);