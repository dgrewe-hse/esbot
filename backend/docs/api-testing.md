# Manual API Testing (Postman & Talend API Tester)

This guide covers how to run the ESBot backend **on your host machine** (without the dev container) and exercise the REST API with **Postman** or the **Talend API Tester** Chrome extension.

## Run the backend without the dev container

### Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python + [uv](https://docs.astral.sh/uv/) | 3.11+ / latest | Only for native setup (Options B/C) |
| PostgreSQL | 16 | Optional — see SQLite quick start below |
| Docker / Podman | optional | Run API without Python/uv on the host (Option A) |

### Option A — Docker / Podman (no uv on host)

Use the official **uv** container image to run the backend. No local Python or uv install required.

**Quick start (SQLite, single container)** — from the repository root:

```bash
# Docker
docker run --rm -p 8000:8000 \
  -v "$(pwd)/backend:/app" -w /app \
  -e DATABASE_URL=sqlite:// \
  -e LLM_PROVIDER=mock \
  ghcr.io/astral-sh/uv:python3.12-bookworm-slim \
  sh -c "uv sync --no-dev && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"

# Podman (same command; add :Z on SELinux systems)
podman run --rm -p 8000:8000 \
  -v "$(pwd)/backend:/app:Z" -w /app \
  -e DATABASE_URL=sqlite:// \
  -e LLM_PROVIDER=mock \
  ghcr.io/astral-sh/uv:python3.12-bookworm-slim \
  sh -c "uv sync --no-dev && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

Verify: http://localhost:8000/api/v1/health

**With PostgreSQL (two steps)** — database via compose, API in a container:

```bash
# 1. Start PostgreSQL only (from repo root)
docker compose -f .devcontainer/docker-compose.yml up -d db
# Podman: podman compose -f .devcontainer/docker-compose.yml up -d db

# 2. Run the API container (Linux: reach host DB on port 5433)
docker run --rm -p 8000:8000 \
  --add-host=host.docker.internal:host-gateway \
  -v "$(pwd)/backend:/app" -w /app \
  -e DATABASE_URL=postgresql+psycopg://esbot_user:esbot_password@host.docker.internal:5433/esbot \
  -e LLM_PROVIDER=mock \
  ghcr.io/astral-sh/uv:python3.12-bookworm-slim \
  sh -c "uv sync --no-dev && uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

On **Podman** (Linux), replace `host.docker.internal` with `host.containers.internal`:

```bash
-e DATABASE_URL=postgresql+psycopg://esbot_user:esbot_password@host.containers.internal:5433/esbot
```

On **macOS/Windows** Docker Desktop, `host.docker.internal` usually works without `--add-host`.

### Option B — PostgreSQL + uv on host (native development)

**1. Install dependencies**

```bash
cd backend
uv sync --extra dev
cp .env.example .env
```

**2. Start PostgreSQL** (database only — no dev container required)

From the repository root:

```bash
docker compose -f .devcontainer/docker-compose.yml up -d db
```

This exposes PostgreSQL on **localhost:5433** (user `esbot_user`, password `esbot_password`, database `esbot`). The default `DATABASE_URL` in `.env.example` already points there.

**3. Apply migrations**

```bash
cd backend
uv run alembic upgrade head
```

**4. Start the API**

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify: http://localhost:8000/api/v1/health

### Option C — SQLite quick start (native, no Docker)

Useful for quick manual checks when you do not want PostgreSQL:

```bash
cd backend
uv sync --extra dev
export DATABASE_URL=sqlite:///esbot_local.db
export LLM_PROVIDER=mock
uv run uvicorn app.main:app --reload --port 8000
```

Tables are created automatically on startup when using SQLite.

### Environment variables

| Variable | Typical local value | Description |
|----------|---------------------|-------------|
| `DATABASE_URL` | see `.env.example` | Database connection string |
| `LLM_PROVIDER` | `mock` | Use `mock` without Ollama; chat/quiz return deterministic responses |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Only when `LLM_PROVIDER=ollama` |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

Copy and edit `.env` from `.env.example`, or export variables in your shell before starting Uvicorn.

### Interactive API docs

FastAPI serves OpenAPI documentation while the server is running:

| URL | Purpose |
|-----|---------|
| http://localhost:8000/docs | Swagger UI — try endpoints in the browser |
| http://localhost:8000/redoc | ReDoc reference |
| http://localhost:8000/openapi.json | Raw OpenAPI schema |

---

## API overview

Base URL: `http://localhost:8000`

All JSON requests need the header:

