## ESBot Compact UX Evaluation Plan

### 1. Evaluation Scope
* **UX Factors to Test**:
    * **Clarity / Comprehensibility**: Can users find the prompt bar and navigate without friction?
    * **Feedback Quality**: Is the AI's content pedagogically sound and accurate?
    * **Usability**: Are all functional features accessible without unnecessary redirects?
    * **Efficiency**: Can users complete tasks quickly via quick actions/chips?
    * **Trustability / Transparency**: Does the AI properly explain its reasoning or cite sources?
* **User Journeys to Evaluate**:
    * *Journey A*: Asking a learning question and understanding the AI response.
    * *Journey B*: Requesting, completing, and reviewing a generated practice quiz.
    * *Journey C*: Returning to the app to find and review previous chat history.

### 2. Method Set
To balance deep user insights with fast execution, we will use a hybrid approach of expert evaluation and user testing:

* **Heuristic Evaluation (Internal)**: Team members (QA or Design Manager) will evaluate the UI against *Nielsen's 10 Usability Heuristics* and the ESBot Constitution.
* **Scenario-Based Think-Aloud Sessions (External)**: Direct observation of real target users attempting to complete tasks while speaking their thought process aloud.

### 3. Participants and Setup
Since computer science students are the target audience and are highly critical of poor chat UI, testing must reflect this demographic.

* **Participants**: ≥5 CS students not involved in the project development (as 5 users typically find 80% of usability issues).
* **Duration**: 30 minutes per session (15 mins testing + 15 mins post-test interview).
* **Materials**:
    * A running test instance of the full ESBot Application.
    * A set of 3 written task scenarios (e.g., *"Ask ESBot to explain 'polymorphism' and see if it gives you an example"*).
    * Screen and audio recording setup (consent required).

### 4. Metrics and Acceptance Criteria
Aligned with the ISO/IEC 25010-based quality requirements and the ESBot Constitution's performance expectations:

| Metric | Measurement Method | Acceptance Criterion | ISO 25010 Mapping |
| --- | --- | --- | --- |
| **Time to Prompt** | Stop-watch / Analytics | < 5 seconds to locate input on landing. | Usability (Learnability) |
| **Time to First Explanation** | Stop-watch / Analytics | < 30 seconds for first-time users. | Performance Efficiency |
| **Quick Action Ratio** | Event logging | ≥ 40% of quiz interactions done via buttons instead of typing. | Usability (Operability) |
| **AI Transparency Score** | Post-test review of outputs | ≥ 90% of factual responses have logic steps or valid sources. | Reliability / Trust |
| **Task Success Rate** | Observation | ≥ 80% of tasks completed without moderator intervention. | Functional Suitability |

### 5. Findings Template
All UX issues found during Heuristic and Think-Aloud evaluations will be logged in this format in your issue tracker:

| Field | Description | Example |
| --- | --- | --- |
| **Issue ID** | UX-XXX | UX-004 |
| **Description** | Clear summary of the problem. | Users couldn't find the quiz evaluation feedback. |
| **Severity** | Critical / High / Medium / Low | **High** |
| **Evidence** | Direct quote or recorded timestamp. | *"User 2 spent 45 seconds clicking on the prompt bar instead of hitting the submit button."* |
| **Recommendation**| Actionable fix aligned with the Constitution. | Make the feedback section auto-expand after quiz submission. |

> **Severity Scale Guide**:
> * **Critical**: User cannot complete the task (e.g., cannot submit a message).
> * **High**: Severe frustration or long delays (e.g., cannot find the history sidebar).
> * **Medium**: Minor friction, but task completion is possible.
> * **Low**: Purely cosmetic issues.

### 6. Quality Gate Proposal (UX Release Blocker)
To uphold the **Comprehensive Testing** and **Learning-Centered Design** principles of the ESBot Constitution, UX evaluation findings will act as a strict quality gate:

1.  **Zero Critical/High UX Issues**: No release to staging or production may occur if there are open Critical or High severity UX issues.
2.  **Metric Compliance**: If the "Time to First Prompt" exceeds 30 seconds or the AI fails to provide reasoning/sources in ≥ 90% of sampled responses, the release is blocked.
3.  **Exception Handling**: If a fallback response (due to LLM timeout) fails to instruct the user on what to do next (violating the Graceful AI Degradation principle), it is treated as a High severity issue.

`Grammtic, translation and text structure improvements with ChatGPT Version 5.3 (03.04.2026 12:20)`