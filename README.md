# JIRA Assistant Skills for Claude Code

> **Talk to JIRA like you talk to a teammate.** No JQL memorization. No API documentation. Just natural language.

Transform how your team interacts with JIRA. These 14 modular Claude Code Skills give you the complete JIRA ecosystem at your fingertips—from sprint planning to incident response—all through natural conversation.

```
You: "What's blocking the release?"
Claude: [Analyzes dependencies across 47 issues, identifies 3 blockers, shows resolution paths]

You: "Plan next sprint with the top priorities from backlog"
Claude: [Creates sprint, analyzes velocity, moves 8 issues totaling 34 story points]

You: "There's a P1 incident - database is down"
Claude: [Creates JSM ticket, sets SLA, notifies on-call, links related issues from last month]
```

---

## Why JIRA Assistant Skills?

### Context-Efficient Architecture (vs MCP Servers)

Traditional MCP servers load **everything** into context—every endpoint, every schema, every capability. This burns tokens and slows responses.

JIRA Assistant Skills use **progressive disclosure**:

| Approach | Context Usage | Behavior |
|----------|---------------|----------|
| **MCP Server** | ~50-100KB always loaded | All endpoints in context, even unused ones |
| **JIRA Skills** | ~6KB base + on-demand | Only active skill loaded; deep docs fetched when needed |

**Result:** 10x more context-efficient. Claude stays fast and focused.

### 14 Modular Skills, One Unified Experience

Each skill is purpose-built and autonomously discovered:

| Skill | Purpose | Key Capabilities |
|-------|---------|------------------|
| **jira-assistant** | Meta-router | Natural language routing to specialized skills |
| **jira-issue** | Core CRUD | Create, read, update, delete issues |
| **jira-lifecycle** | Workflows | Transitions, assignments, resolve/reopen |
| **jira-search** | Discovery | JQL, filters, bulk operations, exports |
| **jira-collaborate** | Teamwork | Comments, attachments, watchers |
| **jira-agile** | Scrum/Kanban | Epics, sprints, backlog, story points |
| **jira-relationships** | Dependencies | Links, blockers, cloning, impact analysis |
| **jira-time** | Tracking | Worklogs, estimates, timesheets |
| **jira-jsm** | Service Mgmt | Requests, SLAs, queues, approvals, CMDB |
| **jira-bulk** | Scale | Bulk transitions, assignments, cloning |
| **jira-dev** | Developer DX | Git branches, commits, PR descriptions |
| **jira-fields** | Configuration | Custom fields, Agile field setup |
| **jira-ops** | Operations | Caching, performance, diagnostics |
| **jira-admin** | Administration | Projects, schemes, workflows, permissions |

### Natural Language, Not CLI Memorization

**Before:** Memorize flags, read docs, copy-paste commands
```bash
python .claude/skills/jira-search/scripts/jql_search.py \
  "project = PROJ AND status = 'In Progress' AND assignee = currentUser() \
   AND sprint in openSprints() ORDER BY priority DESC" \
  --fields summary,priority,status --max-results 50 --output json
```

**After:** Just ask
```
"Show me my in-progress work for this sprint, sorted by priority"
```

Claude understands context, remembers your project, and picks the right tool.

---

## Innovative Use Cases

### AI-Powered Sprint Planning

Let Claude be your sprint planning co-pilot:

```
You: "Plan Sprint 23 based on our velocity and current priorities"

Claude:
├── Analyzes last 3 sprints: avg velocity 42 points
├── Reviews backlog: 127 unestimated, 89 ready
├── Identifies: 12 items match sprint goal "Payment System v2"
├── Recommends: 8 stories (38 points) + 20% buffer
├── Creates sprint, moves issues, sets dates
└── Flags: "PROJ-456 has external dependency on API team"
```

**Capabilities:**
- Velocity analysis from historical sprints
- Capacity planning with team availability
- Automatic backlog prioritization
- Dependency detection before sprint starts
- Story point anomaly detection ("This 2-pointer looks like an 8")

### Cross-Project Intelligence

See patterns humans miss:

```
You: "Are there any duplicate efforts across our mobile and web teams?"

Claude:
├── Scans 3 projects: MOBILE, WEB, PLATFORM
├── Semantic analysis of 847 open issues
├── Found: 4 potential duplicates
│   ├── MOBILE-234 ↔ WEB-567: "OAuth refresh token handling"
│   ├── MOBILE-289 ↔ WEB-612: "Dark mode color palette"
│   └── [2 more...]
├── Found: 3 parallel implementations
│   └── "Payment validation logic" in 3 separate repos
└── Recommendation: Create shared PLATFORM epic for consolidation
```

**Capabilities:**
- Cross-project issue similarity detection
- Dependency mapping across team boundaries
- Blocker chain analysis ("PROJ-1 → blocks 7 issues across 3 teams")
- Workload distribution insights
- Release coordination across projects

### Intelligent Incident Response

From alert to resolution, streamlined:

```
You: "P1 incident: Payment processing is failing in production"

Claude:
├── Creates JSM incident: INC-789 (Priority: Critical)
├── Sets SLA: 1-hour response, 4-hour resolution
├── Links related:
│   ├── PROJ-234: "Payment timeout errors" (closed 2 weeks ago)
│   ├── PROJ-567: "Database connection pool" (open, assigned to @jane)
│   └── INC-456: Similar incident last month (root cause: Redis)
├── Notifies: @oncall-payments, @platform-lead
├── Creates war room: #inc-789-payments
└── Suggests: "Check Redis cluster health - similar to INC-456"
```

**Capabilities:**
- Automatic incident creation with proper categorization
- SLA tracking with breach predictions
- Historical pattern matching ("This looks like the issue from March")
- Stakeholder notification workflows
- Post-incident report generation

---

## Quick Start (5 Minutes)

### 1. Install

```bash
pip install -r .claude/skills/shared/scripts/lib/requirements.txt
```

### 2. Get API Token

