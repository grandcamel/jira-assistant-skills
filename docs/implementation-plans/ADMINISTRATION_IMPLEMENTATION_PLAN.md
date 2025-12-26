# Administration Skill - TDD Implementation Plan

## Overview

**Objective:** Implement comprehensive JIRA administration functionality for project setup, user management, and configuration automation using Test-Driven Development (TDD)

**Current Coverage:** 10% (Only custom field creation via jira-fields)

**Target Coverage:** 70%

**Note:** Many administration features require JIRA Administrator permissions. This skill targets power users and DevOps automation scenarios.

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
- **Test Location:** `.claude/skills/jira-admin/tests/`

**Feature Priority:**
1. **Phase 1: Project Management** (Project CRUD)
2. **Phase 2: User & Group Management** (User operations)
3. **Phase 3: Permission Schemes** (Security configuration)
4. **Phase 4: Workflow Management** (Workflow operations)
5. **Phase 5: Scheme Management** (Notification, issue type schemes)
6. **Phase 6: Automation Rules** (Automation CRUD)

---

## Proposed Skill Structure

```
.claude/skills/jira-admin/
├── SKILL.md
├── scripts/
│   ├── # Phase 1: Project Management
│   ├── create_project.py          # Create new project
│   ├── get_project.py             # Get project details
│   ├── update_project.py          # Update project settings
│   ├── delete_project.py          # Delete project
│   ├── list_projects.py           # List all projects
│   ├── archive_project.py         # Archive project
│   ├── get_project_settings.py    # Get project configuration
│   │
│   ├── # Phase 2: User & Group Management
│   ├── search_users.py            # Search for users
│   ├── get_user.py                # Get user details
│   ├── list_groups.py             # List all groups
│   ├── get_group_members.py       # Get group members
│   ├── add_user_to_group.py       # Add user to group
│   ├── remove_user_from_group.py  # Remove user from group
│   ├── create_group.py            # Create group
│   ├── delete_group.py            # Delete group
│   │
│   ├── # Phase 3: Permission Schemes
│   ├── list_permission_schemes.py # List permission schemes
│   ├── get_permission_scheme.py   # Get scheme details
│   ├── create_permission_scheme.py# Create scheme
│   ├── update_permission_scheme.py# Update scheme
│   ├── assign_permission_scheme.py# Assign to project
│   │
│   ├── # Phase 4: Workflow Management
│   ├── list_workflows.py          # List workflows
│   ├── get_workflow.py            # Get workflow details
│   ├── list_workflow_schemes.py   # List workflow schemes
│   ├── get_workflow_scheme.py     # Get workflow scheme
│   ├── assign_workflow_scheme.py  # Assign to project
│   │
│   ├── # Phase 5: Scheme Management
│   ├── list_issue_type_schemes.py # List issue type schemes
│   ├── get_issue_type_scheme.py   # Get scheme details
│   ├── list_notification_schemes.py# List notification schemes
│   ├── get_notification_scheme.py # Get scheme details
│   ├── list_screen_schemes.py     # List screen schemes
│   │
│   └── # Phase 6: Automation Rules
│       ├── list_automation_rules.py    # List automation rules
│       ├── get_automation_rule.py      # Get rule details
│       ├── enable_automation_rule.py   # Enable/disable rule
│       └── create_automation_rule.py   # Create simple rule
│
└── tests/
    ├── conftest.py
    ├── test_project_management.py
    ├── test_user_management.py
    ├── test_permission_schemes.py
    ├── test_workflow_management.py
    ├── test_scheme_management.py
    └── test_automation_rules.py
```

---

## Phase 1: Project Management

### Feature 1.1: Create Project

**Script:** `create_project.py`

**JIRA API:**
- `POST /rest/api/3/project` - Create project
- `GET /rest/api/3/project/type` - Get project types

**Test File:** `tests/test_project_management.py`

**Test Cases:**
```python
def test_create_project_basic():
    """Test creating project with minimal fields"""

def test_create_project_with_template():
    """Test creating project from template"""

def test_create_project_scrum():
    """Test creating Scrum board project"""

def test_create_project_kanban():
    """Test creating Kanban board project"""

def test_create_project_with_lead():
    """Test setting project lead"""

def test_create_project_with_category():
    """Test setting project category"""

def test_create_project_with_permission_scheme():
    """Test assigning permission scheme on creation"""

def test_create_project_invalid_key():
    """Test validation of project key"""

def test_create_project_duplicate_key():
    """Test error for duplicate project key"""
```

