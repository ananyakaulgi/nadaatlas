#!/usr/bin/env bash
# NādaAtlas — local development setup
# Idempotent: safe to run multiple times.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cd "${PROJECT_ROOT}"

# ── Colours ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { echo -e "${CYAN}[nadaatlas]${NC} $*"; }
success() { echo -e "${GREEN}[nadaatlas]${NC} $*"; }
warn()    { echo -e "${YELLOW}[nadaatlas]${NC} $*"; }

# ── 1. Copy .env.example → .env ───────────────────────────────────────────────
if [[ ! -f "${PROJECT_ROOT}/.env" ]]; then
  info "Creating .env from .env.example …"
  cp "${PROJECT_ROOT}/.env.example" "${PROJECT_ROOT}/.env"
  warn ".env created — edit it and replace all 'change-me' placeholders before continuing."
  warn "Then re-run this script."
  exit 0
else
  info ".env already exists — skipping copy."
fi

# ── 2. Create secrets/ directory ─────────────────────────────────────────────
if [[ ! -d "${PROJECT_ROOT}/secrets" ]]; then
  info "Creating secrets/ directory …"
  mkdir -p "${PROJECT_ROOT}/secrets"
  # Prevent accidental git commits of key material
  if ! grep -q "^secrets/" "${PROJECT_ROOT}/.gitignore" 2>/dev/null; then
    echo "secrets/" >> "${PROJECT_ROOT}/.gitignore"
    info "Added secrets/ to .gitignore."
  fi
else
  info "secrets/ directory already exists — skipping."
fi

# ── 3. JWT key generation reminder ───────────────────────────────────────────
JWT_PRIVATE="${PROJECT_ROOT}/secrets/jwt_private.pem"
JWT_PUBLIC="${PROJECT_ROOT}/secrets/jwt_public.pem"
if [[ ! -f "${JWT_PRIVATE}" || ! -f "${JWT_PUBLIC}" ]]; then
  warn "JWT keys not found. Generate them now with:"
  warn ""
  warn "  openssl genrsa -out secrets/jwt_private.pem 4096"
  warn "  openssl rsa -in secrets/jwt_private.pem -pubout -out secrets/jwt_public.pem"
  warn ""
  warn "Then re-run this script."
  exit 0
else
  info "JWT keys present — skipping generation."
fi

# ── 4. Start stateful infrastructure services ─────────────────────────────────
info "Starting infrastructure services (postgres, redis, elasticsearch, minio) …"
docker compose up -d postgres redis elasticsearch minio

# ── 5. Wait for postgres to be healthy ───────────────────────────────────────
info "Waiting for postgres to be healthy …"
RETRIES=30
until docker compose exec -T postgres pg_isready -U "${POSTGRES_USER:-nadaatlas}" -d "${POSTGRES_DB:-nadaatlas}" &>/dev/null; do
  RETRIES=$((RETRIES - 1))
  if [[ "${RETRIES}" -le 0 ]]; then
    echo ""
    warn "postgres did not become healthy in time. Check logs: docker compose logs postgres"
    exit 1
  fi
  printf "."
  sleep 2
done
echo ""
success "postgres is ready."

# ── 6. Run database migrations ────────────────────────────────────────────────
info "Running Alembic migrations …"
docker compose run --rm api alembic upgrade head
success "Migrations complete."

# ── 7. Start application services ─────────────────────────────────────────────
info "Starting api and worker services …"
docker compose up -d api worker

# ── 8. Done ───────────────────────────────────────────────────────────────────
echo ""
success "NādaAtlas is running at http://localhost:8000/api/docs"
success "Adminer (DB UI)  →  http://localhost:8080"
success "MinIO console    →  http://localhost:9001"
echo ""
info  "To tail all logs:  docker compose logs -f"
info  "To stop all:       docker compose down"
