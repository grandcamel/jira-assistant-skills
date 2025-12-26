# JIRA Assistant Skills for Claude Code

A comprehensive set of Claude Code Skills for automating JIRA and JIRA Service Management operations. Designed for SREs, Developers, and Application Analysts to streamline issue management, workflow automation, and team collaboration.

## Overview

This project provides twelve modular skills that enable Claude Code to interact with JIRA:

- **jira-issue** - Core CRUD operations (create, read, update, delete issues)
- **jira-lifecycle** - Workflow management (transitions, assignments, resolve/reopen)
- **jira-search** - Query operations (JQL search, JQL builder/validator, saved filters, bulk operations)
- **jira-collaborate** - Collaboration features (comments, attachments, watchers, custom fields)
- **jira-agile** - Agile/Scrum workflows (epics, sprints, backlog, story points)
- **jira-relationships** - Issue linking (dependencies, blocker chains, cloning)
- **jira-time** - Time tracking (worklogs, estimates, time reports)
- **jira-jsm** - Jira Service Management (service desks, requests, SLAs, queues, customers, approvals)
- **jira-bulk** - Bulk operations (transitions, assignments, priorities, cloning) at scale
- **jira-dev** - Developer workflow integration (Git branches, commit parsing, PR descriptions)
- **jira-fields** - Custom field management and Agile field configuration
- **jira-ops** - Cache management, request batching, and operational utilities

## Features

- **Autonomous Discovery** - Claude Code automatically discovers and uses skills based on context
- **Multi-Profile Support** - Manage multiple JIRA instances (dev, staging, production)
- **Secure Credentials** - API tokens via environment variables, never committed to git
- **Rich Text Support** - Markdown to Atlassian Document Format (ADF) conversion
- **Error Handling** - Comprehensive error messages with troubleshooting hints
- **Retry Logic** - Automatic retry with exponential backoff for transient failures

## Quick Start

### 1. Install Dependencies

```bash
pip install -r .claude/skills/shared/scripts/lib/requirements.txt
```

### 2. Get JIRA API Token

1. Visit https://id.atlassian.com/manage-profile/security/api-tokens
2. Create a new API token
3. Copy the token

### 3. Configure

Set environment variables:

```bash
export JIRA_API_TOKEN="your-api-token-here"
export JIRA_EMAIL="your-email@company.com"
export JIRA_SITE_URL="https://your-company.atlassian.net"
```

Or edit `.claude/settings.local.json`:

```json
{
  "jira": {
    "credentials": {
      "production": {
        "email": "your-email@company.com"
      }
    }
  }
}
```

### 4. Test

```bash
# Get an issue
python .claude/skills/jira-issue/scripts/get_issue.py PROJ-123

# Search for issues
python .claude/skills/jira-search/scripts/jql_search.py "project = PROJ AND status = Open"
```

## Skills Overview

### jira-issue (4 scripts)

Core issue operations:

```bash
# Create a bug
python .claude/skills/jira-issue/scripts/create_issue.py \
  --project PROJ --type Bug --summary "Login fails" --priority High

# Get issue details
python .claude/skills/jira-issue/scripts/get_issue.py PROJ-123 --detailed

# Update issue
python .claude/skills/jira-issue/scripts/update_issue.py PROJ-123 \
  --summary "New summary" --priority Critical

# Delete issue
python .claude/skills/jira-issue/scripts/delete_issue.py PROJ-456
```

### jira-lifecycle (5 scripts)

Workflow and status management:

```bash
# View available transitions
python .claude/skills/jira-lifecycle/scripts/get_transitions.py PROJ-123

# Transition to In Progress
python .claude/skills/jira-lifecycle/scripts/transition_issue.py PROJ-123 \
  --name "In Progress"

# Assign issue
python .claude/skills/jira-lifecycle/scripts/assign_issue.py PROJ-123 \
  --user user@example.com

# Resolve issue
python .claude/skills/jira-lifecycle/scripts/resolve_issue.py PROJ-123 \
  --resolution "Fixed" --comment "Issue resolved"

# Reopen issue
python .claude/skills/jira-lifecycle/scripts/reopen_issue.py PROJ-123
```

### jira-search (17 scripts)

Query, filter management, and JQL assistance:

```bash
# JQL search
python .claude/skills/jira-search/scripts/jql_search.py \
  "assignee = currentUser() AND status != Done"

# List saved filters
python .claude/skills/jira-search/scripts/get_filters.py

# Run saved filter
python .claude/skills/jira-search/scripts/run_filter.py --name "My Open Issues"

# Export results
python .claude/skills/jira-search/scripts/export_results.py \
  "project = PROJ AND created >= -7d" --output report.csv

# Bulk update
python .claude/skills/jira-search/scripts/bulk_update.py \
  "project = PROJ AND labels = old" --add-labels "new"
```

