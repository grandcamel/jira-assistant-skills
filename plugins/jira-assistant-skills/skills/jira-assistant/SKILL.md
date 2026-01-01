---
name: "jira-assistant"
description: "JIRA automation hub routing to 14 specialized skills for any JIRA task: issues, workflows, agile, search, time tracking, service management, and more."
version: "2.0.0"
author: "jira-assistant-skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# JIRA Assistant

Complete JIRA automation hub that routes to 14 specialized skills.

## Quick Start

Tell me what you need in natural language:

- "Create a bug in TES for login issues and assign to me"
- "Move PROJ-123 to In Progress"
- "Find all open bugs assigned to me"
- "Log 2 hours on PROJ-456"
- "What's blocking PROJ-789?"

---

## Skill Registry

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `jira-issue` | Create, read, update, delete issues | create, get, update, delete, new bug/task/story |
| `jira-lifecycle` | Workflow transitions, versions | transition, move to, close, reopen, resolve |
| `jira-search` | JQL queries, filters, export | search, find, JQL, filter, list issues |
| `jira-collaborate` | Comments, attachments, watchers | comment, attach, upload, watch |
| `jira-agile` | Sprints, epics, backlog | sprint, epic, backlog, story points |
| `jira-relationships` | Links, dependencies, cloning | link, blocks, depends on, clone |
| `jira-time` | Worklogs, estimates | log time, worklog, estimate |
| `jira-jsm` | Service desks, SLAs | service desk, request, SLA, customer |
| `jira-bulk` | Mass operations (50+) | bulk, batch, mass update |
| `jira-dev` | Git branches, commits, PRs | branch name, commit, PR description |
| `jira-fields` | Custom field discovery | custom field, field ID |
| `jira-ops` | Cache, diagnostics | cache, discover project |
| `jira-admin` | Projects, permissions, workflows | project settings, permissions, workflow |

**Capability Matrix:**

|  | Create | Read | Update | Delete | Search | Bulk |
|--|:------:|:----:|:------:|:------:|:------:|:----:|
| jira-issue | X | X | X | X | - | - |
| jira-search | - | X | - | - | X | - |
| jira-bulk | - | - | X | X | - | X |
| jira-admin | X | X | X | X | - | - |

---

## Routing Logic

### Disambiguation

When multiple skills match, use these precedence rules:

1. **Explicit skill mention wins**: "use jira-bulk to..." → `jira-bulk`
2. **Quantity determines bulk**: 5+ issues → `jira-bulk`
3. **Recent context**: Just created issue + "assign it" → `jira-issue`
4. **Destructive caution**: Prefer read-only when ambiguous

### Common Ambiguities

| Query | Resolution |
|-------|------------|
| "Show me the sprint" | Ask: sprint details (`jira-agile`) or issues in sprint (`jira-search`)? |
| "Link the PR" | Check context: GitHub PR (`jira-dev`) or issue link (`jira-relationships`)? |
| "Update the issues" | Ask: how many? 1-4 (`jira-issue`), 5+ (`jira-bulk`) |

### Entity Extraction

Automatically extract from queries:
- **Issue keys**: `TES-123`, `PROJ-1` → `[A-Z][A-Z0-9]+-[0-9]+`
- **Project keys**: `TES`, `PROJ` → context: "in TES", "TES project"
- **Users**: `@username`, `me`, emails → resolve to accountId
- **Time**: `2h`, `1d 4h`, `last week` → duration or JQL
- **Quantities**: `all`, `first 10`, `5 issues` → limit, is_bulk flag

---

## Multi-Skill Operations

### Automatic Chaining

| Pattern | Chain | Example |
|---------|-------|---------|
| Search + Bulk | `jira-search` → `jira-bulk` | "Find P1 bugs and close them" |
| Create + Link | `jira-issue` → `jira-relationships` | "Create bug blocking TES-50" |
| Create + Sprint | `jira-issue` → `jira-agile` | "Create task and add to sprint" |

### Composite Queries

For multi-intent requests like:
```
"Create a bug, assign to me, link to TES-100, add to sprint"
```

Execute in dependency order:
1. Create issue → get new key
2. Assign (depends on 1)
3. Link (depends on 1)
4. Add to sprint (depends on 1)

---

## Safeguards

### Destructive Operations

| Risk | Operations | Safeguard |
|:----:|------------|-----------|
| HIGH | delete issue, bulk transition | Require `--confirm` or dry-run |
| CRITICAL | delete project, bulk delete | Double confirmation |

**Always suggest dry-run for bulk operations:**
```
jira bulk transition "project=TES AND type=Bug" --to Done --dry-run
```

### Quick Error Recovery

| Error | Recovery |
|-------|----------|
| "Issue not found" | Verify key format and project access |
| "Transition unavailable" | Check valid transitions with `jira-lifecycle` |
| "Permission denied" | Check permissions with `jira-admin` |
| "Field not found" | Discover fields with `jira-fields` |

---

## Discoverability

- `/jira-assistant-skills:browse-skills` - List all skills
- `/jira-assistant-skills:skill-info <name>` - Skill details

### "Did You Mean?"

```
User: "Show me the roadmap"
→ JIRA has no native roadmap. Did you mean:
  - jira-agile: View epics?
  - jira-search: Find by fix version?
```

---

## Configuration

```bash
export JIRA_SITE_URL="https://company.atlassian.net"
export JIRA_EMAIL="you@company.com"
export JIRA_API_TOKEN="your-token"
export JIRA_PROFILE="production"  # optional
```

---

## Reference Documentation

| Document | Content |
|----------|---------|
| [ROUTING_REFERENCE.md](docs/ROUTING_REFERENCE.md) | Entity patterns, composite parsing, chaining, normalization |
| [SAFEGUARDS.md](docs/SAFEGUARDS.md) | Destructive ops, error handling, rollback |
| [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) | JQL patterns, time formats, issue types |
| [BEST_PRACTICES.md](docs/BEST_PRACTICES.md) | Workflow design, estimation, organization |
| [SCRIPT_EXECUTION.md](docs/SCRIPT_EXECUTION.md) | Command syntax, parameter patterns |
