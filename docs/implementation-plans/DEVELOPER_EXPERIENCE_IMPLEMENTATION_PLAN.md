# Developer Experience Skill - TDD Implementation Plan

## Overview

**Objective:** Implement developer experience enhancements including interactive mode, fuzzy search, recent items cache, command aliases, shell completion, and IDE integration using Test-Driven Development (TDD)

**Current Coverage:** 0% (No developer experience features exist)

**Target Coverage:** 75%

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
- **Test Location:** `.claude/skills/jira-dx/tests/`

**Feature Priority:**
1. **Phase 1: Recent Items Cache** (Quick access to recent issues)
2. **Phase 2: Fuzzy Search** (Autocomplete and suggestions)
3. **Phase 3: Smart Defaults** (Learn from user behavior)
4. **Phase 4: Command Aliases** (Short commands)
5. **Phase 5: Shell Completion** (Bash/zsh integration)
6. **Phase 6: Interactive Mode** (TUI workflows)

---

## Proposed Skill Structure

```
.claude/skills/jira-dx/
├── SKILL.md
├── scripts/
│   ├── # Phase 1: Recent Items Cache
│   ├── recent.py                  # Show/manage recent items
│   ├── history.py                 # Command history
│   │
│   ├── # Phase 2: Fuzzy Search
│   ├── suggest_projects.py        # Project autocomplete
│   ├── suggest_users.py           # User autocomplete
│   ├── suggest_issues.py          # Issue autocomplete
│   ├── suggest_fields.py          # Field autocomplete
│   │
│   ├── # Phase 3: Smart Defaults
│   ├── set_default.py             # Set default values
│   ├── get_defaults.py            # Get current defaults
│   ├── learn_defaults.py          # Learn from usage
│   │
│   ├── # Phase 4: Command Aliases
│   ├── alias.py                   # Manage aliases
│   ├── run_alias.py               # Run aliased command
│   │
│   ├── # Phase 5: Shell Completion
│   ├── generate_completions.py    # Generate completion scripts
│   ├── complete.py                # Completion handler
│   │
│   └── # Phase 6: Interactive Mode
│       ├── interactive.py         # TUI main entry
│       ├── quick_create.py        # Quick issue creation wizard
│       └── quick_search.py        # Quick search interface
│
├── lib/
│   ├── cache.py                   # Caching utilities
│   ├── fuzzy.py                   # Fuzzy matching utilities
│   ├── defaults.py                # Smart defaults manager
│   ├── aliases.py                 # Alias manager
│   └── completions.py             # Completion generator
│
└── tests/
    ├── conftest.py
    ├── test_recent_items.py
    ├── test_fuzzy_search.py
    ├── test_smart_defaults.py
    ├── test_aliases.py
    ├── test_shell_completion.py
    └── test_interactive.py
```

---

## Phase 1: Recent Items Cache

### Feature 1.1: Recent Issues

**Script:** `recent.py`

**Purpose:** Quick access to recently viewed/modified issues.

**Storage:** `~/.jira-skills/recent.json`

**Test File:** `tests/test_recent_items.py`

**Test Cases:**
```python
def test_record_recent_issue():
    """Test recording recently accessed issue"""

def test_get_recent_issues():
    """Test retrieving recent issues"""

def test_recent_issues_max_limit():
    """Test maximum items limit (default 50)"""

def test_recent_issues_by_project():
    """Test filtering by project"""

def test_recent_issues_by_action():
    """Test filtering by action (view, edit, create)"""

def test_recent_issues_clear():
    """Test clearing recent items"""

def test_recent_issues_persistence():
    """Test persistence across sessions"""

def test_recent_issues_with_preview():
    """Test including issue preview"""
```