**CLI Interface:**
```bash
# Basic project creation
python create_project.py --key PROJ --name "My Project" --type software

# Create Scrum project
python create_project.py --key PROJ --name "My Project" --template scrum

# Create Kanban project
python create_project.py --key PROJ --name "My Project" --template kanban

# With lead and category
python create_project.py --key PROJ --name "My Project" --lead john.doe --category "Engineering"

# With permission scheme
python create_project.py --key PROJ --name "My Project" --permission-scheme "Developer Scheme"

# Dry run
python create_project.py --key PROJ --name "My Project" --dry-run
```

**Acceptance Criteria:**
- [ ] All 9 tests pass
- [ ] Supports software/business project types
- [ ] Supports Scrum/Kanban templates
- [ ] Validates project key format

---

### Feature 1.2: Get Project Details

**Script:** `get_project.py`

**Test Cases:**
```python
def test_get_project_basic():
    """Test getting project details"""

def test_get_project_with_components():
    """Test including components in output"""

def test_get_project_with_versions():
    """Test including versions in output"""

def test_get_project_with_schemes():
    """Test including assigned schemes"""

def test_get_project_not_found():
    """Test error handling for invalid project"""
```

**CLI Interface:**
```bash
# Get project details
python get_project.py PROJ

# Include components and versions
python get_project.py PROJ --include-components --include-versions

# Include all schemes
python get_project.py PROJ --include-schemes

# Output as JSON
python get_project.py PROJ --output json
```

---

### Feature 1.3: Update Project

**Script:** `update_project.py`

**Test Cases:**
```python
def test_update_project_name():
    """Test updating project name"""

def test_update_project_lead():
    """Test changing project lead"""

def test_update_project_description():
    """Test updating description"""

def test_update_project_category():
    """Test changing category"""

def test_update_project_url():
    """Test setting project URL"""
```

**CLI Interface:**
```bash
python update_project.py PROJ --name "New Project Name"
python update_project.py PROJ --lead jane.doe
python update_project.py PROJ --description "Updated description"
python update_project.py PROJ --category "DevOps"
```

---

### Feature 1.4: Delete/Archive Project

**Scripts:** `delete_project.py`, `archive_project.py`

**Test Cases:**
```python
def test_delete_project_with_confirm():
    """Test deleting project with confirmation"""

def test_delete_project_requires_confirm():
    """Test confirmation is required"""

def test_archive_project():
    """Test archiving project"""

def test_restore_project():
    """Test restoring archived project"""
```

**CLI Interface:**
```bash
# Delete (requires confirmation)
python delete_project.py PROJ --confirm

# Archive
python archive_project.py PROJ

# Restore
python archive_project.py PROJ --restore
```

---

### Feature 1.5: List Projects

**Script:** `list_projects.py`

**Test Cases:**
```python
def test_list_projects_all():
    """Test listing all projects"""

def test_list_projects_by_type():
    """Test filtering by project type"""

def test_list_projects_by_category():
    """Test filtering by category"""

def test_list_projects_archived():
    """Test including archived projects"""
```

**CLI Interface:**
```bash
python list_projects.py
python list_projects.py --type software
python list_projects.py --category "Engineering"
python list_projects.py --include-archived
```

---

### Phase 1 Completion

- [ ] **Phase 1 Summary:**
  - [ ] 7 scripts implemented
  - [ ] 27 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-admin): complete Phase 1 - Project Management`

---

## Phase 2: User & Group Management

### Feature 2.1: Search Users

**Script:** `search_users.py`

**JIRA API:**
- `GET /rest/api/3/user/search` - Search users
- `GET /rest/api/3/user/assignable/search` - Assignable users

**Test Cases:**
```python
def test_search_users_by_query():
    """Test searching users by query string"""

def test_search_users_by_email():
    """Test searching by email"""

def test_search_users_assignable():
    """Test finding assignable users for project"""

def test_search_users_active_only():
    """Test filtering to active users only"""

def test_search_users_with_groups():
    """Test including group membership"""
```

**CLI Interface:**
```bash
# Search by name/email
python search_users.py "john"

# Search assignable for project
python search_users.py "john" --project PROJ --assignable

# Active users only
python search_users.py "john" --active-only

# Include group membership
python search_users.py "john" --include-groups
```

---

### Feature 2.2: Get User Details

**Script:** `get_user.py`

**Test Cases:**
```python
def test_get_user_by_account_id():
    """Test getting user by account ID"""

