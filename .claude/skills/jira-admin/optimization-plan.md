# Progressive Disclosure Optimization Plan - jira-admin Skill

**Analysis Date:** 2025-12-28
**Analyst:** Code Quality Analyzer
**Skill:** jira-admin (JIRA Administration)

---

## Executive Summary

The jira-admin skill exhibits **significant progressive disclosure violations** that compromise user onboarding and cognitive load. The SKILL.md file is bloated at **1,863 lines (62KB)** containing excessive inline documentation, repeated explanations across 8 major subsystems, and deep nesting of examples. This creates a **Level 2 avalanche** that overwhelms users before they can discover what the skill does.

**Critical Finding:** The skill needs **immediate restructuring** to separate discovery (metadata), learning (main documentation), and reference (detailed guides).

---

## Disclosure Model Violations

### Violation 1: Bloated Frontside Metadata
**Severity:** HIGH
**Location:** Line 3 - SKILL.md description frontmatter

```yaml
description: "JIRA project and system administration - projects, automation rules,
  permissions, users, notifications, screens, issue types, workflows. Use when
  managing projects, configuring automation, or administering JIRA."
```

**Analysis:**
- **Current length:** ~200 chars (compliant)
- **Trigger clarity:** FAIR - Mentions use cases but lacks context
- **Issue:** Description is correct length but provides NO progressive disclosure guidance

**Recommendation:**
```yaml
description: >
  Comprehensive JIRA administration: projects, automation, permissions, users,
  notifications, screens, issue types, and workflows. Use when managing
  project structure, automating workflows, or configuring admin settings.
```

---

### Violation 2: Monolithic SKILL.md (1,863 lines in single file)
**Severity:** CRITICAL
**Impact:** User must scroll through entire document to find relevant information

#### Structural Analysis

| Section | Lines | Content Type | Nesting Depth |
|---------|-------|--------------|---------------|
| Frontmatter | 4 | Metadata | 0 |
| When to Use | 34 | Discovery | 1 |
| What This Skill Does | 59 | Overview | 2 |
| Troubleshooting | 57 | Reference | 2 |
| Available Scripts | ~150 | Index | 3 |
| **Examples (8 major subsystems)** | **~900 lines** | **Detailed usage** | **3-4** |
| Project Management Section | ~125 lines | Subsystem docs | 2-3 |
| Automation Rules Section | ~104 lines | Subsystem docs | 2-3 |
| Permission Schemes Section | ~164 lines | Subsystem docs | 2-3 |
| User & Group Section | ~120 lines | Subsystem docs | 2-3 |
| Notification Schemes Section | ~164 lines | Subsystem docs | 2-3 |
| Screen Management Section | ~196 lines | Subsystem docs | 2-3 |
| Issue Type Management Section | ~135 lines | Subsystem docs | 2-3 |
| Issue Type Schemes Section | ~198 lines | Subsystem docs | 2-3 |
| Workflow Management Section | ~248 lines | Subsystem docs | 2-3 |
| Related Skills | ~15 lines | Cross-reference | 1 |

**Problem:** Each subsystem contains:
1. "When to Use" (repeats skill-level discovery)
2. "What it does" (repeats skill overview)
3. "Scripts" (table format)
4. "Examples" (50-100+ line code blocks)
5. "API Requirements" (technical details)
6. "Limitations" (edge case handling)
7. "Permission Requirements" (access control matrix)
8. "Important Notes" (gotchas and patterns)

**Result:** User must process 10+ levels of nested subsections to find relevant script documentation.

---

### Violation 3: Inline Code Dumps (> 50 lines per section)
**Severity:** MEDIUM-HIGH
**Example Locations:**
- Lines 197-320: Project CRUD examples (~120 lines)
- Lines 423-471: Automation examples (~48 lines)
- Lines 523-563: Permission scheme examples (~40 lines)
- Lines 668-717: User/Group examples (~50 lines)
- Lines 788-914: Notification scheme examples (~127 lines)
- Lines 1038-1143: Screen examples (~105 lines)
- Lines 1199-1280: Issue type examples (~82 lines)
- Lines 1354-1500: Issue type scheme examples (~146 lines)
- Lines 1585-1774: Workflow examples (~189 lines)

