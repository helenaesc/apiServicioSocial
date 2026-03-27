-- =========================================
-- 006_access_code_minutes.sql
-- Accesos al catálogo: un solo uso + duración global en minutos
-- =========================================

ALTER TABLE email_verification_codes
  ADD COLUMN used_at DATETIME NULL,
  ADD COLUMN revoked BOOLEAN NOT NULL DEFAULT FALSE;

INSERT INTO app_settings (k, v)
VALUES ('ACCESS_CODE_TTL_MINUTES', '5')
ON DUPLICATE KEY UPDATE v = v;