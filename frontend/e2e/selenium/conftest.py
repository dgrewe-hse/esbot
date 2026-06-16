"""Pytest fixtures for Selenium E2E tests."""

import glob
import os
import platform

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def _is_arm64_linux() -> bool:
    return platform.system() == "Linux" and platform.machine() in {"aarch64", "arm64"}


def _find_playwright_chrome() -> str | None:
    """Locate Playwright-managed Chromium binary when available."""
    pattern = os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")
    matches = sorted(glob.glob(pattern))
    return matches[-1] if matches else None


@pytest.fixture(scope="session")
def base_url() -> str:
    """Frontend URL under test."""
    return os.environ.get("ESBOT_UI_URL", "http://localhost:5173")


@pytest.fixture
def driver(base_url: str):
    """Create a headless Chrome WebDriver instance."""
    if _is_arm64_linux():
        pytest.skip(
            "ChromeDriver has no linux-arm64 build. "
            "Run Selenium tests on x86_64/macOS/Windows, or use Cypress/Playwright."
        )

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")

    chrome_binary = _find_playwright_chrome()
    if chrome_binary:
        options.binary_location = chrome_binary

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)
    browser.get(base_url)
    yield browser
    browser.quit()
