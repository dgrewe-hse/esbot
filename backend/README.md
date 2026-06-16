# ESBot Backend

FastAPI backend for the ESBot AI-powered learning assistant.

## Quick start

```bash
cd backend
uv sync --extra dev
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Testing

```bash
uv run ruff check .
uv run pytest -m "unit or integration" --cov=app --cov-report=term-missing
```

See [docs/setup.md](docs/setup.md) for environment variables and Ollama configuration.

## Manual API testing (Postman / Talend)

Run the backend on your host without the dev container and test endpoints with Postman or the Talend API Tester Chrome extension:

- Guide: [docs/api-testing.md](docs/api-testing.md)
- Postman collection: [docs/esbot-api.postman_collection.json](docs/esbot-api.postman_collection.json)

## Performance testing

JMeter and Gatling scenarios for load and stress testing live in [performance/](performance/README.md).
