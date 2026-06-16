<template>
  <div class="chat-layout">
    <!-- Error banner -->
    <div
      v-if="error"
      class="error-banner"
      role="alert"
      data-testid="error-banner"
    >
      {{ error }}
      <button type="button" aria-label="Dismiss error" @click="clearError">×</button>
    </div>

    <!-- Health status -->
    <div class="health-row">
      <span
        class="health-badge"
        :class="{ ok: healthStatus === 'ok', fail: healthStatus === 'error' }"
        data-testid="health-status"
      >
        API: {{ healthLabel }}
      </span>
    </div>

    <div class="panels">
      <!-- Sidebar: sessions -->
      <aside class="sidebar" aria-label="Session management">
        <h2>Sessions</h2>

        <label for="user-id-input">User ID</label>
        <input
          id="user-id-input"
          v-model="userId"
          type="text"
          data-testid="user-id-input"
          aria-label="User ID"
          @change="onUserIdChange"
        />

        <button
          type="button"
          class="btn primary"
          data-testid="new-session-btn"
          :disabled="loading"
          @click="onNewSession"
        >
          New Session
        </button>

        <ul
          v-if="sessions.length"
          class="session-list"
          data-testid="session-list"
        >
          <li
            v-for="session in sessions"
            :key="session.id"
            :data-testid="`session-item-${session.id}`"
            :class="{ active: session.id === activeSessionId }"
            @click="selectSession(session.id)"
          >
            <strong>{{ session.title }}</strong>
            <small>{{ formatDate(session.last_activity_at) }}</small>
          </li>
        </ul>
        <p v-else class="empty-hint">No sessions yet. Create one to start learning.</p>
      </aside>

      <!-- Chat panel -->
      <section class="chat-panel" aria-label="Chat">
        <h2>Chat</h2>

        <div v-if="!activeSessionId" class="empty-hint" data-testid="no-session-hint">
          Select or create a session to start chatting.
        </div>

        <template v-else>
          <div
            class="message-list"
            data-testid="message-list"
            aria-live="polite"
          >
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="message"
              :class="msg.role"
              :data-testid="msg.role === 'assistant' ? 'assistant-message' : 'user-message'"
            >
              <span class="role">{{ msg.role }}</span>
              <p>{{ msg.content }}</p>
            </div>
            <div v-if="loading" class="loading" data-testid="chat-loading">
              Loading…
            </div>
          </div>

          <form class="message-form" @submit.prevent="onSendMessage">
            <label for="message-input">Your message</label>
            <textarea
              id="message-input"
              v-model="messageInput"
              rows="3"
              data-testid="message-input"
              aria-label="Message input"
              :disabled="loading"
              placeholder="Ask a question about your course material…"
            />
            <button
              type="submit"
              class="btn primary"
              data-testid="send-message-btn"
              :disabled="loading || !messageInput.trim()"
            >
              Send
            </button>
          </form>
        </template>
      </section>

      <!-- Quiz panel -->
      <section class="quiz-panel" aria-label="Quiz">
        <h2>Quiz</h2>

        <div v-if="!activeSessionId" class="empty-hint">
          Select a session to generate a quiz.
        </div>

        <template v-else>
          <form class="quiz-form" @submit.prevent="onGenerateQuiz">
            <label for="quiz-topic-input">Topic</label>
            <input
              id="quiz-topic-input"
              v-model="quizTopic"
              type="text"
              data-testid="quiz-topic-input"
              aria-label="Quiz topic"
              :disabled="loading"
              placeholder="e.g. Software Testing"
            />
            <button
              type="submit"
              class="btn secondary"
              data-testid="generate-quiz-btn"
              :disabled="loading || !quizTopic.trim()"
            >
              Generate Quiz
            </button>
          </form>

          <div v-if="quizItems.length" class="quiz-questions">
            <div
              v-for="(item, index) in quizItems"
              :key="item.id"
              class="quiz-item"
            >
              <p class="quiz-question" data-testid="quiz-question">
                {{ item.question }}
              </p>
              <fieldset>
                <legend class="sr-only">Answer options</legend>
                <label
                  v-for="(option, optIndex) in item.options"
                  :key="optIndex"
                  class="quiz-option"
                  :data-testid="`quiz-option-${optIndex}`"
                >
                  <input
                    v-model="selectedAnswers[item.id]"
                    type="radio"
                    :name="`quiz-${item.id}`"
                    :value="option"
                    :disabled="loading"
                  />
                  {{ option }}
                </label>
              </fieldset>
              <button
                type="button"
                class="btn primary"
                data-testid="submit-answer-btn"
                :disabled="loading || !selectedAnswers[item.id]"
                @click="onSubmitAnswer(item)"
              >
                Submit Answer
              </button>
            </div>
          </div>

          <div
            v-if="quizFeedback"
            class="quiz-feedback"
            :class="{ correct: quizFeedback.is_correct, incorrect: !quizFeedback.is_correct }"
            data-testid="quiz-feedback"
            role="status"
          >
            {{ quizFeedback.feedback }}
          </div>
        </template>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import * as api from '../api/esbot.js'
