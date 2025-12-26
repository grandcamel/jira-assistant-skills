# Test Remediation Plan: jira-admin Skill

**Created:** 2025-12-26
**Status:** Draft
**Test Files Reviewed:** 49
**Total Issues Identified:** ~200+

---

## Executive Summary

This plan addresses test quality issues discovered during a comprehensive review of the `jira-admin` skill test suite. Issues are organized by priority and grouped into actionable phases.

**Estimated Effort:**
- Phase 1 (Critical): 2-4 hours
- Phase 2 (High Priority): 4-6 hours
- Phase 3 (Medium Priority): 6-8 hours
- Phase 4 (Low Priority): 2-3 hours

---

## Phase 1: Critical Issues (Must Fix)

### 1.1 Empty CLI Test Stubs

**Impact:** False test coverage metrics, no actual CLI testing
**Files Affected:** 14 test files
**Action:** Either implement actual CLI tests or remove stubs entirely

| File | Lines | Stub Count |
|------|-------|------------|
| `tests/unit/test_get_project.py` | 207-223 | 3 stubs |
| `tests/unit/test_list_projects.py` | 244-272 | 4 stubs |
| `tests/unit/test_delete_project.py` | 206-222 | 3 stubs |
| `tests/unit/test_update_project.py` | 221-237 | 3 stubs |
| `tests/unit/test_archive_restore.py` | 333-352 | 3 stubs |
| `tests/unit/test_project_categories.py` | 288-310 | 3 stubs |
| `tests/unit/test_project_config.py` | 438-472 | 5 stubs |
| `tests/unit/test_get_issue_type.py` | 151-161 | 3 stubs |
| `tests/unit/test_list_issue_types.py` | 165-176 | 3 stubs |
| `tests/unit/test_create_issue_type.py` | 187-197 | 3 stubs |
| `tests/unit/test_delete_issue_type.py` | 191-205 | 4 stubs |
| `tests/unit/test_update_issue_type.py` | 201-211 | 3 stubs |
| `tests/unit/test_issue_type_schemes.py` | N/A | Missing CRUD tests |
| `tests/unit/test_issue_type_screen_schemes.py` | N/A | Missing CRUD tests |

**Remediation Steps:**

```python
# Option A: Implement actual CLI tests
def test_cli_with_id(self, mock_jira_client, sample_response, capsys):
    """Test CLI with ID argument."""
    mock_jira_client.get_xxx.return_value = sample_response

    with patch('config_manager.get_jira_client', return_value=mock_jira_client):
        import sys
        with patch.object(sys, 'argv', ['script.py', '10000']):
            from script_name import main
            main()

    captured = capsys.readouterr()
    assert 'Expected Output' in captured.out

# Option B: Remove stubs entirely and document as TODO
# Delete the empty test methods and add comment:
# TODO: CLI tests pending - see TEST_REMEDIATION_PLAN.md
```

---

### 1.2 Weak Assertions That Always Pass

**Impact:** Tests pass even when functionality is broken
**Files Affected:** 8 files

| File | Line | Current Assertion | Fix |
|------|------|-------------------|-----|
| `test_list_statuses.py` | 104 | `assert len(result['statuses']) >= 0` | `assert len(result['statuses']) > 0` |
| `test_list_statuses.py` | 137 | `... or len(result['statuses']) >= 0` | Remove fallback clause |
| `test_get_workflow.py` | 194 | `... or result.get('has_rules', False) is not None` | `assert 'rules' in transition` |
| `test_get_workflow_for_issue.py` | 83 | `... or len(transition_names) > 0` | `assert 'Start Progress' in transition_names` |
| `test_workflow_schemes.py` | 222 | `... or result.get('project_count', 0) >= 0` | `assert 'projects' in result` |
| `test_create_group.py` | 166 | `assert warning is not None or warning is None` | `assert warning is None` (for non-system) |
| `test_screen_operations.py` | 518 | `result.get('dry_run', False)` on boolean | Add type check first |
| `test_search_workflows.py` | 79 | `... or len(status_names) == 0` | Ensure statuses loaded or split test |

**Remediation Template:**

