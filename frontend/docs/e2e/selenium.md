# ESBot E2E Testing with Selenium — Step-by-Step Guide

This guide explains how to run and extend the **Selenium (Python + pytest)** end-to-end tests for the ESBot Vue frontend.

For manual UI verification first, see [UI Testing Guide](../ui-testing.md).

---

## 1. What Selenium tests in this project

The golden-path spec [`e2e/selenium/test_learning_session.py`](../../e2e/selenium/test_learning_session.py) automates:

1. Open the app in headless Chrome
2. Verify API health is "connected"
3. Create a new learning session
4. Send a chat message and assert the mock assistant reply
5. Generate a quiz, select Option A, submit, and assert "Correct!"

Fixtures live in [`e2e/selenium/conftest.py`](../../e2e/selenium/conftest.py).

---

## 2. Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.11+ | Same as backend |
| Google Chrome | Installed on the system |
| Selenium Manager | Bundled with Selenium 4.6+ (auto-downloads ChromeDriver) |
| Running backend | Port **8000**, `LLM_PROVIDER=mock` |
| Running frontend | Port **5173**, `npm run dev` |

### Platform note: linux-arm64

Google does **not** publish ChromeDriver for `linux-arm64`. On ARM dev containers (e.g. Apple Silicon Docker), Selenium tests are **skipped** automatically. Use **Cypress** or **Playwright** on ARM, or run Selenium on **x86_64 Linux**, **macOS**, or **Windows**.

---

## 3. One-time setup

### Step 3.1 — Install Python dependencies

```bash
cd frontend
pip install -r e2e/selenium/requirements.txt
```

Or with a virtual environment (recommended):

```bash
cd frontend
python -m venv .venv-selenium
source .venv-selenium/bin/activate   # Windows: .venv-selenium\Scripts\activate
pip install -r e2e/selenium/requirements.txt
```

### Step 3.2 — Verify Chrome is installed

```bash
google-chrome --version
# or on macOS:
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

### Step 3.3 — Configure frontend environment

```bash
cd frontend
cp .env.example .env
npm install
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

## 5. Run Selenium tests

### Step 5.1 — Run all Selenium E2E tests

Open **Terminal 3**:

```bash
cd frontend
pytest e2e/selenium/ -v
```

**Expected output (x86_64 / macOS / Windows):**

```
e2e/selenium/test_learning_session.py::test_learning_session_golden_path PASSED
```

**Expected on linux-arm64:**

```
e2e/selenium/test_learning_session.py::test_learning_session_golden_path SKIPPED
```

### Step 5.2 — Run with verbose browser logging

```bash
pytest e2e/selenium/ -v -s
```

### Step 5.3 — Override frontend URL

```bash
ESBOT_UI_URL=http://localhost:5173 pytest e2e/selenium/ -v
```

---

## 6. Understand the test file

### Fixture: `driver`

`conftest.py` creates a headless Chrome WebDriver:

- Opens `http://localhost:5173` (or `ESBOT_UI_URL`)
- Uses Selenium Manager to resolve ChromeDriver automatically
- Quits the browser after each test

### Locator strategy

Tests use **CSS selectors** with `data-testid` attributes:

```python
driver.find_element(By.CSS_SELECTOR, '[data-testid="new-session-btn"]').click()
```

### Explicit waits

Selenium uses `WebDriverWait` instead of fixed `sleep()`:

```python
wait = WebDriverWait(driver, 15)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="quiz-question"]')))
```

| Step | Selenium API | Selector |
|------|--------------|----------|
| Health check | `WebDriverWait` + `visibility_of_element_located` | `health-status` |
| Click button | `find_element(...).click()` | `new-session-btn` |
| Type text | `send_keys(...)` | `message-input` |
| Assert reply | custom `wait.until(...)` | `assistant-message` |
| Quiz feedback | `visibility_of_element_located` | `quiz-feedback` |

---

## 7. Add your own Selenium test

### Step 7.1 — Create a new test file

```bash
touch frontend/e2e/selenium/test_my_feature.py
```

### Step 7.2 — Example skeleton

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_my_feature(driver):
  wait = WebDriverWait(driver, 10)
  health = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="health-status"]'))
  )
  assert "connected" in health.text
```

The `driver` fixture is provided automatically by `conftest.py`.

### Step 7.3 — Run only your test

```bash
pytest e2e/selenium/test_my_feature.py -v
```

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `SKIPPED` on ARM Linux | Expected — use Cypress/Playwright, or run on x86_64/macOS/Windows |
| `Unable to obtain driver for chrome` | Install Google Chrome; ensure Selenium ≥ 4.6 |
| `NoSuchElementException` | Increase wait timeout; confirm `data-testid` matches the UI |
| Health check fails | Start backend; leave `VITE_API_BASE_URL` empty in frontend `.env` |
| `Connection refused` on `driver.get()` | Start frontend with `npm run dev` |
| Stale element after DOM update | Re-find the element after page changes |

---

## 9. Command reference

| Task | Command |
|------|---------|
| Run all tests | `pytest e2e/selenium/ -v` |
| Run one file | `pytest e2e/selenium/test_learning_session.py -v` |
| Show print output | `pytest e2e/selenium/ -v -s` |
| Custom UI URL | `ESBOT_UI_URL=http://localhost:5173 pytest e2e/selenium/` |
