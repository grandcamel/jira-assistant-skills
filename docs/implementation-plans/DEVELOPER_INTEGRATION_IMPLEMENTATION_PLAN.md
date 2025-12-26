# Developer Integration Skill - TDD Implementation Plan

## Overview

**Objective:** Implement comprehensive Git, CI/CD, and developer workflow integration for JIRA using Test-Driven Development (TDD)

**Current Coverage:** 0% (No developer integration exists)

**Target Coverage:** 80%

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
- **Test Location:** `.claude/skills/jira-dev/tests/`

**Feature Priority:**
1. **Phase 1: Git Integration** (Branch & commit linking)
2. **Phase 2: PR Management** (Pull request linking)
3. **Phase 3: CI/CD Integration** (Build status & deployments)
4. **Phase 4: Release Automation** (Release notes & changelogs)
5. **Phase 5: Webhook Management** (Event subscriptions)

---

## Proposed Skill Structure

```
.claude/skills/jira-dev/
├── SKILL.md
├── scripts/
│   ├── # Phase 1: Git Integration
│   ├── create_branch_name.py     # Generate branch name from issue
│   ├── link_commit.py            # Link commit to issue
│   ├── parse_commit_issues.py    # Extract issue keys from commit message
│   ├── get_issue_commits.py      # Get commits linked to issue
│   │
│   ├── # Phase 2: PR Management
│   ├── link_pr.py                # Link pull request to issue
│   ├── get_issue_prs.py          # Get PRs linked to issue
│   ├── create_pr_description.py  # Generate PR description from issue
│   ├── update_issue_from_pr.py   # Update issue based on PR status
│   │
│   ├── # Phase 3: CI/CD Integration
│   ├── link_build.py             # Link CI build to issue
│   ├── get_issue_builds.py       # Get builds for issue
│   ├── mark_deployed.py          # Mark issue as deployed to environment
│   ├── get_deployment_status.py  # Get deployment status for issues
│   │
│   ├── # Phase 4: Release Automation
│   ├── create_release_notes.py   # Generate release notes from issues
│   ├── create_changelog.py       # Generate CHANGELOG from version
│   ├── release_version.py        # Release version and transition issues
│   ├── get_version_issues.py     # Get all issues for version
│   │
│   └── # Phase 5: Webhook Management
│       ├── register_webhook.py   # Register JIRA webhook
│       ├── list_webhooks.py      # List registered webhooks
│       ├── delete_webhook.py     # Delete webhook
│       └── webhook_events.py     # List available webhook events
│
└── tests/
    ├── conftest.py
    ├── test_git_integration.py
    ├── test_pr_management.py
    ├── test_cicd_integration.py
    ├── test_release_automation.py
    └── test_webhook_management.py
```

---

## Phase 1: Git Integration

### Feature 1.1: Create Branch Name

**Script:** `create_branch_name.py`

**Purpose:** Generate consistent branch names from JIRA issue keys and summaries.

**JIRA API:**
- `GET /rest/api/3/issue/{issueIdOrKey}` - Get issue details

**Test File:** `tests/test_git_integration.py`

**Test Cases:**
```python
def test_create_branch_name_basic():
    """Test creating branch name from issue"""
    # PROJ-123: Fix login button → feature/PROJ-123-fix-login-button

def test_create_branch_name_with_prefix():
    """Test custom prefix (feature, bugfix, hotfix)"""
    # --prefix bugfix → bugfix/PROJ-123-fix-login-button

def test_create_branch_name_sanitizes_special_chars():
    """Test removing special characters from summary"""
    # "Fix bug: login (v2)" → fix-bug-login-v2

def test_create_branch_name_max_length():
    """Test truncating long summaries"""
    # Max 50 chars for branch name portion

def test_create_branch_name_lowercase():
    """Test converting to lowercase"""

def test_create_branch_name_issue_type_prefix():
    """Test auto-prefix based on issue type"""
    # Bug → bugfix/, Story → feature/, Task → task/

def test_create_branch_name_output_formats():
    """Test different output formats (text, JSON, git command)"""
```

