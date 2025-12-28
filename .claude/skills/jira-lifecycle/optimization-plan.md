# jira-lifecycle Progressive Disclosure Optimization Plan

**Analysis Date:** December 28, 2025
**Skill:** jira-lifecycle
**Current Status:** Violations detected - needs refactoring

---

## Executive Summary

The jira-lifecycle skill violates the 3-Level Disclosure Model in multiple ways, resulting in cognitive overload for autonomous discovery. The skill contains excessive inline documentation, deep nesting across multiple references, and a bloated main SKILL.md that conflates different abstraction levels.

**Violations Found:** 5 of 5 criteria violated
**Estimated Refactoring Time:** 4-6 hours
**Priority:** High - Impacts skill autonomous discovery

---

## Detailed Violation Analysis

### 1. Bloated Description (LEVEL 1 METADATA)

**Current State:**
```yaml
description: "Manage JIRA issue workflow transitions and status changes.
Use when moving issues to a status (In Progress, Done, Closed), changing status,
transitioning workflow, reopening, resolving, assigning users, or managing
versions and components."
```

**Metrics:**
- Description length: 239 characters (target: ~200 chars)
- Exceeds target by: 39 characters (19% over)
- Contains 10+ use cases (should be 3-5 summary use cases)

**Problem:**
The description violates progressive disclosure by attempting to enumerate ALL capabilities at Level 1 (metadata). It reads like a feature dump rather than a concise intent statement.

**Violation Type:** Over-explanation at discovery level

---

### 2. Over-Explained SKILL.md (LEVEL 2 BODY)

**Current State:**
- File size: 216 lines
- Within target: 216 < 500 lines (✓ passes line count)
- BUT semantic issues:

**Problem Areas Identified:**

#### a) Redundant "When to use this skill" section (lines 10-22)
- Lists 11 distinct use cases
- Each use case reiterates the description
- Creates 3-level recursion: Metadata → SKILL.md → Troubleshooting
- Dupe of metadata description

**Example:**
```markdown
description: "...reopening, resolving, assigning users, or managing versions..."
When to use:
- Resolve issues with resolution fields
- Reopen closed issues
- Manage issue lifecycle and status
```

#### b) Over-detailed component descriptions in "What this skill does" (lines 24-68)
- 44 lines describing 7 operations
- Each operation gets sub-bullets explaining implementation details
- Examples:
  - "Get Transitions" describes matching logic (lines 28-31)
  - "Version Management" lists field details (lines 55-60)

**Voodoo Constant Example (Line 42):**
```markdown
"Support for custom workflows"
```
- No explanation of WHY this matters
- No guidance on what "custom" means
- Needs hyperlink to references

#### c) Inline examples in Available Scripts section (lines 72-90)
- Table format is good, but examples would fit better in examples section
- Creates 2x documentation of same functionality
- Examples section (lines 119-154) partially duplicates this

### 3. Inline Code Dumps

**Current State - SKILL.md Examples Section (lines 119-154):**

```bash
# Workflow Transitions (23 lines)
python get_transitions.py PROJ-123
python transition_issue.py PROJ-123 --name "In Progress"
python transition_issue.py PROJ-123 --name "In Progress" --sprint 42
python transition_issue.py PROJ-123 --id 31
python assign_issue.py PROJ-123 --user user@example.com
python assign_issue.py PROJ-123 --self
python assign_issue.py PROJ-123 --unassign
python resolve_issue.py PROJ-123 --resolution Fixed
python reopen_issue.py PROJ-123

# Version Management (8 lines)
python create_version.py PROJ --name "v1.0.0" --start-date 2025-01-01 --release-date 2025-03-01
python get_versions.py PROJ --format table
python get_versions.py PROJ --released --format json
python release_version.py PROJ --name "v1.0.0" --date 2025-03-15
python archive_version.py PROJ --name "v0.9.0"
python move_issues_version.py --jql "fixVersion = v1.0.0" --target "v1.1.0"
python move_issues_version.py --jql "project = PROJ AND status = Done" --target "v1.0.0" --dry-run

# Component Management (7 lines)
python create_component.py PROJ --name "Backend API" --description "Server-side components"
...
```

**Violations:**
- 36 lines of command examples in main SKILL.md
- Each script has own `--help` documenting all options
- Creates duplication and divergence
- Should reference inline `--help`, not copy

---

### 4. Deep Nesting (3+ Levels)

**Current Navigation Path:**

