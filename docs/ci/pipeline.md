# CI Pipeline Design (Exercise 9)

## Overview

GitHub Actions workflow: [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)

## Triggers

- **`push`** — every branch push runs CI so broken commits are caught early
- **`pull_request`** — verifies contributions before merge

`workflow_dispatch` could be added later for manual runs (e.g. performance tests).

## Runner

`ubuntu-latest` — standard hosted runner with good Python and Docker support for the Postgres service container.

## Jobs

### 1. `lint`

- Installs Python 3.12 via uv
- Runs `ruff check` and `ruff format --check` on `backend/`

### 2. `test` (matrix)

- Python **3.11** and **3.12** for compatibility coverage
- Postgres 16 service container (parity with local docker-compose)
- `LLM_PROVIDER=mock` — deterministic, no Ollama in CI
- `pytest -m "unit or integration"` with 80% coverage gate
- Coverage XML artifact uploaded from Python 3.12 job

### 3. `security` (Exercise 9.2 enhancement)

- Runs `pip-audit` to scan Python dependencies for known vulnerabilities

## Intentionally excluded from CI

| Check | Reason |
|-------|--------|
| Live Ollama / LLM | Non-deterministic; use `MockLLM` in CI |
| Contract tests (`@pytest.mark.contract`) | Enabled in a later lab |
| Performance tests (`@pytest.mark.performance`) | Optional `workflow_dispatch` later |
| Frontend (Next.js) | Separate round of development |

## Local / CI parity

| Local command | CI step |
|---------------|---------|
| `uv run ruff check .` | `lint` job |
| `uv run ruff format --check .` | `lint` job |
| `uv run pytest -m "unit or integration" --cov=app` | `test` job |
| `uv run pip-audit` | `security` job |

Integration tests use **SQLite in-memory** locally and in CI, so they do not require the Postgres service. The Postgres service is provisioned for future repository tests against PostgreSQL and for migration smoke checks if added later.

## Exercise 9.2 enhancements

**Tool:** `pip-audit` (security & dependency management)

**Why it fits ESBot:** The backend depends on many packages (FastAPI, SQLAlchemy, LiteLLM). Automated vulnerability scanning catches known CVEs before they reach students' environments.

**Value vs. cost:** Low maintenance, ~30s runtime, occasional false positives on dev dependencies — acceptable for a teaching project.

**Local sync:** Run `uv run pip-audit` from `backend/` before pushing (documented in `local-verification.md`).
