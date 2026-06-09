-- Archivo 01: Esquema limpio de base de datos
-- Motor: MySQL 8.0+


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP DATABASE IF EXISTS poncho;
CREATE DATABASE poncho
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE poncho;


-- CONFIGURACIÓN GLOBAL DEL SISTEMA


CREATE TABLE app_settings (
  k VARCHAR(60) NOT NULL,
  v VARCHAR(225) NOT NULL,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (k)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- USUARIOS ALUMNOS


CREATE TABLE users (
  id BIGINT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  second_name VARCHAR(50) NULL,
  p_last_name VARCHAR(100) NOT NULL,
  m_last_name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  secondary_email VARCHAR(100) NULL,
  enrolment_number VARCHAR(10) NULL,
  phone_number VARCHAR(12) NULL,
  password VARCHAR(100) NOT NULL,
  salt VARCHAR(10) NOT NULL,
  admin BOOLEAN NOT NULL DEFAULT FALSE,
  degree VARCHAR(10) NULL,
  semester TINYINT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_users_email (email),
  UNIQUE KEY uk_users_enrolment (enrolment_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- USUARIOS ADMINISTRATIVOS / STAFF


CREATE TABLE admin_users (
  id BIGINT NOT NULL AUTO_INCREMENT,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(120) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('ADMIN','STAFF') NOT NULL,
  status ENUM('ACTIVE','DISABLED') NOT NULL DEFAULT 'ACTIVE',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  last_login_at DATETIME NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_admin_users_email (email),
  KEY idx_admin_users_role_status (role, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- CATÁLOGOS BASE


CREATE TABLE partner (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_partner_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE partner_group (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(60) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_partner_group_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE partner_group_member (
  group_id INT NOT NULL,
  partner_id INT NOT NULL,
  PRIMARY KEY (group_id, partner_id),
  KEY idx_pgm_partner (partner_id),
  CONSTRAINT fk_pgm_group
    FOREIGN KEY (group_id) REFERENCES partner_group(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_pgm_partner
    FOREIGN KEY (partner_id) REFERENCES partner(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE week_days (
  id TINYINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_week_days_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE modality (
  id TINYINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_modality_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE schedule (
  id TINYINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_schedule_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE status (
  id TINYINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_status_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- PROYECTOS BASE


CREATE TABLE project (
  id INT NOT NULL AUTO_INCREMENT,
  general_name VARCHAR(300) NULL,
  name VARCHAR(300) NOT NULL,
  id_partner INT NOT NULL,
  id_modality TINYINT NOT NULL,
  id_week_days TINYINT NOT NULL,
  id_schedule TINYINT NOT NULL,
  slots INT NOT NULL DEFAULT 0,
  schedule_description VARCHAR(300) NULL,
  team_owners VARCHAR(300) NULL,
  objectives TEXT NULL,
  activities TEXT NULL,
  clave VARCHAR(30) NULL,
  competencies TEXT NULL,
  location VARCHAR(300) NULL,
  duration VARCHAR(80) NULL,
  audience TEXT NULL,
  max_hours INT NULL,
  comments TEXT NULL,
  season VARCHAR(40) NULL,
  academy_mode ENUM('ALL','GROUP','CUSTOM') NOT NULL DEFAULT 'ALL',
  academy_group_id INT NULL,
  PRIMARY KEY (id),
  KEY idx_project_partner (id_partner),
  KEY idx_project_modality (id_modality),
  KEY idx_project_week_days (id_week_days),
  KEY idx_project_schedule (id_schedule),
  KEY idx_project_academy_group (academy_group_id),
  CONSTRAINT fk_project_partner
    FOREIGN KEY (id_partner) REFERENCES partner(id),
  CONSTRAINT fk_project_modality
    FOREIGN KEY (id_modality) REFERENCES modality(id),
  CONSTRAINT fk_project_week_days
    FOREIGN KEY (id_week_days) REFERENCES week_days(id),
  CONSTRAINT fk_project_schedule
    FOREIGN KEY (id_schedule) REFERENCES schedule(id),
  CONSTRAINT fk_project_academy_group
    FOREIGN KEY (academy_group_id) REFERENCES partner_group(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE project_partner_pref (
  project_id INT NOT NULL,
  partner_id INT NOT NULL,
  PRIMARY KEY (project_id, partner_id),
  KEY idx_ppp_partner (partner_id),
  CONSTRAINT fk_ppp_project
    FOREIGN KEY (project_id) REFERENCES project(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_ppp_partner
    FOREIGN KEY (partner_id) REFERENCES partner(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- TABLAS LEGACY / COMPATIBILIDAD
-- Estas tablas permanecen para no romper módulos anteriores.


CREATE TABLE token (
  id BIGINT NOT NULL AUTO_INCREMENT,
  id_project INT NULL,
  token VARCHAR(20) NULL,
  used BOOLEAN NOT NULL DEFAULT FALSE,
  revoked BOOLEAN NOT NULL DEFAULT FALSE,
  expires_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_token_value (token),
  KEY idx_token_project (id_project),
  CONSTRAINT fk_token_project
    FOREIGN KEY (id_project) REFERENCES project(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE enrolment (
  id BIGINT NOT NULL AUTO_INCREMENT,
  id_student BIGINT NOT NULL,
  id_project INT NOT NULL,
  enrolment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_status TINYINT NULL,
  id_token BIGINT NULL,
  PRIMARY KEY (id),
  KEY idx_enrolment_student (id_student),
  KEY idx_enrolment_project (id_project),
  KEY idx_enrolment_status (id_status),
  KEY idx_enrolment_token (id_token),
  CONSTRAINT fk_enrolment_student
    FOREIGN KEY (id_student) REFERENCES users(id),
  CONSTRAINT fk_enrolment_project
    FOREIGN KEY (id_project) REFERENCES project(id),
  CONSTRAINT fk_enrolment_status
    FOREIGN KEY (id_status) REFERENCES status(id),
  CONSTRAINT fk_enrolment_token
    FOREIGN KEY (id_token) REFERENCES token(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE email_verification_codes (
  id BIGINT NOT NULL AUTO_INCREMENT,
  id_user BIGINT NOT NULL,
  code_hash VARCHAR(255) NOT NULL,
  expires_at DATETIME NOT NULL,
  used BOOLEAN NOT NULL DEFAULT FALSE,
  used_at DATETIME NULL,
  revoked BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_email_codes_user (id_user),
  CONSTRAINT fk_email_codes_user
    FOREIGN KEY (id_user) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- EVENTOS / PERIODOS


CREATE TABLE events (
  id BIGINT NOT NULL AUTO_INCREMENT,
  year SMALLINT NOT NULL,
  season ENUM('PRIMAVERA','INVIERNO') NOT NULL,
  display_name VARCHAR(40) NOT NULL,
  catalog_open_at DATETIME NULL,
  onsite_start_at DATETIME NULL,
  onsite_end_at DATETIME NULL,
  registration_close_at DATETIME NULL,
  status ENUM('DRAFT','VISIBLE','ONSITE','CLOSED','ARCHIVED') NOT NULL DEFAULT 'DRAFT',
  is_visible_to_students BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_events_year_season (year, season),
  KEY idx_events_status_visibility (status, is_visible_to_students),
  KEY idx_events_season_status (season, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE event_projects (
  id BIGINT NOT NULL AUTO_INCREMENT,
  event_id BIGINT NOT NULL,
  project_id INT NOT NULL,
  slots_total INT NOT NULL DEFAULT 0,
  status ENUM('ACTIVE','HIDDEN','CLOSED') NOT NULL DEFAULT 'ACTIVE',
  notes VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_event_project (event_id, project_id),
  KEY idx_event_projects_event_status (event_id, status),
  KEY idx_event_projects_project (project_id),
  CONSTRAINT fk_event_projects_event
    FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_event_projects_project
    FOREIGN KEY (project_id) REFERENCES project(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- SOLICITUDES DE ALUMNOS POR EVENTO


CREATE TABLE student_event_requests (
  id BIGINT NOT NULL AUTO_INCREMENT,
  event_id BIGINT NOT NULL,
  id_user BIGINT NOT NULL,
  folio VARCHAR(20) NOT NULL,
  status ENUM(
    'REQUESTED',
    'VALIDATED',
    'ACCESS_ENABLED',
    'REGISTERED',
    'CANCELLED',
    'CLOSED'
  ) NOT NULL DEFAULT 'REQUESTED',
  requested_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  validated_at DATETIME NULL,
  validated_by_user_id BIGINT NULL,
  access_enabled_at DATETIME NULL,
  registered_at DATETIME NULL,
  cancelled_at DATETIME NULL,
  closed_at DATETIME NULL,
  notes VARCHAR(255) NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_request_event_user (event_id, id_user),
  UNIQUE KEY uk_request_folio (folio),
  KEY idx_request_event (event_id),
  KEY idx_request_user (id_user),
  KEY idx_request_status_event (status, event_id),
  KEY idx_request_access_enabled_at (access_enabled_at),
  KEY idx_request_registered_at (registered_at),
  CONSTRAINT fk_request_event
    FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_request_user
    FOREIGN KEY (id_user) REFERENCES users(id),
  CONSTRAINT fk_request_validated_by_user
    FOREIGN KEY (validated_by_user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- SESIONES DE PASE / QR


CREATE TABLE pass_sessions (
  id BIGINT NOT NULL AUTO_INCREMENT,
  request_id BIGINT NOT NULL,
  qr_token_hash VARCHAR(255) NOT NULL,
  status ENUM('ACTIVE','USED','EXPIRED','REVOKED') NOT NULL DEFAULT 'ACTIVE',
  issued_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at DATETIME NOT NULL,
  used_at DATETIME NULL,
  revoked_at DATETIME NULL,
  refresh_count INT NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uk_pass_token_hash (qr_token_hash),
  KEY idx_pass_request (request_id),
  KEY idx_pass_request_status (request_id, status),
  KEY idx_pass_expires_at (expires_at),
  KEY idx_pass_status_expires (status, expires_at),
  KEY idx_pass_request_issued (request_id, issued_at),
  CONSTRAINT fk_pass_request
    FOREIGN KEY (request_id) REFERENCES student_event_requests(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- TOKENS DE PROYECTOS POR EVENTO


CREATE TABLE project_tokens (
  id BIGINT NOT NULL AUTO_INCREMENT,
  event_project_id BIGINT NOT NULL,
  token_value VARCHAR(20) NOT NULL,
  status ENUM('AVAILABLE','RESERVED','USED','REVOKED','EXPIRED') NOT NULL DEFAULT 'AVAILABLE',
  reserved_by_request_id BIGINT NULL,
  reserved_at DATETIME NULL,
  reserved_until DATETIME NULL,
  used_by_request_id BIGINT NULL,
  used_at DATETIME NULL,
  revoked_at DATETIME NULL,
  revoke_reason VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at DATETIME NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_project_tokens_value (token_value),
  KEY idx_project_tokens_event_project (event_project_id),
  KEY idx_project_tokens_status (event_project_id, status),
  KEY idx_project_tokens_reserved_until (reserved_until),
  KEY idx_project_tokens_used_request (used_by_request_id),
  KEY idx_project_tokens_reserved_request (reserved_by_request_id),
  CONSTRAINT fk_project_tokens_event_project
    FOREIGN KEY (event_project_id) REFERENCES event_projects(id),
  CONSTRAINT fk_project_tokens_reserved_request
    FOREIGN KEY (reserved_by_request_id) REFERENCES student_event_requests(id),
  CONSTRAINT fk_project_tokens_used_request
    FOREIGN KEY (used_by_request_id) REFERENCES student_event_requests(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- REGISTROS / EVIDENCIA LEGAL


CREATE TABLE registrations (
  id BIGINT NOT NULL AUTO_INCREMENT,
  event_id BIGINT NOT NULL,
  event_project_id BIGINT NOT NULL,
  id_user BIGINT NOT NULL,
  request_id BIGINT NOT NULL,
  project_token_id BIGINT NOT NULL,
  accepted_checkbox BOOLEAN NOT NULL,
  accepted_full_name VARCHAR(200) NOT NULL,
  legal_text_version VARCHAR(30) NOT NULL DEFAULT 'v1',
  accepted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  acceptance_snapshot_json JSON NULL,
  acceptance_hash CHAR(64) NULL,
  acceptance_signature VARCHAR(64) NOT NULL,
  accepted_ip VARCHAR(64) NULL,
  accepted_user_agent VARCHAR(255) NULL,
  status ENUM('ACTIVE','CANCELLED') NOT NULL DEFAULT 'ACTIVE',
  cancelled_at DATETIME NULL,
  cancel_reason VARCHAR(255) NULL,
  cancelled_by_admin_user_id BIGINT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_reg_event_user (event_id, id_user),
  UNIQUE KEY uk_reg_token (project_token_id),
  KEY idx_reg_event_project (event_project_id),
  KEY idx_reg_event_user_status (event_id, id_user, status),
  KEY idx_reg_request (request_id),
  KEY idx_reg_accepted_at (accepted_at),
  CONSTRAINT fk_reg_event
    FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_reg_event_project
    FOREIGN KEY (event_project_id) REFERENCES event_projects(id),
  CONSTRAINT fk_reg_user
    FOREIGN KEY (id_user) REFERENCES users(id),
  CONSTRAINT fk_reg_request
    FOREIGN KEY (request_id) REFERENCES student_event_requests(id),
  CONSTRAINT fk_reg_token
    FOREIGN KEY (project_token_id) REFERENCES project_tokens(id),
  CONSTRAINT fk_reg_cancelled_by_admin
    FOREIGN KEY (cancelled_by_admin_user_id) REFERENCES admin_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE registration_audit_log (
  id BIGINT NOT NULL AUTO_INCREMENT,
  registration_id BIGINT NOT NULL,
  event_id BIGINT NOT NULL,
  id_user BIGINT NOT NULL,
  action_type VARCHAR(50) NOT NULL,
  old_status VARCHAR(30) NULL,
  new_status VARCHAR(30) NULL,
  actor_type VARCHAR(30) NOT NULL,
  actor_admin_user_id BIGINT NULL,
  reason VARCHAR(255) NULL,
  snapshot_json JSON NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_reg_audit_registration (registration_id),
  KEY idx_reg_audit_event (event_id),
  KEY idx_reg_audit_user (id_user),
  KEY idx_reg_audit_actor_admin (actor_admin_user_id),
  KEY idx_reg_audit_created_at (created_at),
  CONSTRAINT fk_reg_audit_registration
    FOREIGN KEY (registration_id) REFERENCES registrations(id),
  CONSTRAINT fk_reg_audit_event
    FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_reg_audit_user
    FOREIGN KEY (id_user) REFERENCES users(id),
  CONSTRAINT fk_reg_audit_actor_admin
    FOREIGN KEY (actor_admin_user_id) REFERENCES admin_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- INCIDENTES OPERATIVOS


CREATE TABLE incident_reports (
  id BIGINT NOT NULL AUTO_INCREMENT,
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
  PRIMARY KEY (id),
  KEY idx_incident_event (event_id),
  KEY idx_incident_request (request_id),
  KEY idx_incident_user (id_user),
  KEY idx_incident_reported_by (reported_by_user_id),
  CONSTRAINT fk_incident_event
    FOREIGN KEY (event_id) REFERENCES events(id),
  CONSTRAINT fk_incident_request
    FOREIGN KEY (request_id) REFERENCES student_event_requests(id),
  CONSTRAINT fk_incident_user
    FOREIGN KEY (id_user) REFERENCES users(id),
  CONSTRAINT fk_incident_reported_by
    FOREIGN KEY (reported_by_user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- AUDITORÍA GENERAL


CREATE TABLE audit_logs (
  id BIGINT NOT NULL AUTO_INCREMENT,
  event_id BIGINT NULL,
  actor_role VARCHAR(20) NOT NULL,
  actor_identifier VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50) NOT NULL,
  entity_id BIGINT NOT NULL,
  action VARCHAR(50) NOT NULL,
  reason VARCHAR(255) NULL,
  old_values_json JSON NULL,
  new_values_json JSON NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_audit_event (event_id),
  KEY idx_audit_entity (entity_type, entity_id),
  CONSTRAINT fk_audit_event
    FOREIGN KEY (event_id) REFERENCES events(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


SET FOREIGN_KEY_CHECKS = 1;