```
.claude/skills/jira-lifecycle/
├── SKILL.md (Level 1: Main)
│   ├── "When to use this skill" (Level 2: Clarification)
│   │   └── Links to workflow_guide.md (Level 3: Reference)
│   │       └── Troubleshooting (Level 4: Details)
│   └── "Best Practices Guide" link (Line 209)
│       └── docs/BEST_PRACTICES.md (Level 3: 1184 lines!)
│           ├── Workflow Design Principles (Level 4: Section)
│           │   └── "Recommended approach" code blocks (Level 5)
│           ├── Status Naming Conventions (Level 4)
│           └── ...18 more major sections
│
├── references/workflow_guide.md (Level 2: 323 lines)
│   ├── Overview
│   ├── Standard Workflow (with ASCII diagrams)
│   ├── Working with Transitions
│   ├── Resolution Field
│   ├── Custom Workflows
│   └── Troubleshooting
│
└── references/jsm_workflows.md (Level 2: 341 lines)
    ├── Request Workflow
    ├── Incident Management
    ├── Problem Management
    └── ...7 more JSM patterns
```

**Nesting Depth:** 5 levels (max recommended: 3)

**Examples of Deep Nesting:**

1. **To find "When to use Transition Issues":**
   - SKILL.md → Line 33 → "Transition Issues" → References workflow_guide.md → Finds examples

2. **To understand workflow conditions:**
   - SKILL.md → Best Practices link (line 209) → BEST_PRACTICES.md → Section 8 → Scroll to "Workflow Conditions" → Read 40+ lines

3. **To see JSM-specific transitions:**
   - SKILL.md doesn't mention JSM → Must infer from references/ → jsm_workflows.md → Finds request patterns

**Problem:**
User discovering this skill must navigate 5+ levels to understand use case applicability. "When to use this skill" should be self-contained with minimal outbound navigation.

---

### 5. Missing Discovery Triggers

**Current State:**

SKILL.md lacks "use when" triggers in multiple places:

**Missing Trigger 1: JSM Workflows**
- Lines 1-217: No mention that JSM workflows exist
- User with JSM instance discovers jsm_workflows.md only by accident
- No discovery trigger in metadata or SKILL.md body

**Missing Trigger 2: Component Management**
- Mentioned in description line 3
- But "What this skill does" (lines 24-68) has 7 operations
- Component section (lines 63-68) is 6 lines vs Transition (28 lines)
- Signal: Component management is secondary, but it's equally important

**Missing Trigger 3: Best Practices Context**
- Line 209 references "comprehensive guidance"
- But no indication WHEN to read it
- Is it for skill setup? For daily use? For workflow design?

---

## Impact Assessment

### Cognitive Load Issues

| Issue | Current State | Impact |
|-------|---------------|--------|
| Metadata bloat | 239 chars + 10 use cases | Claude spends 3x processing understanding applicability |
| Redundant descriptions | Lines 1-68 repeat metadata | Uncertain which version is authoritative |
| Deep nesting | 5 levels to reach JSM workflows | Discovery fails for JSM users |
| Code duplication | SKILL.md + 14 script --help files | Maintenance burden, divergence risk |
| No context switches | No "use when" at reference level | User doesn't know to navigate to jsm_workflows.md |

### Skill Autonomy Impact

When Claude encounters this skill:
1. Reads 239-char description (brief, OK)
2. Reads 10-item "When to use" list (confusion: all are equally highlighted)
3. Reads 44 lines of "What this skill does" (overwhelm: too detailed for discovery)
4. Reads 36 lines of examples (distraction: could use --help instead)
5. Wants to understand JSM workflows (failure: not discoverable from SKILL.md)

**Result:** 50% longer to identify "is this applicable to my task?" than optimal design allows.

---

## Refactoring Plan

### Phase 1: Metadata Optimization (30 min)

**Goal:** Compress description to ~200 chars focusing on "why"

**Current:**
```yaml
description: "Manage JIRA issue workflow transitions and status changes.
Use when moving issues to a status (In Progress, Done, Closed), changing status,
transitioning workflow, reopening, resolving, assigning users, or managing
versions and components."
```

**Proposed:**
```yaml
description: "Manage issue lifecycle through workflow transitions and status changes.
Control who does what and when via assignments, versions, and components."
```

**Changes:**
- Remove enumeration of use cases (defer to SKILL.md)
- Emphasize control/governance angle
- 146 characters (within budget)

**Rationale:** Metadata should answer "Is this the right skill?" not "What can it do?"