**CLI Interface:**
```bash
# Basic branch name
python create_branch_name.py PROJ-123
# Output: feature/PROJ-123-fix-login-button

# With custom prefix
python create_branch_name.py PROJ-123 --prefix bugfix
# Output: bugfix/PROJ-123-fix-login-button

# Auto-detect prefix from issue type
python create_branch_name.py PROJ-123 --auto-prefix
# Output: bugfix/PROJ-123-fix-login-button (if Bug type)

# Output as git command
python create_branch_name.py PROJ-123 --output git
# Output: git checkout -b feature/PROJ-123-fix-login-button

# Output as JSON
python create_branch_name.py PROJ-123 --output json
```

**Acceptance Criteria:**
- [ ] All 7 tests pass
- [ ] Generates valid git branch names
- [ ] Sanitizes special characters
- [ ] Configurable prefix
- [ ] Issue type-based auto-prefix

**Commits:**
1. `test(jira-dev): add failing tests for create_branch_name`
2. `feat(jira-dev): implement create_branch_name.py (7/7 tests passing)`

---

### Feature 1.2: Link Commit to Issue

**Script:** `link_commit.py`

**Purpose:** Add a comment linking a commit to a JIRA issue.

**JIRA API:**
- `POST /rest/api/3/issue/{issueIdOrKey}/comment` - Add comment with commit info

**Test Cases:**
```python
def test_link_commit_basic():
    """Test linking commit to issue via comment"""

def test_link_commit_with_repo():
    """Test including repository URL"""

def test_link_commit_with_github_link():
    """Test creating GitHub commit link"""

def test_link_commit_multiple_issues():
    """Test linking same commit to multiple issues"""

def test_link_commit_from_message():
    """Test extracting issues from commit message"""
```

**CLI Interface:**
```bash
# Link specific commit
python link_commit.py PROJ-123 --commit abc123 --repo github.com/org/repo

# Link with message
python link_commit.py PROJ-123 --commit abc123 --message "Fixed authentication"

# Extract from commit message and link
python link_commit.py --from-message "PROJ-123: Fix login bug" --commit abc123
```

---

### Feature 1.3: Parse Commit Issues

**Script:** `parse_commit_issues.py`

**Purpose:** Extract JIRA issue keys from commit messages.

**Test Cases:**
```python
def test_parse_single_issue():
    """Test extracting single issue key"""
    # "PROJ-123: Fix bug" → ["PROJ-123"]

def test_parse_multiple_issues():
    """Test extracting multiple issue keys"""
    # "Fix PROJ-123 and PROJ-456" → ["PROJ-123", "PROJ-456"]

def test_parse_with_prefixes():
    """Test various prefixes (fixes, closes, refs)"""
    # "Fixes PROJ-123" → ["PROJ-123"]

def test_parse_case_insensitive():
    """Test case-insensitive matching"""

def test_parse_filter_by_project():
    """Test filtering by project key"""

def test_parse_from_stdin():
    """Test reading from stdin (git log pipe)"""
```

**CLI Interface:**
```bash
# Parse from argument
python parse_commit_issues.py "PROJ-123: Fix login bug"
# Output: PROJ-123

# Parse from git log
git log --oneline -10 | python parse_commit_issues.py --from-stdin

# Filter by project
git log --oneline | python parse_commit_issues.py --project PROJ

# Output as JSON
python parse_commit_issues.py "Fixes PROJ-123 and PROJ-456" --output json
```

---

### Feature 1.4: Get Issue Commits

**Script:** `get_issue_commits.py`

**Purpose:** Get all commits linked to an issue (via Development Information API).

**JIRA API:**
- `GET /rest/dev-status/latest/issue/detail` - Get development info

**Test Cases:**
```python
def test_get_commits_basic():
    """Test retrieving commits for issue"""

def test_get_commits_with_details():
    """Test including commit message and author"""

def test_get_commits_by_repo():
    """Test filtering by repository"""

def test_get_commits_no_development_info():
    """Test handling when no dev info available"""
```

**CLI Interface:**
```bash
# Get commits for issue
python get_issue_commits.py PROJ-123

# With details
python get_issue_commits.py PROJ-123 --detailed

# Filter by repo
python get_issue_commits.py PROJ-123 --repo "org/repo"
```