**Pattern:** Code blocks in examples section often exceed 50 lines, mixing:
- Basic usage (5-10 lines)
- Advanced usage (20-30 lines)
- Edge cases (10-20 lines)
- All bundled together with minimal separation

**Example - Workflow section:**
```bash
# Lines 1585-1774 contain continuous example blocks
# Many blocks have 20+ lines before showing different variations
# Users must scan entire block to find their use case
```

---

### Violation 4: Deep Nesting (File A → File B → File C)
**Severity:** MEDIUM
**Chain:**
1. **SKILL.md (Level 1):** Discovery + full documentation (1,863 lines)
2. **docs/BEST_PRACTICES.md (Level 2):** 1,021 lines of detailed patterns
3. **assets/templates/ (Level 3):** JSON templates
4. **references/ (implied but not created):** API docs

**Current Nesting Problem:**
```
User discovers skill → Must read entire SKILL.md →
  Link to BEST_PRACTICES.md → 1,000+ more lines →
    May reference templates → May need API docs
```

**What's Missing:**
- No per-subsystem "Getting Started" guide
- No quick reference card in SKILL.md
- No decision tree for choosing scripts
- BEST_PRACTICES is referenced at end (line 1835) but user can't find it mid-document

---

### Violation 5: Missing Triggers & Decision Paths
**Severity:** HIGH

**Location:** Line 10 - "When to Use This Skill" section

**Current Structure:**
```markdown
Use this skill when you need to:
- Create, configure, or delete JIRA projects
- Manage project categories
- Update project settings
- ... (20+ bullet points)
```

**Problem:**
- No decision tree for "I want to do X, which script?"
- No "Typical Workflows" (e.g., "Setting up a new project from scratch")
- No "Common Mistakes" with preventive guidance
- No "Decision Matrix" for complex choices

**Example Gap:**
User wants to "configure project templates" → Which subsystem?
- Project Management? (Line 37)
- Project Configuration? (Line 49)
- Issue Type Schemes? (Line 76)
- Notification Schemes? (Line 60)
- Screen Management? (Line 968)
- Automation Rules? (Line 367)

**Answer:** User must search through entire document.

---

### Violation 6: Repeated "Setup" Content
**Severity:** MEDIUM

**Pattern Found Across Subsystems:**

| Subsystem | "When to Use" Content |
|-----------|---------------------|
| **Project Mgmt** | Line 10-32 (intro) |
| **Automation** | Line 367-391 (repeats trigger types) |
| **Permissions** | Line 499-506 (repeats use cases) |
| **User/Group** | Line 630-638 (repeats discovery) |
| **Notification** | Line 752-772 (repeats event concepts) |
| **Screen** | Line 972-1000 (repeats 3-tier hierarchy) |
| **Issue Types** | Line 1169-1186 (repeats hierarchy) |
| **Issue Type Schemes** | Line 1304-1324 (repeats scheme concept) |
| **Workflow** | Line 1529-1551 (repeats status concepts) |

**Cost:** ~100+ lines of repetitive explanatory content that should be in a single reference section.

---

## Recommended Restructuring

### Phase 1: Extract Supporting Content (Weeks 1-2)

#### 1.1 Create `docs/SUBSYSTEM_GUIDE.md` (Per-subsystem deep dives)
**Purpose:** Move subsystem-specific deep content out of main SKILL.md

**Structure:**
```
docs/
├── BEST_PRACTICES.md (existing - keep)
├── subsystems/
│   ├── project-management-guide.md
│   ├── automation-rules-guide.md
│   ├── permission-schemes-guide.md
│   ├── user-group-guide.md
│   ├── notification-schemes-guide.md
│   ├── screen-management-guide.md
│   ├── issue-types-guide.md
│   ├── issue-type-schemes-guide.md
│   └── workflow-management-guide.md
└── quick-reference.md
```

