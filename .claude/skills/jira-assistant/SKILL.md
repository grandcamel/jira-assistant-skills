---
name: "JIRA Assistant"
description: "Complete JIRA automation hub for issues, workflows, search, agile, time tracking, service management, and more. Use when working with JIRA in any capacity - creating issues, managing sprints, tracking time, searching, bulk operations, or any JIRA-related task."
---

# JIRA Assistant

Complete JIRA automation hub that routes to 12 specialized skills for comprehensive JIRA automation.

## Quick Start

Tell me what you need in natural language. I'll load the appropriate specialized skill and execute your request.

**Examples:**
- "Create a bug in TES for login issues and assign to me"
- "Move PROJ-123 to In Progress"
- "Find all open bugs assigned to me"
- "Log 2 hours on PROJ-456"
- "What's blocking PROJ-789?"

---

## Skill Routing Guide

### Issue Management

| Need | Skill | Triggers |
|------|-------|----------|
| Create, read, update, delete issues | `jira-issue` | "create issue", "get issue", "update issue", "delete issue", "new bug", "new task", "new story" |
| Transitions, workflow, status changes | `jira-lifecycle` | "transition", "move to", "change status", "close", "reopen", "resolve" |

### Search & Discovery

| Need | Skill | Triggers |
|------|-------|----------|
| JQL queries, saved filters, search | `jira-search` | "search", "find issues", "JQL", "filter", "query" |
| Custom field discovery, field IDs | `jira-fields` | "custom field", "field ID", "what fields", "agile fields" |

### Collaboration

| Need | Skill | Triggers |
|------|-------|----------|
| Comments, attachments, watchers | `jira-collaborate` | "comment", "attach", "upload", "watch", "notify" |
| Issue links, dependencies, cloning | `jira-relationships` | "link issues", "blocks", "is blocked by", "depends on", "clone", "duplicate" |

### Agile & Planning

| Need | Skill | Triggers |
|------|-------|----------|
| Sprints, epics, backlog, boards | `jira-agile` | "sprint", "epic", "backlog", "story points", "board", "velocity" |
| Time tracking, worklogs, estimates | `jira-time` | "log time", "worklog", "time spent", "estimate", "remaining time" |

### Bulk & Automation

| Need | Skill | Triggers |
|------|-------|----------|
| Bulk operations at scale | `jira-bulk` | "bulk", "batch", "multiple issues", "mass update", "bulk transition" |
| Git branches, commits, PRs | `jira-dev` | "branch name", "commit message", "PR description", "git" |

### Service Management

| Need | Skill | Triggers |
|------|-------|----------|
| Service desks, requests, SLAs, customers | `jira-jsm` | "service desk", "request", "SLA", "customer", "queue", "approval", "knowledge base" |

### Operations

| Need | Skill | Triggers |
|------|-------|----------|
| Cache management, diagnostics | `jira-ops` | "cache", "warm cache", "clear cache", "performance" |

---

## How This Works

1. **You describe your task** in natural language
2. **I identify** which specialized skill applies based on the routing table above
3. **I invoke** that skill (e.g., `Skill: jira-issue`)
4. **The skill loads** with detailed scripts and instructions
5. **I execute** your request using the loaded capabilities

---

## Script Execution Guidelines

**IMPORTANT: Always verify command syntax before execution.**

Before running any JIRA script, check the syntax and available options:

```bash
# Always run --help first to verify syntax
python script_name.py --help
```

### Why This Matters

1. **Parameter validation** - Confirm required vs optional arguments
2. **Correct flags** - Verify exact flag names (e.g., `--issue-key` vs `--issue`)
3. **Value formats** - Check expected formats (dates, time strings, JQL)
4. **Avoid failures** - Prevent execution errors from incorrect syntax

### Execution Pattern

Follow this pattern for every script execution:

```bash
# Step 1: Check syntax first
python .claude/skills/jira-issue/scripts/create_issue.py --help

# Step 2: Execute with verified parameters
python .claude/skills/jira-issue/scripts/create_issue.py --project PROJ --type Bug --summary "Issue title"
```

### Common Parameter Patterns

| Pattern | Example | Notes |
|---------|---------|-------|
| Issue key | `PROJ-123` | Positional or `--issue-key` |
| Project | `--project PROJ` | 2-10 char uppercase |
| Profile | `--profile development` | JIRA instance to use |
| Dry run | `--dry-run` | Preview without changes |
| Output | `--output json` | json, table, or csv |

### Error Prevention

When a script fails:
1. Re-run with `--help` to verify exact syntax
2. Check if required parameters are missing
3. Validate parameter value formats
4. Verify `--profile` matches configured instance

---

## Available Skills Summary