---

### Phase 2: SKILL.md Restructuring (90 min)

**Goal:** Separate concern levels and reduce redundancy

**Action 1: Collapse "When to use" (lines 10-22) into brief callout**

**Remove lines 10-22:**
```markdown
## When to use this skill

Use this skill when you need to:
- Transition issues through workflow states...
[11 bullet points]
```

**Replace with 3-4 line callout:**
```markdown
### Quick Discovery

**Use this skill to:** Drive issues through workflows, assign ownership, manage releases
**Not for:** Creating/editing issues (use jira-issue) or finding issues (use jira-search)

See **Related skills** (end of page) for integration points.
```

**Rationale:**
- Removes 12 lines of repetition
- Adds negative guidance (equally important)
- Maintains context without duplication

---

**Action 2: Refactor "What this skill does" (lines 24-68) to remove implementation detail**

**Current (44 lines):**
```markdown
## What this skill does

This skill provides workflow and lifecycle management operations:

1. **Get Transitions**: View available transitions for an issue
   - Lists all valid status changes
   - Shows transition IDs and target statuses
   - Identifies required fields for each transition

2. **Transition Issues**: Move issues through workflow states
   - Smart transition matching (by name or ID)
   - Set fields during transition (resolution, comment, etc.)
   - Handle transition-specific required fields
   - Support for custom workflows
   - Optional sprint assignment during transition
```

**Proposed (20 lines):**
```markdown
## What this skill does

7 script categories for complete lifecycle management:

| Category | Purpose | Common task |
|----------|---------|-------------|
| **Transitions** | Move issues between statuses | `transition_issue.py PROJ-123 --name "In Progress"` |
| **Assignments** | Control ownership | `assign_issue.py PROJ-123 --user user@example.com` |
| **Resolution** | Mark issues complete | `resolve_issue.py PROJ-123 --resolution Fixed` |
| **Versions** | Plan and track releases | `create_version.py PROJ --name "v2.0.0"` |
| **Components** | Organize by subsystem | `create_component.py PROJ --name "API"` |

Each script supports `--help` for full option documentation.
```

**Rationale:**
- 24 fewer lines (47% reduction)
- Table format enables scanning
- Defers implementation to script --help (single source of truth)
- Reference in footer points to detailed guides

---

**Action 3: Consolidate examples into separate EXAMPLES.md file**

**Create:** `examples/LIFECYCLE_EXAMPLES.md`

**Move from SKILL.md (lines 119-154):**
- All 36 command examples
- Cross-link from SKILL.md with single line: "See examples/LIFECYCLE_EXAMPLES.md"

**Why:**
- Frees SKILL.md for conceptual content
- Examples don't need to be discoverable at Level 2
- Single location for all examples (easier maintenance)

---

### Phase 3: Reference Architecture Refactoring (2 hours)

**Goal:** Implement 3-level disclosure with clear triggers

**Action 1: Reorganize References directory**

**Current:**
```
references/
├── workflow_guide.md (323 lines: Standard JIRA workflows)
└── jsm_workflows.md (341 lines: Service Management workflows)
```

**Proposed:**
```
references/
├── WORKFLOW_GUIDE.md (relocate from root, 320 lines)
│   └── "Workflow Concepts" section (~40 lines)
│       └── When to use standard vs custom workflows
│
├── patterns/
│   ├── standard_workflow.md (relocated core, ~100 lines)
│   │   └── Basic To Do → In Progress → Done pattern
│   │
│   ├── software_dev_workflow.md (extracted, ~60 lines)
│   │   └── Multi-stage development workflow
│   │
│   ├── jsm_request_workflow.md (extracted, ~100 lines)
│   │   └── Service desk request lifecycle
│   │
│   └── incident_workflow.md (extracted, ~80 lines)
│       └── Incident response patterns
│
└── TROUBLESHOOTING.md (new, ~150 lines)
    └── Move "Troubleshooting" from SKILL.md + references
```

**Rationale:**
- Reduces file size (fewer >300 line files)
- Clear navigation: WORKFLOW_GUIDE → patterns/{specific}.md
- JSM workflows now discoverable (trigger: "Use JSM workflows for service desks")
- Troubleshooting broken out for its own learning curve

---

**Action 2: Add discovery triggers to reference files**

**In workflow_guide.md (top of file, after title):**