**CLI Interface:**
```bash
# Show recent issues
python recent.py
# Output:
# Recent Issues:
# 1. PROJ-123 - Fix login button [viewed 5m ago]
# 2. PROJ-456 - Add dark mode [edited 1h ago]
# 3. DEV-789 - Update docs [created 2h ago]

# Filter by project
python recent.py --project PROJ

# Filter by action
python recent.py --action edited

# Clear recent
python recent.py --clear

# Set max items
python recent.py --max 20

# Output as JSON
python recent.py --output json
```

**Acceptance Criteria:**
- [ ] All 8 tests pass
- [ ] Persists across sessions
- [ ] Configurable max items
- [ ] Quick access numbers (1-9)

---

### Feature 1.2: Command History

**Script:** `history.py`

**Purpose:** Track and replay command history.

**Storage:** `~/.jira-skills/history.json`

**Test Cases:**
```python
def test_record_command():
    """Test recording executed command"""

def test_get_history():
    """Test retrieving command history"""

def test_search_history():
    """Test searching command history"""

def test_replay_command():
    """Test replaying command from history"""

def test_history_max_limit():
    """Test maximum history limit"""
```

**CLI Interface:**
```bash
# Show history
python history.py
# Output:
# 1. jql_search.py "project=PROJ" [5m ago]
# 2. create_issue.py --project PROJ --type Bug [1h ago]
# 3. transition_issue.py PROJ-123 --to Done [2h ago]

# Search history
python history.py --search "create"

# Replay command
python history.py --replay 2

# Clear history
python history.py --clear
```

---

### Phase 1 Completion

- [ ] **Phase 1 Summary:**
  - [ ] 2 scripts implemented
  - [ ] 13 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dx): complete Phase 1 - Recent Items Cache`

---

## Phase 2: Fuzzy Search & Autocomplete

### Feature 2.1: Project Suggestions

**Script:** `suggest_projects.py`

**Purpose:** Autocomplete project names/keys.

**Test Cases:**
```python
def test_suggest_project_by_key():
    """Test suggesting by key prefix"""
    # "PRO" → ["PROJ", "PRODUCT", "PROTO"]

def test_suggest_project_by_name():
    """Test suggesting by name substring"""
    # "mobile" → ["Mobile App", "Mobile Backend"]

def test_suggest_project_fuzzy():
    """Test fuzzy matching"""
    # "prj" → ["PROJ"] (fuzzy match)

def test_suggest_project_ranked():
    """Test ranking by usage frequency"""

def test_suggest_project_cached():
    """Test caching of project list"""
```

**CLI Interface:**
```bash
# Suggest projects
python suggest_projects.py "pro"
# Output:
# PROJ - Project Management
# PRODUCT - Product Development
# PROTO - Prototypes

# With recent first
python suggest_projects.py "pro" --recent-first

# Output for shell completion
python suggest_projects.py "pro" --shell
```

---

### Feature 2.2: User Suggestions

**Script:** `suggest_users.py`

**Test Cases:**
```python
def test_suggest_user_by_name():
    """Test suggesting by display name"""

def test_suggest_user_by_email():
    """Test suggesting by email"""

def test_suggest_user_assignable():
    """Test filtering to assignable users"""

def test_suggest_user_recent():
    """Test prioritizing recently used users"""
```

**CLI Interface:**
```bash
python suggest_users.py "john"
python suggest_users.py "john" --project PROJ --assignable
```

---

### Feature 2.3: Issue Suggestions

**Script:** `suggest_issues.py`

**Test Cases:**
```python
def test_suggest_issue_by_key():
    """Test suggesting by key"""
    # "PROJ-12" → ["PROJ-123", "PROJ-124", "PROJ-125"]

def test_suggest_issue_by_summary():
    """Test suggesting by summary text"""

def test_suggest_issue_recent():
    """Test prioritizing recent issues"""

def test_suggest_issue_smart():
    """Test smart suggestions based on context"""
```

**CLI Interface:**
```bash
python suggest_issues.py "PROJ-12"
python suggest_issues.py "login bug" --project PROJ
```

---

### Feature 2.4: Field Suggestions

**Script:** `suggest_fields.py`

**Test Cases:**
```python
def test_suggest_field_by_name():
    """Test suggesting fields by name"""