### Core Operations
- **jira-issue**: CRUD operations - create bugs, tasks, stories; get issue details; update fields; delete issues
- **jira-lifecycle**: Workflow management - transitions, assignments, versions, components

### Search & Fields
- **jira-search**: JQL queries, saved filters, bulk search, export results
- **jira-fields**: Custom field discovery, Agile field configuration, project field mapping

### Collaboration
- **jira-collaborate**: Comments (add/edit/delete), attachments (upload/download), watchers, notifications
- **jira-relationships**: Issue linking, dependency chains, blocker analysis, issue cloning

### Agile
- **jira-agile**: Sprint management, epic creation, backlog ranking, story point estimation, board operations
- **jira-time**: Time logging, worklog management, estimate tracking, time reports

### Scale & Automation
- **jira-bulk**: Bulk transitions, mass assignments, priority updates, batch cloning with dry-run support
- **jira-dev**: Git branch name generation, commit message parsing, PR description creation

### Service Management
- **jira-jsm**: Service desks, customer requests, SLA tracking, queues, approvals, knowledge base, Assets/CMDB

### Operations
- **jira-ops**: Cache warming, cache clearing, request batching, operational diagnostics

---

## Multi-Skill Operations

Some tasks require multiple skills. I'll load them sequentially:

**Example: "Create an epic with 3 stories and estimate them"**
1. Load `jira-agile` - Create the epic
2. Load `jira-issue` - Create the stories linked to the epic
3. Load `jira-time` - Set estimates on each story

**Example: "Find all bugs from last week and bulk-transition them to Done"**
1. Load `jira-search` - Find the issues with JQL
2. Load `jira-bulk` - Bulk transition the results

---

## Quick Reference

### JQL Patterns

| Need | JQL |
|------|-----|
| My open issues | `assignee = currentUser() AND status != Done` |
| My in-progress | `assignee = currentUser() AND status = "In Progress"` |
| Recent bugs | `type = Bug AND created >= -7d` |
| Sprint work | `sprint in openSprints()` |
| Blockers | `status = Blocked OR "Flagged" = Impediment` |
| Unestimated stories | `"Story Points" is EMPTY AND type = Story` |
| Updated today | `updated >= startOfDay()` |
| Watching | `watcher = currentUser()` |

### Time Formats

| Format | Meaning | Example |
|--------|---------|---------|
| `30m` | 30 minutes | `--estimate 30m` |
| `2h` | 2 hours | `--estimate 2h` |
| `1d` | 1 day (8h default) | `--estimate 1d` |
| `1w` | 1 week (5d default) | `--estimate 1w` |
| Combined | Mix units | `1d 4h 30m` |

### Issue Types

| Type | Use When |
|------|----------|
| **Epic** | Large feature spanning multiple sprints |
| **Story** | User-facing functionality, estimatable in points |
| **Task** | Technical work, not directly user-facing |
| **Bug** | Defect in existing functionality |
| **Subtask** | Breakdown of a parent issue |

### Link Types

| Link | Meaning |
|------|---------|
| **Blocks / Is blocked by** | Dependency - work cannot proceed |
| **Clones / Is cloned by** | Copy relationship |
| **Duplicates / Is duplicated by** | Same issue reported twice |
| **Relates to** | General relationship |

---

## Best Practices

### Issue Organization
- **One issue = one deliverable** - if summary has "and", split it
- **Action-oriented summaries** - "Add login validation" not "Login stuff"
- **Labels for cross-cutting concerns** - `security`, `tech-debt`, `perf`
- **Components for architecture** - `api`, `frontend`, `database`

### Agile Estimation
- **Fibonacci scale**: 1, 2, 3, 5, 8, 13 story points
- **13+ means split** - too large to estimate accurately
- **Sprint capacity**: Plan for ~80% of velocity (buffer for unknowns)
- **Velocity = completed points** - not committed, not started

### JSM vs JIRA Software

| Use JSM | Use JIRA Software |
|---------|-------------------|
| External customers/portals | Internal dev teams |
| SLA tracking required | No SLA requirements |
| ITIL processes (incident, change) | Agile/Scrum workflows |
| Queue-based triage | Sprint-based planning |

### Workflow Design
- **Statuses = states, not actions** - "In Review" not "Review"
- **Limit WIP** - too many "In Progress" = bottleneck
- **Require fields on transition** - resolution on close, assignee on start

For comprehensive guidance, see [Best Practices Guide](docs/BEST_PRACTICES.md).

---

## Configuration

All skills share configuration from:
- Environment: `JIRA_API_TOKEN`, `JIRA_EMAIL`, `JIRA_SITE_URL`
- Settings: `.claude/settings.local.json` or `.claude/settings.json`
- Profiles: Support for multiple JIRA instances (dev/staging/prod)

See individual skill documentation for detailed configuration options.