**Per-Subsystem Guide Content (from SKILL.md):**
- Full "When to Use" section (moved from SKILL.md)
- "Understanding [Concept]" deep dive (3-4KB)
- All examples (50+ lines)
- All "Important Notes" and "Limitations"
- All permission requirements tables
- API requirements details

**Benefit:** SKILL.md shrinks from 1,863 to ~400-500 lines

---

#### 1.2 Create `docs/WORKFLOWS.md` (Common Administration Workflows)
**Purpose:** Decision trees + typical sequences

**Content Structure:**
```markdown
# Common JIRA Administration Workflows

## Setting Up a New Project (5-10 steps)
1. Create project with `create_project.py`
2. Assign project lead with `set_project_lead.py`
3. Configure issue types with `assign_issue_type_scheme.py`
4. Set up notification scheme with `assign_notification_scheme.py`
5. Configure screens with `get_project_screens.py`
6. Add automation rules with `create_rule_from_template.py`
7. Test with `get_config.py --show-schemes`

## Migrating Existing Project to New Workflow
1. List current workflow with `get_workflow_for_issue.py`
2. Review new workflow with `get_workflow.py`
3. Plan status mappings (create JSON)
4. Assign new scheme with `assign_workflow_scheme.py --mappings`
5. Verify with `get_project_screens.py`

## Configuring Notification Rules for Team
1. List existing schemes with `list_notification_schemes.py`
2. Create new scheme with `create_notification_scheme.py`
3. Add event recipients with `add_notification.py`
4. Assign to projects with `assign_notification_scheme.py`
5. Test with team

## Setting Up Permission Tiers
1. List current schemes with `list_permission_schemes.py`
2. Review template with `get_permission_scheme.py`
3. Create custom scheme with `create_permission_scheme.py`
4. Define grants with `--grant` parameters
5. Assign to projects with `assign_permission_scheme.py`
```

**Benefit:** Users see "I want to X" → "Do these 5-7 steps in order"

---

#### 1.3 Create `docs/DECISION-TREE.md` (Choose Right Script)
**Purpose:** "I want to do X, which script?" → One-page reference

