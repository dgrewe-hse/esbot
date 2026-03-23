# Development Task Organization

## Overview

We organize our development using GitHub Issues, feature branches, and pull requests.  
Each task is tracked as an issue and implemented in a separate branch.

---

## Workflow

### 1. Create an issue

- Every task starts with a GitHub issue
- The issue describes the goal of the task

---

### 2. Create a feature branch

- Create a branch based on the issue
- Naming convention:
  - `feature/<issue-number>-short-description`
- Example:
  - `feature/12-add-techstack-doc`

---

### 3. Implement the task

- Work on the feature in the created branch
- Make clear and structured commits
- Use conventional commit messages (e.g. `docs: add tech stack document`)
- Write appropriate tests for your implementation (unit, integration, or API tests if applicable)

---

### 4. Sync with main branch

- Before creating a pull request, update your feature branch with the latest changes from the main branch
- This ensures your code is up to date and reduces merge conflicts

Steps:

- Pull the latest changes from `main`
- Merge or rebase them into your feature branch
- Run all relevant tests again

- Only create a pull request if:
  - All tests pass
  - The application works as expected

---

### 5. Create a pull request

- Open a pull request to merge into the main branch
- In the PR description, reference the issue: `Closes/Fixes/Resolves #12`

- This links the PR to the issue

---

### 6. Review and merge

- At least one team member should review the pull request before merging
- After approval, the PR is merged into the main branch

---

### 7. Issue is closed automatically

- After merging the PR:
  - The linked issue is automatically closed
  - The task is considered completed

---

### Summary

- Issue = Task
- Branch = Implementation
- Pull Request = Review and Integration
- Merge = Completion

This workflow ensures clear structure, traceability, and collaboration within the team.
