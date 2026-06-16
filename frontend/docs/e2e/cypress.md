# ESBot E2E Testing with Cypress — Step-by-Step Guide

This guide explains how to run and extend the **Cypress** end-to-end tests for the ESBot Vue frontend.

For manual UI verification first, see [UI Testing Guide](../ui-testing.md).

---

## 1. What Cypress tests in this project

The golden-path spec [`cypress/e2e/learning-session.cy.js`](../../cypress/e2e/learning-session.cy.js) automates:

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
| npm dependencies | Installed via `npm install` in `frontend/` |
| Running backend | Port **8000**, `LLM_PROVIDER=mock` |
| Running frontend | Port **5173**, `npm run dev` |
| Linux only | Cypress needs `xvfb` and GTK libraries on headless Linux |

Install Linux dependencies (if needed):

```bash
sudo apt-get install -y xvfb libgtk-3-0 libnss3 libgbm1
```

---

## 3. One-time setup

### Step 3.1 — Install frontend dependencies

```bash
cd frontend
npm install
```

### Step 3.2 — Configure environment

```bash
cp .env.example .env
```

Leave `VITE_API_BASE_URL` **empty** (recommended — uses Vite proxy and avoids CORS issues in Cypress Electron).

### Step 3.3 — Verify Cypress is available

```bash
npx cypress verify
```

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

## 5. Run Cypress tests

### Step 5.1 — Headless run (CI-style)

Open **Terminal 3**:

```bash
cd frontend
npm run test:e2e:cypress
```

**Expected output:**

```
✓ creates a session, chats, and completes a quiz

1 passing
```

### Step 5.2 — Interactive mode (recommended for learning)

```bash
cd frontend
npm run test:e2e:cypress:open
```

1. Cypress Test Runner opens
2. Click **E2E Testing**
3. Choose a browser (e.g. Electron or Chrome)
4. Click `learning-session.cy.js`
5. Watch the test execute step by step

---

## 6. Understand the test file

Config: [`cypress.config.js`](../../cypress.config.js)

```javascript
baseUrl: 'http://localhost:5173'
```

Key commands in the spec:

| Step | Cypress command | Selector |
|------|-----------------|----------|
| Open app | `cy.visit('/')` | — |
| Health check | `cy.get('[data-testid="health-status"]')` | `health-status` |
| New session | `cy.get('[data-testid="new-session-btn"]').click()` | `new-session-btn` |
| Type message | `cy.get('[data-testid="message-input"]').type(...)` | `message-input` |
| Assert reply | `cy.get('[data-testid="assistant-message"]').last()` | `assistant-message` |
| Quiz feedback | `cy.get('[data-testid="quiz-feedback"]')` | `quiz-feedback` |

---

## 7. Add your own Cypress test

### Step 7.1 — Create a new spec

```bash
touch frontend/cypress/e2e/my-feature.cy.js
```

### Step 7.2 — Example skeleton

```javascript
describe('My feature', () => {
  it('does something', () => {
    cy.visit('/')
    cy.get('[data-testid="health-status"]').should('contain', 'connected')
    // add steps here
  })
})
```

### Step 7.3 — Run only your spec

```bash
npx cypress run --spec cypress/e2e/my-feature.cy.js
```

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `expected health-status to contain connected` | Start backend; ensure frontend uses proxy (empty `VITE_API_BASE_URL`) |
| `cy.visit` failed / connection refused | Start frontend with `npm run dev` |
| Cypress won't start on Linux | Install `xvfb` and `libgtk-3-0` (see Section 2) |
| Test passes locally but flakes in CI | Increase timeouts; ensure `LLM_PROVIDER=mock` for deterministic replies |
| Screenshots on failure | See `frontend/cypress/screenshots/` |

---

## 9. npm scripts reference

| Script | Command |
|--------|---------|
| Headless | `npm run test:e2e:cypress` |
| Interactive | `npm run test:e2e:cypress:open` |