---

### Phase 1 Completion

- [ ] **Phase 1 Summary:**
  - [ ] 4 scripts implemented
  - [ ] 23 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dev): complete Phase 1 - Git Integration`

---

## Phase 2: PR Management

### Feature 2.1: Link Pull Request

**Script:** `link_pr.py`

**Purpose:** Link GitHub/GitLab/Bitbucket PR to JIRA issue.

**JIRA API:**
- `POST /rest/api/3/issue/{issueIdOrKey}/comment` - Add PR link as comment
- Remote links API for richer integration

**Test Cases:**
```python
def test_link_pr_github():
    """Test linking GitHub PR"""

def test_link_pr_gitlab():
    """Test linking GitLab MR"""

def test_link_pr_bitbucket():
    """Test linking Bitbucket PR"""

def test_link_pr_with_status():
    """Test including PR status (open, merged, closed)"""

def test_link_pr_as_remote_link():
    """Test creating remote link instead of comment"""

def test_link_pr_auto_transition():
    """Test auto-transitioning issue based on PR state"""
```

**CLI Interface:**
```bash
# Link PR to issue
python link_pr.py PROJ-123 --pr https://github.com/org/repo/pull/456

# Link with auto-transition (move to "In Review" when PR opened)
python link_pr.py PROJ-123 --pr https://github.com/org/repo/pull/456 --transition "In Review"

# Link as remote link (shows in development panel)
python link_pr.py PROJ-123 --pr https://github.com/org/repo/pull/456 --as-remote-link
```

---

### Feature 2.2: Get Issue PRs

**Script:** `get_issue_prs.py`

**Purpose:** Get all pull requests linked to an issue.

**Test Cases:**
```python
def test_get_prs_basic():
    """Test retrieving PRs for issue"""

def test_get_prs_with_status():
    """Test including PR status"""

def test_get_prs_with_reviews():
    """Test including review status"""

def test_get_prs_filter_merged():
    """Test filtering by merged status"""
```

**CLI Interface:**
```bash
python get_issue_prs.py PROJ-123
python get_issue_prs.py PROJ-123 --status merged
python get_issue_prs.py PROJ-123 --include-reviews
```

---

### Feature 2.3: Create PR Description

**Script:** `create_pr_description.py`

**Purpose:** Generate pull request description from JIRA issue details.

**Test Cases:**
```python
def test_create_pr_description_basic():
    """Test generating PR description from issue"""

def test_create_pr_description_template():
    """Test using custom template"""

def test_create_pr_description_checklist():
    """Test including checklist items"""

def test_create_pr_description_linked_issues():
    """Test including linked issues"""

def test_create_pr_description_acceptance_criteria():
    """Test extracting acceptance criteria from description"""
```

**CLI Interface:**
```bash
# Generate PR description
python create_pr_description.py PROJ-123

# Use template
python create_pr_description.py PROJ-123 --template pr_template.md

# Include checklist
python create_pr_description.py PROJ-123 --include-checklist

# Output to clipboard
python create_pr_description.py PROJ-123 --copy
```

**Output Example:**
```markdown
## Summary
Fix login button not responding on mobile devices