**Structure:**
```markdown
# Which Script Should I Use?

## I want to manage PROJECTS
- [ ] Create a new project → `create_project.py`
- [ ] View project details → `get_project.py`
- [ ] Change project name/lead → `update_project.py`
- [ ] Archive inactive project → `archive_project.py`
- [ ] Restore deleted project → `restore_project.py`
- [ ] List all projects → `list_projects.py`
- [ ] View complete configuration → `get_config.py`

## I want to configure AUTOMATION
- [ ] See all automation rules → `list_automation_rules.py`
- [ ] Get rule details → `get_automation_rule.py`
- [ ] Enable/disable rule → `enable_automation_rule.py` / `disable_automation_rule.py`
- [ ] Run manual rule → `invoke_manual_rule.py`
- [ ] Create from template → `create_rule_from_template.py`
- [ ] Modify rule config → `update_automation_rule.py`

## I want to manage USERS & GROUPS
- [ ] Find a user → `search_users.py`
- [ ] View user details → `get_user.py`
- [ ] List groups → `list_groups.py`
- [ ] Add user to group → `add_user_to_group.py`
- [ ] Remove user from group → `remove_user_from_group.py`
- [ ] Create new group → `create_group.py`

## I want to set up NOTIFICATIONS
- [ ] See notification schemes → `list_notification_schemes.py`
- [ ] View scheme details → `get_notification_scheme.py`
- [ ] Create new scheme → `create_notification_scheme.py`
- [ ] Add event notifications → `add_notification.py`
- [ ] Remove notifications → `remove_notification.py`
- [ ] Assign scheme to project → [via update_project] (TBD)

## I want to configure PERMISSIONS
- [ ] List permission schemes → `list_permission_schemes.py`
- [ ] View scheme details → `get_permission_scheme.py`
- [ ] Create permission scheme → `create_permission_scheme.py`
- [ ] Add permission grants → `update_permission_scheme.py --add-grant`
- [ ] Remove grants → `update_permission_scheme.py --remove-grant`
- [ ] Assign to projects → `assign_permission_scheme.py`

## I want to manage ISSUE TYPES
- [ ] See all issue types → `list_issue_types.py`
- [ ] View type details → `get_issue_type.py`
- [ ] Create new type → `create_issue_type.py`
- [ ] Edit type properties → `update_issue_type.py`
- [ ] Delete unused type → `delete_issue_type.py`

## I want to configure ISSUE TYPE SCHEMES
- [ ] View all schemes → `list_issue_type_schemes.py`
- [ ] Get scheme details → `get_issue_type_scheme.py`
- [ ] Create new scheme → `create_issue_type_scheme.py`
- [ ] Add types to scheme → `add_issue_types_to_scheme.py`
- [ ] Remove type from scheme → `remove_issue_type_from_scheme.py`
- [ ] Assign scheme to project → `assign_issue_type_scheme.py`

## I want to manage SCREENS
- [ ] List all screens → `list_screens.py`
- [ ] View screen details → `get_screen.py`
- [ ] Add field to screen → `add_field_to_screen.py`
- [ ] Remove field from screen → `remove_field_from_screen.py`
- [ ] View project screens → `get_project_screens.py`

## I want to configure WORKFLOWS
- [ ] List workflows → `list_workflows.py`
- [ ] View workflow details → `get_workflow.py`
- [ ] Get issue's workflow → `get_workflow_for_issue.py`
- [ ] List workflow schemes → `list_workflow_schemes.py`
- [ ] Assign scheme to project → `assign_workflow_scheme.py`
- [ ] List statuses → `list_statuses.py`

**Note:** Workflow creation/editing requires JIRA UI (not available via REST API)
```

**Benefit:** Single page, answer to "which script?" in <30 seconds

---

#### 1.4 Create `assets/VOODOO_CONSTANTS.md` (Magic Numbers Reference)
**Purpose:** Explain field IDs, event IDs, permission keys

**Content:**
```markdown
# JIRA Field IDs, Event IDs, and Constants Reference

## Common Custom Field IDs
These vary by instance! Use `get_config.py PROJ` to discover YOUR instance's IDs:

| Field | Common ID | Description | How to Find Yours |
|-------|-----------|-------------|--------------------|
| Story Points | `customfield_10016` | Agile field | Check project config |
| Epic Link | `customfield_10014` | Epic relationship | Use field discovery |
| Sprint | `customfield_10020` | Sprint assignment | Run `get_project.py` |

## Common Notification Event IDs
| Event | ID | Name |
|-------|----|----|
| Issue Created | 1 | `jira.issue.event.trigger:created` |
| Issue Updated | 2 | `jira.issue.event.trigger:updated` |
| Issue Assigned | 3 | `jira.issue.event.trigger:assigned` |
| ... | ... | ... |

## Permission Keys (Complete List)
| Key | Description |
|-----|-------------|
| `BROWSE_PROJECTS` | View projects |
| `CREATE_ISSUES` | Create issues |
| ... | ... |

## Holder Types Reference
| Type | Format | Example |
|------|--------|---------|
| `anyone` | `anyone` | Anyone |
| `group` | `group:NAME` | `group:developers` |
| `projectRole` | `projectRole:ID` | `projectRole:10002` |
| ... | ... | ... |
```

**Benefit:** User can quickly decode reference material

---

### Phase 2: Rewrite SKILL.md for Discovery (Week 2)

#### 2.1 Target Structure (~400-500 lines)

