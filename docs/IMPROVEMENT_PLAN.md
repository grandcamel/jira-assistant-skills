# JIRA Assistant Skills - Improvement Plan

**Created:** 2025-12-26
**Based on:** Code reviews from docs/analysis/

This plan consolidates findings from code reviews of all 12 JIRA skills and organizes them into actionable improvements by priority.

---

## Executive Summary

All 12 skills are **production-ready** with ratings ranging from A- to A+ (4.0-5.0/5.0). The codebase demonstrates excellent engineering practices with consistent patterns, comprehensive error handling, and strong test coverage. The improvements identified are primarily enhancements rather than critical fixes.

### Overall Skill Ratings

| Skill | Rating | Grade | Critical Issues |
|-------|--------|-------|-----------------|
| jira-jsm | 9.35/10 | A | None |
| jira-ops | 9.2/10 | A | None |
| jira-fields | 9.5/10 | A+ | None |
| jira-dev | 9.2/10 | A | None |
| jira-bulk | 9.35/10 | A | None |
| jira-agile | 4.5/5 | A | None |
| jira-issue | 4.5/5 | A | None |
| jira-search | 4.5/5 | A | None |
| jira-time | 4.5/5 | A | None |
| jira-relationships | 4.5/5 | A | None |
| jira-collaborate | A- | A- | None |
| jira-lifecycle | A | A | None |

---

## P0 - Critical (Must Fix Immediately)

**None identified.** All skills are production-ready with no blocking issues.

---

## P1 - High Priority (Fix Within 1 Week)

### 1. Add Live Integration Tests to Missing Skills

**Affected Skills:** jira-collaborate, jira-relationships, jira-time, jira-lifecycle

**Current State:**
- jira-jsm: 94 live integration tests ✓
- jira-ops: 22 live integration tests ✓
- jira-bulk: 22 live integration tests ✓
- jira-dev: 25 live integration tests ✓
- jira-fields: 18 live integration tests ✓
- shared: 157 live integration tests ✓
- jira-collaborate: 0 live integration tests ❌
- jira-relationships: 0 live integration tests ❌
- jira-time: 0 live integration tests ❌
- jira-lifecycle: 0 live integration tests ❌

**Action Items:**

```
[ ] Create tests/live_integration/ for jira-collaborate
    - test_comment_lifecycle.py (add, update, delete comments)
    - test_notification_integration.py
    Estimated: 4 hours

[ ] Create tests/live_integration/ for jira-relationships
    - test_link_lifecycle.py (create, get, delete links)
    - test_blocker_chain.py (recursive traversal)
    - test_clone_issue.py
    Estimated: 4 hours

[ ] Create tests/live_integration/ for jira-time
    - test_worklog_lifecycle.py (add, update, delete)
    - test_time_tracking_flow.py
    - test_bulk_log_time.py
    Estimated: 4 hours

[ ] Create tests/live_integration/ for jira-lifecycle
    - test_transition_workflow.py
    - test_version_lifecycle.py
    - test_component_operations.py
    Estimated: 4 hours
```

**Total Estimated Effort:** 16 hours

---

### 2. Fix N+1 Query in jira-bulk

**File:** `.claude/skills/jira-bulk/scripts/bulk_clone.py`
**Lines:** 264-270
**Impact:** 10x performance improvement for bulk cloning

**Current Code:**
```python
result = client.search_issues(jql, fields=['key'], max_results=max_issues)
issue_keys = [i['key'] for i in result.get('issues', [])]
issues = []
for key in issue_keys:
    issue = client.get_issue(key)  # N additional API calls!
    issues.append(issue)
```

**Fix:**
```python
result = client.search_issues(jql, fields=['*all'], max_results=max_issues)
issues = result.get('issues', [])
```

**Estimated Effort:** 15 minutes

---

### 3. Fix Hardcoded Custom Field IDs

**Affected Skills:** jira-agile, jira-issue

**Current State:**
```python
# Hardcoded in multiple files:
EPIC_LINK_FIELD = 'customfield_10014'
STORY_POINTS_FIELD = 'customfield_10016'
EPIC_NAME_FIELD = 'customfield_10011'
EPIC_COLOR_FIELD = 'customfield_10012'
```

**Issue:** Field IDs vary by JIRA instance, causing failures on different installations.

**Solution Options:**
1. Move to config_manager with per-profile field ID mapping
2. Add field discovery with caching (leverage jira-fields skill)
3. Provide clear error messages when fields don't exist

**Action Items:**
```
[ ] Add agile_fields configuration to settings.json schema
[ ] Update config_manager to support custom field ID overrides
[ ] Add field discovery fallback using jira-fields APIs
[ ] Update jira-agile scripts to use configurable field IDs
[ ] Update jira-issue scripts to use configurable field IDs
[ ] Add documentation for field ID configuration
```

**Estimated Effort:** 4-6 hours

---

### 4. Fix Silent Exception Handling

**File:** `.claude/skills/jira-issue/scripts/create_issue.py`
**Lines:** 148-152, 156-161

