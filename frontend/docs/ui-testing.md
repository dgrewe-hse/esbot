# ESBot UI Testing — Step-by-Step Guide

This guide walks you through **manual UI testing** of the ESBot frontend. Use it for exploratory testing, UX evaluation, or as a baseline before writing automated E2E tests.

For automated end-to-end tests, see the tool-specific guides:

- [Cypress E2E](e2e/cypress.md)
- [Playwright E2E](e2e/playwright.md)
- [Selenium E2E](e2e/selenium.md)

---

## 1. Prerequisites

| Requirement | Version / note |
|-------------|----------------|
| Node.js | 18+ |
| Python + uv | For the backend (see [`backend/docs/setup.md`](../../backend/docs/setup.md)) |
| Web browser | Chrome, Firefox, or Edge |

---

## 2. Start the application

### Step 2.1 — Start the backend

Open **Terminal 1**:

```bash
cd backend
uv sync --extra dev
export LLM_PROVIDER=mock
export DATABASE_URL=sqlite:///esbot_local.db
uv run uvicorn app.main:app --reload --port 8000
```

**Verify:** open http://localhost:8000/api/v1/health — you should see:

```json
{"status":"ok","app":"ESBot API","version":"0.1.0"}
```

### Step 2.2 — Start the frontend

Open **Terminal 2**:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

**Verify:** open http://localhost:5173 — the ESBot page loads with header, sidebar, chat, and quiz panels.

> **Tip:** Leave `VITE_API_BASE_URL` empty in `.env` so API calls go through the Vite proxy (`/api` → port 8000).

---

## 3. UI layout overview

The screen has three panels on a single page (`/`):

| Panel | Location | Purpose |
|-------|----------|---------|
| **Sessions** | Left sidebar | User ID, session list, create session |
| **Chat** | Center | Message history, send questions |
| **Quiz** | Right | Generate and answer practice questions |

---

## 4. Test cases (step by step)

### TC-UI-01 — API health indicator

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Open http://localhost:5173 | Page loads without errors |
| 2 | Look at the badge below the header (`data-testid="health-status"`) | Text shows **API: connected** (green badge) |
| 3 | Stop the backend (`Ctrl+C` in Terminal 1) | Badge changes to **API: unreachable** (red) and error banner may appear |
| 4 | Restart the backend | Badge returns to **connected** after refresh |

---

### TC-UI-02 — Create a learning session

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Ensure API is connected | Health badge shows "connected" |
| 2 | Check the **User ID** field (`data-testid="user-id-input"`) | Default value: `student-1` |
| 3 | Click **New Session** (`data-testid="new-session-btn"`) | Button is enabled; no error banner |
| 4 | Check the session list (`data-testid="session-list"`) | A new session appears with title "New Learning Session" |
| 5 | Check the **Chat** panel | Placeholder disappears; message area and input are visible |

---

### TC-UI-03 — Send a chat message

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Select or create a session | Chat panel is active |
| 2 | Type `What is unit testing?` in the message input (`data-testid="message-input"`) | Text appears in the textarea |
| 3 | Click **Send** (`data-testid="send-message-btn"`) | Brief loading indicator (`data-testid="chat-loading"`) may appear |
| 4 | Check the message list (`data-testid="message-list"`) | Your message appears as **user** (blue bubble, right-aligned) |
| 5 | Wait for the assistant reply (`data-testid="assistant-message"`) | Gray bubble with text containing *"This is a mock response for testing purposes."* (when `LLM_PROVIDER=mock`) |

---

### TC-UI-04 — Generate and answer a quiz

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Ensure a session is selected | Quiz panel is active |
| 2 | Enter `Software Testing` in the topic field (`data-testid="quiz-topic-input"`) | Text is accepted |
| 3 | Click **Generate Quiz** (`data-testid="generate-quiz-btn"`) | A question appears (`data-testid="quiz-question"`) with four options |
| 4 | Select **Option A** (`data-testid="quiz-option-0"`) | Radio button is checked |
| 5 | Click **Submit Answer** (`data-testid="submit-answer-btn"`) | Feedback area appears (`data-testid="quiz-feedback"`) |
| 6 | Read the feedback | Green box with text containing **Correct!** |

---

### TC-UI-05 — Switch sessions

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Create a second session via **New Session** | Session list has two entries |
| 2 | Click the first session in the list (`data-testid="session-item-{id}"`) | Session is highlighted; chat shows that session's messages |
| 3 | Click the second session | Chat updates to the second session's (empty) history |

---

### TC-UI-06 — Error handling

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | With backend stopped, click **New Session** | Red error banner (`data-testid="error-banner"`) appears with a meaningful message |
| 2 | Click the **×** on the error banner | Banner is dismissed |
| 3 | Try to send a message with an empty input | **Send** button stays disabled |

---

## 5. Selector reference (`data-testid`)

Use these stable selectors when writing automated tests:

| Element | `data-testid` |
|---------|---------------|
| API health badge | `health-status` |
| Error banner | `error-banner` |
| User ID input | `user-id-input` |
| New session button | `new-session-btn` |
| Session list | `session-list` |
| Session item | `session-item-{uuid}` |
| Message list | `message-list` |
| Message input | `message-input` |
| Send button | `send-message-btn` |
| Chat loading indicator | `chat-loading` |
| User message bubble | `user-message` |
| Assistant message bubble | `assistant-message` |
| Quiz topic input | `quiz-topic-input` |
| Generate quiz button | `generate-quiz-btn` |
| Quiz question text | `quiz-question` |
| Quiz option (0-based) | `quiz-option-0` … `quiz-option-3` |
| Submit answer button | `submit-answer-btn` |
| Quiz feedback | `quiz-feedback` |

---

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| **API: unreachable** | Backend not running | Start uvicorn on port 8000 |
| **Failed to fetch** (with direct API URL) | CORS not configured | Leave `VITE_API_BASE_URL` empty, or add your origin to `CORS_ORIGINS` in the backend |
| No assistant reply | Wrong `LLM_PROVIDER` or backend error | Use `LLM_PROVIDER=mock`; check backend terminal for errors |
| Quiz feedback says incorrect | Wrong option selected | With mock LLM, **Option A** is always correct |
| Sessions from a previous run | Data persisted in SQLite/Postgres | Delete `backend/esbot_local.db` or use a new `user_id` |

---

## 7. Recording results

For lab submissions, document each test case with:

1. **Test case ID** (e.g. TC-UI-03)
2. **Date and tester**
3. **Environment** (OS, browser, `LLM_PROVIDER`)
4. **Steps performed**
5. **Expected vs. actual result**
6. **Pass / Fail**
7. **Screenshot** (optional, for failures)