def test_get_user_by_email():
    """Test getting user by email"""

def test_get_user_with_groups():
    """Test including group membership"""

def test_get_current_user():
    """Test getting current user info"""
```

**CLI Interface:**
```bash
python get_user.py "john@example.com"
python get_user.py --account-id "abc123"
python get_user.py --me  # Current user
python get_user.py "john" --include-groups
```

---

### Feature 2.3: Group Operations

**Scripts:** `list_groups.py`, `get_group_members.py`, `add_user_to_group.py`, `remove_user_from_group.py`, `create_group.py`, `delete_group.py`

**Test Cases:**
```python
def test_list_groups():
    """Test listing all groups"""

def test_get_group_members():
    """Test getting group members"""

def test_add_user_to_group():
    """Test adding user to group"""

def test_remove_user_from_group():
    """Test removing user from group"""

def test_create_group():
    """Test creating group"""

def test_delete_group():
    """Test deleting group"""
```

**CLI Interface:**
```bash
# List groups
python list_groups.py

# Get members
python get_group_members.py "developers"

# Add user
python add_user_to_group.py "john@example.com" --group "developers"

# Remove user
python remove_user_from_group.py "john@example.com" --group "developers"

# Create group
python create_group.py "new-team"

# Delete group
python delete_group.py "old-team" --confirm
```

---

### Phase 2 Completion

- [ ] **Phase 2 Summary:**
  - [ ] 8 scripts implemented
  - [ ] 15 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-admin): complete Phase 2 - User & Group Management`

---

## Phase 3: Permission Schemes

### Feature 3.1: Permission Scheme Operations

**Scripts:** `list_permission_schemes.py`, `get_permission_scheme.py`, `create_permission_scheme.py`, `update_permission_scheme.py`, `assign_permission_scheme.py`

**JIRA API:**
- `GET /rest/api/3/permissionscheme` - List schemes
- `POST /rest/api/3/permissionscheme` - Create scheme
- `PUT /rest/api/3/project/{projectKeyOrId}/permissionscheme` - Assign scheme

**Test Cases:**
```python
def test_list_permission_schemes():
    """Test listing all permission schemes"""

def test_get_permission_scheme():
    """Test getting scheme details with grants"""

def test_create_permission_scheme():
    """Test creating permission scheme"""

def test_add_permission_grant():
    """Test adding permission grant to scheme"""

def test_assign_permission_scheme():
    """Test assigning scheme to project"""
```

**CLI Interface:**
```bash
# List schemes
python list_permission_schemes.py

# Get scheme details
python get_permission_scheme.py "Developer Scheme"

# Create scheme
python create_permission_scheme.py --name "Custom Scheme" --description "Custom permissions"

# Assign to project
python assign_permission_scheme.py --project PROJ --scheme "Custom Scheme"
```

---

### Phase 3 Completion

- [ ] **Phase 3 Summary:**
  - [ ] 5 scripts implemented
  - [ ] 10 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-admin): complete Phase 3 - Permission Schemes`

---

## Phase 4: Workflow Management

### Feature 4.1: Workflow Operations

**Scripts:** `list_workflows.py`, `get_workflow.py`, `list_workflow_schemes.py`, `get_workflow_scheme.py`, `assign_workflow_scheme.py`

**JIRA API:**
- `GET /rest/api/3/workflow` - List workflows
- `GET /rest/api/3/workflowscheme` - List workflow schemes

**Test Cases:**
```python
def test_list_workflows():
    """Test listing all workflows"""

def test_get_workflow_details():
    """Test getting workflow with statuses and transitions"""

def test_list_workflow_schemes():
    """Test listing workflow schemes"""

def test_get_workflow_scheme():
    """Test getting scheme with issue type mappings"""

def test_assign_workflow_scheme():
    """Test assigning workflow scheme to project"""
```

**CLI Interface:**
```bash
# List workflows
python list_workflows.py

# Get workflow details
python get_workflow.py "Software Development Workflow"

# List workflow schemes
python list_workflow_schemes.py

# Get workflow scheme
python get_workflow_scheme.py "Software Development Scheme"

# Assign to project
python assign_workflow_scheme.py --project PROJ --scheme "Software Development Scheme"
```

---

### Phase 4 Completion

- [ ] **Phase 4 Summary:**
  - [ ] 5 scripts implemented
  - [ ] 10 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-admin): complete Phase 4 - Workflow Management`

---

## Phase 5: Scheme Management

