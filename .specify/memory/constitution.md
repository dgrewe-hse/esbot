<!--
  Sync Impact Report - ESBot Constitution v1.0.0
  =============================================
  Version change: N/A → 1.0.0 (Initial Creation)
  
  Modified principles: None (all new)
  Added sections:
    - Core Principles (5 principles derived from ESBot requirements)
    - Technology Stack
    - Development Workflow
    - Governance
  
  Removed sections: None
  
  Templates requiring updates:
    ✅ .specify/templates/plan-template.md - Constitution Check section already exists
    ✅ .specify/templates/spec-template.md - Already aligned with user stories + requirements format
    ⚠ .specify/templates/tasks-template.md - Does not exist yet (pending creation)
    ✅ No command templates exist (no updates needed)
  
  Follow-up TODOs:
    - TODO(TEAM_ROLES): Consider formalizing team role definitions in a separate document
    - TODO(AI_INTEGRATION): Document LLM integration strategy when AI features are implemented
-->

# ESBot Constitution

## Core Principles

### I. Learning-Centered Design

The system MUST prioritize student learning outcomes above all other design considerations. Every feature must support, enhance, or enable effective learning interactions. The system shall facilitate active engagement rather than passive information consumption, guiding users through structured learning experiences that encourage practice and feedback. Responses and interactions MUST be pedagogically structured to maximize educational value.

**Rationale**: ESBot is fundamentally an educational tool; without learning-centered design, it loses its core purpose.

### II. Modular Layered Architecture

The system MUST follow a strict three-tier architecture with clear separation of concerns:
- **Tier 1 (UI)**: Angular-based web frontend handling user interaction
- **Tier 2 (Backend)**: .NET (C#) application handling business logic and API
- **Tier 3 (Database)**: PostgreSQL for persistent storage of sessions and messages

AI inference components MUST be isolated as a separate service layer that can be independently replaced, mocked, or disabled. Each layer MUST be independently testable and deployable.

**Rationale**: Modular architecture ensures maintainability, testability, and extensibility. Clear boundaries enable independent development and testing of each component.

### III. Comprehensive Testing (NON-NEGOTIABLE)

The system MUST support testing across all layers with the following mandatory requirements:
- **Unit Tests**: Every module/function MUST have unit tests achieving >80% code coverage
- **Integration Tests**: API endpoints and database interactions MUST be integration tested
- **System Tests**: End-to-end user journeys MUST be tested including session flows
- **AI Mocking**: AI inference components MUST be fully mockable for deterministic testing

Tests MUST be executable in CI/CD pipelines. All new features MUST include tests before merge.

**Rationale**: AI-integrated systems have inherent non-determinism. Comprehensive mocking and testing at all layers ensures reliability and enables confident refactoring.

### IV. Observability & Structured Logging

The system MUST provide comprehensive logging and monitoring capabilities:
- All API requests MUST be logged with request ID, user ID, timestamp, and response time
- All AI inference calls MUST be logged with prompts, model info, and response metadata
- Errors and exceptions MUST include stack traces and context for debugging
- Response times MUST be tracked to verify performance requirements (2-5 second SLA)
- Session state changes MUST be traceable for debugging learning continuity issues

**Rationale**: Observability is essential for debugging AI behavior, monitoring system health, and ensuring the learning experience meets performance expectations.

### V. Graceful AI Degradation

The system MUST handle AI service failures and non-deterministic outputs gracefully:
- When AI services are unavailable, the system MUST provide meaningful fallback responses
- The system MUST NEVER expose raw AI errors to end users
- Timeout handling for AI requests MUST be implemented (recommended: 10 second max)
- AI responses MUST be validated for format and basic safety before presentation
- Fallback responses MUST be logged for later review and improvement

**Rationale**: AI services can fail or be slow. Students must always receive helpful responses; system reliability is paramount for educational contexts.

## Technology Stack

The following technology choices have been ratified for ESBot:

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Frontend (UI) | Angular | Team experience; cross-platform web access |
| Backend | .NET (C#) | Team experience; load balancing and caching expertise |
| Database | PostgreSQL | Team experience; existing server infrastructure |
| AI Inference | Optional (Ollama/vLLM/LM Studio) | Currently deferred to avoid costs |

**Constraint**: Any deviation from this stack MUST be justified in a technical document and approved by the Design Manager before implementation.

## Development Workflow

### Team Roles & Responsibilities

| Role | Name | Responsibilities |
|------|------|------------------|
| Design Manager | Leon Kirasic | Final UI decisions, design consistency |
| Scrum Master / Project Lead | Jan Schröter | Ticket distribution, progress tracking |
| Documentation Reviewer | Jan Rörhle | Completeness and quality of documentation |
| Test Manager | All team members | Test coverage, quality assurance |
| QA | Benjamin Supke | Requirement compliance verification |

### Quality Gates

All pull requests MUST pass the following gates before merge:
1. ✅ All unit tests pass
2. ✅ Code coverage remains >80%
3. ✅ Integration tests pass
4. ✅ No new security vulnerabilities (OWASP dependency check)
5. ✅ Documentation updated (if applicable)
6. ✅ Code review approved by at least one peer

### Code Review Requirements

- Reviews MUST include verification of test coverage
- Complex AI integration code requires two reviewer approvals
- Documentation changes require review by Documentation Reviewer

## Governance

### Amendment Procedure

1. Proposed changes MUST be documented in a change proposal document
2. Changes MUST be reviewed for constitutional compliance
3. Major changes (backward-incompatible) require team vote (majority approval)
4. Minor changes require Scrum Master approval
5. Patch changes (clarifications) can be made by any team member with peer review

### Versioning Policy

- **MAJOR** (X.0.0): Backward-incompatible architecture changes, removal of principles
- **MINOR** (0.X.0): New principles added, material expansion of existing principles
- **PATCH** (0.0.X): Clarifications, wording fixes, non-semantic refinements

### Compliance

- This constitution SUPERSEDES all other development practices
- All PRs and reviews MUST verify compliance with constitutional principles
- Complexity that violates principles MUST be explicitly justified and documented
- Runtime development guidance: See `docs/specs/` for detailed specifications

### Review Cycle

Constitutional compliance MUST be reviewed:
- At the start of each sprint (during planning)
- Before major feature releases
- When new team members join

**Version**: 1.0.0 | **Ratified**: 2026-04-01 | **Last Amended**: 2026-04-01
