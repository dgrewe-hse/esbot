/**
 * Golden-path E2E test: session → chat → quiz.
 *
 * Prerequisites:
 * - Backend on http://localhost:8000 (LLM_PROVIDER=mock)
 * - Frontend on http://localhost:5173
 */

import { test, expect } from '@playwright/test'

test('creates a session, chats, and completes a quiz', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByTestId('health-status')).toContainText('connected')

  await page.getByTestId('new-session-btn').click()

  await expect(page.getByTestId('session-list').locator('li').first()).toBeVisible({
    timeout: 10000,
  })

  await page.getByTestId('message-input').fill('What is unit testing?')
  await page.getByTestId('send-message-btn').click()

  const assistantMessage = page.getByTestId('assistant-message').last()
  await expect(assistantMessage).toContainText(
    'This is a mock response for testing purposes.',
    { timeout: 10000 },
  )

  await page.getByTestId('quiz-topic-input').fill('Software Testing')
  await page.getByTestId('generate-quiz-btn').click()

  await expect(page.getByTestId('quiz-question')).toBeVisible()

  await page.getByTestId('quiz-option-0').getByText('Option A').click()
  await page.getByTestId('submit-answer-btn').click()

  await expect(page.getByTestId('quiz-feedback')).toContainText('Correct!', {
    timeout: 10000,
  })
})