```
Content-Type: application/json
```

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/health` | Liveness check |
| 2 | `POST` | `/api/v1/sessions` | Create learning session |
| 3 | `GET` | `/api/v1/sessions?user_id={id}` | List sessions for a user |
| 4 | `GET` | `/api/v1/sessions/{session_id}` | Get session metadata |
| 5 | `DELETE` | `/api/v1/sessions/{session_id}` | Delete session |
| 6 | `POST` | `/api/v1/sessions/{session_id}/messages` | Send chat message |
| 7 | `GET` | `/api/v1/sessions/{session_id}/messages` | Message history |
| 8 | `POST` | `/api/v1/sessions/{session_id}/quiz` | Generate quiz |
| 9 | `POST` | `/api/v1/sessions/{session_id}/quiz/{question_id}/answer` | Submit quiz answer |

> **LLM note:** With `LLM_PROVIDER=mock` (default), chat and quiz endpoints work without a real AI model. They return deterministic placeholder content. Set `LLM_PROVIDER=ollama` only if Ollama is running locally.

---

## Postman

### Import the collection

1. Start the backend (see above).
2. Open Postman → **Import** → **Upload Files**.
3. Select [`esbot-api.postman_collection.json`](esbot-api.postman_collection.json).
4. Open the collection variables and confirm `baseUrl` is `http://localhost:8000`.

### Suggested test order

Run the requests **top to bottom** in the collection folder **ESBot API**:

1. **Health Check** — expect `200`, body `"status": "ok"`.
2. **Create Session** — expect `201`; saves `session_id` automatically.
3. **List Sessions** — expect `200`.
4. **Get Session** — expect `200`.
5. **Send Message** — expect `201`; uses saved `session_id`.
6. **Get Message History** — expect `200`.
7. **Generate Quiz** — expect `201`; saves `question_id` and `correct_answer`.
8. **Submit Quiz Answer** — expect `200`.
9. **Delete Session** — expect `204` (optional cleanup).

The collection uses a **test script** on *Create Session* and *Generate Quiz* to store IDs in collection variables for later requests.

### Manual request examples

**Create session** — `POST {{baseUrl}}/api/v1/sessions`

```json
{
  "user_id": "student-1",
  "title": "Python Basics"
}
```

**Send message** — `POST {{baseUrl}}/api/v1/sessions/{{session_id}}/messages`

```json
{
  "content": "What is a unit test?"
}
```

**Generate quiz** — `POST {{baseUrl}}/api/v1/sessions/{{session_id}}/quiz`

```json
{
  "topic": "Software Testing",
  "count": 2
}
```

---

## Talend API Tester (Chrome extension)

[Talend API Tester](https://chrome.google.com/webstore/detail/talend-api-tester/aejoelaoggembcgapehfcdmlicigmgdi) is a free REST client that runs in Chrome. The workflow is similar to Postman.

### Setup

1. Install **Talend API Tester** from the Chrome Web Store.
2. Start the ESBot backend on `http://localhost:8000`.
3. Open the extension → **Import** → **Postman Collection** → select [`esbot-api.postman_collection.json`](esbot-api.postman_collection.json).

> Talend can import Postman v2 collections. If import fails, recreate the requests manually using the table and JSON bodies above.

### Configure the environment

1. In Talend, open **Environments** (or project settings).
2. Add a variable `baseUrl` = `http://localhost:8000`.
3. Replace `{{baseUrl}}` in request URLs if the import does not resolve variables automatically.

### Run requests

Execute requests in the same order as the Postman section. After **Create Session**, copy the `id` field from the response into your `session_id` variable (or the next URL path). After **Generate Quiz**, copy `items[0].id` and `items[0].correct_answer` for the answer request.

### Talend vs Postman

| Feature | Postman | Talend API Tester |
|---------|---------|-------------------|
| Install | Desktop app or web | Chrome extension |
| Import collection | Native | Postman v2 import |
| Auto-save variables | Test scripts | Manual or import |
| Offline | Yes | Yes (extension) |

For coursework, either tool is fine. Postman is smoother with the provided collection because variable extraction is pre-configured.

---

## Common issues

| Problem | Solution |
|---------|----------|
| `Connection refused` | Start Uvicorn; check port `8000` is free |
| `500` on session create (PostgreSQL) | Run `docker compose … up -d db` and `uv run alembic upgrade head` |
| `404` on messages/quiz | Create a session first; use the returned UUID in the path |
| `422` validation error | Check JSON body — `user_id`, `content`, and `topic` must not be blank |
| Chat returns `degraded: true` | LLM unavailable; with `mock` this should not happen — restart the API |
| CORS errors from a browser UI | Talend/Postman do not trigger CORS; a separate frontend may need CORS configured |

---

## See also

- [setup.md](setup.md) — full backend configuration
- [performance/README.md](../performance/README.md) — JMeter, Gatling, Locust
- [../performance/openapi/esbot-api.yaml](../performance/openapi/esbot-api.yaml) — OpenAPI reference
