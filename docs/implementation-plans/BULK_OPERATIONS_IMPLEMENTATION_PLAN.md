# Bulk Operations Skill - TDD Implementation Plan

## Overview

**Objective:** Implement comprehensive bulk operations functionality for JIRA issue management at scale using Test-Driven Development (TDD)

**Current Coverage:** 30% (bulk_update.py, bulk_link.py, bulk_log_time.py exist)

**Target Coverage:** 90%

**Approach:**
1. Write failing tests first for each feature
2. Implement minimum code to pass tests
3. Refactor while keeping tests green
4. Commit after each successful test suite
5. Update documentation as features complete

**Testing Stack:**
- **Framework:** pytest
- **Mocking:** unittest.mock / responses library
- **Coverage Target:** 85%+
- **Test Location:** `.claude/skills/jira-bulk/tests/`

**Feature Priority:**
1. **Phase 1: Bulk Transitions** (Core workflow automation)
2. **Phase 2: Bulk Clone/Copy** (Duplication workflows)
3. **Phase 3: Bulk Move** (Project migration)
4. **Phase 4: Bulk Delete** (Cleanup with safety)
5. **Phase 5: Bulk Export/Import** (CSV round-trip)
6. **Phase 6: Progress & Resume** (Enterprise reliability)

---

## Proposed Skill Structure

```
.claude/skills/jira-bulk/
├── SKILL.md
├── scripts/
│   ├── # Phase 1: Bulk Transitions
│   ├── bulk_transition.py        # Transition multiple issues
│   ├── bulk_assign.py            # Assign multiple issues to user
│   ├── bulk_set_priority.py      # Set priority on multiple issues
│   │
│   ├── # Phase 2: Bulk Clone/Copy
│   ├── bulk_clone.py             # Clone issues with options
│   ├── bulk_copy_to_project.py   # Copy issues to another project
│   │
│   ├── # Phase 3: Bulk Move
│   ├── bulk_move_project.py      # Move issues between projects
│   ├── bulk_move_version.py      # Move issues between versions
│   ├── bulk_move_component.py    # Reassign components
│   │
│   ├── # Phase 4: Bulk Delete
│   ├── bulk_delete.py            # Delete with safety checks
│   ├── bulk_archive.py           # Archive issues (soft delete)
│   │
│   ├── # Phase 5: Bulk Export/Import
│   ├── bulk_export.py            # Export to CSV/JSON with all fields
│   ├── bulk_import.py            # Import from CSV with validation
│   ├── bulk_sync.py              # Two-way sync with external source
│   │
│   └── # Phase 6: Progress & Resume
│       ├── bulk_progress.py      # Check progress of bulk operation
│       └── bulk_resume.py        # Resume interrupted operation
│
└── tests/
    ├── conftest.py
    ├── test_bulk_transition.py
    ├── test_bulk_clone.py
    ├── test_bulk_move.py
    ├── test_bulk_delete.py
    ├── test_bulk_export_import.py
    └── test_bulk_progress.py
```

---

## Phase 1: Bulk Transitions

### Feature 1.1: Bulk Transition Issues

**Script:** `bulk_transition.py`

**JIRA API:**
- `GET /rest/api/3/issue/{issueIdOrKey}/transitions` - Get available transitions
- `POST /rest/api/3/issue/{issueIdOrKey}/transitions` - Execute transition

**Test File:** `tests/test_bulk_transition.py`

**Test Cases:**
```python
def test_bulk_transition_by_keys():
    """Test transitioning multiple issues by key list"""

def test_bulk_transition_by_jql():
    """Test transitioning all issues matching JQL query"""

def test_bulk_transition_with_resolution():
    """Test setting resolution during transition"""

def test_bulk_transition_with_comment():
    """Test adding comment during transition"""

def test_bulk_transition_dry_run():
    """Test dry-run mode shows preview without changes"""

def test_bulk_transition_rate_limiting():
    """Test rate limiting and throttling"""

def test_bulk_transition_partial_failure():
    """Test handling when some issues fail to transition"""

def test_bulk_transition_invalid_transition():
    """Test error when transition not available for issue status"""

def test_bulk_transition_progress_callback():
    """Test progress reporting during operation"""

def test_bulk_transition_resume():
    """Test resuming interrupted bulk transition"""
```

