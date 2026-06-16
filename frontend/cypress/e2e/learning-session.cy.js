/**
 * Golden-path E2E test: session → chat → quiz.
 *
 * Prerequisites:
 * - Backend on http://localhost:8000 (LLM_PROVIDER=mock)
 * - Frontend on http://localhost:5173
 */

describe('ESBot learning session', () => {
  it('creates a session, chats, and completes a quiz', () => {
    cy.visit('/')

    cy.get('[data-testid="health-status"]', { timeout: 15000 }).should('contain', 'connected')

    cy.get('[data-testid="new-session-btn"]').click()

    cy.get('[data-testid="session-list"] li').should('have.length.at.least', 1)

    cy.get('[data-testid="message-input"]').type('What is unit testing?')
    cy.get('[data-testid="send-message-btn"]').click()

    cy.get('[data-testid="assistant-message"]', { timeout: 10000 })
      .last()
      .should('contain', 'This is a mock response for testing purposes.')

    cy.get('[data-testid="quiz-topic-input"]').type('Software Testing')
    cy.get('[data-testid="generate-quiz-btn"]').click()

    cy.get('[data-testid="quiz-question"]').should('be.visible')
    cy.contains('[data-testid="quiz-option-0"]', 'Option A').click()
    cy.get('[data-testid="submit-answer-btn"]').click()

    cy.get('[data-testid="quiz-feedback"]', { timeout: 10000 })
      .should('contain', 'Correct!')
  })
})