def test_suggest_field_values():
    """Test suggesting field values"""

def test_suggest_field_for_project():
    """Test project-specific fields"""
```

**CLI Interface:**
```bash
python suggest_fields.py "prio"
# Output: Priority, Priority Score

python suggest_fields.py --field Priority --values
# Output: Blocker, Critical, High, Medium, Low
```

---

### Phase 2 Completion

- [ ] **Phase 2 Summary:**
  - [ ] 4 scripts implemented
  - [ ] 16 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dx): complete Phase 2 - Fuzzy Search`

---

## Phase 3: Smart Defaults

### Feature 3.1: Manage Defaults

**Scripts:** `set_default.py`, `get_defaults.py`

**Purpose:** Remember user preferences and common values.

**Storage:** `~/.jira-skills/defaults.json`

**Test Cases:**
```python
def test_set_default_project():
    """Test setting default project"""

def test_set_default_issue_type():
    """Test setting default issue type"""

def test_set_default_assignee():
    """Test setting default assignee"""

def test_get_defaults():
    """Test getting all defaults"""

def test_get_default_for_project():
    """Test project-specific defaults"""

def test_clear_defaults():
    """Test clearing defaults"""
```

**CLI Interface:**
```bash
# Set defaults
python set_default.py --project PROJ
python set_default.py --issue-type Bug
python set_default.py --assignee self

# Project-specific defaults
python set_default.py --for-project PROJ --issue-type Story

# Get defaults
python get_defaults.py
# Output:
# Global Defaults:
#   project: PROJ
#   issue_type: Bug
#   assignee: self
#
# Project: PROJ
#   issue_type: Story

# Clear
python set_default.py --clear
```

---

### Feature 3.2: Learn Defaults

**Script:** `learn_defaults.py`

**Purpose:** Automatically learn defaults from usage patterns.

**Test Cases:**
```python
def test_learn_from_create():
    """Test learning from create operations"""

def test_learn_most_frequent():
    """Test identifying most frequent values"""

def test_learn_by_context():
    """Test learning context-specific defaults"""

def test_suggest_from_learned():
    """Test suggesting learned values"""
```

**CLI Interface:**
```bash
# Enable learning
python learn_defaults.py --enable

# Show learned patterns
python learn_defaults.py --show

# Apply learned defaults
python learn_defaults.py --apply
```

---

### Phase 3 Completion

- [ ] **Phase 3 Summary:**
  - [ ] 3 scripts implemented
  - [ ] 10 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dx): complete Phase 3 - Smart Defaults`

---

## Phase 4: Command Aliases

### Feature 4.1: Alias Management

**Script:** `alias.py`

**Purpose:** Create short aliases for common commands.

**Storage:** `~/.jira-skills/aliases.json`

**Test Cases:**
```python
def test_create_alias():
    """Test creating command alias"""

def test_list_aliases():
    """Test listing all aliases"""

def test_delete_alias():
    """Test deleting alias"""

def test_alias_with_parameters():
    """Test alias with parameter placeholders"""

def test_alias_expansion():
    """Test expanding alias to full command"""
```

**CLI Interface:**
```bash
# Create alias
python alias.py add "mybug" "create_issue.py --project PROJ --type Bug"

# With parameters
python alias.py add "bug" "create_issue.py --project {1} --type Bug --summary '{2}'"

# List aliases
python alias.py list
# Output:
# mybug → create_issue.py --project PROJ --type Bug
# bug   → create_issue.py --project {1} --type Bug --summary '{2}'

# Delete alias
python alias.py delete "mybug"

# Show expansion
python alias.py expand "bug" PROJ "Fix login"
# Output: create_issue.py --project PROJ --type Bug --summary 'Fix login'
```

---

### Feature 4.2: Run Alias

**Script:** `run_alias.py`

**Purpose:** Execute aliased commands.

**Test Cases:**
```python
def test_run_alias_simple():
    """Test running simple alias"""