**CLI Interface:**
```bash
# Transition by keys
python bulk_transition.py --issues PROJ-1,PROJ-2,PROJ-3 --to "Done"

# Transition by JQL
python bulk_transition.py --jql "project=PROJ AND status='In Progress'" --to "Done"

# With resolution
python bulk_transition.py --jql "project=PROJ AND type=Bug" --to "Done" --resolution "Fixed"

# With comment
python bulk_transition.py --issues PROJ-1,PROJ-2 --to "In Review" --comment "Ready for review"

# Dry run
python bulk_transition.py --jql "project=PROJ" --to "Done" --dry-run

# With progress tracking
python bulk_transition.py --jql "sprint=123" --to "Done" --track-progress

# Resume interrupted operation
python bulk_transition.py --resume session-123
```

**Acceptance Criteria:**
- [ ] All 10 tests pass
- [ ] Coverage ≥ 85% for bulk_transition.py
- [ ] Script executable from command line
- [ ] Help text shows all options
- [ ] Supports both keys and JQL
- [ ] Progress indicator for operations
- [ ] Resume capability for large operations

**Commits:**
1. `test(jira-bulk): add failing tests for bulk_transition`
2. `feat(jira-bulk): implement bulk_transition.py (10/10 tests passing)`
3. `docs(jira-bulk): add bulk transition to SKILL.md`

---

### Feature 1.2: Bulk Assign Issues

**Script:** `bulk_assign.py`

**JIRA API:**
- `PUT /rest/api/3/issue/{issueIdOrKey}/assignee`

**Test File:** `tests/test_bulk_assign.py`

**Test Cases:**
```python
def test_bulk_assign_to_user():
    """Test assigning multiple issues to specific user"""

def test_bulk_assign_to_self():
    """Test assigning to self"""

def test_bulk_assign_unassign():
    """Test removing assignee (unassign)"""

def test_bulk_assign_by_jql():
    """Test assigning issues matching JQL"""

def test_bulk_assign_with_email():
    """Test resolving user by email"""

def test_bulk_assign_dry_run():
    """Test dry-run preview"""

def test_bulk_assign_invalid_user():
    """Test error handling for invalid user"""
```

**CLI Interface:**
```bash
python bulk_assign.py --issues PROJ-1,PROJ-2 --assignee "john.doe"
python bulk_assign.py --jql "project=PROJ AND status=Open" --assignee self
python bulk_assign.py --jql "project=PROJ AND assignee=john" --unassign
python bulk_assign.py --issues PROJ-1 --assignee "john@company.com" --dry-run
```

**Acceptance Criteria:**
- [ ] All 7 tests pass
- [ ] Supports user lookup by email
- [ ] Supports 'self' keyword
- [ ] Supports unassignment
- [ ] Progress indicator

---

### Feature 1.3: Bulk Set Priority

**Script:** `bulk_set_priority.py`

**JIRA API:**
- `PUT /rest/api/3/issue/{issueIdOrKey}` with priority field

**Test Cases:**
```python
def test_bulk_priority_by_keys():
    """Test setting priority on multiple issues"""

def test_bulk_priority_by_jql():
    """Test setting priority via JQL filter"""

def test_bulk_priority_invalid():
    """Test error for invalid priority name"""

def test_bulk_priority_dry_run():
    """Test dry-run preview"""
```

**CLI Interface:**
```bash
python bulk_set_priority.py --issues PROJ-1,PROJ-2 --priority High
python bulk_set_priority.py --jql "project=PROJ AND type=Bug" --priority Blocker
```

---

### Phase 1 Completion

- [ ] **Phase 1 Summary:**
  - [ ] 3 scripts implemented (bulk_transition, bulk_assign, bulk_set_priority)
  - [ ] 21 tests passing
  - [ ] Coverage ≥ 85% for all Phase 1 scripts
  - [ ] SKILL.md created with Phase 1 documentation
  - **Commit:** `docs(jira-bulk): complete Phase 1 - Bulk Transitions`

---

## Phase 2: Bulk Clone/Copy

### Feature 2.1: Bulk Clone Issues

**Script:** `bulk_clone.py`

**JIRA API:**
- `POST /rest/api/3/issue` (create with cloned data)

