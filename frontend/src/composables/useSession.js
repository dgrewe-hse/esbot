import { ref, watch } from 'vue'
import * as api from '../api/esbot.js'

const USER_ID_KEY = 'esbot-user-id'
const DEFAULT_USER_ID = 'student-1'

/** Shared session state for the chat UI. */
export function useSession() {
  const userId = ref(localStorage.getItem(USER_ID_KEY) || DEFAULT_USER_ID)
  const sessions = ref([])
  const activeSessionId = ref(null)
  const messages = ref([])
  const loading = ref(false)
  const error = ref(null)

  watch(userId, (value) => {
    localStorage.setItem(USER_ID_KEY, value)
  })

  function clearError() {
    error.value = null
  }

  function setError(message) {
    error.value = message
  }

  async function loadSessions() {
    clearError()
    loading.value = true
    try {
      const data = await api.listSessions(userId.value)
      sessions.value = data.sessions
    } catch (err) {
      setError(err.message)
    } finally {
      loading.value = false
    }
  }

  async function createNewSession(title = 'New Learning Session') {
    clearError()
    loading.value = true
    try {
      const session = await api.createSession(userId.value, title)
      sessions.value = [session, ...sessions.value]
      await selectSession(session.id)
      return session
    } catch (err) {
      setError(err.message)
      return null
    } finally {
      loading.value = false
    }
  }

  async function selectSession(sessionId) {
    clearError()
    activeSessionId.value = sessionId
    loading.value = true
    try {
      const data = await api.getMessages(sessionId)
      messages.value = data.messages
    } catch (err) {
      setError(err.message)
      messages.value = []
    } finally {
      loading.value = false
    }
  }

  async function sendChatMessage(content) {
    if (!activeSessionId.value) {
      setError('Select or create a session first.')
      return null
    }
    clearError()
    loading.value = true
    try {
      const exchange = await api.sendMessage(activeSessionId.value, content)
      messages.value = [...messages.value, exchange.user_message, exchange.assistant_message]
      return exchange
    } catch (err) {
      setError(err.message)
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    userId,
    sessions,
    activeSessionId,
    messages,
    loading,
    error,
    clearError,
    loadSessions,
    createNewSession,
    selectSession,
    sendChatMessage,
  }
}