## JIRA Issue
[PROJ-123](https://jira.example.com/browse/PROJ-123)

## Changes
- Fixed touch event handling on login button
- Added mobile-specific CSS

## Acceptance Criteria
- [ ] Login button responds to touch on iOS
- [ ] Login button responds to touch on Android

## Testing
- Tested on iPhone 14 and Pixel 7
```

---

### Feature 2.4: Update Issue from PR

**Script:** `update_issue_from_pr.py`

**Purpose:** Update JIRA issue based on PR events (merged, closed, etc.).

**Test Cases:**
```python
def test_update_on_pr_merged():
    """Test transitioning issue when PR merged"""

def test_update_on_pr_closed():
    """Test handling PR closed without merge"""

def test_update_add_comment():
    """Test adding comment on PR events"""

def test_update_set_fix_version():
    """Test setting fix version when merged"""
```

**CLI Interface:**
```bash
# Update issue when PR merged
python update_issue_from_pr.py PROJ-123 --event merged --transition "Done"

# Add comment and transition
python update_issue_from_pr.py PROJ-123 --event merged --comment "Merged in PR #456" --transition "Done"

# Set fix version
python update_issue_from_pr.py PROJ-123 --event merged --fix-version "1.2.0"
```

---

### Phase 2 Completion

- [ ] **Phase 2 Summary:**
  - [ ] 4 scripts implemented
  - [ ] 19 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dev): complete Phase 2 - PR Management`

---

## Phase 3: CI/CD Integration

### Feature 3.1: Link Build

**Script:** `link_build.py`

**Purpose:** Link CI/CD build to JIRA issue.

**Test Cases:**
```python
def test_link_build_basic():
    """Test linking build to issue"""

def test_link_build_with_status():
    """Test including build status (success, failed)"""

def test_link_build_github_actions():
    """Test GitHub Actions format"""

def test_link_build_jenkins():
    """Test Jenkins format"""

def test_link_build_multiple_issues():
    """Test linking build to multiple issues"""
```

**CLI Interface:**
```bash
# Link build
python link_build.py PROJ-123 --build-url https://github.com/org/repo/actions/runs/123

# With status
python link_build.py PROJ-123 --build-url ... --status success --build-number 456

# From commit (extract issues)
python link_build.py --from-commit "PROJ-123: Fix bug" --build-url ... --status success
```

---

### Feature 3.2: Get Issue Builds

**Script:** `get_issue_builds.py`

**Purpose:** Get all builds associated with an issue.

**Test Cases:**
```python
def test_get_builds_basic():
    """Test retrieving builds for issue"""

def test_get_builds_filter_status():
    """Test filtering by build status"""

def test_get_builds_latest():
    """Test getting only latest build"""
```

---

### Feature 3.3: Mark Deployed

**Script:** `mark_deployed.py`

**Purpose:** Mark issue as deployed to an environment.

**Test Cases:**
```python
def test_mark_deployed_basic():
    """Test marking issue as deployed"""

def test_mark_deployed_environment():
    """Test specifying environment (dev, staging, prod)"""

def test_mark_deployed_version():
    """Test including version number"""

def test_mark_deployed_add_label():
    """Test adding deployment label"""

def test_mark_deployed_transition():
    """Test transitioning to deployed status"""
```

**CLI Interface:**
```bash
# Mark deployed
python mark_deployed.py PROJ-123 --environment production

# With version
python mark_deployed.py PROJ-123 --environment staging --version "1.2.0"

# Transition and add label
python mark_deployed.py PROJ-123 --environment production --transition "Released" --label "deployed-prod"

# Mark multiple issues
python mark_deployed.py PROJ-123,PROJ-124,PROJ-125 --environment production
```

---

### Feature 3.4: Get Deployment Status

**Script:** `get_deployment_status.py`

**Purpose:** Get deployment status for issues.

**Test Cases:**
```python
def test_get_deployment_status_single():
    """Test getting deployment status for issue"""

def test_get_deployment_status_version():
    """Test getting deployment status for version"""

def test_get_deployment_status_not_deployed():
    """Test handling undeployed issues"""
```

**CLI Interface:**
```bash
# Get deployment status
python get_deployment_status.py PROJ-123

# Check if version is deployed
python get_deployment_status.py --version "1.2.0" --project PROJ

# Check multiple issues
python get_deployment_status.py --jql "fixVersion='1.2.0' AND project=PROJ"
```

---

### Phase 3 Completion

- [ ] **Phase 3 Summary:**
  - [ ] 4 scripts implemented
  - [ ] 16 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dev): complete Phase 3 - CI/CD Integration`

---

## Phase 4: Release Automation

### Feature 4.1: Create Release Notes

**Script:** `create_release_notes.py`

**Purpose:** Generate release notes from JIRA issues in a version.

**Test Cases:**
```python
def test_create_release_notes_basic():
    """Test generating release notes from version"""

def test_create_release_notes_grouped():
    """Test grouping by issue type"""

def test_create_release_notes_template():
    """Test using custom template"""

def test_create_release_notes_exclude_types():
    """Test excluding certain issue types"""

