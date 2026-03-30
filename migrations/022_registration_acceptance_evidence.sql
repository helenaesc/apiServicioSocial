ALTER TABLE registrations
ADD COLUMN acceptance_snapshot_json JSON NULL,
ADD COLUMN acceptance_hash CHAR(64) NULL,
ADD COLUMN accepted_ip VARCHAR(64) NULL,
ADD COLUMN accepted_user_agent VARCHAR(255) NULL;