**Test Cases:**
```python
def test_bulk_clone_basic():
    """Test cloning multiple issues"""

def test_bulk_clone_with_subtasks():
    """Test including subtasks in clone"""

def test_bulk_clone_with_links():
    """Test copying issue links"""

def test_bulk_clone_with_attachments():
    """Test copying attachments"""

def test_bulk_clone_with_prefix():
    """Test adding prefix to cloned summaries"""

def test_bulk_clone_to_project():
    """Test cloning to different project"""

def test_bulk_clone_strip_values():
    """Test stripping certain fields (status, assignee)"""

def test_bulk_clone_dry_run():
    """Test dry-run preview"""
```

**CLI Interface:**
```bash
# Clone issues with subtasks
python bulk_clone.py --issues PROJ-1,PROJ-2 --include-subtasks

# Clone with links
python bulk_clone.py --issues PROJ-1,PROJ-2 --include-links

# Clone to different project
python bulk_clone.py --issues PROJ-1,PROJ-2 --target-project NEWPROJ

# Clone with prefix
python bulk_clone.py --issues PROJ-1,PROJ-2 --prefix "[Clone]"

# Clone from JQL
python bulk_clone.py --jql "sprint=123" --include-subtasks --include-links
```

**Acceptance Criteria:**
- [ ] All 8 tests pass
- [ ] Supports subtask cloning
- [ ] Supports link preservation
- [ ] Supports cross-project cloning
- [ ] Progress tracking

---

### Feature 2.2: Bulk Copy to Project

**Script:** `bulk_copy_to_project.py`

**Test Cases:**
```python
def test_copy_to_project_basic():
    """Test copying issues to different project"""

def test_copy_to_project_field_mapping():
    """Test mapping fields between projects"""

def test_copy_to_project_type_mapping():
    """Test mapping issue types"""

def test_copy_to_project_preserve_hierarchy():
    """Test preserving epic/story/subtask hierarchy"""

def test_copy_to_project_validation():
    """Test field validation before copy"""
```

**CLI Interface:**
```bash
python bulk_copy_to_project.py --source PROJ --target NEWPROJ --jql "sprint=123"
python bulk_copy_to_project.py --source PROJ --target NEWPROJ --field-map mapping.json
python bulk_copy_to_project.py --issues PROJ-1,PROJ-2 --target NEWPROJ --preserve-hierarchy
```

---

### Phase 2 Completion

- [ ] **Phase 2 Summary:**
  - [ ] 2 scripts implemented
  - [ ] 13 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-bulk): complete Phase 2 - Bulk Clone/Copy`

---

## Phase 3: Bulk Move

### Feature 3.1: Bulk Move Between Projects

**Script:** `bulk_move_project.py`

**JIRA API:**
- `PUT /rest/api/3/issue/{issueIdOrKey}` (requires project change permission)

**Test Cases:**
```python
def test_bulk_move_project_basic():
    """Test moving issues to different project"""

def test_bulk_move_project_with_type_mapping():
    """Test issue type mapping during move"""

def test_bulk_move_project_preserve_keys():
    """Test behavior when project keys change"""

def test_bulk_move_project_field_validation():
    """Test required field validation"""

def test_bulk_move_project_permission_check():
    """Test permission validation before move"""

def test_bulk_move_project_dry_run():
    """Test dry-run preview"""
```

**CLI Interface:**
```bash
python bulk_move_project.py --issues PROJ-1,PROJ-2 --target NEWPROJ
python bulk_move_project.py --jql "project=PROJ" --target NEWPROJ --type-map types.json
python bulk_move_project.py --issues PROJ-1,PROJ-2 --target NEWPROJ --dry-run
```

---

### Feature 3.2: Bulk Move Between Versions

**Script:** `bulk_move_version.py`

**Test Cases:**
```python
def test_bulk_move_fix_version():
    """Test changing fixVersion on multiple issues"""

def test_bulk_move_affects_version():
    """Test changing affectsVersion on multiple issues"""

def test_bulk_move_version_by_jql():
    """Test moving via JQL filter"""

def test_bulk_move_version_clear():
    """Test clearing version field"""
