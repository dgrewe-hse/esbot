# ESBot Performance, Load & Stress Testing

Performance tooling for the ESBot REST API using **Apache JMeter**, **Gatling**, and **Locust**.

> **Important:** There is no real LLM bound to the backend in the dev environment. Performance tests target **session and health endpoints only** — they do **not** call chat (`POST …/messages`) or quiz routes that depend on AI inference.

| Tool | Best for | Scenarios |
|------|----------|-----------|
| **JMeter** | GUI design, HTML dashboards | Smoke, load (50 users), stress (200 users) |
| **Gatling** | Code-as-test, rich reports | Smoke, load, stress |
| **Locust** | Python-native quick runs | [`../locustfile.py`](../locustfile.py) |

## Endpoints under test

| Method | Endpoint | LLM? | In perf tests |
|--------|----------|------|---------------|
| `GET` | `/api/v1/health` | No | Yes |
| `POST` | `/api/v1/sessions` | No | Yes |
| `GET` | `/api/v1/sessions?user_id=` | No | Yes |
| `GET` | `/api/v1/sessions/{id}` | No | Yes |
| `GET` | `/api/v1/sessions/{id}/messages` | No (read-only) | Yes |
| `POST` | `/api/v1/sessions/{id}/messages` | **Yes** | **No** |
| `POST` | `/api/v1/sessions/{id}/quiz` | **Yes** | **No** |
| `POST` | `/api/v1/sessions/{id}/quiz/{qid}/answer` | **Yes** | **No** |

OpenAPI reference: [`openapi/esbot-api.yaml`](openapi/esbot-api.yaml)

## Dev container

The dev container installs **Locust** (`uv sync --extra dev`) and **Apache JMeter 5.6** (`JMETER_HOME=/opt/apache-jmeter`) via `post-create.sh`. **Gatling** still requires Maven (install separately or use the Java feature + SDKMAN).

## Prepare the backend

Performance runs use **in-memory SQLite** — no PostgreSQL or migrations required.

```bash
cd backend
./performance/scripts/start-api-for-perf.sh
```

Defaults:

| Setting | Value | Why |
|---------|-------|-----|
| `DATABASE_URL` | `sqlite://` | In-memory DB for speed |
| `WORKERS` | `1` | SQLite in-memory is per-process |
| `LLM_PROVIDER` | `mock` | Not used by perf endpoints |

The API auto-creates tables on startup when using SQLite.

## Apache JMeter

**Prerequisites:** [Apache JMeter](https://jmeter.apache.org/) 5.6+

| File | Type | Profile |
|------|------|---------|
| `jmeter/esbot-smoke-test.jmx` | Smoke | 1 user × 3 loops |
| `jmeter/esbot-load-test.jmx` | Load | 50 users, 60s ramp, 5 min |
| `jmeter/esbot-stress-test.jmx` | Stress | 200 users, 10 min ramp |

```bash
cd backend/performance/jmeter
./run-smoke.sh
./run-load.sh
```

Override host: `-Jbase.host=127.0.0.1 -Jbase.port=8000`

## Gatling

**Prerequisites:** Java 17+, Maven 3.9+

| Class | Type |
|-------|------|
| `ESBotSmokeSimulation` | Smoke (single pass) |
| `ESBotLoadSimulation` | Load (50 users) |
| `ESBotStressSimulation` | Stress (200 users) |

```bash
cd backend/performance/gatling
./run-smoke.sh
./run-load.sh
```

## Locust

```bash
cd backend
./performance/scripts/start-api-for-perf.sh   # terminal 1
uv run locust -f locustfile.py --host http://localhost:8000
# or headless:
uv run locust -f locustfile.py --host http://localhost:8000 --headless -u 10 -r 2 --run-time 30s
```

Locust is included in backend dev dependencies (`uv sync --extra dev`).

## NFR target (from `docs/esbot.md`)

- **Load:** up to **50 concurrent users**
- **Response time:** **2–5 seconds** under normal load

With in-memory SQLite and session-only endpoints, observed latencies should be well below the NFR.

## Troubleshooting

| Symptom | Likely cause |
|---------|----------------|
| Connection refused | Run `start-api-for-perf.sh` first |
| 500 on session create | Old API process with empty DB — restart perf script |
| Gatling runs all simulations | Use `./run-smoke.sh` or `-Dgatling.runMultipleSimulations=false` |
| Multi-worker + SQLite | Use `WORKERS=1` (default) |
