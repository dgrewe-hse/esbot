#!/usr/bin/env bash
# Start the ESBot API for performance/load testing.
# Uses in-memory SQLite (no PostgreSQL) and session-only safe endpoints in test plans.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cd "${BACKEND_DIR}"

: "${HOST:=0.0.0.0}"
: "${PORT:=8000}"
: "${WORKERS:=1}"
: "${LLM_PROVIDER:=mock}"
: "${DATABASE_URL:=sqlite://}"

export LLM_PROVIDER DATABASE_URL

echo "Starting ESBot API for performance testing"
echo "  host=${HOST} port=${PORT} workers=${WORKERS}"
echo "  database=in-memory SQLite (${DATABASE_URL})"
echo "  note=perf tests target session/health endpoints only (no real LLM)"

if [[ "${WORKERS}" != "1" && "${DATABASE_URL}" == sqlite://* ]]; then
  echo "WARNING: SQLite in-memory does not share state across workers; forcing WORKERS=1." >&2
  WORKERS=1
fi

exec uv run uvicorn app.main:app \
  --host "${HOST}" \
  --port "${PORT}" \
  --workers "${WORKERS}"