### jira-collaborate (4 scripts)

Collaboration features:

```bash
# Add comment
python .claude/skills/jira-collaborate/scripts/add_comment.py PROJ-123 \
  --body "Working on this now"

# Add comment with Markdown
python .claude/skills/jira-collaborate/scripts/add_comment.py PROJ-123 \
  --format markdown --body "## Update\nFixed the **critical** issue"

# Upload attachment
python .claude/skills/jira-collaborate/scripts/upload_attachment.py PROJ-123 \
  --file screenshot.png

# Manage watchers
python .claude/skills/jira-collaborate/scripts/manage_watchers.py PROJ-123 \
  --add user@example.com

# Update custom fields
python .claude/skills/jira-collaborate/scripts/update_custom_fields.py PROJ-123 \
  --field customfield_10001 --value "Production"
```

### jira-agile (12 scripts)

Agile and Scrum workflow management:

```bash
# Create an epic
python .claude/skills/jira-agile/scripts/create_epic.py \
  --project PROJ --summary "Mobile App v2.0" --epic-name "MVP"

# Create a sprint
python .claude/skills/jira-agile/scripts/create_sprint.py \
  --board 123 --name "Sprint 42" --start 2025-01-01 --end 2025-01-14

# Move issues to sprint
python .claude/skills/jira-agile/scripts/move_to_sprint.py \
  --sprint 456 --issues PROJ-1,PROJ-2,PROJ-3

# Set story points
python .claude/skills/jira-agile/scripts/estimate_issue.py PROJ-1 --points 5

# View backlog
python .claude/skills/jira-agile/scripts/get_backlog.py --board 123 --group-by epic

# Rank issues
python .claude/skills/jira-agile/scripts/rank_issue.py PROJ-1 --before PROJ-2
```

### jira-relationships (8 scripts)

Issue linking and dependency management:

```bash
# Create issue links
python .claude/skills/jira-relationships/scripts/link_issue.py PROJ-1 --blocks PROJ-2
python .claude/skills/jira-relationships/scripts/link_issue.py PROJ-1 --relates-to PROJ-3

# View links and blockers
python .claude/skills/jira-relationships/scripts/get_links.py PROJ-1
python .claude/skills/jira-relationships/scripts/get_blockers.py PROJ-1 --recursive

# Export dependency graph
python .claude/skills/jira-relationships/scripts/get_dependencies.py PROJ-1 --output mermaid

# Clone an issue
python .claude/skills/jira-relationships/scripts/clone_issue.py PROJ-123 \
  --include-subtasks --include-links
```

### jira-time (9 scripts)

Time tracking and worklog management:

```bash
# Log work time
python .claude/skills/jira-time/scripts/add_worklog.py PROJ-1 \
  --time 2h --comment "Debugging auth issue"

# Set estimates
python .claude/skills/jira-time/scripts/set_estimate.py PROJ-1 \
  --original 8h --remaining 6h

# View time tracking
python .claude/skills/jira-time/scripts/get_worklogs.py PROJ-1

# Generate time report
python .claude/skills/jira-time/scripts/time_report.py \
  --user currentUser() --period last-week

# Export timesheet
python .claude/skills/jira-time/scripts/export_timesheets.py \
  --project PROJ --period 2025-01 --output timesheets.csv
```

### jira-jsm (Service Management)

Jira Service Management operations:

```bash
# List service desks
python .claude/skills/jira-jsm/scripts/list_service_desks.py

# Create a service request
python .claude/skills/jira-jsm/scripts/create_request.py \
  --service-desk 1 --request-type 10 \
  --summary "Laptop not working" --description "Screen is black"

# Get request details
python .claude/skills/jira-jsm/scripts/get_request.py SD-123

# Manage customers
python .claude/skills/jira-jsm/scripts/add_customer.py \
  --service-desk 1 --email customer@example.com

# View SLA status
python .claude/skills/jira-jsm/scripts/get_sla.py SD-123

# List queues
python .claude/skills/jira-jsm/scripts/list_queues.py --service-desk 1

# Search knowledge base
python .claude/skills/jira-jsm/scripts/search_kb.py --service-desk 1 --query "password reset"

# Manage approvals
python .claude/skills/jira-jsm/scripts/get_approvals.py SD-123
python .claude/skills/jira-jsm/scripts/approve_request.py SD-123 --approval-id 456
```

### jira-bulk (4 scripts)

Bulk operations at scale:

```bash
# Bulk transition issues
python .claude/skills/jira-bulk/scripts/bulk_transition.py \
  --issues PROJ-1,PROJ-2,PROJ-3 --to "Done"
python .claude/skills/jira-bulk/scripts/bulk_transition.py \
  --jql "project=PROJ AND status='In Progress'" --to "Done" --dry-run

# Bulk assign issues
python .claude/skills/jira-bulk/scripts/bulk_assign.py \
  --jql "project=PROJ AND status=Open" --assignee self

# Bulk set priority
python .claude/skills/jira-bulk/scripts/bulk_set_priority.py \
  --issues PROJ-1,PROJ-2 --priority High

# Bulk clone issues
python .claude/skills/jira-bulk/scripts/bulk_clone.py \
  --issues PROJ-1,PROJ-2 --include-subtasks --include-links
```

### jira-dev (6 scripts)

Developer workflow integration:

```bash
# Generate Git branch name from issue
python .claude/skills/jira-dev/scripts/create_branch_name.py PROJ-123 --auto-prefix

# Link commits to issues
python .claude/skills/jira-dev/scripts/link_commit.py PROJ-123 \
  --commit abc123def --repo https://github.com/org/repo

# Link pull requests
python .claude/skills/jira-dev/scripts/link_pr.py PROJ-123 \
  --pr https://github.com/org/repo/pull/456

# Generate PR description from issue
python .claude/skills/jira-dev/scripts/create_pr_description.py PROJ-123 --include-checklist
```

### jira-ops (3 scripts)

Cache management and operations:

```bash
# Check cache status
python .claude/skills/jira-ops/scripts/cache_status.py

# Warm cache with project/field data
python .claude/skills/jira-ops/scripts/cache_warm.py --all --profile production

# Clear cache
python .claude/skills/jira-ops/scripts/cache_clear.py --force
```

## Configuration

### Multi-Profile Setup

Configure multiple JIRA instances in `.claude/settings.json`:

```json
{
  "jira": {
    "default_profile": "production",
    "profiles": {
      "production": {
        "url": "https://company.atlassian.net",
        "project_keys": ["PROD", "OPS"],
        "default_project": "PROD"
      },
      "development": {
        "url": "https://company-dev.atlassian.net",
        "project_keys": ["DEV", "TEST"],
        "default_project": "DEV"
      }
    }
  }
}
```

Use with `--profile` flag:

```bash
python get_issue.py PROJ-123 --profile development
```

### Configuration Priority

Settings are merged in order (later overrides earlier):

1. Hardcoded defaults
2. `.claude/settings.json` (team defaults, committed)
3. `.claude/settings.local.json` (personal settings, gitignored)
4. Environment variables (highest priority)

## Directory Structure

```
.claude/
├── settings.json                    # Team defaults (committed)
├── settings.local.json             # Personal credentials (gitignored)
└── skills/
    ├── jira-issue/                 # Core CRUD operations
    ├── jira-lifecycle/             # Workflow management
    ├── jira-search/                # JQL, filters, bulk ops
    ├── jira-collaborate/           # Comments, attachments
    ├── jira-agile/                 # Epics, sprints, backlog
    ├── jira-relationships/         # Issue linking, cloning
    ├── jira-time/                  # Time tracking, worklogs
    ├── jira-jsm/                   # Jira Service Management
    ├── jira-bulk/                  # Bulk operations at scale
    ├── jira-dev/                   # Developer workflow integration
    ├── jira-fields/                # Custom field management
    ├── jira-ops/                   # Cache and operational utilities
    └── shared/
        ├── scripts/lib/            # Shared Python modules
        ├── tests/                  # Unit and live integration tests
        ├── references/             # Setup & troubleshooting
        └── config/                 # Configuration schemas
```

## Documentation

- **[Setup Guide](.claude/skills/shared/references/setup_guide.md)** - Complete setup instructions
- **[Troubleshooting](.claude/skills/shared/references/troubleshooting.md)** - Common issues and solutions
- **Skill SKILL.md files** - Usage examples for each skill
- **References directories** - API documentation and guides

## Use with Claude Code

These skills are designed for autonomous use by Claude Code:

```
User: "Create a bug ticket for the login issue with high priority"
Claude: [Uses jira-issue skill to create the bug]

User: "Show me all open bugs in the PROJ project"
Claude: [Uses jira-search skill with JQL query]

User: "Move PROJ-123 to In Progress and assign it to me"
Claude: [Uses jira-lifecycle skill to transition and assign]

User: "Create a sprint for next week and move the top 5 backlog items to it"
Claude: [Uses jira-agile skill to create sprint and move issues]

User: "What's blocking PROJ-123?"
Claude: [Uses jira-relationships skill to show blocker chain]

User: "Log 2 hours on PROJ-123 for debugging"
Claude: [Uses jira-time skill to add worklog]

User: "Create a service request for a laptop issue"
Claude: [Uses jira-jsm skill to create request]

User: "What's the SLA status on SD-456?"
Claude: [Uses jira-jsm skill to check SLA]

User: "Approve the pending request SD-789"
Claude: [Uses jira-jsm skill to approve]
```

