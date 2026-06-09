# Local Development: Testing and Static Analysis

## Prerequisites

The project requires:

* .NET SDK 9.0.x
* All solution dependencies

---

## Running the Test Suite

### Command

```bash
dotnet test --configuration Release --logger "trx;LogFileName=test_results.trx" --results-directory ./TestResults
```

### Expected Outcome

Successful execution should:

1. Build the solution and test projects.
2. Execute all unit tests.
3. Produce console output showing the number of passed/failed tests.
4. Generate a TRX test report at:

```text
./TestResults/test_results.trx
```

Example successful output:

```text
Passed!  - Failed: 0, Passed: <n>, Skipped: 0
```

### Viewing Test Results

The generated TRX file can be found at:

```text
./TestResults/test_results.trx
```

---

## Running Static Analysis / Style Checks

### Command

```bash
dotnet format style --verify-no-changes
```

### Expected Outcome

If the codebase complies with the configured formatting and style rules:

```text
Format complete.
```

Exit code:

```text
0
```

If formatting or style violations exist, the command will:

* Report the violations.
* Exit with a non-zero status code.

To automatically apply fixes locally, you can run:

```bash
dotnet format style
```

---

## Environment Variables

For local verification, only the following values are required:

```bash
export CONFIGURATION=Release
```

or on Windows PowerShell:

```powershell
$env:CONFIGURATION="Release"
```

---

## Required Services

No external services are required to:

* Run tests
* Run static analysis
* Build the solution