```

**CLI Interface:**
```bash
python bulk_move_version.py --jql "fixVersion='1.0'" --target-version "1.1"
python bulk_move_version.py --issues PROJ-1,PROJ-2 --fix-version "2.0"
python bulk_move_version.py --jql "project=PROJ" --clear-affects-version
```

---

### Feature 3.3: Bulk Move Components

**Script:** `bulk_move_component.py`

**Test Cases:**
```python
def test_bulk_move_component_add():
    """Test adding component to multiple issues"""

def test_bulk_move_component_remove():
    """Test removing component from multiple issues"""

def test_bulk_move_component_replace():
    """Test replacing one component with another"""

def test_bulk_move_component_by_jql():
    """Test via JQL filter"""
```

**CLI Interface:**
```bash
python bulk_move_component.py --jql "component='Backend'" --add-component "API"
python bulk_move_component.py --issues PROJ-1,PROJ-2 --remove-component "Legacy"
python bulk_move_component.py --jql "project=PROJ" --replace "OldName" --with "NewName"
```

---

### Phase 3 Completion

- [ ] **Phase 3 Summary:**
  - [ ] 3 scripts implemented
  - [ ] 14 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-bulk): complete Phase 3 - Bulk Move`

---

## Phase 4: Bulk Delete

### Feature 4.1: Bulk Delete with Safety

**Script:** `bulk_delete.py`

**JIRA API:**
- `DELETE /rest/api/3/issue/{issueIdOrKey}`

**Test Cases:**
```python
def test_bulk_delete_by_keys():
    """Test deleting specific issues"""

def test_bulk_delete_by_jql():
    """Test deleting via JQL (with confirmation)"""

def test_bulk_delete_requires_confirmation():
    """Test that --confirm is required"""

def test_bulk_delete_with_subtasks():
    """Test cascade delete of subtasks"""

def test_bulk_delete_dry_run():
    """Test dry-run preview with impact analysis"""

def test_bulk_delete_backup_first():
    """Test creating backup before delete"""

def test_bulk_delete_max_limit():
    """Test safety limit on maximum issues"""

def test_bulk_delete_protected_types():
    """Test protection for certain issue types"""
```

**CLI Interface:**
```bash
# Delete with explicit confirmation
python bulk_delete.py --issues PROJ-1,PROJ-2 --confirm

# Delete via JQL (dangerous - requires confirmation)
python bulk_delete.py --jql "project=PROJ AND status=Cancelled" --confirm

# Dry run with impact analysis
python bulk_delete.py --jql "project=PROJ" --dry-run

# Delete with backup
python bulk_delete.py --issues PROJ-1,PROJ-2 --backup deleted.json --confirm

# Include subtasks
python bulk_delete.py --issues PROJ-1 --delete-subtasks --confirm
```

**Safety Features:**
- **Confirmation required:** `--confirm` flag mandatory
- **Max limit:** Default 100 issues, override with `--max-delete 500`
- **Backup option:** `--backup` creates JSON backup before deletion
- **Protected types:** Optionally protect Epic, Sub-task types
- **Dry run:** Shows exactly what will be deleted
- **Pause between batches:** Rate limiting to prevent accidents

**Acceptance Criteria:**
- [ ] All 8 tests pass
- [ ] Confirmation required for all deletes
- [ ] Backup capability
- [ ] Progress indicator
- [ ] Safety limits enforced

---

### Feature 4.2: Bulk Archive

**Script:** `bulk_archive.py`

**Note:** JIRA doesn't have native archive. This transitions to a custom "Archived" status.

**Test Cases:**
```python
def test_bulk_archive_transitions():
    """Test transitioning to archived status"""

def test_bulk_archive_sets_label():
    """Test adding archived label"""

def test_bulk_archive_unarchive():
    """Test reversing archive operation"""

def test_bulk_archive_dry_run():
    """Test dry-run preview"""
```

**CLI Interface:**
```bash
python bulk_archive.py --jql "project=PROJ AND updated < -1y" --confirm
python bulk_archive.py --issues PROJ-1,PROJ-2 --add-label archived
python bulk_archive.py --jql "labels=archived" --unarchive
```

---

### Phase 4 Completion

- [ ] **Phase 4 Summary:**
  - [ ] 2 scripts implemented
  - [ ] 12 tests passing
  - [ ] Coverage ≥ 85%
  - [ ] Safety features documented
  - **Commit:** `docs(jira-bulk): complete Phase 4 - Bulk Delete`

