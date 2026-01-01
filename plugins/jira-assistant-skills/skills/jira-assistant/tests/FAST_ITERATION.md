# Fast Iteration Workflow for Routing Tests

This document describes how to minimize the fix-test-pass/fail cycle when improving routing accuracy.

## The Problem

Full test suite takes **~22 minutes** (79 tests × ~17 seconds each). This makes iteration painfully slow when tuning skill descriptions.

## The Solution

Three optimizations reduce cycle time from 22 minutes to **1-4 minutes**:

| Optimization | Speed-Up | Trade-off |
|--------------|----------|-----------|
| Targeted tests | 10-20x | Only tests relevant skill |
| Parallel execution | 2-4x | May hit rate limits |
| Haiku model | ~2x | May behave slightly differently |

## Quick Start

```bash
cd plugins/jira-assistant-skills/skills/jira-assistant/tests

# Fast iteration on a single skill (recommended workflow)
./fast_test.sh --skill agile --fast --parallel 2

# Quick smoke test (5 representative tests)
./fast_test.sh --smoke --fast

# Test specific failing cases
./fast_test.sh --id TC012,TC015,TC020 --fast

# Re-run only previously failed tests
./fast_test.sh --failed --fast

# Full validation (before committing)
./fast_test.sh --production
```

## Recommended Workflow

### 1. Identify Failing Tests

Run the full suite once to establish baseline:

```bash
pytest test_routing.py -v 2>&1 | tee baseline.log
```

### 2. Group Failures by Skill

From the test output, identify which skills need work. Common failure patterns:

| Failure Pattern | Skill to Fix | Command |
|-----------------|--------------|---------|
| "Expected jira-agile, got jira-issue" | jira-agile | `--skill agile` |
| "Expected jira-bulk, got jira-search" | jira-bulk | `--skill bulk` |
| "Expected jira-dev, got jira-issue" | jira-dev | `--skill dev` |

### 3. Fast Iteration Loop

```bash
# 1. Edit the skill description
vim ../../jira-agile/SKILL.md

# 2. Test quickly with haiku (~2 min)
./fast_test.sh --skill agile --fast

# 3. If passing, validate with production model (~4 min)
./fast_test.sh --skill agile --production

# 4. Repeat until skill passes
```

### 4. Validate Full Suite

Before committing, run the full suite:

```bash
# Parallel for speed, production model for accuracy
./fast_test.sh --all --parallel 4

# Or sequential for maximum reliability
./fast_test.sh --production
```

## Test Subsets by Skill

| Skill | Test IDs | Estimated Time (--fast) |
|-------|----------|------------------------|
| jira-issue | TC001-TC004, TC039, TC047 | ~2 min |
| jira-search | TC005-TC008 | ~1 min |
| jira-lifecycle | TC009-TC011, TC040 | ~1 min |
| jira-agile | TC012-TC015, TC031 | ~1.5 min |
| jira-bulk | TC024-TC025, TC041, TC036 | ~1 min |
| jira-dev | TC026-TC027, TC079 | ~1 min |
| jira-relationships | TC019-TC021, TC063 | ~1 min |
| jira-time | TC022-TC023, TC075 | ~1 min |
| jira-fields | TC028, TC077 | ~30 sec |
| jira-ops | TC029, TC078 | ~30 sec |

## CLI Options

### Using pytest directly

```bash
# Target specific tests
pytest test_routing.py -v -k "TC012 or TC015"

# Use haiku model
pytest test_routing.py -v --model haiku

# Parallel execution (4 workers)
pytest test_routing.py -v -n 4

# Combine all
pytest test_routing.py -v -k "TC012" --model haiku -n 2

# Re-run failed tests only
pytest test_routing.py -v --lf
```

### Using fast_test.sh

```bash
./fast_test.sh --skill agile           # Test agile skill
./fast_test.sh --skill agile,bulk      # Test multiple skills
./fast_test.sh --id TC012,TC015        # Test specific IDs
./fast_test.sh --smoke                 # Quick 5-test smoke
./fast_test.sh --fast                  # Use haiku model
./fast_test.sh --parallel 4            # 4 parallel workers
./fast_test.sh --failed                # Re-run failures only
./fast_test.sh --production            # Full production validation
```

## Timing Estimates

| Scenario | Command | Time |
|----------|---------|------|
| Single test | `--id TC012 --fast` | ~15 sec |
| Smoke test (5) | `--smoke --fast` | ~1.5 min |
| Single skill | `--skill agile --fast` | ~2 min |
| Single skill + parallel | `--skill agile --fast --parallel 2` | ~1 min |
| All tests + haiku + parallel | `--fast --parallel 4` | ~8-10 min |
| Full production run | `--production` | ~22 min |

## Model Differences

The `--fast` flag uses Claude Haiku which is faster but may route slightly differently than the production model (Sonnet).

**Recommendation:**
- Use `--fast` during iteration for quick feedback
- Validate with `--production` before committing changes
- If a test passes with haiku but fails with production, investigate the specific case

## Parallel Execution Notes

- `--parallel 2` is safe and provides ~2x speedup
- `--parallel 4` may hit rate limits on slower connections
- If you see timeout errors, reduce parallelism or add delays
- Parallel tests may have non-deterministic output ordering

## Troubleshooting

### "ModuleNotFoundError: conftest"

Run from the tests directory:
```bash
cd plugins/jira-assistant-skills/skills/jira-assistant/tests
./fast_test.sh --smoke
```

### Rate Limit Errors (429)

Reduce parallelism:
```bash
./fast_test.sh --skill agile --fast --parallel 1
```

### Tests Pass with Haiku but Fail with Production

The models may interpret skill descriptions differently. Test with production model and adjust descriptions accordingly:
```bash
./fast_test.sh --id TC012 --production
```

## Integration with CI/CD

For pull request validation:

```yaml
# Fast check (gate merge)
- run: ./fast_test.sh --smoke --fast

# Full validation (nightly)
- run: ./fast_test.sh --production
```

## Next Steps

See [ROUTING_ACCURACY_PROPOSAL.md](ROUTING_ACCURACY_PROPOSAL.md) for specific skill description changes to improve routing accuracy.
