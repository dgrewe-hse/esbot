# Local Verification (ESBot)

This document describes the exact commands used to verify ESBot's quality locally,
before and in sync with the CI pipeline.

---

## Prerequisites

- Python 3.11 or higher
- [`uv`](https://docs.astral.sh/uv/) installed (`pip install uv`)
- No external services required — tests use an in-memory SQLite database; no PostgreSQL, no live LLM

---

## Step 1 — Run the test suite

From the `backend/` directory:

```bash
uv run pytest
```

Expected outcome: all tests pass, exit code 0.

```
98 passed, 125 warnings in 0.24s
```

The test suite covers:
- Domain model unit tests (`tests/test_*.py`) — use SQLite in-memory via SQLAlchemy's `StaticPool`
- Smoke tests (`test_smoke.py`) — use a `TestClient` with a dependency-overridden in-memory DB

No network connection, no LLM, no database server is needed. The environment variable `DATABASE_URL` is overridden in `conftest.py` at test time.

---

## Step 2 — Run static analysis (Bandit)

From the `backend/` directory:

```bash
uv run bandit -r app/
```

Expected outcome: `No issues identified.`, exit code 0.

Bandit scans the application source (`app/`) for security issues. Configuration is in `pyproject.toml` under `[tool.bandit]`:
- `B101` (assert statements) is suppressed — asserts are only in test files, which are excluded from the scan
- `B104` (binding to all interfaces) is suppressed — `host=0.0.0.0` is expected behaviour in a dev/container environment and is not a real vulnerability here

---

## Step 3 — Run complexity analysis (Radon, informational only)

From the `backend/` directory:

```bash
uv run radon cc app/ -a -s
```

This is **not** a pass/fail gate. Output is informational — it highlights functions with elevated cyclomatic complexity so they can be reviewed manually. No exit code is enforced.

```bash
# Maintainability index per file
uv run radon mi app/
```

---

## Summary

| Check | Command | Gate? |
|---|---|---|
| Unit tests | `uv run pytest` | yes — fails on test failure |
| Security scan | `uv run bandit -r app/` | yes — fails on any new finding |
| Complexity | `uv run radon cc app/ -a -s` | no — informational only |

---

## Environment variables

No environment variables are required to run tests or static analysis locally.
The `DATABASE_URL` setting in `backend/.env` (if present) is not used during tests — `conftest.py` overrides the database connection with an in-memory SQLite URL directly.