---

## Phase 5: Bulk Export/Import

### Feature 5.1: Bulk Export

**Script:** `bulk_export.py`

**Test Cases:**
```python
def test_export_to_csv():
    """Test exporting to CSV format"""

def test_export_to_json():
    """Test exporting to JSON format"""

def test_export_to_excel():
    """Test exporting to Excel format"""

def test_export_all_fields():
    """Test exporting all fields including custom"""

def test_export_specific_fields():
    """Test exporting only specified fields"""

def test_export_with_attachments():
    """Test including attachment URLs/content"""

def test_export_with_comments():
    """Test including comment history"""

def test_export_with_history():
    """Test including changelog"""

def test_export_by_jql():
    """Test exporting via JQL filter"""

def test_export_pagination():
    """Test handling large result sets"""
```

**CLI Interface:**
```bash
# Export to CSV
python bulk_export.py --jql "project=PROJ" --output issues.csv

# Export to JSON with all fields
python bulk_export.py --jql "project=PROJ" --output issues.json --all-fields

# Export specific fields
python bulk_export.py --jql "project=PROJ" --fields "key,summary,status,assignee" --output issues.csv

# Include comments and history
python bulk_export.py --jql "project=PROJ" --include-comments --include-history --output issues.json

# Export with attachments
python bulk_export.py --issues PROJ-1,PROJ-2 --include-attachments --output-dir ./export/
```

**Acceptance Criteria:**
- [ ] All 10 tests pass
- [ ] CSV, JSON, Excel formats supported
- [ ] Custom field export
- [ ] Attachment download option
- [ ] Progress indicator for large exports

---

### Feature 5.2: Bulk Import

**Script:** `bulk_import.py`

**Test Cases:**
```python
def test_import_from_csv():
    """Test importing from CSV"""

def test_import_from_json():
    """Test importing from JSON"""

def test_import_validation():
    """Test validation before import"""

def test_import_field_mapping():
    """Test custom field mapping"""

def test_import_dry_run():
    """Test dry-run preview"""

def test_import_update_existing():
    """Test updating existing issues"""

def test_import_create_only():
    """Test creating new issues only"""

def test_import_with_attachments():
    """Test uploading attachments during import"""

def test_import_error_handling():
    """Test handling of validation errors"""

def test_import_rollback():
    """Test rollback on failure"""
```

**CLI Interface:**
```bash
# Import from CSV
python bulk_import.py --input issues.csv --project PROJ

# Validate only (dry-run)
python bulk_import.py --input issues.csv --project PROJ --validate-only

# Import with field mapping
python bulk_import.py --input issues.csv --project PROJ --field-map mapping.json

# Update existing issues
python bulk_import.py --input issues.csv --project PROJ --update-existing

# Create with attachments
python bulk_import.py --input issues.json --project PROJ --attachments-dir ./attachments/
```

**Acceptance Criteria:**
- [ ] All 10 tests pass
- [ ] CSV and JSON import
- [ ] Field mapping/transformation
- [ ] Validation with helpful errors
- [ ] Update-or-create mode
- [ ] Rollback capability

---

### Feature 5.3: Bulk Sync

**Script:** `bulk_sync.py`

**Test Cases:**
```python
def test_sync_export():
    """Test exporting for sync"""

def test_sync_import():
    """Test importing sync changes"""

def test_sync_bidirectional():
    """Test two-way sync"""

def test_sync_conflict_resolution():
    """Test handling conflicts"""

def test_sync_incremental():
    """Test incremental sync based on updated date"""
```

**CLI Interface:**
```bash
# Export for sync
python bulk_sync.py --export --jql "project=PROJ" --output sync.json

# Import sync changes
python bulk_sync.py --import --input sync.json --project PROJ

# Incremental sync
python bulk_sync.py --sync --jql "project=PROJ" --since "2025-01-01" --output sync.json
```

---

### Phase 5 Completion

- [ ] **Phase 5 Summary:**
  - [ ] 3 scripts implemented
  - [ ] 25 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-bulk): complete Phase 5 - Bulk Export/Import`

---

## Phase 6: Progress & Resume

### Feature 6.1: Progress Tracking

**Script:** `bulk_progress.py`

**Test Cases:**
```python
def test_progress_active_operations():
    """Test listing active bulk operations"""