import { useSession } from '../composables/useSession.js'

const {
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
} = useSession()

const healthStatus = ref('checking')
const healthLabel = ref('checking…')
const messageInput = ref('')
const quizTopic = ref('')
const quizItems = ref([])
const selectedAnswers = ref({})
const quizFeedback = ref(null)

onMounted(async () => {
  await checkHealth()
  await loadSessions()
})

async function checkHealth() {
  try {
    const data = await api.getHealth()
    healthStatus.value = data.status === 'ok' ? 'ok' : 'error'
    healthLabel.value = data.status === 'ok' ? 'connected' : data.status
  } catch {
    healthStatus.value = 'error'
    healthLabel.value = 'unreachable'
  }
}

async function onUserIdChange() {
  activeSessionId.value = null
  messages.value = []
  quizItems.value = []
  quizFeedback.value = null
  await loadSessions()
}

async function onNewSession() {
  quizItems.value = []
  quizFeedback.value = null
  selectedAnswers.value = {}
  await createNewSession()
}

async function onSendMessage() {
  const content = messageInput.value.trim()
  if (!content) return
  const result = await sendChatMessage(content)
  if (result) {
    messageInput.value = ''
  }
}

async function onGenerateQuiz() {
  if (!activeSessionId.value) return
  clearError()
  quizFeedback.value = null
  loading.value = true
  try {
    const data = await api.generateQuiz(activeSessionId.value, quizTopic.value.trim(), 1)
    quizItems.value = data.items
    selectedAnswers.value = {}
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function onSubmitAnswer(item) {
  if (!activeSessionId.value) return
  const answer = selectedAnswers.value[item.id]
  if (!answer) return
  clearError()
  loading.value = true
  try {
    quizFeedback.value = await api.submitQuizAnswer(activeSessionId.value, item.id, answer)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleString()
}
</script>

<style scoped>
.chat-layout {
  max-width: 1400px;
  margin: 0 auto;
}

.error-banner {
  background: #fde8e8;
  color: #9b1c1c;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-banner button {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: inherit;
}

.health-row {
  margin-bottom: 0.75rem;
}

.health-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  background: #e2e8f0;
}

.health-badge.ok {
  background: #d1fae5;
  color: #065f46;
}

.health-badge.fail {
  background: #fee2e2;
  color: #991b1b;
}

.panels {
  display: grid;
  grid-template-columns: 240px 1fr 300px;
  gap: 1rem;
  min-height: 500px;
}

.sidebar,
.chat-panel,
.quiz-panel {
  background: #fff;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h2 {
  margin: 0 0 0.75rem;
  font-size: 1.1rem;
}

label {
  display: block;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
  color: #4a5568;
}

input[type='text'],
textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.btn {
  display: inline-block;
  padding: 0.45rem 0.9rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  margin-bottom: 0.75rem;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.primary {
  background: #0a7ea4;
  color: #fff;
}

.btn.secondary {
  background: #4a5568;
  color: #fff;
}

.session-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.session-list li {
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 0.25rem;
  border: 1px solid transparent;
}

.session-list li:hover {
  background: #f7fafc;
}

.session-list li.active {
  background: #e6f4f8;
  border-color: #0a7ea4;
}

.session-list small {
  display: block;
  color: #718096;
  font-size: 0.75rem;
}

.message-list {
  min-height: 280px;
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 0.75rem;
  padding: 0.5rem;
  background: #f7fafc;
  border-radius: 6px;
}

.message {
  margin-bottom: 0.75rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  max-width: 85%;
}

.message.user {
  background: #dbeafe;
  margin-left: auto;
}

.message.assistant {
  background: #e2e8f0;
}

.message .role {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: #718096;
  display: block;
  margin-bottom: 0.15rem;
}

.message p {
  margin: 0;
  white-space: pre-wrap;
}

.loading {
  text-align: center;
  color: #718096;
  font-style: italic;
}

.message-form {
  display: flex;
  flex-direction: column;
}

.quiz-form {
  margin-bottom: 1rem;
}

.quiz-item {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f7fafc;
  border-radius: 6px;
}

.quiz-question {
  font-weight: 600;
  margin: 0 0 0.5rem;
}

.quiz-option {
  display: block;
  padding: 0.25rem 0;
  cursor: pointer;
}

.quiz-feedback {
  margin-top: 0.75rem;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

.quiz-feedback.correct {
  background: #d1fae5;
  color: #065f46;
}

.quiz-feedback.incorrect {
  background: #fee2e2;
  color: #991b1b;
}

.empty-hint {
  color: #718096;
  font-size: 0.9rem;
  font-style: italic;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

@media (max-width: 900px) {
  .panels {
    grid-template-columns: 1fr;
  }
}
</style>
