# NādaAtlas — Phase 1 Implementation Guide

Local setup, manual testing, and deployment for Phase 1 (Encyclopedia API + Data Ingestion).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Environment Configuration](#environment-configuration)
4. [Running the Stack](#running-the-stack)
5. [Database Migrations](#database-migrations)
6. [Manual API Testing](#manual-api-testing)
7. [Ingestion Pipeline](#ingestion-pipeline)
8. [Deployment — Hetzner VPS](#deployment--hetzner-vps)

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Docker | 25+ | https://docs.docker.com/get-docker/ |
| Docker Compose | v2 (bundled with Docker Desktop) | — |
| Python | 3.12+ | `brew install python@3.12` |
| OpenSSL | any | pre-installed on macOS/Linux |
| `gh` CLI | 2+ | `brew install gh` |

Verify:
```bash
docker --version
docker compose version
python3.12 --version
openssl version
```

---

## Local Development Setup

### 1. Clone and enter the repo
```bash
git clone https://github.com/ananyakaulgi/nadaatlas.git
cd nadaatlas
```

### 2. Generate JWT keypair
RS256 keys are required before the API can start. Run once:
```bash
bash infra/scripts/generate_keys.sh
# Creates: secrets/jwt_private.pem (600) and secrets/jwt_public.pem (644)
```

### 3. Configure environment
```bash
cp .env.example .env
```

Open `.env` and fill in the required values:

| Variable | What to set |
|----------|------------|
| `SECRET_KEY` | Run `openssl rand -hex 32` and paste the output |
| `POSTGRES_PASSWORD` | Any strong password, e.g. `openssl rand -hex 16` |
| `REDIS_PASSWORD` | Any strong password |
| `MINIO_ROOT_PASSWORD` | Any strong password |
| `DATABASE_URL` | Update the password to match `POSTGRES_PASSWORD` |
| `REDIS_URL` | Update the password to match `REDIS_PASSWORD` |
| `MUSICBRAINZ_CONTACT` | Your email (required by MusicBrainz API policy) |

External API keys (optional for Phase 1 — ingestion will skip those sources if blank):

| Variable | Where to get it |
|----------|----------------|
| `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` | https://developer.spotify.com/dashboard |
| `YOUTUBE_API_KEY` | https://console.cloud.google.com → APIs → YouTube Data API v3 |

### 4. Start everything
The setup script handles the full sequence automatically:
```bash
bash infra/scripts/setup_dev.sh
```

What it does:
1. Starts postgres, redis, elasticsearch, minio
2. Waits for postgres to be healthy
3. Runs `alembic upgrade head` (creates all tables)
4. Starts the api and worker

Or step by step manually:
```bash
# Start infrastructure only
docker compose up -d postgres redis elasticsearch minio

# Wait ~15 seconds for postgres to initialize, then run migrations
cd services/api
DATABASE_URL="postgresql+asyncpg://nadaatlas:<your-password>@localhost:5432/nadaatlas" \
  alembic upgrade head
cd ../..

# Start application services
docker compose up -d api worker

# (Optional) Start Adminer DB browser
docker compose --profile dev up -d adminer
```

### 5. Verify everything is running
```bash
docker compose ps
curl http://localhost:8000/health
```

Expected health response:
```json
{"status": "ok", "version": "0.1.0", "environment": "development"}
```

---

## Environment Configuration

All configuration is via environment variables — no code changes needed between environments. Key variables:

| Variable | Development | Production |
|----------|------------|-----------|
| `APP_ENV` | `development` | `production` |
| `DEBUG` | `true` | `false` |
| `DATABASE_URL` | `postgresql+asyncpg://...@localhost:5432/...` | `postgresql+asyncpg://...@postgres:5432/...` |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | `["https://nadaatlas.com"]` |
| `API_RELOAD` | `--reload` | _(leave blank)_ |

In Docker Compose, services reference each other by service name (`postgres`, `redis`, etc.) not `localhost`.

---

## Running the Stack

### Common commands

```bash
# Start all services
docker compose up -d

# Start with Adminer (DB browser at http://localhost:8080)
docker compose --profile dev up -d

# View logs
docker compose logs -f api
docker compose logs -f worker

# Restart a single service
docker compose restart api

# Stop everything (preserves data volumes)
docker compose down

# Stop and wipe all data (destructive — resets the database)
docker compose down -v
```

### Service URLs (local)

| Service | URL | Notes |
|---------|-----|-------|
| API | http://localhost:8000 | — |
| API Docs (Swagger) | http://localhost:8000/api/docs | Interactive |
| API Docs (ReDoc) | http://localhost:8000/api/redoc | — |
| Adminer (DB browser) | http://localhost:8080 | dev profile only |
| MinIO Console | http://localhost:9001 | Object storage UI |
| Elasticsearch | http://localhost:9200 | — |

---

## Database Migrations

Alembic manages all schema changes. **Never modify the database manually.**

```bash
cd services/api

# Apply all pending migrations
alembic upgrade head

# Check current migration state
alembic current

# View migration history
alembic history --verbose

# Roll back one migration
alembic downgrade -1

# Roll back to initial state (drops all tables)
alembic downgrade base
```

The `DATABASE_URL` environment variable must be set when running Alembic outside Docker. The value should use `postgresql+asyncpg://` prefix.

To create a new migration (Phase 2+):
```bash
alembic revision --autogenerate -m "add_phase2_catalog_tables"
# Review the generated file in db/migrations/versions/ before running it
```

---

## Manual API Testing

The API is fully browsable at **http://localhost:8000/api/docs** (Swagger UI). You can test all endpoints directly from the browser.

For terminal testing:

### Health check
```bash
curl http://localhost:8000/health
```

### Authentication

**Create your first admin user** (direct DB insert — no signup endpoint in Phase 1):
```bash
# Get a Python shell inside the API container
docker compose exec api python3 -c "
from app.core.security import hash_password
print(hash_password('your-password-here'))
"

# Then insert the user via Adminer (http://localhost:8080) or psql:
docker compose exec postgres psql -U nadaatlas -d nadaatlas -c "
INSERT INTO users (id, email, hashed_password, is_active, is_superuser)
VALUES (gen_random_uuid(), 'you@example.com', '<paste-hash-here>', true, true);
"
```

**Log in and get a token:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=you@example.com&password=your-password-here"
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

Save the token:
```bash
TOKEN="eyJ..."  # paste from above
```

### Musical Traditions

```bash
# List all traditions
curl http://localhost:8000/api/v1/traditions

# Filter by region
curl "http://localhost:8000/api/v1/traditions?region=South%20Asia"

# Create a tradition (requires auth)
curl -X POST http://localhost:8000/api/v1/traditions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hindustani Classical",
    "name_native": "हिन्दुस्तानी शास्त्रीय संगीत",
    "region": "South Asia",
    "subregion": "North India",
    "origin_period": "13th century CE",
    "description": "The North Indian classical music tradition, characterized by raga and tala."
  }'
```

### Instruments

```bash
# List all instruments
curl http://localhost:8000/api/v1/instruments

# Filter by Hornbostel-Sachs category
curl "http://localhost:8000/api/v1/instruments?hs_category=chordophone"

# Create an instrument (requires auth)
curl -X POST http://localhost:8000/api/v1/instruments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sitar",
    "name_native": "सितार",
    "hornbostel_sachs": "321.321",
    "hs_category": "chordophone",
    "origin_region": "South Asia",
    "description": "Long-necked plucked lute central to Hindustani classical music."
  }'
```

### Artists

```bash
# List artists
curl http://localhost:8000/api/v1/artists

# Filter by tradition
curl "http://localhost:8000/api/v1/artists?musical_tradition=Hindustani%20Classical"

# Search by name
curl "http://localhost:8000/api/v1/artists/search?q=ravi"

# Get artist detail (full biography)
curl http://localhost:8000/api/v1/artists/<uuid>

# Create an artist (requires auth)
curl -X POST http://localhost:8000/api/v1/artists \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ravi Shankar",
    "name_native": "रवि शंकर",
    "name_sort": "Shankar, Ravi",
    "musical_tradition": "Hindustani Classical",
    "nationality": "Indian",
    "born": "1920-04-07",
    "died": "2012-12-11",
    "birth_place": "Varanasi, India",
    "biography_short": "Sitar maestro who brought Indian classical music to global audiences."
  }'
```

### TOTP MFA Setup (optional)

```bash
# Generate TOTP secret (returns QR URI for Google Authenticator)
curl -X POST http://localhost:8000/api/v1/auth/totp/setup \
  -H "Authorization: Bearer $TOKEN"

# Enable TOTP after scanning the QR code
curl -X POST http://localhost:8000/api/v1/auth/totp/verify \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"totp_code": "123456"}'
```

Once enabled, log in with:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "your-password", "totp_code": "123456"}'
```

---

## Ingestion Pipeline

The worker runs on APScheduler. Jobs fire automatically on schedule, but can also be triggered manually for testing.

### Check scheduled jobs
```bash
docker compose logs worker | grep "registered"
```

### Trigger a job manually (inside the container)
```bash
docker compose exec worker python3 -c "
import asyncio
from config import WorkerSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from jobs.musicbrainz import MusicBrainzIngestionJob

settings = WorkerSettings()
engine = create_async_engine(settings.DATABASE_URL)
SessionFactory = async_sessionmaker(engine)

async def run():
    job = MusicBrainzIngestionJob(SessionFactory, settings)
    await job.ingest_artists_by_tag(
        mb_tag='hindustani classical',
        tradition='Hindustani Classical',
        region='South Asia',
        limit=10  # start small for testing
    )

asyncio.run(run())
"
```

### Monitor ingestion logs
```bash
docker compose logs -f worker
```

### Verify data appeared
```bash
curl "http://localhost:8000/api/v1/artists?musical_tradition=Hindustani%20Classical"
```

---

## Deployment — Hetzner VPS

### 1. Provision the server

- Create a **CX32** instance ($9/month) at https://console.hetzner.cloud
- OS: **Ubuntu 24.04**
- Add your SSH public key during provisioning
- Note the server IP

### 2. Initial server setup
```bash
ssh root@<server-ip>

# Create non-root deploy user
adduser deploy
usermod -aG sudo,docker deploy
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy

# Install Docker
curl -fsSL https://get.docker.com | bash

# Install Docker Compose plugin
apt-get install -y docker-compose-plugin

# Harden SSH
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart ssh

# Basic firewall
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

### 3. Deploy the application
```bash
# Switch to deploy user
su - deploy

# Clone repo
git clone https://github.com/ananyakaulgi/nadaatlas.git
cd nadaatlas

# Generate JWT keys
bash infra/scripts/generate_keys.sh

# Configure production environment
cp .env.example .env
# Edit .env:
#   APP_ENV=production
#   DEBUG=false
#   All passwords: use `openssl rand -hex 32` for each
#   CORS_ORIGINS=["https://nadaatlas.com"]  (update when domain is ready)
#   Leave API_RELOAD blank (no auto-reload in production)

# Start all services
docker compose up -d

# Run migrations
docker compose exec api alembic upgrade head

# Create admin user (same as local setup above)
```

### 4. Verify deployment
```bash
curl http://<server-ip>:8000/health
```

### 5. Point a domain (when ready)

Set an A record pointing to the server IP, then add Cloudflare as a proxy (orange cloud) for:
- DDoS protection
- SSL termination
- CDN caching

With Cloudflare in front, set `CORS_ORIGINS=["https://nadaatlas.com"]` in `.env` and restart:
```bash
docker compose restart api
```

### Ongoing operations

```bash
# Pull and redeploy latest code
git pull origin main
docker compose build api worker
docker compose up -d api worker

# Run new migrations after a deploy
docker compose exec api alembic upgrade head

# View live logs
docker compose logs -f api
docker compose logs -f worker

# Backup the database
docker compose exec postgres pg_dump -U nadaatlas nadaatlas | gzip > backup_$(date +%Y%m%d).sql.gz
```

---

## Phase 1 Checklist

Before calling Phase 1 complete:

- [ ] `docker compose up -d` starts without errors
- [ ] `GET /health` returns `{"status": "ok"}`
- [ ] Alembic migration runs cleanly (`alembic upgrade head`)
- [ ] Can create a tradition, instrument, and artist via API
- [ ] Auth login returns a JWT token
- [ ] Protected endpoints reject requests without a token (401)
- [ ] Worker starts and logs scheduled jobs
- [ ] MusicBrainz ingestion job runs and artists appear in the DB
- [ ] Wikipedia enrichment fills in `biography` and `name_native`