```python
# Before (weak):
assert len(result['statuses']) >= 0  # Always true

# After (strong):
assert len(result['statuses']) > 0
assert all('name' in s for s in result['statuses'])
```

---

### 1.3 Missing pytest Marker Registration

**Impact:** pytest warnings, inconsistent test selection
**File:** `tests/conftest.py`

**Add at top of conftest.py:**

```python
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "admin: mark test as admin skill test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
```

---

### 1.4 Missing pytest Markers on Test Classes

**Impact:** Inconsistent test categorization
**Files Affected:** 6 files

| File | Classes Missing Markers |
|------|------------------------|
| `test_screen_operations.py` | All 6 classes (lines 26, 114, 197, 262, 341, 444) |
| `test_screen_schemes.py` | All 2 classes (lines 22, 120) |
| `test_list_statuses.py` | All 8 classes (lines 17, 42, 85, 107, 123, 140, 170, 186) |
| `test_issue_type_screen_schemes.py` | All 2 classes (lines 22, 92) |
| `test_project_screens.py` | TestGetProjectScreens (line 19) |

**Remediation:**

```python
# Add to each test class:
@pytest.mark.admin
@pytest.mark.unit
class TestClassName:
    """Test description."""
```

---

## Phase 2: High Priority Issues

### 2.1 Missing Dry-Run Tests

**Impact:** Dry-run feature untested, could modify data unexpectedly
**Scripts Affected:** 5

| Script | Test File | Missing Test |
|--------|-----------|--------------|
| `disable_automation_rule.py` | `test_rule_state_management.py` | `test_disable_rule_dry_run` |
| `toggle_automation_rule.py` | `test_rule_state_management.py` | `test_toggle_rule_dry_run` |
| `update_automation_rule.py` | `test_templates_creation.py` | `test_update_rule_dry_run` |
| `invoke_manual_rule.py` | `test_manual_rules.py` | `test_invoke_rule_dry_run` |
| `remove_field_from_screen.py` | `test_screen_operations.py` | Fix existing test (line 518) |

**Remediation Template:**

```python
class TestDisableAutomationRuleDryRun:
    """Test dry-run mode for disable operations."""

    def test_disable_rule_dry_run(self, mock_automation_client, sample_rule_detail):
        """Test dry-run mode shows preview without changes."""
        from disable_automation_rule import disable_automation_rule

        mock_automation_client.get_rule.return_value = sample_rule_detail

        result = disable_automation_rule(
            client=mock_automation_client,
            rule_id='ari:cloud:jira::site/12345-rule-001',
            dry_run=True
        )

        # Verify no actual disable was called
        mock_automation_client.disable_rule.assert_not_called()
        assert result.get('dry_run') is True
        assert result.get('would_disable') is True
```

---

### 2.2 Missing API Error Handling Tests

**Impact:** Error scenarios untested, poor user experience on failures
**Coverage Gap:** All test files missing tests for:
- `AuthenticationError` (401)
- Rate limiting (429)
- Network timeout/connection errors

**Files to Update:** All 49 test files

**Remediation Template:**

```python
class TestApiErrorHandling:
    """Test API error handling scenarios."""

    def test_authentication_error(self, mock_jira_client):
        """Test handling of 401 unauthorized."""
        from error_handler import AuthenticationError
        mock_jira_client.some_method.side_effect = AuthenticationError("Invalid token")

        from script_name import function_name
        with pytest.raises(AuthenticationError):
            function_name(client=mock_jira_client)

    def test_rate_limit_error(self, mock_jira_client):
        """Test handling of 429 rate limit."""
        from error_handler import JiraError
        mock_jira_client.some_method.side_effect = JiraError(
            "Rate limit exceeded", status_code=429
        )

        from script_name import function_name
        with pytest.raises(JiraError) as exc_info:
            function_name(client=mock_jira_client)
        assert exc_info.value.status_code == 429

    def test_network_timeout(self, mock_jira_client):
        """Test handling of network timeout."""
        from error_handler import JiraError
        mock_jira_client.some_method.side_effect = JiraError("Connection timeout")

        from script_name import function_name
        with pytest.raises(JiraError):
            function_name(client=mock_jira_client)
```

---

### 2.3 Missing Task Failure Tests (Workflow Assignment)

