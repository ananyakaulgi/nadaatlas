-- NādaAtlas — PostgreSQL initialization
-- Runs once on first container start (docker-entrypoint-initdb.d)

-- ── Extensions ────────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";   -- fast trigram text search
CREATE EXTENSION IF NOT EXISTS "unaccent";  -- accent-insensitive search
-- pgvector is enabled via Alembic migration, not here

-- ── Application role (principle of least privilege) ───────────────────────────
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'nadaatlas_app') THEN
    CREATE ROLE nadaatlas_app WITH LOGIN PASSWORD 'change-me-matches-postgres-password';
  END IF;
END
$$;

GRANT CONNECT ON DATABASE nadaatlas TO nadaatlas_app;
GRANT USAGE ON SCHEMA public TO nadaatlas_app;

-- After tables are created by Alembic, run the post-migration grant script:
--   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO nadaatlas_app;
--   ALTER DEFAULT PRIVILEGES IN SCHEMA public
--     GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO nadaatlas_app;