**Current Code:**
```python
try:
    client.create_link('Blocks', issue_key, target_key)
    links_created.append(f"blocks {target_key}")
except Exception:
    pass  # Silent failure!
```

**Fix:**
```python
try:
    client.create_link('Blocks', issue_key, target_key)
    links_created.append(f"blocks {target_key}")
except JiraError as e:
    if isinstance(e, (PermissionError, NotFoundError)):
        links_failed.append(f"blocks {target_key}: {str(e)}")
    else:
        raise
```

**Estimated Effort:** 1 hour

---

### 5. Fix Pytest Test Discovery (jira-lifecycle)

**Location:** `.claude/skills/jira-lifecycle/tests/`
**Issue:** pytest cannot discover tests despite test files existing

**Action Items:**
```
[ ] Debug pytest import errors with -v --tb=short
[ ] Verify conftest.py is loading correctly
[ ] Check for missing __init__.py files
[ ] Add pytest.ini configuration if needed
[ ] Document test running procedure
```

**Estimated Effort:** 2 hours

---

## P2 - Medium Priority (Fix Within 1 Month)

### 6. Extract Shared Bulk Operation Patterns

**Affected Skill:** jira-bulk

**Issue:** ~8% code duplication across 4 scripts for:
- Issue retrieval (by keys or JQL)
- Dry-run preview logic
- Progress tracking loops
- Result dictionary construction

**Action Items:**
```
[ ] Create .claude/skills/jira-bulk/scripts/bulk_utils.py
[ ] Implement get_issues_to_process(client, issue_keys, jql, max_issues, fields)
[ ] Implement execute_bulk_operation(issues, operation_func, dry_run, delay, progress_callback)
[ ] Refactor bulk_transition.py to use bulk_utils
[ ] Refactor bulk_assign.py to use bulk_utils
[ ] Refactor bulk_set_priority.py to use bulk_utils
[ ] Refactor bulk_clone.py to use bulk_utils
```

**Estimated Effort:** 3 hours

---

### 7. Deduplicate Date Parsing Logic

**Affected Skills:** jira-agile, jira-time

**Issue:** Date parsing duplicated in create_sprint.py, manage_sprint.py, get_worklogs.py, time_report.py

**Action Items:**
```
[ ] Add parse_date_to_iso() to shared/scripts/lib/time_utils.py
[ ] Add convert_to_jira_datetime_string() to time_utils.py
[ ] Update jira-agile scripts to use shared function
[ ] Update jira-time scripts to use shared function
```

**Estimated Effort:** 2 hours

---

### 8. Move Common Transition Logic to Shared Library

**Affected Skills:** jira-lifecycle (potentially jira-issue, jira-bulk)

**Function:** `find_transition_by_name()`

**Action Items:**
```
[ ] Create shared/scripts/lib/transition_helpers.py
[ ] Move find_transition_by_name() with exact/partial match logic
[ ] Update transition_issue.py to import from shared
[ ] Update resolve_issue.py to import from shared
[ ] Update reopen_issue.py to import from shared
[ ] Add tests for transition_helpers.py
```

**Estimated Effort:** 2 hours

---

### 9. Move ADF Building to Shared Library

**Affected Skills:** jira-dev (link_commit.py, link_pr.py)

**Issue:** 47+ lines of manual ADF building in each script

**Action Items:**
```
[ ] Add wiki_markup_to_adf() to shared/scripts/lib/adf_helper.py
[ ] Support *bold*, [text|url] patterns
[ ] Update link_commit.py to use shared function
[ ] Update link_pr.py to use shared function
[ ] Add tests for wiki_markup_to_adf()
```

**Estimated Effort:** 3 hours

---

### 10. Refactor Large Functions

**File:** `.claude/skills/jira-search/scripts/share_filter.py`
**Issue:** main() is 130+ lines

**Action Items:**
```
[ ] Extract handle_list_permissions(client, args)
[ ] Extract handle_share_project(client, args)
[ ] Extract handle_share_group(client, args)
[ ] Extract handle_share_user(client, args)
[ ] Update main() to dispatch to handlers
```

**Estimated Effort:** 2 hours

---

### 11. Update Documentation

**Multiple Skills:**

```
[ ] jira-bulk: Add return values and exit codes to SKILL.md
[ ] jira-bulk: Document delay_between_ops parameter
[ ] jira-jsm: Add section on finding service desk IDs
[ ] jira-jsm: Document rate limiting considerations
[ ] jira-lifecycle: Update help text for assign_issue.py email/accountID
[ ] jira-ops: Add troubleshooting section to SKILL.md
[ ] jira-search: Add streaming export documentation
```

**Estimated Effort:** 4 hours

---

### 12. Add Missing Validation

**jira-bulk (bulk_set_priority.py):**
- Move priority validation before client creation

**jira-jsm (multiple scripts):**
- Validate comma-separated lists are non-empty after parsing
- Add validation for positive object_type_id

**jira-ops (cache.py):**
- Add single entry size validation
- Add cache directory permission check (0700)

**Estimated Effort:** 2 hours

---

### 13. Improve Error Handling Consistency

**jira-jsm:**
- Replace print() with print_error() in approve_request.py
- Standardize error output format

