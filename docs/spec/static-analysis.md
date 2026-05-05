# Stytic Code Analysis

## Selected Categories and Tools

- **Linters:** ESBot contains orchestration logic between APIs and AI components. Poor structure or hidden bugs at this level can propagate incorrect outputs or unstable behavior.
- **Type checkers:** ESBot relies on structured data exchange between components and external APIs. Type checking ensures that data structures and interfaces are used correctly, preventing runtime errors caused by invalid assumptions about input and output formats.
- **Code Coverage:** Since ESBot processes dynamic inputs, it is essential to verify that critical execution paths are actually tested.
- **Style / format checkers:** ESBot is developed collaboratively and contains complex logic. Consistent formatting and coding style improve readability and maintainability, making it easier to understand, review, and extend the codebase.

### Tool 1: SonarQube

**Categories covered:**

- Linters / Code Quality Analysis
- Type checkers
- Code Coverage (via integration with coverage reports)
- Complexity
- Style / format checkers
- Dead code

**Justification**
SonarQube provides deep static analysis including:

- Detection of code smells, bugs and anti-patterns
- Maintainability metrics and duplication / dead code detection
- Integration with coverage reports for combined quality evaluation
- Code complexity calculation and detection

For ESBot, this is particularly relevant because:

- It highlights fragile integration logic (e.g., API handling)
- It enforces consistent structure across contributors
- It combines structural quality with test coverage insight in one place
- It detects and highlights dead code

### Tool 2: JetBrains Rider (Built-in Analysis Tools)

**Categories covered:**

- Linters / Code Quality Analysis
- Type checkers
- Code Coverage
- Style / format checkers

**Justification**
JetBrains Rider provides real-time static analysis and integrated coverage tools:

- On-the-fly linting and inspections during development
- Built-in code style enforcement
- Built-in type checks
- Native test coverage visualization

For ESBot, this ensures:

- Immediate feedback while writing code (faster iteration)
- Continuous visibility into test completeness
- Reduced friction compared to external tools


## Evaluation

### Effectiveness

- **SonarQube**

  - Strong at identifying structural issues and deeper code smells
  - Useful for periodic review of overall code quality

- **Rider**

  - Excellent for immediate feedback during development
  - Encourages fixing issues early

### Noise / False Positives

- **SonarQube**

  - Moderate noise, especially in complex or unconventional logic
  - Requires developer judgment

- **Rider**

  - Lower noise due to context-aware IDE inspections

### Impact on Development Speed

- **Rider**

  - Minimal overhead, integrates seamlessly

- **SonarQube**

  - Slightly slower, better suited for occasional full scans
  - difficult to explicitly implement and use locally