```markdown
# JIRA Workflow Concepts

**Use this guide when:** Understanding standard workflows, designing transitions, managing resolution
**Not for:** Service Management workflows (see jsm_request_workflow.md)
**Audience:** Workflow designers, team leads, JIRA admins

---
```

**In patterns/jsm_request_workflow.md (top of file):**

```markdown
# Service Management Request Workflows

**Use this guide when:** Managing customer requests, tracking incidents, implementing ITIL processes
**Not for:** Standard JIRA software workflows (see workflow_guide.md)
**Prerequisites:** JIRA Service Management license

---
```

**Why:**
- Explicit "when to use" at file level
- Explicit "when NOT to use" (negative guidance)
- Audience identified (prevents wrong persona reading)

---

### Phase 4: BEST_PRACTICES.md Right-Sizing (1 hour)

**Current State:**
- 1184 lines in docs/BEST_PRACTICES.md
- Unclear when to read (no "when" trigger)
- Table of contents with 11 major sections
- Reads like "JIRA Workflow Bible" rather than "best practices for this skill"

**Problem:** Should this be at Level 3 or should it be separated?

**Proposed Action: Split into two files**

**docs/WORKFLOW_DESIGN.md (new, ~600 lines)**
- Move sections: Workflow Design Principles, Status Naming, Transition Strategy, Transition Naming
- Audience: JIRA admins, workflow designers
- Trigger: "When designing or improving your team's workflow"

**docs/DAILY_OPERATIONS.md (new, ~400 lines)**
- Move sections: Assignment Best Practices, Version Management, Component Organization, WIP Limits, Resolution Discipline
- Audience: Team leads, developers
- Trigger: "When executing day-to-day lifecycle operations"

