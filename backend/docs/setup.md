# ESBot Backend Setup

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- PostgreSQL 16 (optional for local dev; tests use SQLite)

## Installation

```bash
cd backend
uv sync --extra dev
cp .env.example .env
```

## Database

Start PostgreSQL via docker-compose from the repo root:

```bash
docker compose -f .devcontainer/docker-compose.yml up -d db
```

Run migrations:

```bash
uv run alembic upgrade head
```

## Run the API

```bash
uv run uvicorn app.main:app --reload --port 8000
```

- Swagger UI: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg://esbot_user:esbot_password@localhost:5433/esbot` | Database connection |
| `LLM_PROVIDER` | `mock` | `mock`, `ollama`, or `litellm` |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API base URL |
| `OLLAMA_MODEL` | `ollama/llama3.2` | LiteLLM model identifier |
| `LOG_LEVEL` | `INFO` | Logging level |

## Using local Ollama (Llama 3.2)

```bash
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
uv run uvicorn app.main:app --reload --port 8000
```

From inside a dev container, use `http://host.docker.internal:11434` if Ollama runs on the host.

## LLM failure behavior

When the LLM is unavailable, services persist a **fallback assistant message** and return HTTP 201/200 with `degraded: true` in the response body. This keeps the API usable while signaling degraded mode.

## Testing

```bash
uv run pytest -m "unit or integration" --cov=app
uv run pytest -m contract    # skipped by default
uv run pytest -m performance # skipped by default
```

## Manual API testing (Postman / Talend)

To run the backend **without the dev container** and test endpoints manually, see [api-testing.md](api-testing.md). Import [`esbot-api.postman_collection.json`](esbot-api.postman_collection.json) into Postman or Talend API Tester.

## Performance, load & stress testing

See [`performance/README.md`](../performance/README.md). Tests target **session/health endpoints only** (no real LLM). The perf script uses **in-memory SQLite** — no PostgreSQL required.

```bash
./performance/scripts/start-api-for-perf.sh
```
