# ESBot Frontend

Vue 3 + Vite single-page UI for the ESBot learning assistant. Designed for **automated UI and E2E testing** with stable `data-testid` selectors.

## Prerequisites

- Node.js 18+
- ESBot backend running on port **8000** with `LLM_PROVIDER=mock`

## Quick start

```bash
# Terminal 1 — backend (from repo root)
cd backend
export LLM_PROVIDER=mock DATABASE_URL=sqlite:///esbot_local.db
uv run uvicorn app.main:app --port 8000

# Terminal 2 — frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | *(empty)* | Backend API base URL. **Leave empty** to use the Vite dev proxy (`/api` → port 8000). Set to `http://localhost:8000` only when not using the proxy (requires backend `CORS_ORIGINS`). |

## UI layout

Single-screen chat view with three panels:

- **Sidebar** — user ID, session list, new session
- **Chat** — message history and input
- **Quiz** — generate questions and submit answers

All interactive elements expose `data-testid` attributes for Cypress, Playwright, and Selenium.

## Testing documentation

| Guide | Description |
|-------|-------------|
| [UI Testing (manual)](docs/ui-testing.md) | Step-by-step manual UI test cases |
| [Cypress E2E](docs/e2e/cypress.md) | Automated E2E tests with Cypress |
| [Playwright E2E](docs/e2e/playwright.md) | Automated E2E tests with Playwright |
| [Selenium E2E](docs/e2e/selenium.md) | Automated E2E tests with Selenium (Python) |

## E2E tests (quick reference)

Start both backend and frontend before running E2E tests.

### Cypress

```bash
npm run test:e2e:cypress
# Interactive mode:
npm run test:e2e:cypress:open
```

See [docs/e2e/cypress.md](docs/e2e/cypress.md) for full instructions.

### Playwright

```bash
npx playwright install chromium
npm run test:e2e:playwright
```

See [docs/e2e/playwright.md](docs/e2e/playwright.md) for full instructions.

### Selenium (Python)

Uses headless Chrome via Selenium Manager (Chrome must be installed). **Note:** Google does not publish ChromeDriver for `linux-arm64`; on ARM dev containers use Cypress or Playwright instead. Selenium runs on x86_64 Linux, macOS, and Windows.

```bash
pip install -r e2e/selenium/requirements.txt
pytest e2e/selenium/
```

See [docs/e2e/selenium.md](docs/e2e/selenium.md) for full instructions.

## Golden-path test scenario

All three frameworks run the same flow:

1. Verify API health badge shows "connected"
2. Create a new learning session
3. Send message: "What is unit testing?"
4. Assert mock assistant reply contains "This is a mock response for testing purposes."
5. Generate quiz for topic "Software Testing"
6. Select "Option A" and submit
7. Assert feedback contains "Correct!"

## Build for production

```bash
npm run build
npm run preview
```

Ensure `CORS_ORIGINS` on the backend includes your frontend origin.