## Security

- API tokens are **never** committed to git
- `.gitignore` excludes `.claude/settings.local.json`
- Use environment variables for sensitive data
- HTTPS-only connections enforced
- Input validation prevents injection attacks

## Requirements

- Python 3.8+
- JIRA Cloud (for core skills) or JIRA Service Management (for jira-jsm)
- API token with appropriate permissions
- Dependencies: `requests`, `tabulate`, `colorama`, `python-dotenv`

### JSM-Specific Requirements

For jira-jsm skill:
- Jira Service Management Cloud instance
- Service Desk Agent permissions
- Assets/CMDB features require JSM Premium license

## Permissions

Minimum JIRA permissions required:

- Browse Projects
- Create Issues
- Edit Issues
- Add Comments
- Transition Issues
- Assign Issues
- Manage Sprints (for jira-agile)
- Log Work (for jira-time)
- Service Desk Agent (for jira-jsm)
- Manage Customers (for jira-jsm customer operations)

## Testing

The project includes comprehensive test coverage with both unit tests and live integration tests.

**Test Summary:**
- **Total Tests:** 560+ tests
- **Core Live Integration:** 157 tests (8 skills)
- **JSM Live Integration:** 94 tests
- **New Skills Live Integration:** 85 tests (jira-bulk, jira-dev, jira-fields, jira-ops)
- **Unit Tests:** 224+ tests

```bash
# Run unit tests
pytest .claude/skills/*/tests/ -v --ignore="**/live_integration"

# Run live integration tests (requires JIRA credentials)
pytest .claude/skills/shared/tests/live_integration/ --profile development -v
pytest .claude/skills/jira-jsm/tests/live_integration/ --profile development --skip-premium -v
pytest .claude/skills/jira-bulk/tests/live_integration/ --profile development -v
pytest .claude/skills/jira-dev/tests/live_integration/ --profile development -v
pytest .claude/skills/jira-fields/tests/live_integration/ --profile development -v
pytest .claude/skills/jira-ops/tests/live_integration/ --profile development -v
```

## Troubleshooting

Common issues:

- **Authentication failed** - Check API token and email
- **Permission denied** - Verify JIRA permissions
- **Profile not found** - Check `.claude/settings.json`
- **Connection timeout** - Verify JIRA URL and network

See [Troubleshooting Guide](.claude/skills/shared/references/troubleshooting.md) for more.

## Contributing

When adding new features:

1. Follow existing code structure
2. Update relevant SKILL.md files
3. Add error handling
4. Update documentation
5. Test with real JIRA instance

## License

See LICENSE file for details.

## Support

- Check skill `SKILL.md` files for usage
- Review `references/` directories for detailed docs
- See troubleshooting guide for common issues
- Test scripts with `--help` flag for options

## Examples

### Create and Resolve a Bug

```bash
# Create bug
python .claude/skills/jira-issue/scripts/create_issue.py \
  --project PROJ --type Bug \
  --summary "Database connection fails" \
  --description "Connection timeout after 30 seconds" \
  --priority High

# Assign to self and start work
python .claude/skills/jira-lifecycle/scripts/assign_issue.py PROJ-789 --self
python .claude/skills/jira-lifecycle/scripts/transition_issue.py PROJ-789 \
  --name "In Progress"

# Add progress update
python .claude/skills/jira-collaborate/scripts/add_comment.py PROJ-789 \
  --body "Root cause identified: connection pool exhausted"

# Resolve
python .claude/skills/jira-lifecycle/scripts/resolve_issue.py PROJ-789 \
  --resolution "Fixed" \
  --comment "Increased connection pool size to 50"
```

### Weekly Report

```bash
# Export issues created this week
python .claude/skills/jira-search/scripts/export_results.py \
  "project = PROJ AND created >= startOfWeek()" \
  --output weekly-report.csv

# Find high priority unassigned issues
python .claude/skills/jira-search/scripts/jql_search.py \
  "project = PROJ AND priority = High AND assignee is EMPTY"
```

### Bulk Operations

```bash
# Find and tag stale issues
python .claude/skills/jira-search/scripts/bulk_update.py \
  "updated <= -30d AND status != Done" \
  --add-labels "stale" --dry-run

# After review, apply changes
python .claude/skills/jira-search/scripts/bulk_update.py \
  "updated <= -30d AND status != Done" \
  --add-labels "stale"
```

## Author

Created for use with Claude Code by Anthropic.
