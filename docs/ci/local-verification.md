# Local Verification (Exercise 9.1)

Commands to run locally before pushing. CI mirrors these steps.

## Backend tests

```bash
cd backend
uv sync --extra dev
uv run pytest -m "unit or integration" --cov=app --cov-report=term-missing
```

**Expected outcome:** All tests pass (48+), coverage ≥ 80%. No live LLM or production database required — tests use SQLite in-memory and `MockLLM`.

## Linting

```bash
cd backend
uv run ruff check .
uv run ruff format --check .
```

**Expected outcome:** No lint or format violations.

## Security audit (optional, also runs in CI)

```bash
cd backend
uv run pip-audit
```

## Environment variables

| Variable | Test default | Description |
|----------|--------------|-------------|
| `LLM_PROVIDER` | `mock` | Use `ollama` for local Llama 3.2 |
| `DATABASE_URL` | SQLite (tests) | PostgreSQL URL for local dev |

## Optional: run full verification

```bash
cd backend
uv run ruff check . && uv run ruff format --check . && uv run pytest -m "unit or integration" --cov=app
```