def test_progress_completed():
    """Test showing completed operations"""

def test_progress_details():
    """Test getting detailed progress info"""

def test_progress_cancel():
    """Test cancelling in-progress operation"""
```

**CLI Interface:**
```bash
# List active operations
python bulk_progress.py --list

# Get specific operation status
python bulk_progress.py --session session-123

# Cancel operation
python bulk_progress.py --cancel session-123
```

---

### Feature 6.2: Resume Interrupted Operations

**Script:** `bulk_resume.py`

**Test Cases:**
```python
def test_resume_incomplete():
    """Test resuming incomplete operation"""

def test_resume_from_checkpoint():
    """Test resuming from last checkpoint"""

def test_resume_list_resumable():
    """Test listing resumable operations"""

def test_resume_cleanup():
    """Test cleaning up old sessions"""
```

**CLI Interface:**
```bash
# List resumable operations
python bulk_resume.py --list

# Resume specific operation
python bulk_resume.py --session session-123

# Resume from checkpoint
python bulk_resume.py --session session-123 --from-checkpoint cp-5

# Clean up old sessions
python bulk_resume.py --cleanup --older-than 7d
```

---

### Phase 6 Completion

- [ ] **Phase 6 Summary:**
  - [ ] 2 scripts implemented
  - [ ] 8 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-bulk): complete Phase 6 - Progress & Resume`

---

## Integration & Polish

### Integration Tasks

- [ ] **Integration 1:** Update jira-search scripts
  - [ ] Add `--export` flag to jql_search.py for quick export
  - [ ] Add `--bulk` flag to show bulk operation suggestions
  - **Commit:** `feat(jira-search): add bulk operation integration`

- [ ] **Integration 2:** Session Management
  - [ ] Create session state storage (JSON file or SQLite)
  - [ ] Add checkpoint creation during bulk operations
  - [ ] Store progress for resume capability
  - **Commit:** `feat(jira-bulk): add session management for resume`

### Documentation Updates

- [ ] **Docs 1:** Create comprehensive SKILL.md for jira-bulk
- [ ] **Docs 2:** Update CLAUDE.md with jira-bulk skill
- [ ] **Docs 3:** Update GAP_ANALYSIS.md - Mark bulk operations as complete

---

## Success Metrics

### Completion Criteria

**Tests:**
- [ ] 90+ unit tests passing
- [ ] 5+ integration tests passing
- [ ] Coverage ≥ 85%

**Scripts:**
- [ ] 15 new scripts implemented
- [ ] All scripts have `--help`
- [ ] All scripts support `--profile`
- [ ] All mutation scripts have `--dry-run`
- [ ] All scripts have `--confirm` where appropriate

**Documentation:**
- [ ] SKILL.md complete with examples
- [ ] CLAUDE.md updated
- [ ] GAP_ANALYSIS.md updated

---

## Summary Metrics

| Phase | Scripts | Tests | Priority |
|-------|---------|-------|----------|
| 1. Bulk Transitions | 3 | 21 | Critical |
| 2. Bulk Clone/Copy | 2 | 13 | High |
| 3. Bulk Move | 3 | 14 | High |
| 4. Bulk Delete | 2 | 12 | Medium |
| 5. Bulk Export/Import | 3 | 25 | High |
| 6. Progress & Resume | 2 | 8 | Medium |
| **TOTAL** | **15** | **93** | - |

---

## Risk Assessment

### Technical Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Rate limiting on bulk operations | High | Implement throttling and backoff |
| Permission issues during move/delete | Medium | Pre-validation and dry-run |
| Large dataset memory issues | Medium | Streaming and pagination |
| Data loss during delete | High | Mandatory confirmation and backup |
| Resume state corruption | Low | Checksum validation |

### Safety Considerations
- All delete operations require explicit `--confirm` flag
- Default maximum limit on bulk operations (100 issues)
- Mandatory dry-run capability on all mutation operations
- Backup option before destructive operations
- Rate limiting to prevent accidental impact

---

**Document Version:** 1.0
**Created:** 2025-12-25
**Status:** Ready for Implementation
