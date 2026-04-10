## Quality Model according to ISO 25010: ESBot

### 1. Selection of Quality Characteristics (Top 4)

#### 1.1 Functional Suitability
* **Definition:** The degree to which the system provides functions that meet stated requirements (learning support, quiz generation).
* **Relevance for ESBot:** As an educational tool, it is crucial that the AI does not just "respond" but provides didactically valuable explanations and ensures that exercises (FR-3) actually align with the course content.

#### 1.2 Performance Efficiency
* **Definition:** Performance relative to the amount of resources used under stated conditions.
* **Relevance for ESBot:** AI inference is resource-intensive. Despite the inherent latency of Large Language Models (LLMs), the system must enable fluid interaction (NFR-2) so that the students' learning flow is not interrupted.

#### 1.3 Usability
* **Definition:** The degree to which a product can be used by specified users to achieve specified goals with effectiveness and satisfaction.
* **Relevance for ESBot:** Since the system must function without prior training (NFR-1), the interface must be self-explanatory. A complicated chat experience would hinder the primary objective: learning.

#### 1.4 Maintainability – Focus: Testability
* **Definition:** The ease with which a system can be modified to correct defects or implement new requirements.
* **Relevance for ESBot:** In the context of this course, **testability** (a sub-characteristic of maintainability) is central. The system must be modular enough to allow the non-deterministic component (the AI) to be tested in isolation.

---

### 2. Documentation of Quality Models (Metrics & Goals)

| Quality Characteristic | Quality Goal (Measurable) | Method / Metric |
| :--- | :--- | :--- |
| **Functional Suitability** | Correctness of quiz logic | Percentage of correctly evaluated user answers (FR-4) via expert review > 90%. |
| **Performance Efficiency** | Response latency under load | Time to First Token (TTFT) < 2–5 seconds with 50 concurrent users. |
| **Usability** | Learnability | "Time-to-first-prompt": A new user submits their first subject-related question in < 30 seconds after login. |
| **Maintainability** | Logic testability | 100% of backend interfaces (APIs) are coverable by automated tests (mocking capability). |

---

### 3. Measures to Ensure Testability

To guarantee **testability** during the development of ESBot, we propose the following specific measures:

#### A. Decoupling via Adapter Pattern
AI inference (Ollama/vLLM) should be accessed through an adapter. This allows the use of a "stub adapter" during testing, which returns predefined text. This enables backend testing without relying on expensive or slow AI calls.

#### B. Structuring AI Responses (Schema Validation)
Since AI output is often unpredictable, ESBot should force the AI to provide responses (especially for quiz questions) in a structured format such as JSON.
* **Measure:** Automated tests validate the output against a JSON schema. This significantly increases the testability of "Answer Evaluation" (FR-4).

#### C. Containerization for Integration Tests
To ensure every developer and the CI (Continuous Integration) pipeline share the same environment, the entire system (UI, Backend, DB) will be deployed in Docker containers.
* **Measure:** Integration tests can use scripts to spin up a clean test database and tear it down after completion.

#### D. Logging & Tracing for Troubleshooting
To identify errors within the "User -> Backend -> AI -> User" chain, every step must be logged.
* **Measure:** Implementation of detailed logs that show exactly which prompt was sent to the AI. This is essential for distinguishing AI "hallucinations" from bugs in the backend code.

`Grammtic,translation and sorting improvements with ChatGPT Version 5.3 (27.03.2026 15:45)``
