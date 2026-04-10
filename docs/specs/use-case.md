# Diagram

UC : Use Case

``` mermaid
flowchart TB
    %% External Actors
    Student((Student))
    DB[(Database / Tier 3)]
    LLM[LLM Inference Engine]

    subgraph Tier1 [Tier 1: Frontend]
        UI[Web / Mobile Interface]
    end

    subgraph Tier2 [Tier 2: Application Backend]
        direction TB
        Auth[Session Manager]
        PromptEng[Prompt Generator]
        
        subgraph Logic [Functional Use Cases]
            UC1(UC1: Ask Learning Question)
            UC2(UC2: Generate Practice Quiz)
            UC3(UC3: Submit Quiz Answers)
            UC4(UC4: View Learning History)
            UC5(UC5: Provide Contextual Feedback)
        end
    end

    %% Flow of Data
    Student <-->|HTTPS/REST| UI
    UI <-->|API Requests| Auth
    
    %% Internal Logic Mapping
    Auth --> Logic
    UC1 & UC2 & UC5 --> PromptEng
    
    %% External System Integration
    PromptEng <-->|JSON Prompt/Response| LLM
    Logic <-->|SQL/Queries to store and retrieve Logs| DB
    
    %% Relationships
    UC2 -.->|requests| UC3
    UC3 -.->|trigger| UC5


```

# Use Case: Ask Learning Question

### Name
**Ask Question**

### Summary
The User submits a natural language query regarding course material to the ESBot. The system processes the request via an LLM and provides a contextualized explanation to support the student's learning process.

### Actor
Student (User)

### Triggering Event
The User types a question into the chat interface and presses "Send."

### Inputs
* User’s text query (string).
* Current Session ID (to maintain context).

### Pre-Conditions
* The User has accessed the Web UI.
* The Backend and LLM Inference Engine are online.

### Process Description
1. The UI sends the question and Session ID to the Backend API.
2. The Backend retrieves previous interaction history from the Database for context.
3. The Backend constructs a prompt and sends it to the LLM Inference Engine.
4. The LLM generates a response and returns it to the Backend.
5. The Backend saves the question and the response to the Database.
6. The UI displays the response to the User.

### Exceptions
* **LLM Timeout:** If the LLM does not respond within 5 seconds, the system displays a "Service busy" message.
* **Database Error:** If the interaction cannot be saved, the UI warns the user that progress is not being tracked.

### Outputs and Post-Conditions
* **Output:** A structured AI-generated explanation.
* **Post-Condition:** The interaction is persistently stored in the Database; the UI state is updated.

# Use Case: Generate Practice Quiz

### Name
**Generate Quiz**

### Summary
The User requests a practice quiz on a specific topic. The system uses the AI engine to create a set of questions and displays them in the interface for the user to solve.

### Actor
Student (User)

### Triggering Event
The User clicks the "Generate Practice Quiz" button or types a request for a quiz.

### Inputs
* Target Topic (string).
* Difficulty level or number of questions (optional).

### Pre-Conditions
* A valid session is active.

### Process Description
1. The Backend sends a specialized "Quiz Generation" prompt to the LLM.
2. The LLM returns a structured set of questions (and internal answers for evaluation).
3. The Backend parses the AI output into a quiz format.
4. The Backend stores the quiz metadata in the Database.
5. The UI renders the quiz questions as interactive elements.

### Exceptions
* **Invalid Topic:** If the topic is outside the course scope, the system asks the user to choose a relevant subject.
* **Formatting Error:** If the LLM returns unstructured text instead of a quiz format, the Backend triggers a "Regenerate" request.

### Outputs and Post-Conditions
* **Output:** A list of interactive practice questions.
* **Post-Condition:** The system enters "Quiz Mode" for the current session.

# Use Case: View Learning History

### Name
**Retrieve History**

### Summary
The User revisits the application to continue learning. The system fetches and displays previous conversations and quiz results to ensure continuity and track progress.

### Actor
Student (User)

### Triggering Event
The User opens the ESBot application or selects a specific past session from a sidebar.

### Inputs
* User ID or Session ID.

### Pre-Conditions
* The User has interacted with the system previously (data exists in Tier 3).

### Process Description
1. The UI requests session logs for the User ID from the Backend.
2. The Backend queries the Database for all messages and logs associated with that ID.
3. The Database returns the chronological message history.
4. The Backend sends the structured history back to the UI.
5. The UI renders the past chat bubbles and results in the main view.

### Exceptions
* **No Data Found:** The system displays a "Welcome! Start your first session" message.

### Outputs and Post-Conditions
* **Output:** A chronologically ordered display of past interactions.
* **Post-Condition:** The current conversational state is synchronized with the last known interaction in the Database.

`Grammtic and sorting improvements with ChatGPT Version 5.3 (27.03.2026 15:45)`