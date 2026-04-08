# UX Evaluation Plan and Acceptance Criteria

## 1. Evaluation Scope
The scope defines which UX factors and user journeys are tested to validate that ESBot delivers a high-quality learning experience.

* **UX Factors Tested:**
    * Clarity & Comprehensibility
    * Feedback Quality
    * Trust & Transparency
    * Learnability
    * Error Tolerance
* **Key User Journeys:**
    * **The "Guided Start":** Evaluation of whether Quick-Start suggestions make system capabilities immediately recognizable.
    * **The "Deep Dive":** Verification that responses follow the required structure (Definition → Importance → Example).
    * **The "Quiz Remediation":** Assessment of the pedagogical quality of feedback after incorrect answers.
    * **The "Stress Test":** Evaluation of system behavior when handling vague or invalid inputs.
      
**Verification Approach**
Each journey is tested against predefined UX criteria and expected interaction patterns

## 2. Method Set
To ensure results are testable and reviewable, a hybrid approach is used:

* **Heuristic Evaluation (Internal):** Review of the interface based on predefined templates and ISO 9241-110 principles.
* **Think-Aloud Sessions (User-centric):** Users verbalize their thoughts while completing tasks to identify usability and cognitive load issues.
* **Automated Contract Testing:** Validation that system outputs conform to defined structural and architectural constraints (e.g., response format, source references).

**Verification Method**
Each method produces measurable or reviewable results, allowing classification into pass/fail or qualitative ratings

## 3. Participants and Setup
* **Participants:** at least 4 students representing the target user group.
* **Setup:** * **Environment:** Standardized Docker-based staging system (Frontend, Backend, Database).
    * **Duration:** 30–45 minutes per session.
    * **Materials:** Pre-defined task scenarios, screen recording software, and a post-session questionnaire (e.g., UEQ or AttrakDiff).

## 4. Metrics and Acceptance Criteria
These criteria define the measurable thresholds that must be met for a successful release.

| UX Factor | ISO 25010 Mapping | Quality Criterion | Verification Method |
| :--- | :--- | :--- | :--- | 
| **Clarity** | Usability (Appropriateness Recognizability) | Responses follow the structured template (Definition → Importance → Example). | Automated structure validation (Pass/Fail) |
| **Feedback** | Functional Suitability (Functional Correctness) | Feedback explains incorrect answers and provides correct reasoning. | Template comparison (qualitative scale) |
| **Trust** | Reliability (Maturity), Security (Integrity) | Responses include source references or indicate uncertainty. | Presence check (Pass/Fail) |
| **Learnability** | Usability (Learnability) | Users recognize and use Quick-Start features within a short time. | Observation & usage tracking |
| **Error Tol.** | Reliability (Fault Tolerance) | System provides meaningful fallback responses instead of errors. | Comparison with fallback templates |

**Acceptance Tresholds**
* 100% template adherence for structured responses
* 100% explanatory feedback for incorrect answers
* ≥ 95% transparency (source or uncertainty indication)
* ≥ 80% Quick-Start usage within 60 seconds
* 100% user-friendly fallback handling
  
## 5. Findings Documentation

* **ID:** `ESB-UX-[Number]`
* **Factor:** (e.g., Trust & Transparency)
* **ISO 25010 Mapping:** (e.g., Reliability)
* **Description:** Clear explanation of the observed issue.
* **Severity:**
    * **Critical:** System crash or critical misinformation (Blocks Release).
    * **High:** Major obstacle in a core user journey (Blocks Release).
    * **Medium/Low:** Minor layout or friction issue (Sprint Backlog).
* **Evidence:** Screenshot, Log-ID, or Video Timestamp.
* **Recommendation:** Specific technical or design fix (e.g., "Refine LangChain prompt").

## 6. Quality Gate Proposal
The UX Evaluation results act as a mandatory gate in the deployment pipeline.

* **BLOCK Release if:**
    * Any **Critical** or **High** severity findings remain unresolved.
    * The **Clarity** automated check fails (Template mismatch).
    * **Trust** metrics fall below the 95% threshold (Risk of exam-prep failure).
* **PASS Release if:**
    * All thresholds in Section 4 are verified as "Met".
    * All remaining findings are documented as "Medium/Low" with an assigned developer recommendation.