```markdown
---
name: "JIRA Administration"
description: "Complete JIRA project and system administration including projects,
  automation, permissions, users, notifications, screens, issue types, and
  workflows. Use when managing project structure, automating work, configuring
  team access, or setting up issue tracking."
---

# JIRA Admin Skill

## What This Skill Does

**8 Major Administration Areas:**

1. **Project Management** - Create, configure, and organize JIRA projects
2. **Automation Rules** - Discover, manage, and invoke automation workflows
3. **Permission Schemes** - Control who can do what across projects
4. **User & Group Management** - Find and organize team members
5. **Notification Schemes** - Configure who receives what notifications
6. **Screen Management** - Control which fields appear in issue workflows
7. **Issue Types & Schemes** - Define work item types and their availability
8. **Workflow Management** - Explore issue lifecycle workflows

Each area has 5-15 scripts for discovery, creation, configuration, and deletion.

---

## Quick Navigation

**In a hurry? Use these:**

### Common Tasks
- [Setting up a new project](docs/WORKFLOWS.md#setting-up-a-new-project) - 5 steps
- [Adding users to projects](docs/WORKFLOWS.md#configuring-team-access) - 3 steps
- [Configuring notifications](docs/WORKFLOWS.md#configuring-notification-rules-for-team) - 5 steps

### Choose Your Task
- [I want to do X, find the script →](docs/DECISION-TREE.md)
- [I'm learning JIRA admin →](docs/BEST_PRACTICES.md)
- [I need per-subsystem guides →](docs/subsystems/)

---

## When to Use This Skill

You should reach for this skill when:

- **Setting up projects** - Create new JIRA projects with appropriate templates
- **Configuring access** - Define who can view, create, or edit issues
- **Automating work** - List, enable, disable, or invoke automation rules
- **Managing users** - Search for users, create groups, manage team membership
- **Setting up notifications** - Define who gets notified about issue changes
- **Configuring screens** - Control which fields appear when creating/editing issues
- **Organizing issue types** - Choose available issue types for projects
- **Managing workflows** - View workflows and assign them to projects

**Required Permissions:**
- Most operations need `Administer Jira` (global) permission
- Some project-level operations need `Administer Projects` permission
- Discovery operations need appropriate `Browse` permissions

---

## 84 Available Scripts

All scripts support `--help` for full documentation. They're organized into 8 categories:

### Project Management (8 scripts)
`create_project.py` • `get_project.py` • `list_projects.py` • `update_project.py` •
`delete_project.py` • `archive_project.py` • `restore_project.py` • `get_config.py`

### Automation Rules (8 scripts)
`list_automation_rules.py` • `get_automation_rule.py` • `search_automation_rules.py` •
`enable_automation_rule.py` • `disable_automation_rule.py` • `toggle_automation_rule.py` •
`invoke_manual_rule.py` • `list_automation_templates.py`

### Permission Schemes (7 scripts)
`list_permission_schemes.py` • `get_permission_scheme.py` • `create_permission_scheme.py` •
`update_permission_scheme.py` • `delete_permission_scheme.py` •
`assign_permission_scheme.py` • `list_permissions.py`

### User & Group Management (8 scripts)
`search_users.py` • `get_user.py` • `list_groups.py` • `get_group_members.py` •
`create_group.py` • `delete_group.py` • `add_user_to_group.py` •
`remove_user_from_group.py`

### Notification Schemes (7 scripts)
`list_notification_schemes.py` • `get_notification_scheme.py` •
`create_notification_scheme.py` • `update_notification_scheme.py` •
`add_notification.py` • `remove_notification.py` • `delete_notification_scheme.py`

### Screen Management (10 scripts)
`list_screens.py` • `get_screen.py` • `list_screen_tabs.py` •
`get_screen_fields.py` • `add_field_to_screen.py` • `remove_field_from_screen.py` •
`list_screen_schemes.py` • `get_screen_scheme.py` •
`list_issue_type_screen_schemes.py` • `get_project_screens.py`

### Issue Types (5 scripts)
`list_issue_types.py` • `get_issue_type.py` • `create_issue_type.py` •
`update_issue_type.py` • `delete_issue_type.py`

### Issue Type & Workflow Schemes (15+ scripts)
Issue Type Schemes: `list_issue_type_schemes.py` • `get_issue_type_scheme.py` •
`create_issue_type_scheme.py` • `update_issue_type_scheme.py` •
`delete_issue_type_scheme.py` • `assign_issue_type_scheme.py` •
`add_issue_types_to_scheme.py` • `remove_issue_type_from_scheme.py`

Workflow Schemes: `list_workflows.py` • `get_workflow.py` • `search_workflows.py` •
`list_workflow_schemes.py` • `get_workflow_scheme.py` • `assign_workflow_scheme.py` •
`list_statuses.py` • `get_workflow_for_issue.py`

---

## Getting Started

### 30-Second Start
```bash
# List all projects
python list_projects.py

