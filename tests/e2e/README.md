# E2E Tests for Jira-Assistant-Skills

End-to-end tests that validate the plugin by interacting with the Claude Code CLI.

## Prerequisites

### Authentication (Choose One)

**Option 1: API Key**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Option 2: OAuth**
```bash
claude auth login
```

## Quick Start

```bash
# Run all tests
./scripts/run-e2e-tests.sh

# Run locally (no Docker)
./scripts/run-e2e-tests.sh --local

# Verbose output
./scripts/run-e2e-tests.sh --verbose

# Debug shell
./scripts/run-e2e-tests.sh --shell
```

## Test Structure

```
tests/e2e/
├── __init__.py
├── conftest.py          # Pytest fixtures
├── runner.py            # Test execution engine
├── test_cases.yaml      # YAML test definitions
└── test_plugin_e2e.py   # Pytest test classes
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | - | API key |
| `E2E_TEST_TIMEOUT` | 120 | Timeout per test (seconds) |
| `E2E_TEST_MODEL` | claude-sonnet-4-20250514 | Model to use |
| `E2E_VERBOSE` | false | Verbose output |

## Output Formats

```bash
# JSON report
python -m tests.e2e.run_tests --json results.json

# JUnit XML (CI integration)
python -m tests.e2e.run_tests --junit results.xml

# HTML report
python -m tests.e2e.run_tests --html report.html

# All formats
python -m tests.e2e.run_tests --all-formats
```

## Adding Tests

### YAML Test Cases

Edit `test_cases.yaml`:

```yaml
suites:
  my_suite:
    description: My tests
    tests:
      - id: my_test
        name: Test something
        prompt: "Do something"
        expect:
          output_contains:
            - "expected"
          no_errors: true
```

### Pytest Classes

Edit `test_plugin_e2e.py`:

```python
class TestMyFeature:
    def test_something(self, claude_runner, e2e_enabled):
        if not e2e_enabled:
            pytest.skip("E2E disabled")

        result = claude_runner.send_prompt("My prompt")
        assert "expected" in result["output"]
```

## Cost Estimates

| Model | Per Test | 20 Tests |
|-------|----------|----------|
| Haiku | ~$0.001 | ~$0.02 |
| Sonnet | ~$0.01 | ~$0.20 |
| Opus | ~$0.05 | ~$1.00 |
