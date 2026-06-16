# ESBot E2E Testing with Playwright — Step-by-Step Guide

This guide explains how to run and extend the **Playwright** end-to-end tests for the ESBot Vue frontend.

For manual UI verification first, see [UI Testing Guide](../ui-testing.md).

---

## 1. What Playwright tests in this project

The golden-path spec [`playwright/learning-session.spec.js`](../../playwright/learning-session.spec.js) automates:

1. Open the app
2. Verify API health is "connected"
3. Create a new learning session
4. Send a chat message and assert the mock assistant reply
5. Generate a quiz, select Option A, submit, and assert "Correct!"

---

## 2. Prerequisites

| Requirement | Notes |
|-------------|-------|
| Node.js 18+ | Same as frontend dev |
| npm dependencies | `npm install` in `frontend/` |
| Playwright browsers | One-time: `npx playwright install chromium` |
| Running backend | Port **8000**, `LLM_PROVIDER=mock` |
| Running frontend | Port **5173**, `npm run dev` |

Install Linux browser dependencies (if Playwright warns about missing libraries):

```bash
npx playwright install-deps
```

---

## 3. One-time setup

### Step 3.1 — Install frontend dependencies

```bash
cd frontend
npm install
```

### Step 3.2 — Install Playwright Chromium

```bash
npx playwright install chromium
```

### Step 3.3 — Configure environment

```bash
cp .env.example .env
```

Leave `VITE_API_BASE_URL` **empty** (uses Vite proxy).

---

## 4. Start the application (required before every test run)

### Step 4.1 — Terminal 1: Backend

```bash
cd backend
export LLM_PROVIDER=mock
export DATABASE_URL=sqlite:///esbot_local.db
uv run uvicorn app.main:app --port 8000
```

### Step 4.2 — Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

Confirm http://localhost:5173 loads and the health badge shows **connected**.

---

## 5. Run Playwright tests

### Step 5.1 — Headless run (default)

Open **Terminal 3**:

```bash
cd frontend
npm run test:e2e:playwright
```

**Expected output:**

```
✓ [chromium] › learning-session.spec.js › creates a session, chats, and completes a quiz

1 passed
```

### Step 5.2 — Headed mode (watch the browser)

```bash
npx playwright test --headed
```

### Step 5.3 — Debug mode (step through)

```bash
npx playwright test --debug
```

Opens Playwright Inspector — step through each action line by line.

### Step 5.4 — UI mode (test explorer)

```bash
npx playwright test --ui
```

---

## 6. Understand the test file

Config: [`playwright.config.js`](../../playwright.config.js)

```javascript
baseURL: 'http://localhost:5173'
testDir: './playwright'
```

Key API usage in the spec:

| Step | Playwright API | Locator |
|------|----------------|---------|
| Open app | `page.goto('/')` | — |
| Health check | `page.getByTestId('health-status')` | `health-status` |
| New session | `page.getByTestId('new-session-btn').click()` | `new-session-btn` |
| Type message | `page.getByTestId('message-input').fill(...)` | `message-input` |
| Assert reply | `page.getByTestId('assistant-message').last()` | `assistant-message` |
| Quiz feedback | `page.getByTestId('quiz-feedback')` | `quiz-feedback` |

Playwright auto-waits for elements — no manual `sleep()` needed in most cases.

---

## 7. Add your own Playwright test

### Step 7.1 — Create a new spec

```bash
touch frontend/playwright/my-feature.spec.js
```

### Step 7.2 — Example skeleton

```javascript
import { test, expect } from '@playwright/test'

test('my feature works', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('health-status')).toContainText('connected')
  // add steps here
})
```

### Step 7.3 — Run only your spec

```bash
npx playwright test playwright/my-feature.spec.js
```

### Step 7.4 — Generate tests with Codegen (optional)

With frontend running:

```bash
npx playwright codegen http://localhost:5173
```

Records clicks and types into Playwright code.

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `Host system is missing dependencies` | Run `npx playwright install-deps` |
| Health check fails | Start backend; check `.env` uses proxy (empty `VITE_API_BASE_URL`) |
| `page.goto: net::ERR_CONNECTION_REFUSED` | Start frontend with `npm run dev` |
| Non-deterministic assistant text | Use `LLM_PROVIDER=mock` on the backend |
| View trace on failure | Traces saved when using `--trace on`; open with `npx playwright show-trace` |

---

## 9. npm scripts reference

| Script | Command |
|--------|---------|
| Headless | `npm run test:e2e:playwright` |
| Headed | `npx playwright test --headed` |
| Debug | `npx playwright test --debug` |
| UI mode | `npx playwright test --ui` |