# See project configuration
python get_config.py PROJ

# Check current user permissions
python search_users.py --me --include-groups
```

### Next Steps
1. **For detailed examples:** See [docs/subsystems/](docs/subsystems/)
2. **For workflows:** See [docs/WORKFLOWS.md](docs/WORKFLOWS.md)
3. **For best practices:** See [docs/BEST_PRACTICES.md](docs/BEST_PRACTICES.md)
4. **To choose scripts:** See [docs/DECISION-TREE.md](docs/DECISION-TREE.md)

---

## Common Errors

| Error | Solution |
|-------|----------|
| 403 Forbidden | Verify you have "Administer Jira" permission |
| 404 Not Found | Check project key or scheme ID spelling |
| 409 Conflict | Resource exists - choose different name/key |
| 400 Bad Request | Validate input format (see script --help) |

---

## Related Skills

- **jira-issue** - Core issue CRUD (uses projects created here)
- **jira-lifecycle** - Transitions (uses workflows configured here)
- **jira-agile** - Sprints and boards (uses projects created here)
- **jira-search** - JQL queries (uses issue types configured here)
- **jira-fields** - Custom field discovery (integrates with screens)
- **jira-bulk** - Bulk operations (uses permission schemes here)
```

**Size:** ~400-450 lines (down from 1,863)

---

### Phase 3: Create Quick Reference Card (Week 2)

#### 3.1 Create `docs/QUICK-REFERENCE.md` (One-page cheat sheet)