1. Visit [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create token → Copy it

### 3. Configure

```bash
export JIRA_API_TOKEN="your-token"
export JIRA_EMAIL="you@company.com"
export JIRA_SITE_URL="https://company.atlassian.net"
```

### 4. Try It

```bash
# Verify connection
python .claude/skills/jira-issue/scripts/get_issue.py PROJ-123

# Or just ask Claude:
# "Show me my open issues"
```

**That's it.** Claude now has full JIRA access.

---

## Talk to JIRA

These skills shine when used conversationally with Claude Code:

### Daily Standup
```
You: "What did I work on yesterday and what's on my plate today?"
Claude: [Queries recent activity, shows today's assigned items by priority]
```

### Sprint Management
```
You: "Sprint ends Friday - what's at risk?"
Claude: [Identifies incomplete items, flags blockers, suggests scope adjustments]
```

### Issue Triage
```
You: "Create a bug for the checkout crash, high priority, assign to mobile team"
Claude: [Creates issue, sets fields, assigns to component lead, adds to current sprint]
```

### Reporting
```
You: "Generate a summary of what the platform team shipped this quarter"
Claude: [Searches resolved issues, groups by epic, calculates stats, formats report]
```

### Incident Management
```
You: "What's the SLA status on the open P1s?"
Claude: [Checks JSM, shows time remaining, predicts breaches, suggests actions]
```

---

## Skills Deep Dive

### Core Operations

#### jira-issue (4 scripts)
```bash
# Create with all the details
python create_issue.py --project PROJ --type Bug \
  --summary "Login fails on Safari" --priority High \
  --description "Steps to reproduce..." --labels browser,auth

# Get comprehensive view
python get_issue.py PROJ-123 --detailed --show-links --show-time
```

#### jira-lifecycle (5 scripts)
```bash
# Workflow transitions
python transition_issue.py PROJ-123 --name "In Progress"
python resolve_issue.py PROJ-123 --resolution Fixed --comment "Deployed in v2.1"

# Assignments
python assign_issue.py PROJ-123 --user alice@company.com
python assign_issue.py PROJ-123 --self  # Assign to me
```

### Search & Discovery

#### jira-search (17 scripts)
```bash
# Complex queries made simple
python jql_search.py "sprint in openSprints() AND assignee = currentUser()"

# Saved filters
python run_filter.py --name "My Team's Blockers"

# Bulk operations
python bulk_update.py "labels = deprecated" --add-labels archived --remove-labels active

# Export for reporting
python export_results.py "project = PROJ AND resolved >= -30d" --output monthly.csv
```

### Agile Workflows

#### jira-agile (12 scripts)
```bash
# Sprint lifecycle
python create_sprint.py --board 42 --name "Sprint 23" --goal "Payment System v2"
python move_to_sprint.py --sprint 456 --issues PROJ-1,PROJ-2,PROJ-3
python close_sprint.py 456 --move-incomplete-to 457

# Backlog management
python get_backlog.py --board 42 --group-by epic
python rank_issue.py PROJ-10 --before PROJ-5

# Estimation
python estimate_issue.py PROJ-123 --points 5
```

### Dependencies & Relationships

#### jira-relationships (8 scripts)
```bash
# Linking
python link_issue.py PROJ-1 --blocks PROJ-2
python link_issue.py PROJ-1 --clones PROJ-99

# Impact analysis
python get_blockers.py PROJ-1 --recursive --max-depth 5
python get_dependencies.py PROJ-1 --output mermaid  # Visualize as diagram

# Cloning
python clone_issue.py PROJ-123 --include-subtasks --include-links --target-project NEWPROJ
```

### Service Management (JSM)

#### jira-jsm (Full ITSM Suite)
```bash
# Request lifecycle
python create_request.py --service-desk 1 --request-type "Hardware Request" \
  --summary "New laptop for onboarding"
python get_sla.py SD-123  # SLA status with breach prediction

# Customer management
python add_customer.py --service-desk 1 --email customer@external.com

# Queue management
python list_queues.py --service-desk 1 --include-counts

# Approvals
python get_approvals.py SD-123
python approve_request.py SD-123 --decision approve --comment "Budget approved"

# Knowledge base
python search_kb.py --service-desk 1 --query "password reset"
```

### Bulk Operations

#### jira-bulk (4 scripts)
```bash
# Mass transitions (with safety)
python bulk_transition.py --jql "sprint = 456 AND status != Done" --to Done --dry-run
python bulk_transition.py --jql "sprint = 456 AND status != Done" --to Done

# Bulk assignments
python bulk_assign.py --jql "component = Backend AND assignee is EMPTY" --assignee self

# Clone entire sprints
python bulk_clone.py --jql "sprint = 456" --include-subtasks --target-project ARCHIVE
```

### Developer Integration

#### jira-dev (6 scripts)
```bash
# Git workflow
python create_branch_name.py PROJ-123 --auto-prefix
# Output: feature/proj-123-implement-oauth-refresh

# PR integration
python create_pr_description.py PROJ-123 --include-checklist --include-labels
# Output: Full PR template with JIRA context

# Commit linking
python link_commit.py PROJ-123 --commit abc123 --repo https://github.com/org/repo
```

---

## Architecture

### Progressive Disclosure in Action

```
Level 1: Skill Metadata (always loaded)
├── 14 skills × ~200 chars = ~3KB
├── Enables: Autonomous skill matching
└── Cost: Minimal context usage

Level 2: Active Skill (loaded on match)
├── SKILL.md body: 2-10KB per skill
├── Enables: Main procedures, scripts, examples
└── Cost: Only active skill loaded

Level 3: Deep Reference (loaded on demand)
├── docs/BEST_PRACTICES.md: 5-30KB per skill
├── Enables: Advanced patterns, troubleshooting
└── Cost: Only when user needs advanced help
```

### Directory Structure

```
.claude/
├── settings.json           # Team configuration (committed)
├── settings.local.json     # Personal credentials (gitignored)
└── skills/
    ├── jira-assistant/     # Meta-router skill
    ├── jira-issue/         # Core CRUD
    ├── jira-lifecycle/     # Workflows
    ├── jira-search/        # JQL, filters
    ├── jira-collaborate/   # Comments, attachments
    ├── jira-agile/         # Sprints, epics
    ├── jira-relationships/ # Links, dependencies
    ├── jira-time/          # Time tracking
    ├── jira-jsm/           # Service Management
    ├── jira-bulk/          # Bulk operations
    ├── jira-dev/           # Developer workflows
    ├── jira-fields/        # Custom fields
    ├── jira-ops/           # Cache, performance
    ├── jira-admin/         # Administration
    └── shared/
        ├── scripts/lib/    # Shared Python modules
        ├── tests/          # 560+ tests
        └── config/         # Schemas
```

---

## Multi-Environment Support

Manage dev, staging, and production from one configuration:

```json
{
  "jira": {
    "default_profile": "production",
    "profiles": {
      "production": {
        "url": "https://company.atlassian.net",
        "project_keys": ["PROD", "OPS", "PLATFORM"],
        "default_project": "PROD"
      },
      "staging": {
        "url": "https://company-staging.atlassian.net",
        "project_keys": ["STG"],
        "default_project": "STG"
      },
      "development": {
        "url": "https://company-dev.atlassian.net",
        "project_keys": ["DEV", "TEST", "SANDBOX"],
        "default_project": "DEV"
      }
    }
  }
}
```

Switch instantly:
```bash
python get_issue.py TEST-123 --profile development
```

Or let Claude handle it:
```
You: "Check the staging environment for that bug we fixed"
Claude: [Automatically uses staging profile based on context]
```

---

## Testing & Reliability

**560+ tests** ensure reliability across all skills:

| Category | Tests | Coverage |
|----------|-------|----------|
| Core Live Integration | 157 | Issue, lifecycle, search, collaborate, agile, relationships, time |
| JSM Live Integration | 94 | Service desks, requests, SLAs, customers, approvals, KB |
| New Skills Live Integration | 87 | Bulk, dev, fields, ops |
| Unit Tests | 224+ | All modules, error handling, edge cases |

```bash
# Run all unit tests
pytest .claude/skills/*/tests/ -v --ignore="**/live_integration"

# Run live integration (requires JIRA credentials)
pytest .claude/skills/shared/tests/live_integration/ --profile development -v
```

---

## Security

- **Credentials never committed** - `.gitignore` protects `settings.local.json`
- **Environment variable priority** - Tokens via `JIRA_API_TOKEN`
- **HTTPS enforced** - All connections validated
- **Input sanitization** - Injection prevention on all inputs
- **Minimal permissions** - Request only what's needed

---

## Requirements

| Requirement | Details |
|-------------|---------|
| Python | 3.8+ |
| JIRA | Cloud (all skills) or Service Management (jira-jsm) |
| Permissions | Browse, Create, Edit, Transition, Assign (minimum) |
| JSM Premium | Required only for Assets/CMDB features |

Install dependencies:
```bash
pip install requests tabulate colorama python-dotenv
# Or: pip install -r .claude/skills/shared/scripts/lib/requirements.txt
```

---

## Get Started Now

1. **Clone this repo** into your project
2. **Set three environment variables** (token, email, URL)
3. **Ask Claude anything** about your JIRA

```
"Show me what needs attention before the release"
"Create a spike for investigating the performance issue"
"What's the team's velocity trend over the last 5 sprints?"
"Find all P1 bugs that have been open more than a week"
```

The skills handle the rest.

---

## Documentation

| Resource | Description |
|----------|-------------|
| [Setup Guide](.claude/skills/shared/references/setup_guide.md) | Complete installation instructions |
| [Troubleshooting](.claude/skills/shared/references/troubleshooting.md) | Common issues and solutions |
| Skill `SKILL.md` files | Usage examples per skill |
| Skill `docs/BEST_PRACTICES.md` | Advanced patterns and anti-patterns |

---

## Contributing

We welcome contributions! When adding features:

1. Follow the existing skill structure
2. Add comprehensive error handling
3. Update SKILL.md with examples
4. Add tests (unit + integration)
5. Test with real JIRA instance

---

## License

See LICENSE file for details.

---

<p align="center">
  <strong>Stop clicking through JIRA. Start talking to it.</strong>
  <br>
  <em>Built for Claude Code by developers who were tired of memorizing JQL.</em>
</p>