**jira-bulk:**
- Add try/except around issue retrieval in bulk_clone

**jira-collaborate:**
- Extract user lookup to shared helper function

**Estimated Effort:** 2 hours

---

## P3 - Low Priority (Consider for Future)

### 14. Performance Optimizations

```
[ ] jira-bulk: Add batching for operations on >500 issues
[ ] jira-bulk: Add checkpoint/resume capability for large operations
[ ] jira-search: Add streaming export for large datasets (>10k issues)
[ ] jira-search: Add autocomplete data caching
[ ] jira-ops: Optimize pattern matching with SQL LIKE for simple patterns
```

### 15. UX Enhancements

```
[ ] jira-bulk: Add progress bar using tqdm
[ ] jira-bulk: Add confirmation prompt for operations >50 issues
[ ] jira-dev: Add edge case handling for empty sanitized summaries
[ ] jira-lifecycle: Add dry-run to transition_issue.py, assign_issue.py
[ ] jira-lifecycle: Add progress reporting to move_issues_version.py
```

### 16. Feature Enhancements

```
[ ] jira-collaborate: Add attachment download functionality
[ ] jira-collaborate: Add activity filtering by field type
[ ] jira-relationships: Add link statistics script
[ ] jira-relationships: Add PlantUML/d2 export formats
[ ] jira-search: Add JQL query history/cache
[ ] jira-search: Add interactive query builder
[ ] jira-time: Add worklog visibility options (group/role)
```

### 17. Test Improvements

```
[ ] Add CLI argument parsing tests (all skills)
[ ] Add template validation tests (jira-issue)
[ ] Add concurrent operations tests (jira-relationships)
[ ] Add negative tests for jira-ops (invalid credentials, network)
[ ] Use parametrized tests for DRYer test code (jira-dev)
```

### 18. Security Hardening

```
[ ] jira-ops: Set restrictive cache directory permissions (0700)
[ ] jira-ops: Document that cache contains sensitive data
[ ] jira-bulk: Sanitize error messages for production logging
```

---

## Implementation Priority Matrix

| Priority | Count | Total Effort | Timeline |
|----------|-------|--------------|----------|
| P1 (High) | 5 items | ~26 hours | Week 1 |
| P2 (Medium) | 8 items | ~20 hours | Week 2-4 |
| P3 (Low) | 18 items | ~40+ hours | Backlog |

---

## Recommended Sprint Plan

### Sprint 1 (Week 1)
**Goal:** Address all P1 items

1. Fix N+1 query in bulk_clone.py (15 min)
2. Fix silent exception handling in create_issue.py (1 hr)
3. Fix pytest discovery in jira-lifecycle (2 hrs)
4. Add live integration tests for 4 skills (16 hrs)
5. Begin work on custom field ID configuration (2 hrs)

### Sprint 2 (Week 2)
**Goal:** Complete P1, start P2

1. Complete custom field ID configuration (4 hrs)
2. Extract shared bulk operation patterns (3 hrs)
3. Deduplicate date parsing logic (2 hrs)
4. Update documentation (4 hrs)

### Sprint 3 (Week 3-4)
**Goal:** Complete P2

1. Move common transition logic to shared lib (2 hrs)
2. Move ADF building to shared lib (3 hrs)
3. Refactor large functions (2 hrs)
4. Add missing validation (2 hrs)
5. Improve error handling consistency (2 hrs)

### Backlog
- All P3 items for future consideration

---

## Success Metrics

After implementing P1 and P2 items:

1. **Test Coverage**: All 12 skills have live integration tests
2. **Code Duplication**: Reduced from ~8% to <2% in jira-bulk
3. **Configuration**: Custom field IDs configurable per profile
4. **Documentation**: All skills have complete SKILL.md with troubleshooting
5. **Error Handling**: No silent exception swallowing
6. **Performance**: bulk_clone 10x faster with N+1 fix

---

## Appendix: Files to Modify

### P1 Changes
```
.claude/skills/jira-bulk/scripts/bulk_clone.py
.claude/skills/jira-issue/scripts/create_issue.py
.claude/skills/jira-lifecycle/tests/
.claude/skills/jira-collaborate/tests/live_integration/ (new)
.claude/skills/jira-relationships/tests/live_integration/ (new)
.claude/skills/jira-time/tests/live_integration/ (new)
.claude/skills/jira-lifecycle/tests/live_integration/ (new)
.claude/settings.json (schema update)
.claude/skills/shared/scripts/lib/config_manager.py
```

### P2 Changes
```
.claude/skills/jira-bulk/scripts/bulk_utils.py (new)
.claude/skills/jira-bulk/scripts/bulk_transition.py
.claude/skills/jira-bulk/scripts/bulk_assign.py
.claude/skills/jira-bulk/scripts/bulk_set_priority.py
.claude/skills/shared/scripts/lib/time_utils.py
.claude/skills/shared/scripts/lib/transition_helpers.py (new)
.claude/skills/shared/scripts/lib/adf_helper.py
.claude/skills/jira-search/scripts/share_filter.py
.claude/skills/*/SKILL.md (documentation updates)
```