```markdown
# JIRA Admin Quick Reference

## Scripts by Goal (Ctrl+F to find)

### Projects
- Create: `create_project.py --key X --name X --type software --template scrum`
- Get info: `get_project.py PROJ`
- List: `list_projects.py [--type software]`
- Update: `update_project.py PROJ --name X`
- Delete: `delete_project.py PROJ [--yes]`
- Archive: `archive_project.py PROJ [--yes]`
- Restore: `restore_project.py PROJ`
- Config: `get_config.py PROJ [--show-schemes]`

### Automation
- List: `list_automation_rules.py [--project PROJ] [--state enabled]`
- Get: `get_automation_rule.py RULE_ID`
- Enable: `enable_automation_rule.py RULE_ID`
- Disable: `disable_automation_rule.py RULE_ID`
- Invoke: `invoke_manual_rule.py RULE_ID --issue PROJ-123`
- Templates: `list_automation_templates.py`
- Create from template: `create_rule_from_template.py TEMPLATE_ID --project PROJ`

### Permissions
- List schemes: `list_permission_schemes.py`
- Get scheme: `get_permission_scheme.py 10000`
- Create: `create_permission_scheme.py --name X [--clone 10000]`
- Update: `update_permission_scheme.py 10000 --add-grant "PERM:TYPE:PARAM"`
- Delete: `delete_permission_scheme.py 10050 [--confirm]`
- Assign: `assign_permission_scheme.py --project PROJ --scheme 10050`

### Users & Groups
- Search: `search_users.py "john" [--project PROJ] [--assignable]`
- Get: `get_user.py --email X [--include-groups]`
- Me: `search_users.py --me --include-groups`
- List groups: `list_groups.py [--include-members]`
- Members: `get_group_members.py "group-name"`
- Create group: `create_group.py "group-name"`
- Add user: `add_user_to_group.py user@email --group "group-name"`
- Remove user: `remove_user_from_group.py user@email --group "group-name" --confirm`

### Notifications
- List: `list_notification_schemes.py`
- Get: `get_notification_scheme.py 10000`
- Create: `create_notification_scheme.py --name X`
- Add: `add_notification.py 10000 --event "Issue created" --notify Reporter`
- Remove: `remove_notification.py 10000 --notification-id 12`
- Delete: `delete_notification_scheme.py 10050 [--force]`

### Screens
- List: `list_screens.py [--filter X]`
- Get: `get_screen.py 1 [--tabs]`
- Add field: `add_field_to_screen.py 1 customfield_10016 [--tab X]`
- Remove field: `remove_field_from_screen.py 1 customfield_10016`
- Project screens: `get_project_screens.py PROJ [--full]`

### Issue Types
- List: `list_issue_types.py [--standard-only] [--subtask-only]`
- Get: `get_issue_type.py 10001`
- Create: `create_issue_type.py --name X [--type subtask]`
- Update: `update_issue_type.py 10001 --name X`
- Delete: `delete_issue_type.py 10050 --alternative-id 10001`

### Issue Type Schemes
- List: `list_issue_type_schemes.py`
- Get: `get_issue_type_scheme.py 10001`
- Create: `create_issue_type_scheme.py --name X --issue-type-ids 10001`
- Assign: `assign_issue_type_scheme.py --scheme-id 10001 --project-id 10000`
- Add types: `add_issue_types_to_scheme.py --scheme-id 10001 --issue-type-ids 10003`
- Remove type: `remove_issue_type_from_scheme.py --scheme-id 10001 --issue-type-id 10003`

### Workflows
- List: `list_workflows.py [--name X] [--scope global]`
- Get: `get_workflow.py --name X [--show-statuses] [--show-transitions]`
- Schemes: `list_workflow_schemes.py [--show-mappings]`
- Assign: `assign_workflow_scheme.py --project PROJ --scheme-id 10101 --confirm`
- Issue workflow: `get_workflow_for_issue.py PROJ-123 [--show-transitions]`
- Statuses: `list_statuses.py [--category TODO] [--show-usage]`

## Common Patterns

### Permission Grant Format
```
PERMISSION:HOLDER_TYPE[:PARAM]
BROWSE_PROJECTS:anyone
CREATE_ISSUES:group:developers
EDIT_ISSUES:projectRole:Developers
```

### Notification Recipients
```
CurrentAssignee, Reporter, AllWatchers
Group:group-name
ProjectRole:role-id
User:account-id
```

## Magic Numbers
- Epic Link: `customfield_10014` (discover with `get_config.py`)
- Story Points: `customfield_10016` (instance-specific!)
- Issue Created event ID: 1
- Issue Updated event ID: 2

## Tips
- Use `--dry-run` on all mutation commands first
- Use `--profile X` to target specific JIRA instance
- Use `--output json` for scripting
- Run `script.py --help` for all available options
```

---

### Phase 4: Reorganize Template Assets (Week 3)

#### 4.1 Annotate Template Files

Current:
- `assets/templates/notification_scheme_minimal.json`
- `assets/templates/notification_scheme_basic.json`
- `assets/templates/notification_scheme_comprehensive.json`

**Add to each:**
```json
{
  "__comment": "Template for create_notification_scheme.py --template",
  "__usage": "python create_notification_scheme.py --template assets/templates/notification_scheme_basic.json",
  "__reference": "See docs/VOODOO_CONSTANTS.md for event IDs",
  ...
}
```

---

