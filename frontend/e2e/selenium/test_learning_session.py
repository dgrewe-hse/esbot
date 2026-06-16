"""
Golden-path E2E test: session → chat → quiz.

Prerequisites:
- Backend on http://localhost:8000 (LLM_PROVIDER=mock)
- Frontend on http://localhost:5173
- Chrome browser installed
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_learning_session_golden_path(driver):
    """Create session, send chat message, generate quiz, submit correct answer."""
    wait = WebDriverWait(driver, 15)

    health = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="health-status"]')))
    assert "connected" in health.text

    driver.find_element(By.CSS_SELECTOR, '[data-testid="new-session-btn"]').click()

    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, '[data-testid="session-list"] li')) >= 1)

    message_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="message-input"]')
    message_input.send_keys("What is unit testing?")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="send-message-btn"]').click()

    def assistant_has_mock_response(d):
        messages = d.find_elements(By.CSS_SELECTOR, '[data-testid="assistant-message"]')
        return messages and "This is a mock response for testing purposes." in messages[-1].text

    wait.until(assistant_has_mock_response)

    quiz_topic = driver.find_element(By.CSS_SELECTOR, '[data-testid="quiz-topic-input"]')
    quiz_topic.send_keys("Software Testing")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="generate-quiz-btn"]').click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="quiz-question"]')))

    option_a = driver.find_element(By.CSS_SELECTOR, '[data-testid="quiz-option-0"]')
    option_a.click()
    driver.find_element(By.CSS_SELECTOR, '[data-testid="submit-answer-btn"]').click()

    feedback = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="quiz-feedback"]')))
    assert "Correct!" in feedback.text