def test_create_release_notes_include_links():
    """Test including JIRA links"""

def test_create_release_notes_markdown():
    """Test Markdown output format"""
```

**CLI Interface:**
```bash
# Generate release notes
python create_release_notes.py --project PROJ --version "1.2.0"

# Group by issue type
python create_release_notes.py --project PROJ --version "1.2.0" --group-by-type

# Use template
python create_release_notes.py --project PROJ --version "1.2.0" --template release_notes.md

# Output to file
python create_release_notes.py --project PROJ --version "1.2.0" --output RELEASE_NOTES.md

# Exclude certain types
python create_release_notes.py --project PROJ --version "1.2.0" --exclude-types "Sub-task,Task"
```

**Output Example:**
```markdown
# Release Notes - Version 1.2.0

## New Features
- [PROJ-101](https://jira.example.com/browse/PROJ-101) - Add dark mode support
- [PROJ-102](https://jira.example.com/browse/PROJ-102) - Implement user preferences

## Bug Fixes
- [PROJ-103](https://jira.example.com/browse/PROJ-103) - Fix login timeout issue
- [PROJ-104](https://jira.example.com/browse/PROJ-104) - Resolve memory leak in dashboard

## Improvements
- [PROJ-105](https://jira.example.com/browse/PROJ-105) - Optimize database queries
```

---

### Feature 4.2: Create Changelog

**Script:** `create_changelog.py`

**Purpose:** Generate CHANGELOG.md from JIRA versions.

**Test Cases:**
```python
def test_create_changelog_basic():
    """Test generating changelog"""

def test_create_changelog_multiple_versions():
    """Test including multiple versions"""

def test_create_changelog_keep_existing():
    """Test appending to existing CHANGELOG"""

def test_create_changelog_semver_order():
    """Test ordering by semantic version"""
```

**CLI Interface:**
```bash
# Generate changelog for latest version
python create_changelog.py --project PROJ --version "1.2.0"

# Generate changelog for all released versions
python create_changelog.py --project PROJ --all-released

# Append to existing
python create_changelog.py --project PROJ --version "1.2.0" --output CHANGELOG.md --append
```

---

### Feature 4.3: Release Version

**Script:** `release_version.py`

**Purpose:** Release a version and optionally transition all issues.

**Test Cases:**
```python
def test_release_version_basic():
    """Test releasing version"""

def test_release_version_with_transition():
    """Test transitioning issues on release"""

def test_release_version_set_date():
    """Test setting release date"""

def test_release_version_create_next():
    """Test creating next version"""

def test_release_version_dry_run():
    """Test dry-run preview"""
```

**CLI Interface:**
```bash
# Release version
python release_version.py --project PROJ --version "1.2.0"

# Release and transition issues
python release_version.py --project PROJ --version "1.2.0" --transition-issues "Released"

# Release with date
python release_version.py --project PROJ --version "1.2.0" --release-date "2025-01-20"

# Release and create next version
python release_version.py --project PROJ --version "1.2.0" --create-next "1.3.0"

# Dry run
python release_version.py --project PROJ --version "1.2.0" --dry-run
```

---

### Feature 4.4: Get Version Issues

**Script:** `get_version_issues.py`

**Purpose:** Get all issues for a version with summary.

**Test Cases:**
```python
def test_get_version_issues_basic():
    """Test getting issues for version"""

def test_get_version_issues_summary():
    """Test version summary (counts by type/status)"""

def test_get_version_issues_grouped():
    """Test grouping by type"""
```

**CLI Interface:**
```bash
# Get issues for version
python get_version_issues.py --project PROJ --version "1.2.0"

# Get summary only
python get_version_issues.py --project PROJ --version "1.2.0" --summary

# Group by type
python get_version_issues.py --project PROJ --version "1.2.0" --group-by type
```

---

### Phase 4 Completion

- [ ] **Phase 4 Summary:**
  - [ ] 4 scripts implemented
  - [ ] 17 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dev): complete Phase 4 - Release Automation`

---

## Phase 5: Webhook Management

### Feature 5.1: Register Webhook

**Script:** `register_webhook.py`

**Purpose:** Register JIRA webhooks for event notifications.

**JIRA API:**
- `POST /rest/api/3/webhook` - Register webhook

**Test Cases:**
```python
def test_register_webhook_basic():
    """Test registering webhook"""

def test_register_webhook_with_events():
    """Test specifying events"""

def test_register_webhook_with_jql_filter():
    """Test filtering by JQL"""

def test_register_webhook_with_project():
    """Test filtering by project"""
```

**CLI Interface:**
```bash
# Register webhook
python register_webhook.py --url https://api.example.com/webhook --events issue_created,issue_updated

# With JQL filter
python register_webhook.py --url https://api.example.com/webhook --jql "project=PROJ"

# For specific project
python register_webhook.py --url https://api.example.com/webhook --project PROJ --events issue_created
```

---

### Feature 5.2: List Webhooks

**Script:** `list_webhooks.py`

**Purpose:** List registered webhooks.

**Test Cases:**
```python
def test_list_webhooks_all():
    """Test listing all webhooks"""

def test_list_webhooks_by_url():
    """Test filtering by URL"""
```

---

### Feature 5.3: Delete Webhook

**Script:** `delete_webhook.py`

**Purpose:** Delete a registered webhook.

**Test Cases:**
```python
def test_delete_webhook_by_id():
    """Test deleting webhook by ID"""

def test_delete_webhook_confirm():
    """Test confirmation required"""
```

---

### Feature 5.4: Webhook Events

**Script:** `webhook_events.py`

**Purpose:** List available webhook events.

**Test Cases:**
```python
def test_list_events_all():
    """Test listing all available events"""

def test_list_events_by_category():
    """Test filtering by category (issue, sprint, etc.)"""
```

---

### Phase 5 Completion

- [ ] **Phase 5 Summary:**
  - [ ] 4 scripts implemented
  - [ ] 8 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dev): complete Phase 5 - Webhook Management`

---

## Integration & Polish

### Integration Tasks

- [ ] **Integration 1:** Git hooks
  - [ ] Create pre-commit hook for issue key validation
  - [ ] Create commit-msg hook for issue key extraction
  - **Commit:** `feat(jira-dev): add git hooks integration`

- [ ] **Integration 2:** CI/CD templates
  - [ ] GitHub Actions workflow template
  - [ ] GitLab CI template
  - [ ] Jenkins pipeline template
  - **Commit:** `feat(jira-dev): add CI/CD pipeline templates`

### Documentation Updates

- [ ] **Docs 1:** Create comprehensive SKILL.md for jira-dev
- [ ] **Docs 2:** Update CLAUDE.md with jira-dev skill
- [ ] **Docs 3:** Update GAP_ANALYSIS.md - Mark developer integration as complete

---

## Success Metrics

### Completion Criteria

**Tests:**
- [ ] 80+ unit tests passing
- [ ] 5+ integration tests passing
- [ ] Coverage ≥ 85%

**Scripts:**
- [ ] 20 new scripts implemented
- [ ] All scripts have `--help`
- [ ] All scripts support `--profile`

**Documentation:**
- [ ] SKILL.md complete with examples
- [ ] CLAUDE.md updated
- [ ] GAP_ANALYSIS.md updated

---

## Summary Metrics

| Phase | Scripts | Tests | Priority |
|-------|---------|-------|----------|
| 1. Git Integration | 4 | 23 | Critical |
| 2. PR Management | 4 | 19 | High |
| 3. CI/CD Integration | 4 | 16 | High |
| 4. Release Automation | 4 | 17 | High |
| 5. Webhook Management | 4 | 8 | Medium |
| **TOTAL** | **20** | **83** | - |

---

## Risk Assessment

### Technical Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Development Information API requires DVCS connector | High | Document setup requirements |
| Different VCS providers have different APIs | Medium | Abstract common operations |
| Webhook registration requires admin permissions | Medium | Document permission requirements |
| Release notes format varies by team | Low | Template-based approach |

### External Dependencies
- GitHub/GitLab/Bitbucket integration app in JIRA
- Webhook endpoints need to be publicly accessible
- Development Information API needs DVCS connector

---

**Document Version:** 1.0
**Created:** 2025-12-25
**Status:** Ready for Implementation