def test_run_alias_with_args():
    """Test running alias with arguments"""

def test_run_alias_not_found():
    """Test error for unknown alias"""
```

**CLI Interface:**
```bash
# Run alias
python run_alias.py mybug

# Run with parameters
python run_alias.py bug PROJ "Fix login button"
```

---

### Phase 4 Completion

- [ ] **Phase 4 Summary:**
  - [ ] 2 scripts implemented
  - [ ] 8 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dx): complete Phase 4 - Command Aliases`

---

## Phase 5: Shell Completion

### Feature 5.1: Generate Completions

**Script:** `generate_completions.py`

**Purpose:** Generate shell completion scripts for bash/zsh.

**Test Cases:**
```python
def test_generate_bash_completion():
    """Test generating bash completion script"""

def test_generate_zsh_completion():
    """Test generating zsh completion script"""

def test_generate_fish_completion():
    """Test generating fish completion script"""

def test_completion_includes_options():
    """Test that completions include command options"""

def test_completion_includes_subcommands():
    """Test that completions include subcommands"""
```

**CLI Interface:**
```bash
# Generate bash completion
python generate_completions.py --shell bash > ~/.jira-skills/completions.bash
# Add to .bashrc: source ~/.jira-skills/completions.bash

# Generate zsh completion
python generate_completions.py --shell zsh > ~/.jira-skills/_jira

# Install globally
python generate_completions.py --install bash
python generate_completions.py --install zsh
```

**Completion Script Features:**
```bash
# After installation:
jira <TAB>         # Shows: create, search, get, transition, ...
jira create --<TAB> # Shows: --project, --type, --summary, ...
jira create --project <TAB>  # Shows project suggestions
jira create --type <TAB>     # Shows: Bug, Story, Task, Epic, ...
```

---

### Feature 5.2: Completion Handler

**Script:** `complete.py`

**Purpose:** Handle completion requests from shell.

**Test Cases:**
```python
def test_complete_command():
    """Test completing command names"""

def test_complete_options():
    """Test completing command options"""

def test_complete_values():
    """Test completing option values"""
```

**CLI Interface:**
```bash
# Called by shell completion
python complete.py --word "crea" --line "jira crea"
# Output: create

python complete.py --word "" --line "jira create --project "
# Output: PROJ\nDEV\nTEST
```

---

### Phase 5 Completion

- [ ] **Phase 5 Summary:**
  - [ ] 2 scripts implemented
  - [ ] 8 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dx): complete Phase 5 - Shell Completion`

---

## Phase 6: Interactive Mode

### Feature 6.1: Interactive TUI

**Script:** `interactive.py`

**Purpose:** Text-based UI for guided workflows.

**Dependencies:**
- `rich` - Rich text and tables
- `questionary` or `inquirer` - Interactive prompts

**Test Cases:**
```python
def test_interactive_menu():
    """Test showing main menu"""

def test_interactive_create_flow():
    """Test guided create issue flow"""

def test_interactive_search_flow():
    """Test interactive search"""

def test_interactive_keyboard_nav():
    """Test keyboard navigation"""
```

**CLI Interface:**
```bash
# Launch interactive mode
python interactive.py

# Interactive mode with initial action
python interactive.py --action create
python interactive.py --action search
```

**TUI Features:**
```
┌─────────────────────────────────────────┐
│         JIRA Assistant                   │
├─────────────────────────────────────────┤
│  [1] Create Issue                       │
│  [2] Search Issues                      │
│  [3] Recent Issues                      │
│  [4] My Open Issues                     │
│  [5] Quick Transition                   │
│  [q] Quit                               │
└─────────────────────────────────────────┘
```

---

### Feature 6.2: Quick Create Wizard

**Script:** `quick_create.py`

**Purpose:** Guided issue creation with prompts.

**Test Cases:**
```python
def test_quick_create_prompts():
    """Test creation prompts"""