### Feature 5.1: Issue Type Schemes

**Scripts:** `list_issue_type_schemes.py`, `get_issue_type_scheme.py`

**Test Cases:**
```python
def test_list_issue_type_schemes():
    """Test listing all issue type schemes"""

def test_get_issue_type_scheme():
    """Test getting scheme with issue types"""
```

---

### Feature 5.2: Notification Schemes

**Scripts:** `list_notification_schemes.py`, `get_notification_scheme.py`

**Test Cases:**
```python
def test_list_notification_schemes():
    """Test listing all notification schemes"""

def test_get_notification_scheme():
    """Test getting scheme with events"""
```

---

### Feature 5.3: Screen Schemes

**Script:** `list_screen_schemes.py`

**Test Cases:**
```python
def test_list_screen_schemes():
    """Test listing all screen schemes"""
```

---

### Phase 5 Completion

- [ ] **Phase 5 Summary:**
  - [ ] 5 scripts implemented
  - [ ] 8 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-admin): complete Phase 5 - Scheme Management`

---

## Phase 6: Automation Rules

### Feature 6.1: Automation Operations

**Scripts:** `list_automation_rules.py`, `get_automation_rule.py`, `enable_automation_rule.py`, `create_automation_rule.py`

**Note:** Automation rules have limited API support. Some operations may require the Automation for JIRA app.

**Test Cases:**
```python
def test_list_automation_rules():
    """Test listing automation rules"""

def test_get_automation_rule():
    """Test getting rule details"""

def test_enable_automation_rule():
    """Test enabling/disabling rule"""

def test_create_simple_rule():
    """Test creating simple automation rule"""
```

**CLI Interface:**
```bash
# List rules
python list_automation_rules.py --project PROJ

# Get rule details
python get_automation_rule.py --rule-id 123

# Enable/disable
python enable_automation_rule.py --rule-id 123 --enable
python enable_automation_rule.py --rule-id 123 --disable

# Create simple rule
python create_automation_rule.py --project PROJ \
  --name "Auto-assign on create" \
  --trigger "issue_created" \
  --action "assign_issue" \
  --action-config '{"assignee": "lead"}'
```

---

### Phase 6 Completion

- [ ] **Phase 6 Summary:**
  - [ ] 4 scripts implemented
  - [ ] 8 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-admin): complete Phase 6 - Automation Rules`

---

## Integration & Polish

### Integration Tasks

- [ ] **Integration 1:** Project setup wizard
  - [ ] Create script that sets up complete project with schemes
  - [ ] Template-based project creation
  - **Commit:** `feat(jira-admin): add project setup wizard`

### Documentation Updates

- [ ] **Docs 1:** Create comprehensive SKILL.md for jira-admin
- [ ] **Docs 2:** Update CLAUDE.md with jira-admin skill
- [ ] **Docs 3:** Update GAP_ANALYSIS.md - Mark administration as complete

---

## Success Metrics

### Completion Criteria

**Tests:**
- [ ] 75+ unit tests passing
- [ ] Coverage ≥ 85%

**Scripts:**
- [ ] 34 new scripts implemented
- [ ] All scripts have `--help`
- [ ] All scripts support `--profile`
- [ ] All mutation scripts have `--dry-run` where applicable

**Documentation:**
- [ ] SKILL.md complete with examples
- [ ] CLAUDE.md updated
- [ ] GAP_ANALYSIS.md updated

---

## Summary Metrics

| Phase | Scripts | Tests | Priority |
|-------|---------|-------|----------|
| 1. Project Management | 7 | 27 | High |
| 2. User & Group Management | 8 | 15 | High |
| 3. Permission Schemes | 5 | 10 | Medium |
| 4. Workflow Management | 5 | 10 | Medium |
| 5. Scheme Management | 5 | 8 | Low |
| 6. Automation Rules | 4 | 8 | Low |
| **TOTAL** | **34** | **78** | - |

---

## Risk Assessment

### Technical Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Admin permissions required | High | Document permission requirements |
| Cloud vs Server API differences | Medium | Test both, document differences |
| Some APIs deprecated in Cloud | Medium | Use latest API versions |
| Automation API limited | High | Document limitations |

### Permission Requirements

Most scripts in this skill require one of:
- **JIRA Administrators** global permission
- **Project Administrator** project permission
- **Administer Projects** project permission

Document these requirements clearly in SKILL.md.

---

**Document Version:** 1.0
**Created:** 2025-12-25
**Status:** Ready for Implementation
