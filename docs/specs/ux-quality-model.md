# UX Quality Model
## 1 Clartity / Comprehensibility 
### Quality Characteristic(s)
- Usability
- Functional suitability
- Performance efficiency
- Reliability 

### Measureable quality criterion
- All requirements are met. 
- Users should not search longer than **5 seconds** for the prompt input field after opening the chatbot.
- Every button in the UI has a fitting and clear name.
- The same actions always produce the same results.

### Verification Method (Test)
- Manual comparison of requirements and chatbot functionalities is used. 
- UI will have system test which simulate a user, to get to exprected page results.
- Must be tested with real students at least 5.

## 2 Feedback quality
### Quality Characteristic(s)
- Usability
- Functional Suitability 


### Measureable quality criterion
Quality of feedback: The majority of responses (≥90%) contain technically meaningful and correct explanations, including justifications and further information.
Learning success after feedback: Improvement in user performance following AI feedback. Users complete subsequent tasks of the same type with a lower error rate than before.

### Verification Method (Test)
- Analysis of the content of several AI responses regarding their quality.
- Testing with users: 
    - 1. User solves tasks without AI assistance (measurement of correct answers). 
    - 2. The user receives AI assistance. 
    - 3. The user solves further tasks (measurement of correct answers).
    - 4. Caluclate the diffrence in test score before and after the usage of ESBot

## 3 Usability
### Quality Characteristic(s)
- Usability
- Functional Suitability

### Measureable quality criterion
-  Feature list must be fully fullfilled
- A  User should be able to make a question without navigating (exept logging in).

### Verification Method (Test)
- All features must have a End-to-End test which proves there functionality.
- (Except Login in) no redirects before first question.


## 4 Efficency
### Quality Characteristic(s)
- Performance Efficiency
- Reliability

### Measureable quality criterion
- Prompt Minimization: At least 40% of user interactions during a practice session (Quizzes/Exercises) should be completable via "Quick Action" buttons or suggestion chips rather than manual text entry.
- Onboarding Velocity: A first-time user must be able to receive their first AI-generated explanation within 30 seconds of landing on the application.


### Verification Method (Test)
- Analytics Tracking: Implement event logging to calculate the ratio of button_click events vs. text_submit events.
- First-Click Testing: Conduct an unmoderated usability study with 10 participants to measure "Time to First Prompt."

## 5 Trustability / Transperity
### Quality Characteristic(s)
- Usability
- Functional suitability
- Reliability

### Measureable quality criterion
- ≥ 90% of responses include either a clear explanation of reasoning steps or at least one verifiable source when factual claims are made
- ≥ 90% of cited sources are valid, accessible, and relevant to the answer

### Verification Method (Test)
- Conduct a systematic review of a sample of AI responses (e.g., 100 outputs) and check for presence of explanations/sources
- Validate sources manually or automatically (e.g., do links work, do they support the claim?)
- Perform a user study with CS students where they rate perceived trust, and correlate results with presence of explanations/sources
(Maybe Second AI which just tests correctness)

`Grammtic,translation and text structure improvements with ChatGPT Version 5.3 (03.04.2026 11:50)`