def test_quick_create_validation():
    """Test input validation"""

def test_quick_create_from_template():
    """Test using template"""

def test_quick_create_cancel():
    """Test cancellation handling"""
```

**CLI Interface:**
```bash
python quick_create.py
# Prompts:
# ? Project: [PROJ] (autocomplete)
# ? Issue Type: [Story] (select)
# ? Summary: ___
# ? Description: (optional, opens editor)
# ? Assignee: [self] (autocomplete)
# ? Priority: [Medium] (select)
#
# Preview:
# ┌──────────────────────────────────┐
# │ Project: PROJ                    │
# │ Type: Story                      │
# │ Summary: Fix login button        │
# │ Assignee: John Doe               │
# │ Priority: Medium                 │
# └──────────────────────────────────┘
# ? Create this issue? [Y/n]
```

---

### Feature 6.3: Quick Search Interface

**Script:** `quick_search.py`

**Purpose:** Interactive search with live preview.

**Test Cases:**
```python
def test_quick_search_live():
    """Test live search results"""

def test_quick_search_filters():
    """Test interactive filters"""

def test_quick_search_actions():
    """Test actions on selected issue"""
```

**CLI Interface:**
```bash
python quick_search.py
# ? Search: ___
#
# Results:
# ┌─────────────────────────────────────────────────┐
# │ PROJ-123 [Bug] Fix login button                 │
# │ PROJ-456 [Story] Add dark mode                  │
# │ PROJ-789 [Task] Update documentation            │
# └─────────────────────────────────────────────────┘
#
# [Enter] View  [E] Edit  [T] Transition  [C] Comment
```

---

### Phase 6 Completion

- [ ] **Phase 6 Summary:**
  - [ ] 3 scripts implemented
  - [ ] 10 tests passing
  - [ ] Coverage ≥ 85%
  - **Commit:** `docs(jira-dx): complete Phase 6 - Interactive Mode`

---

## Integration & Polish

### Integration Tasks

- [ ] **Integration 1:** Hook into all scripts
  - [ ] Record recent items on all operations
  - [ ] Track command history
  - [ ] Apply defaults automatically
  - **Commit:** `feat(jira-dx): integrate DX features with all scripts`

- [ ] **Integration 2:** Configuration file
  - [ ] Create `~/.jira-skills/config.yaml`
  - [ ] Store all DX preferences
  - [ ] Profile-specific settings
  - **Commit:** `feat(jira-dx): add unified configuration file`

### Documentation Updates

- [ ] **Docs 1:** Create comprehensive SKILL.md for jira-dx
- [ ] **Docs 2:** Update CLAUDE.md with jira-dx skill
- [ ] **Docs 3:** Update GAP_ANALYSIS.md - Mark developer experience as complete

---

## Success Metrics

### Completion Criteria

**Tests:**
- [ ] 65+ unit tests passing
- [ ] Coverage ≥ 85%

**Scripts:**
- [ ] 16 new scripts implemented
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
| 1. Recent Items Cache | 2 | 13 | High |
| 2. Fuzzy Search | 4 | 16 | High |
| 3. Smart Defaults | 3 | 10 | Medium |
| 4. Command Aliases | 2 | 8 | Medium |
| 5. Shell Completion | 2 | 8 | Medium |
| 6. Interactive Mode | 3 | 10 | Low |
| **TOTAL** | **16** | **65** | - |

---

## Risk Assessment

### Technical Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| TUI library compatibility | Medium | Use well-maintained library (rich) |
| Shell completion complexity | Medium | Focus on bash/zsh first |
| Performance with large caches | Low | Implement cache limits |
| Cross-platform issues | Medium | Test on macOS and Linux |

### Dependencies
- `rich` - Terminal formatting
- `questionary` - Interactive prompts
- `rapidfuzz` - Fuzzy matching

---

**Document Version:** 1.0
**Created:** 2025-12-25
**Status:** Ready for Implementation
