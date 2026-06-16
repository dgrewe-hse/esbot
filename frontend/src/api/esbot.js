/**
 * Thin REST client for the ESBot backend API.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    let detail = `Request failed (${response.status})`
    try {
      const body = await response.json()
      if (body.detail) {
        detail = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail)
      }
    } catch {
      // ignore parse errors
    }
    throw new Error(detail)
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

/** Health check. */
export function getHealth() {
  return request('/api/v1/health')
}

/** Create a new learning session. */
export function createSession(userId, title = 'New Learning Session') {
  return request('/api/v1/sessions', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, title }),
  })
}

/** List sessions for a user. */
export function listSessions(userId) {
  return request(`/api/v1/sessions?user_id=${encodeURIComponent(userId)}`)
}

/** Get session metadata. */
export function getSession(sessionId) {
  return request(`/api/v1/sessions/${sessionId}`)
}

/** Delete a session. */
export function deleteSession(sessionId) {
  return request(`/api/v1/sessions/${sessionId}`, { method: 'DELETE' })
}

/** Send a chat message and receive the AI reply. */
export function sendMessage(sessionId, content) {
  return request(`/api/v1/sessions/${sessionId}/messages`, {
    method: 'POST',
    body: JSON.stringify({ content }),
  })
}

/** Get full message history for a session. */
export function getMessages(sessionId) {
  return request(`/api/v1/sessions/${sessionId}/messages`)
}

/** Generate quiz questions for a topic. */
export function generateQuiz(sessionId, topic, count = 1) {
  return request(`/api/v1/sessions/${sessionId}/quiz`, {
    method: 'POST',
    body: JSON.stringify({ topic, count }),
  })
}

/** Submit an answer to a quiz question. */
export function submitQuizAnswer(sessionId, questionId, answer) {
  return request(`/api/v1/sessions/${sessionId}/quiz/${questionId}/answer`, {
    method: 'POST',
    body: JSON.stringify({ answer }),
  })
}
