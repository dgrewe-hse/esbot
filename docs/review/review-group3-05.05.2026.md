# Review template (inspection / technical review)

**Project / product:** ESBot

**Review object(s):** System description, specification (spec.md), data model, initial implementation (entities, tests) from main branch

**Review type:** Walkthrough characteristics

**Date (planned / actual):** 2026-05-05 / 2026-05-05

**Moderator:** Thomas Barbet

**Author(s):** Team 3 (reviewed team)

**Reviewers:** Kevin Schmidhäusler, Armanbir Singh, Konrad Harnisch-John

---

## 2. Master Plan (MP)

### 2.1 Masterplan — header

| Field | Value |
| --- | --- |
| Review No. | REV-2026-ESBOT-01 |
| Project | ESBot |
| Project manager | Sandro Lipinski (Team 3) |
| Quality expert / manager | —   |
| Moderator | Thomas Barbet |
| Author(s) | Team 3 |

---

### 2.2 Review objects

| #   | Review objects | Abbr. |
| --- | --- | --- |
| 1   | docs/esbot.md / system description | SYS |
| 2   | docs/spec/spec.md (API & requirements) | SPEC |
| 3   | data_model.md + backend entities | DM  |
| 4   | ESBot/../*.java | LOC |

---

### 2.3 Reference documents

| #   | Reference documents | Abbr. |
| --- | --- | --- |
| 1   | docs/esbot.md | EB  |
| 2   | docs/spec/requirements.md | REQ |
| 3   | Lecture materials (reviews & ESBot) | LEC |

---

### 2.4 Checklists / scenarios

| #   | Checklists / scenarios |
| --- | --- |
| 1   | Requirements completeness & consistency checklist |
| 2   | API design & REST compliance checks |
| 3   | Data model consistency & entity mapping |
| 4   | Naming conventions & code quality |

---

### 2.5 Reviewer assignment

| Reviewer | Names (and chapters / checklists or scenarios assigned to the review) | Abbr. |
| --- | --- | --- |
| 1   | Kevin Schmidhäusler: API & specification | R1  |
| 2   | Konrad Harnisch-John: data model & entities | R2  |
| 3   | Armanbir Singh: – architecture & system overview | R3  |

---

### 2.6 Kick-off

| Date / time / location |
| --- |
| 2026-05-05 17:00 CET, Discord |

---

### 2.7 Individual preparation

| Individual preparation | Value | Unit |
| --- | --- | --- |
| Submission of findings by | during meeting | —   |
| Size of review objects | 3-5 pages documentation + code excerpts | pages |
| Optimal inspection rate | —   | —   |
| Optimal inspection time | 0.75 | h   |

---

### 2.8 Review meeting

| Date / time / location |
| --- |
| 2026-05-05 18:00–18:45 CET, Discord |

---

### 2.9 Additional milestones (optional)

| Milestone | Planned date / time | Actual date / time |
| --- | --- | --- |
| End of individual preparation | 2026-05-05 | 2026-05-05 |
| Rework deadline | —   | —   |
| Follow-up / closure | —   | —   |

---

## 3. List of findings (LoF)

| ID  | Location (file / section / module) | Summary | Type | Severity | Status | Owner | Notes / meeting decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F-001 | SPEC | No API implementation available | Question | Minor | Open | Team 3 | API only described, not implemented |
| F-002 | SPEC | spec.md is not a proper OpenAPI specification | Defect | Minor | Open | Team 3 | likely copied, not standard-compliant |
| F-003 | DM  | Inconsistent naming conventions | Defect | Minor | Open | Team 3 | camelCase, snake_case mixed |
| F-004 | DM  | Unclear ID strategy (MessageId, FileId) | Question | Minor | Open | Team 3 | no justification provided |
| F-005 | DM  | sessionId to session_id mapping potentially incorrect | Defect | Major | Open | Team 3 | may cause join issues |
| F-006 | SYS | Architecture only superficially defined (“modular”) | Suggestion | Minor | Open | Team 3 | lacks detail |
| F-007 | SPEC | No proper authentication (only URL hash) | Defect | Major | Open | Team 3 | security concern |
| F-008 | DM  | Field sizes (255 / 4096) lack clear justification | Question | Minor | Open | Team 3 | unclear reasoning |
| F-009 | DM  | Files not clearly linked to messages | Defect | Major | Open | Team 3 | data inconsistency |
| F-010 | SYS | No clear connection between main, DB, and entities | Defect | Major | Open | Team 3 | system integration unclear |
| F-011 | CODE | Cascade delete may be risky | Suggestion | Minor | Open | Team 3 | potential unintended data loss |
| F-012 | CODE | FetchType.LAZY not documented | Suggestion | Minor | Open | Team 3 | unclear for maintainers |

---

## 4. Data Summary (DS)

| Metric | Value | Notes |
| --- | --- | --- |
| Size of review object | ~3-5 pages + code | estimated |
| Preparation effort (hours, optional) | ~0.5 h per reviewer | limited preparation |
| Number of findings (initial) | 12  |     |
| Number of findings after meeting | 12  |     |
| Rework effort (hours, author) | —   | not assessed |
| Re-inspection required? | No  | but recommended |

---

## 5. Review Report (RR)

### 5.1 Summary

This technical review analyzed another team’s ESBot project, focusing on system description, specification, and data model.
Due to limited access to the repository prior to the meeting, the review was conducted as an interactive discussion with one team member.

Several structural and conceptual weaknesses were identified, particularly in API design, consistency, and system integration.

---

### 5.2 Review outcome

- **Review object state after review:** Accepted with major changes required
  
- **Major risks or themes:**
  
  - Missing API implementation
  - Inconsistent data modeling
  - Unclear architecture
  - Security issues (authentication)

---

### 5.3 Decisions and follow-up

| Topic | Decision | Responsible | Due date |
| --- | --- | --- | --- |
| API specification | Use proper OpenAPI standard | Team 3 | —   |
| Naming conventions | Define and enforce consistency | Team 3 | —   |
| Data model | Refine and document structure | Team 3 | —   |
| Authentication | Redesign authentication approach | Team 3 | —   |

---

### 5.4 Positive observations (optional)

- Clear high-level architecture (Angular → Spring → Postgres)
- Use of established technologies (Spring Boot)
- Consideration of performance (lazy loading)
- Focus on simplicity and reduced complexity

---

### 5.5 Lessons learned (optional)

- Early access to the repository is essential for proper preparation
- Better planning would significantly improve review quality
- A structured checklist would increase efficiency

---

### 5.6 Sign-off

| Role | Name | Signature / date |
| --- | --- | --- |
| Moderator | Konrad Harnisch-John | 2026-05-05 |
| Author | Team 3 | 2026-05-05 |