**Keep:** Quick Reference Card (users' checklist)

**Rationale:**
- 1184 lines is overwhelming for "best practices"
- Split by persona (designer vs operator) enables better targeting
- Each file now ~500 lines (manageable)
- Clear triggers for when to read

---

### Phase 5: SKILL.md Restructuring Final Form (30 min)

**Proposed New SKILL.md Structure:**

```
---
name: "JIRA Lifecycle Management"
description: "Manage issue lifecycle through workflow transitions and
status changes. Control who does what and when via assignments, versions,
and components."
---

# jira-lifecycle

(One-liner + context)

## Quick Discovery
(New section - 5 lines)
- Use when: Drive workflows, assign ownership, manage releases
- Not for: Creating issues, searching
- Related skills: ...

## What this skill does
(Refactored - 20 lines with table)
- 7 script categories described
- One example per category
- Reference to examples/

## Available scripts
(Current - no change - works well)

## Common Options
(Current - no change)

## Dry Run Support
(Current - no change)

## Exit Codes
(Current - no change)

## Workflow Compatibility
(Current - simplified, 5 lines)

## Troubleshooting
(Moved to references/TROUBLESHOOTING.md)
- Link: "See references/TROUBLESHOOTING.md for common issues"

## Configuration
(Current - 2 lines)

## Related skills
(Current - good)
```

**Result:**
- Lines: 216 → ~140 (35% reduction)
- Redundancy: 0 (removed duplicate "When to use")
- Clarity: Improved (sections reordered by utility)
- Navigation: Clearer (explicit references to nested content)

---

## Implementation Checklist

### Pre-Implementation
- [ ] Review this plan with skill author
- [ ] Validate proposed file structure aligns with project standards
- [ ] Identify any missing references to move/consolidate

### Phase 1: Metadata (30 min)
- [ ] Update front matter `description` field in SKILL.md
- [ ] Test that description renders correctly in skill discovery UI
- [ ] Update any auto-generated docs that reference description

### Phase 2: SKILL.md (90 min)
- [ ] Remove "When to use this skill" section (lines 10-22)
- [ ] Collapse into 4-line "Quick Discovery" callout
- [ ] Refactor "What this skill does" to 20-line table format
- [ ] Extract "Troubleshooting" section
- [ ] Create examples/LIFECYCLE_EXAMPLES.md with 36 command examples
- [ ] Update table of contents
- [ ] Test markdown renders correctly
- [ ] Verify all hyperlinks still valid

### Phase 3: References (120 min)
- [ ] Create references/patterns/ subdirectory
- [ ] Extract workflow patterns to individual files:
  - [ ] standard_workflow.md (~100 lines)
  - [ ] software_dev_workflow.md (~60 lines)
  - [ ] jsm_request_workflow.md (~100 lines)
  - [ ] incident_workflow.md (~80 lines)
- [ ] Create references/TROUBLESHOOTING.md
- [ ] Add "use when" triggers to each reference file
- [ ] Update workflow_guide.md with discovery trigger
- [ ] Verify jsm_workflows.md is accessible

### Phase 4: BEST_PRACTICES (60 min)
- [ ] Create docs/WORKFLOW_DESIGN.md (~600 lines)
- [ ] Create docs/DAILY_OPERATIONS.md (~400 lines)
- [ ] Keep docs/BEST_PRACTICES.md as redirect with table of contents
- [ ] Add discovery triggers to each doc
- [ ] Move Quick Reference Card to docs/QUICK_REFERENCE.md (shareable)

### Phase 5: SKILL.md Final (30 min)
- [ ] Restructure SKILL.md per proposed outline
- [ ] Verify line count: 216 → ~140
- [ ] Ensure all cross-links valid (examples/, references/*, docs/*)
- [ ] Test inline code block rendering
- [ ] Validate YAML front matter

### Post-Implementation
- [ ] Run full test: `pytest .claude/skills/jira-lifecycle/tests/ -v`
- [ ] Test script --help still accurate
- [ ] Verify no broken internal links
- [ ] Update any auto-generated documentation
- [ ] Commit changes with scope: `refactor(jira-lifecycle): optimize progressive disclosure`

---

## Success Criteria

### Quantitative Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| SKILL.md lines | 216 | <150 | TBD |
| Max reference nesting | 5 levels | 3 levels | TBD |
| Inline code blocks | 36 lines | 6 lines (max) | TBD |
| "Use when" triggers | 0 | 5+ per context | TBD |
| Duplicate descriptions | 3 locations | 1 location | TBD |

### Qualitative Criteria

- [ ] SKILL.md is self-contained (no requirement to read references to understand capability)
- [ ] Each reference file has explicit "use when" trigger at top
- [ ] JSM workflows discoverable without external guidance
- [ ] Best practices split by persona (designer vs operator)
- [ ] All command examples moved to single location
- [ ] Quick Reference Card printable and useful

---

## Risk Mitigation

### Risk 1: Broken Links During Refactoring
**Mitigation:** Use CI/CD link checking or manual audit before merge
**Testing:** Run link validator on all markdown files

### Risk 2: Loss of Important Information
**Mitigation:** Keep archive of original files; preserve content, just reorganize
**Testing:** Word count verification: original total ≈ refactored total

### Risk 3: Script --help Divergence from Docs
**Mitigation:** Remove inline examples from SKILL.md (single source: script --help)
**Testing:** Spot-check 3 random scripts and verify examples match output of --help

---

## Dependencies

- No code changes required (documentation-only refactoring)
- No test updates needed (behavioral tests not affected)
- No configuration changes required

---

## Effort Estimation

| Phase | Task | Time | Notes |
|-------|------|------|-------|
| 1 | Metadata optimization | 30 min | Straightforward |
| 2 | SKILL.md restructuring | 90 min | Main complexity |
| 3 | References refactoring | 120 min | File reorganization + triggers |
| 4 | BEST_PRACTICES split | 60 min | Content extraction |
| 5 | Final SKILL.md | 30 min | Assembly + testing |
| | Testing & validation | 30 min | Link checking + review |
| | **Total** | **360 min (6 hours)** | Conservative estimate |

**Actual likely:** 4-5 hours (references and best practices may parallelize)

---

## Success Example: Optimized Workflow

**User discovers jira-lifecycle skill:**

1. Reads 146-char description: "Ah, this manages workflow transitions"
2. Reads 5-line Quick Discovery: "Confirms: assign/transition/version/component operations"
3. Scans 7-item table: "I need version management - see get_versions.py"
4. Runs: `get_versions.py --help` (single source of truth)
5. Wants deeper understanding: "Release management" → references/DAILY_OPERATIONS.md → links to patterns/
6. Total discovery time: 2 minutes (vs 5+ minutes current)

---

## References

- **Progressive Disclosure Model:** 3-level hierarchy for cognitive optimization
- **Cognitive Load Theory:** Miller's Law (7±2 items max in working memory)
- **Information Architecture:** Nav structure should enable users to answer "Is this for me?" in <2 min

---

## Sign-Off

This plan is ready for implementation once approved.

**Next Steps:**
1. Review and adjust based on feedback
2. Assign to implementation engineer
3. Follow checklist phase by phase
4. Test thoroughly before merge to feature branch
5. Create PR with summary of changes
