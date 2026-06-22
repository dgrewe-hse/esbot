# ESBot – Specification (Specification Driven Development)

## 1. Goals

- Support students in learning
- Provide AI-based explanations
- Enable practice through quizzes

---

## 2. User Journey

1. User opens application
2. User asks a question
3. System processes input
4. AI generates response
5. Response is displayed
6. Interaction is stored

---

## 3. System Architecture

- Frontend: Chat interface (React)
- Backend: API and logic (FastAPI, Python)
- Database: Stores sessions (PostgreSQL)
- AI Layer: LLM integration (LangChain)

---

## 4. Constraints

- Must integrate LLM
- Must store conversation history
- Must support multiple users

---

## 5. Tasks

- Implement UI
- Implement API
- Connect AI model
- Store data
- Implement tests