**Impact:** Async task failures not handled gracefully
**File:** `tests/unit/test_assign_workflow_scheme.py`

**Add fixture to `workflow_responses.py`:**

```python
TASK_FAILED_RESPONSE = {
    "taskId": "10050",
    "self": "https://test.atlassian.net/rest/api/3/task/10050",
    "status": "FAILED",
    "message": "Migration failed due to status mapping error",
    "progress": 45,
    "error": {
        "errorMessages": ["Status 'Old Status' not found in target workflow"],
        "errors": {}
    }
}
```

**Add test:**

```python
def test_assign_scheme_task_failure(self, mock_jira_client, assign_scheme_task_response, task_failed_response):
    """Test handling of failed async task."""
    from assign_workflow_scheme import assign_workflow_scheme
    from error_handler import JiraError

    mock_jira_client.assign_workflow_scheme_to_project.return_value = assign_scheme_task_response
    mock_jira_client.get_task_status.return_value = task_failed_response

    with pytest.raises(JiraError) as exc_info:
        assign_workflow_scheme(
            client=mock_jira_client,
            project_key='PROJ',
            scheme_id=10101,
            confirm=True,
            wait=True
        )

    assert 'failed' in str(exc_info.value).lower()
```

---

### 2.4 Missing Fixture Exports in conftest.py

**Impact:** Error response fixtures not reusable across tests
**File:** `tests/conftest.py`

**Add imports and fixtures:**

```python
# Add to imports section
from fixtures.permission_scheme_responses import (
    SCHEME_NOT_FOUND_ERROR,
    SCHEME_IN_USE_ERROR,
    PERMISSION_DENIED_ERROR,
    INVALID_HOLDER_ERROR,
    PROJECTS_LIST_RESPONSE,
)

from fixtures.workflow_responses import (
    TASK_FAILED_RESPONSE,  # After adding to fixture file
)

# Add fixtures
@pytest.fixture
def scheme_not_found_error():
    import copy
    return copy.deepcopy(SCHEME_NOT_FOUND_ERROR)

@pytest.fixture
def scheme_in_use_error():
    import copy
    return copy.deepcopy(SCHEME_IN_USE_ERROR)

@pytest.fixture
def permission_denied_error():
    import copy
    return copy.deepcopy(PERMISSION_DENIED_ERROR)

@pytest.fixture
def task_failed_response():
    import copy
    return copy.deepcopy(TASK_FAILED_RESPONSE)
```

---

## Phase 3: Medium Priority Issues

### 3.1 Fixture Mutation Issues

**Impact:** Potential test pollution between tests
**Files Affected:** 4

| File | Lines | Issue |
|------|-------|-------|
| `test_create_permission_scheme.py` | 47-62 | Mutates `created_permission_scheme` |
| `test_update_permission_scheme.py` | 47-60 | Mutates `updated_permission_scheme` |
| `test_update_issue_type.py` | 34-36, 58-60, 82-84 | Uses shallow `.copy()` |

**Remediation:**

```python
# Before (mutation risk):
def test_create_with_description(self, mock_jira_client, created_permission_scheme):
    created_permission_scheme['description'] = 'Test description'  # Mutates fixture!

# After (safe):
def test_create_with_description(self, mock_jira_client, created_permission_scheme):
    import copy
    expected = copy.deepcopy(created_permission_scheme)
    expected['description'] = 'Test description'
    mock_jira_client.create_permission_scheme.return_value = expected
```

---

### 3.2 Missing Edge Case Tests

**Priority order by impact:**

| Category | Test File | Missing Edge Case |
|----------|-----------|-------------------|
| Ambiguous matches | `test_get_permission_scheme.py` | Multiple schemes match partial name |
| Ambiguous matches | `test_rule_state_management.py` | Multiple rules match name |
| Empty results | `test_templates_creation.py` | No templates found |
| Empty results | `test_list_permissions.py` | Empty permissions response |
| Boundary values | `test_create_group.py` | 255-char name limit |
| Boundary values | `test_create_permission_scheme.py` | Max name length |
| Duplicate names | `test_create_issue_type.py` | Issue type name exists |
| Duplicate names | `test_create_notification_scheme.py` | Scheme name exists |
| Invalid input | `test_list_statuses.py` | Invalid category filter |
| Invalid input | `test_search_workflows.py` | Invalid order_by value |
| Invalid input | `test_list_workflows.py` | Invalid scope value |

