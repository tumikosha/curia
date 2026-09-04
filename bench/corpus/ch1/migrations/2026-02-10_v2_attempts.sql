CREATE TABLE export_attempts_v2 (
    id BIGSERIAL PRIMARY KEY,
    export_id BIGINT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    ok BOOLEAN NOT NULL
);
-- export_attempts_v1 оставлена до конца переключения (BIL-201)