## Implementation Roadmap

### Week 1: Content Extraction
- [ ] Extract subsystem guides (project, automation, permissions, users, notifications, screens, issue types, workflows)
- [ ] Create `docs/subsystems/` directory
- [ ] Move relevant content from SKILL.md → subsystem guides
- [ ] Create `docs/VOODOO_CONSTANTS.md` (field IDs, event IDs, permissions)

### Week 2: Create Navigation Documents
- [ ] Create `docs/DECISION-TREE.md` (which script?)
- [ ] Create `docs/WORKFLOWS.md` (common sequences)
- [ ] Create `docs/QUICK-REFERENCE.md` (one-page cheat sheet)
- [ ] Rewrite `SKILL.md` for discovery (~400 lines)

### Week 3: Polish & Cross-Reference
- [ ] Annotate template files with usage guidance
- [ ] Add inter-document links
- [ ] Create index of all 84 scripts
- [ ] Verify no broken references

### Week 4: Testing & Validation
- [ ] User test: Can new user find "create project" in < 1 min?
- [ ] User test: Can user follow workflow without leaving docs/SKILL.md?
- [ ] User test: Can user choose script from DECISION-TREE?
- [ ] Ensure all script links work

---

## Expected Outcomes

### Before Optimization
- SKILL.md: 1,863 lines, single file
- Time to find script: 5-10 minutes
- Cognitive load: HIGH (must scan all 8 subsystems)
- Repeated content: ~100+ lines
- Maximum code block: 189 lines

### After Optimization
- SKILL.md: 400-450 lines (77% reduction)
- DECISION-TREE.md: 150-200 lines (choose script in < 30 sec)
- QUICK-REFERENCE.md: 200-250 lines (command syntax at a glance)
- Subsystem guides: 8 files, 100-200 lines each (deep dives)
- Time to find script: < 1 minute
- Cognitive load: LOW (progressive discovery)
- Repeated content: 0 (DRY principle applied)

### Progressive Disclosure Levels
- **Level 1 (Metadata):** SKILL.md frontmatter + "When to Use" (50 lines)
- **Level 2 (Quick Start):** DECISION-TREE.md + QUICK-REFERENCE.md (350-450 lines)
- **Level 3 (Detailed):** Subsystem guides in docs/subsystems/ (1,000-1,500 lines total)
- **Level 4 (Deep Dives):** BEST_PRACTICES.md + VOODOO_CONSTANTS.md (1,500+ lines)

---

## Validation Checklist

- [ ] SKILL.md is < 500 lines
- [ ] All subsystem examples moved to docs/subsystems/
- [ ] No code block > 50 lines in main SKILL.md
- [ ] DECISION-TREE.md covers all 84 scripts
- [ ] Cross-references work in all documents
- [ ] User can find script in < 1 minute from DECISION-TREE
- [ ] User can run command from QUICK-REFERENCE with zero lookups
- [ ] No repeated "When to Use" content across files
- [ ] BEST_PRACTICES.md linked prominently at end of SKILL.md

---

## Success Metrics

1. **Discoverability:** User can find target script in < 1 minute using DECISION-TREE.md
2. **Accessibility:** User can find command syntax in QUICK-REFERENCE.md without scrolling
3. **Cognitive Load:** User experiences "I know where to look" for each task type
4. **DRY Principle:** Zero repeated "When to Use" or "Understanding X" content
5. **Progressive Disclosure:** Core SKILL.md readable in 5 minutes, deeper guides available as needed

---

## Notes

- **Keep BEST_PRACTICES.md intact** - It's well-structured reference material
- **Template structure is good** - Just add usage comments
- **All 84 scripts properly distributed** - No consolidation needed
- **Order matters** - Common tasks (projects) before advanced (workflows)
- **Links are critical** - Ensure all cross-document references work

---

**Report Generated:** 2025-12-28
**Recommendation:** Implement Phase 1-2 within 2 weeks for significant UX improvement