**Remediation Template:**

```python
def test_ambiguous_name_raises_error(self, mock_jira_client, sample_response):
    """Test error when multiple items match name query."""
    from error_handler import ValidationError

    # Setup: Return multiple matches
    mock_jira_client.search_xxx.return_value = {
        'values': [
            {'id': '1', 'name': 'Match One'},
            {'id': '2', 'name': 'Match Two'}
        ]
    }

    from script_name import get_by_name
    with pytest.raises(ValidationError) as exc_info:
        get_by_name(client=mock_jira_client, name='Match')

    assert 'ambiguous' in str(exc_info.value).lower()
```

---

### 3.3 Inconsistent Path Setup

**Impact:** Maintenance burden, potential import issues
**File:** `test_issue_type_screen_schemes.py` (lines 16-17)

**Current (inconsistent):**

```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'shared' / 'scripts' / 'lib'))
```

**Standardize to match other files:**

```python
# Standard path setup used by other test files
test_dir = Path(__file__).parent  # unit
tests_dir = test_dir.parent  # tests
jira_admin_dir = tests_dir.parent  # jira-admin
scripts_dir = jira_admin_dir / 'scripts'
shared_lib_dir = jira_admin_dir.parent / 'shared' / 'scripts' / 'lib'

sys.path.insert(0, str(scripts_dir))
sys.path.insert(0, str(shared_lib_dir))
```

---

### 3.4 Missing JSON Output Format Tests

**Impact:** JSON output untested, could break API consumers
**Files Affected:** 3

| File | Missing Test |
|------|--------------|
| `test_delete_notification_scheme.py` | `test_format_json_output` |
| `test_remove_notification.py` | `test_format_json_output` |
| `test_screen_schemes.py` | CSV format test |

**Remediation Template:**

```python
class TestFormatJsonOutput:
    """Test JSON output formatting."""

    def test_format_json_output(self, mock_jira_client, sample_response):
        """Test JSON output is valid and contains expected fields."""
        import json
        from script_name import function_name, format_json_output

        mock_jira_client.method.return_value = sample_response
        result = function_name(client=mock_jira_client, ...)

        output = format_json_output(result)
        parsed = json.loads(output)

        assert parsed['success'] is True
        assert 'id' in parsed
```

---

### 3.5 Redundant Mock Patching

**Impact:** Unnecessary complexity, slight performance overhead
**Files Affected:** All user/group test files (7 files)

**Current (redundant):**

```python
def test_add_user_success(self, mock_jira_client, sample_group):
    mock_jira_client.add_user_to_group.return_value = sample_group

    with patch('config_manager.get_jira_client', return_value=mock_jira_client):
        from add_user_to_group import add_user_to_group
        result = add_user_to_group(mock_jira_client, ...)  # Already passing client!
```

**Fixed (clean):**

```python
def test_add_user_success(self, mock_jira_client, sample_group):
    mock_jira_client.add_user_to_group.return_value = sample_group

    from add_user_to_group import add_user_to_group
    result = add_user_to_group(mock_jira_client, account_id="...", group_name="...")
```

---

## Phase 4: Low Priority Issues

### 4.1 Remove Unused Imports

**Impact:** Code hygiene
**Files Affected:** 15+

```bash
# Files with unused MagicMock import:
tests/test_add_notification.py:22
tests/test_create_notification_scheme.py:22
tests/test_delete_notification_scheme.py:22
tests/test_remove_notification.py:22
tests/test_update_notification_scheme.py:22
tests/unit/test_get_project.py:23
tests/unit/test_delete_project.py:23
tests/unit/test_update_project.py:23
tests/unit/test_archive_restore.py:23
tests/unit/test_project_categories.py:23
tests/unit/test_project_config.py:24
tests/unit/test_screen_operations.py:14
tests/unit/test_get_workflow.py:9-10
tests/unit/test_get_workflow_for_issue.py:9
tests/unit/test_list_workflows.py:9
tests/unit/test_search_workflows.py:9
tests/unit/test_workflow_schemes.py:9
tests/unit/test_assign_workflow_scheme.py:9

# Files with unused patch import:
tests/unit/test_screen_schemes.py:10
```

**Remediation:**

```python
# Before:
from unittest.mock import MagicMock, patch

# After:
from unittest.mock import patch  # or just Mock if patch unused
```

---

### 4.2 Inconsistent Assertion Patterns

**Impact:** Code maintainability
**Pattern to standardize:**

```python
# Avoid: String representation checking
assert "'expand': 'description'" in str(mock_jira_client.get_project.call_args)

# Prefer: Direct parameter access
call_args = mock_jira_client.get_project.call_args
assert call_args.kwargs.get('expand') == 'description'

# Or use assert_called_with:
mock_jira_client.get_project.assert_called_once_with(
    project_key='PROJ',
    expand='description'
)
```

---

### 4.3 Add Test Count Verification

**Impact:** Catch accidental test deletion

**Add to CI/CD or pre-commit:**

```python
# tests/test_coverage_check.py
import pytest
from pathlib import Path

def test_minimum_test_count():
    """Ensure test count doesn't regress."""
    test_dir = Path(__file__).parent
    test_files = list(test_dir.rglob('test_*.py'))

    # Count test functions
    test_count = 0
    for f in test_files:
        content = f.read_text()
        test_count += content.count('def test_')

    # Minimum expected tests (update as tests are added)
    MIN_TESTS = 400
    assert test_count >= MIN_TESTS, f"Expected {MIN_TESTS}+ tests, found {test_count}"
```

---

## Implementation Checklist

### Phase 1 Checklist (Critical)

- [ ] Decide: Implement or remove CLI test stubs
- [ ] Fix all 8 weak assertions
- [ ] Add `pytest_configure` to conftest.py
- [ ] Add pytest markers to 6 files (16 classes total)

### Phase 2 Checklist (High Priority)

- [ ] Add 5 dry-run tests for automation scripts
- [ ] Add API error handling tests (auth, rate limit, timeout)
- [ ] Add `TASK_FAILED_RESPONSE` fixture
- [ ] Add task failure test for workflow assignment
- [ ] Export missing fixtures from conftest.py

### Phase 3 Checklist (Medium Priority)

- [ ] Fix fixture mutation in 4 files
- [ ] Add 11+ edge case tests (ambiguous, empty, boundary)
- [ ] Standardize path setup in test_issue_type_screen_schemes.py
- [ ] Add JSON output format tests to 2 files
- [ ] Add CSV format test to test_screen_schemes.py
- [ ] Remove redundant patches in 7 user/group test files

### Phase 4 Checklist (Low Priority)

- [ ] Remove unused imports from 18 files
- [ ] Standardize assertion patterns
- [ ] Add test count verification

---

## Verification Commands

```bash
# Run all admin tests
pytest .claude/skills/jira-admin/tests/ -v

# Run only unit tests
pytest .claude/skills/jira-admin/tests/unit/ -v -m unit

# Check for test count
pytest .claude/skills/jira-admin/tests/ --collect-only | grep "test session starts" -A 5

# Verify no unused imports (requires pylint)
pylint .claude/skills/jira-admin/tests/ --disable=all --enable=unused-import

# Check assertion quality (manual review)
grep -rn "assert.*>= 0" .claude/skills/jira-admin/tests/
grep -rn "or len.*>= 0" .claude/skills/jira-admin/tests/
grep -rn "is not None or.*is None" .claude/skills/jira-admin/tests/
```

---

## Success Criteria

1. **All tests pass:** `pytest` exits with code 0
2. **No weak assertions:** grep commands return no results
3. **Consistent markers:** All test classes have `@pytest.mark.admin` and `@pytest.mark.unit`
4. **No pytest warnings:** About unknown markers
5. **Coverage maintained:** Test count >= current count
6. **No unused imports:** pylint reports clean

---

## Notes

- Prioritize Phase 1 before merging to main
- Phase 2 should be completed before next release
- Phases 3-4 can be addressed incrementally
- Consider adding pre-commit hooks to prevent regression
