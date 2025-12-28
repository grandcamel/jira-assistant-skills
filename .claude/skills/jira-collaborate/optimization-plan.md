# Progressive Disclosure Optimization Plan for jira-collaborate

**Analysis Date:** December 28, 2025
**Skill Analyzed:** jira-collaborate
**Optimization Model:** 3-Level Progressive Disclosure

---

## Executive Summary

The jira-collaborate skill has significant progressive disclosure violations that harm user experience:

- **CRITICAL:** BEST_PRACTICES.md is 50KB (1,685 lines) - violates all progressive disclosure principles
- **HIGH:** SKILL.md is 7.1KB with oversized "Common Options" table and deeply nested documentation structure
- **MEDIUM:** References lack clear entry points and organization heuristics
- **Overall Assessment:** Beginner users face massive cognitive overload before using any actual skill

The skill conflates operational documentation (best practices) with feature discovery (SKILL.md). Reorganization is required across 2-3 iterations to reach target state.

---

## Current State Analysis

### File Metrics

| File | Size | Lines | Type | Assessment |
|------|------|-------|------|------------|
| `SKILL.md` | 7.1 KB | 211 | Discovery | ACCEPTABLE (just over 5KB target) |
| `docs/BEST_PRACTICES.md` | 50 KB | 1,685 | Operational | CRITICAL VIOLATION |
| `references/adf_guide.md` | 1.6 KB | 84 | Reference | GOOD |
| Scripts (10 files) | 51.3 KB | ~440 lines avg | Code | GOOD |

### Nesting Depth

```
SKILL.md (Level 1)
├─ References BEST_PRACTICES.md (Level 2)
│  └─ Contains everything: patterns, templates, checklists, troubleshooting
├─ References adf_guide.md (Level 2)
│  └─ Also contains usage examples + cross-references
└─ Examples section (embedded in Level 1)
```

**Problem:** Users discovering the skill encounter:
1. Feature list in SKILL.md (good)
2. Giant best practices guide link (bad - no scoping)
3. Examples embedded in SKILL.md without progressive reveal

---

## Detailed Violation Analysis

### Violation 1: Bloated Best Practices Guide (CRITICAL)

**File:** `docs/BEST_PRACTICES.md`
**Size:** 50 KB (1,685 lines)
**Target:** < 10 KB per reference document
**Severity:** CRITICAL

**Root Causes:**

1. **All-in-one philosophy:** Covers 11 major topics in single file:
   - Writing effective comments (200+ lines)
   - Comment etiquette (250+ lines)
   - @Mentions strategies (150+ lines)
   - Attachment management (400+ lines)
   - Watcher strategies (150+ lines)
   - Notification management (200+ lines)
   - Activity stream usage (200+ lines)
   - Team communication patterns (250+ lines)
   - Linking external resources (150+ lines)
   - Common pitfalls (150+ lines)
   - Quick reference card (100+ lines)

2. **Over-explanation with voodoo constants:**
   - Line 64-68: Excessive explanation of comment length guidelines
   - Line 110-126: Elaborate handoff pattern with full example
   - Line 270-295: Detailed @mention vs watcher decision matrix with full context
   - Line 595-608: Decision tree for notifications (good structure, but context bloat)

3. **Nested templates with multiple examples:**
   - Each major section has: explanation, templates, examples, anti-patterns
   - Example: Watcher strategies section (lines 542-670) is 128 lines for essentially 3 use cases

4. **Repetition across sections:**
   - Notification best practices mentioned in sections: 2, 6, 8 (3x coverage)
   - @Mention guidance appears in: 2, 3, 8 (3x coverage)
   - Attachment naming mentioned in: 4, 7 (2x coverage)

**Impact:** New user navigating `docs/BEST_PRACTICES.md` faces:
- 10-15 minute read before using any script
- Mental model bloat (too many patterns at once)
- Difficulty finding quick answers
- Lost context scrolling between sections

### Violation 2: Undersized Metadata & Missing Triggers (HIGH)

**File:** `SKILL.md` (frontmatter)
**Current:** ~200 chars, decent but needs optimization
**Problem:** No explicit "use when" trigger language

**Current frontmatter:**
```yaml
description: "Collaboration features for JIRA issues - comments, attachments,
watchers, notifications. Use when adding comments, uploading/downloading
attachments, managing watchers, or sending notifications."
```

**Issue:** Vague "Use when" doesn't signal autonomous trigger patterns.

**Better approach (goal):**
```yaml
description: |
  Manage issue collaboration: add/edit comments, upload/download files,
  notify users, track changes. Use when discussing progress, sharing
  evidence, or coordinating with team members.

autonomous_triggers:
  - "user asks to comment on issue"
  - "user wants to attach file or screenshot"
  - "user needs to notify specific people"
  - "user asks for activity history"
```

### Violation 3: Oversized Tables in SKILL.md (MEDIUM)

**Location:** Lines 84-109 ("Common Options" section)
**Size:** 26-line table describing the same 4-5 options repeated 3x

**Problem:**
- Lines 86-92: Generic options (--profile, --help)
- Lines 93-98: Comment-specific options
- Lines 100-109: Notification-specific options

**Impact:** 26 lines to describe 5 unique options. Three tables where 1 would suffice.

**Better structure:**
- Level 1: Single "Universal options" table (2 options only)
- Level 2: Script-specific option details in separate `.claude/skills/jira-collaborate/references/SCRIPT_OPTIONS.md`

### Violation 4: Missing Scenario-Based Organization (MEDIUM)

**Problem:** Best practices are organized by feature, not by user scenarios.

**Current organization:**
- 1. Writing Effective Comments
- 2. Comment Etiquette
- 3. Using @Mentions
- 4. Attachment Management
- ... (8 more sections)

**Better organization (user-centric):**
1. **Getting Started** (500 words max)
   - When to use collaborate skill
   - First 5 minutes guide

2. **Common Scenarios** (3-5 scenarios, 200 words each)
   - "I'm starting work on an issue"
   - "I found a blocker and need help"
   - "I'm handing off work to someone"
   - "I need to share evidence/screenshots"
   - "I want to notify stakeholders"

3. **Advanced Topics** (separate documents)
   - Comment etiquette deep dive
   - Notification strategies
   - Team communication protocols

4. **Reference** (lookup-focused)
   - Templates card
   - JQL queries
   - Keyboard shortcuts

### Violation 5: Nested Code Examples (MEDIUM)

**Location:** Lines 29-100 in adf_guide.md & scattered in BEST_PRACTICES.md

**Problem:** Code blocks showing Python + Bash + Markdown syntax:

```bash
# Lines 37-46: Multi-line Bash example with HEREDOC
python add_comment.py PROJ-123 --format markdown --body "$(cat <<'EOF'
## Update
...
EOF
)"
```

**Impact:** Confuses readers about whether to copy literally or adapt.

**Better approach:**
- `adf_guide.md` stays as is (good progressive disclosure: "simple" → "complex" → "raw JSON")
- `BEST_PRACTICES.md` removes all code examples, references Level 3 docs instead
- New `references/COMMENT_EXAMPLES.md` with executable examples

---

## Implementation Plan

### Phase 1: Restructure Best Practices (Immediate)

**Goal:** Break 50KB guide into modular 5-10KB documents

**Action 1.1:** Extract Getting Started Guide (NEW)
- **File:** `docs/GETTING_STARTED.md`
- **Size:** Target 1.5-2 KB (500 words)
- **Content:**
  - "First 5 minutes" - basic comment workflow
  - 2-3 most common commands
  - Pointer to scenario guides
  - No templates or checklists yet

**Action 1.2:** Extract Scenario Guides (NEW)
- **Directory:** `docs/scenarios/`
- **Files:**
  - `starting_work.md` (200 words) - "I'm claiming this issue"
  - `progress_update.md` (200 words) - "Work in progress, all good"
  - `blocker_escalation.md` (200 words) - "Stuck, need help"
  - `handoff.md` (200 words) - "Taking over from someone"
  - `sharing_evidence.md` (200 words) - "Screenshots, logs, test results"
- **Format:**
  - Scenario description (1 sentence)
  - Template (copy-paste ready)
  - Example (real-world)
  - Related scripts (2-3 references)

**Action 1.3:** Relocate Best Practices (REFACTOR)
- Rename `docs/BEST_PRACTICES.md` → `docs/DEEP_DIVES/BEST_PRACTICES.md`
- Split into topic-specific documents:
  - `docs/DEEP_DIVES/COMMENT_ETIQUETTE.md` (200 lines)
  - `docs/DEEP_DIVES/ATTACHMENT_STRATEGY.md` (150 lines)
  - `docs/DEEP_DIVES/NOTIFICATION_MANAGEMENT.md` (150 lines)
  - `docs/DEEP_DIVES/TEAM_COMMUNICATION.md` (150 lines)
  - `docs/DEEP_DIVES/ACTIVITY_TRACKING.md` (100 lines)

**Action 1.4:** Extract Templates (NEW)
- **File:** `docs/TEMPLATES.md`
- **Content:**
  - Copy-paste templates from BEST_PRACTICES lines 1509-1549
  - Add link: "See DEEP_DIVES/COMMENT_ETIQUETTE for context"

**Action 1.5:** Extract Quick Reference (NEW)
- **File:** `docs/QUICK_REFERENCE.md`
- **Content:**
  - Keyboard shortcuts (from line 1602-1610)
  - When to use what (from line 1612-1624)
  - Essential scripts (copy-paste ready)
  - JQL snippets

**Estimated Result After Phase 1:**
```
Before:
  docs/BEST_PRACTICES.md (50 KB)

After:
  docs/GETTING_STARTED.md (2 KB)
  docs/QUICK_REFERENCE.md (3 KB)
  docs/TEMPLATES.md (2 KB)
  docs/SCENARIOS/
    ├── starting_work.md (500 B)
    ├── progress_update.md (500 B)
    ├── blocker_escalation.md (500 B)
    ├── handoff.md (500 B)
    └── sharing_evidence.md (500 B)
  docs/DEEP_DIVES/
    ├── COMMENT_ETIQUETTE.md (200 lines, 7 KB)
    ├── ATTACHMENT_STRATEGY.md (150 lines, 5 KB)
    ├── NOTIFICATION_MANAGEMENT.md (150 lines, 5 KB)
    ├── TEAM_COMMUNICATION.md (150 lines, 5 KB)
    └── ACTIVITY_TRACKING.md (100 lines, 3 KB)
```

### Phase 2: Optimize SKILL.md Discovery (Week 2)

**Goal:** Add autonomous triggers & consolidate option tables

**Action 2.1:** Add Trigger Metadata
- **File:** Update `SKILL.md` frontmatter
- **Changes:**
  ```yaml
  name: "JIRA Collaboration"
  description: |
    Collaborate on issues: add/edit comments, share attachments, notify
    users, track activity. For team communication and coordination.
  keywords:
    - comments
    - attachments
    - notifications
    - watchers
    - activity history
  use_when:
    - "starting work on an issue (add comment)"
    - "sharing test screenshots or error logs (upload attachment)"
    - "progress is blocked and needs escalation (comment + notify)"
    - "handing off work to teammate (comment + reassign + notify)"
    - "reviewing what changed on an issue (get activity)"
    - "need to add team visibility (manage watchers)"
  ```

**Action 2.2:** Consolidate Option Tables
- **Location:** Lines 84-109
- **Current:** 3 tables (generic, comments, notifications)
- **Proposed:**
  ```markdown
  ## Universal Options (All Scripts)

  | Option | Description |
  |--------|-------------|
  | `--profile` | JIRA profile to use |
  | `--help`, `-h` | Show detailed help |

  ## Script-Specific Options

  Detailed options per script documented in help output:
  ```bash
  python add_comment.py --help    # Comment options
  python download_attachment.py --help  # Attachment options
  python send_notification.py --help    # Notification options
  ```

  See `references/SCRIPT_OPTIONS.md` for full matrix.
  ```

**Action 2.3:** Create Script-Specific Reference (NEW)
- **File:** `references/SCRIPT_OPTIONS.md`
- **Size:** 2-3 KB
- **Content:**
  - Matrix: Script × Options
  - Detailed descriptions per script
  - Keep current table content, move to Level 2

**Action 2.4:** Reorganize Examples
- **File:** Keep in SKILL.md but add structure
- **Changes:**
  ```markdown
  ## Quick Start Examples

  See `docs/SCENARIOS/` for workflow-focused examples:
  - [Starting work](docs/SCENARIOS/starting_work.md)
  - [Progress update](docs/SCENARIOS/progress_update.md)
  - [Escalation](docs/SCENARIOS/blocker_escalation.md)

  For script-specific syntax, use `--help`:
  ```bash
  python add_comment.py --help
  ```
  ```

**Action 2.5:** Update References Section
- **Current:** Line 206-211
- **Proposed:**
  ```markdown
  ## Documentation Structure

  **Getting Started:** [GETTING_STARTED.md](docs/GETTING_STARTED.md) (new user)

  **Common Scenarios:** [scenarios/](docs/scenarios/) (workflow examples)

  **Templates & Reference:** [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)

  **Advanced Topics:** [DEEP_DIVES/](docs/DEEP_DIVES/) (optional reading)

  **Format Reference:** [adf_guide.md](references/adf_guide.md) (Markdown → ADF)

  **Script Options:** [SCRIPT_OPTIONS.md](references/SCRIPT_OPTIONS.md)
  ```

### Phase 3: Reference Hierarchy Cleanup (Week 3)

**Goal:** Establish clear 3-level hierarchy for all resources

**Action 3.1:** Reorganize References Directory
**Current:**
```
references/
└── adf_guide.md
```

**Target:**
```
references/
├── adf_guide.md (unchanged - good progressive disclosure)
├── SCRIPT_OPTIONS.md (NEW - from Phase 2.3)
└── COMMENT_FORMATS.md (NEW - expanded from adf_guide)
```

**Action 3.2:** Create Hierarchy Index (NEW)
- **File:** `docs/INDEX.md`
- **Purpose:** Navigation guide showing which doc to read based on user goal
- **Structure:**
  ```markdown
  # Documentation Index

  ## I want to...

  ### Use the skill (Level 1 - Start here)
  - Learn basic features: [SKILL.md](/SKILL.md) (5 min read)
  - First workflow: [GETTING_STARTED.md](docs/GETTING_STARTED.md) (5 min)

  ### Get things done (Level 2 - Practical guides)
  - Start work on issue: [SCENARIOS/starting_work.md](docs/scenarios/starting_work.md)
  - Share test results: [SCENARIOS/sharing_evidence.md](docs/scenarios/sharing_evidence.md)
  - Escalate a blocker: [SCENARIOS/blocker_escalation.md](docs/scenarios/blocker_escalation.md)
  - Hand off to teammate: [SCENARIOS/handoff.md](docs/scenarios/handoff.md)

  ### Understand best practices (Level 3 - Advanced)
  - Comment etiquette: [DEEP_DIVES/COMMENT_ETIQUETTE.md](docs/DEEP_DIVES/COMMENT_ETIQUETTE.md)
  - Attachment strategy: [DEEP_DIVES/ATTACHMENT_STRATEGY.md](docs/DEEP_DIVES/ATTACHMENT_STRATEGY.md)
  - Notification patterns: [DEEP_DIVES/NOTIFICATION_MANAGEMENT.md](docs/DEEP_DIVES/NOTIFICATION_MANAGEMENT.md)
  - Team communication: [DEEP_DIVES/TEAM_COMMUNICATION.md](docs/DEEP_DIVES/TEAM_COMMUNICATION.md)
  - Activity history: [DEEP_DIVES/ACTIVITY_TRACKING.md](docs/DEEP_DIVES/ACTIVITY_TRACKING.md)

  ### Find a template (Reference)
  - Copy-paste templates: [TEMPLATES.md](docs/TEMPLATES.md)
  - JQL queries: [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)
  - Script options: [references/SCRIPT_OPTIONS.md](references/SCRIPT_OPTIONS.md)
  ```

**Action 3.3:** Add Breadcrumbs to Deep Dives
- Each DEEP_DIVES/*.md file should have:
  ```markdown
  [← Back to Index](../INDEX.md) | [← Back to QUICK_REFERENCE](../QUICK_REFERENCE.md)
  ```

---

## Progressive Disclosure Metrics

### Current State (Before Optimization)

| Level | Document | Size | Lines | Violations |
|-------|----------|------|-------|-----------|
| 1 | SKILL.md | 7.1 KB | 211 | Table consolidation needed |
| 1 | Frontmatter | ~200 chars | 3 | Missing triggers |
| 2 | BEST_PRACTICES.md | 50 KB | 1,685 | **MASSIVE VIOLATION** |
| 2 | adf_guide.md | 1.6 KB | 84 | Good |
| 3 | Scripts | 51 KB | ~440 | Good |

**Median read time to use skill:** ~15 minutes (new user must skim BEST_PRACTICES)

### Target State (After Phase 3)

| Level | Document | Size | Lines | Status |
|-------|----------|------|-------|--------|
| 1 | SKILL.md | 6 KB | 180 | OPTIMIZED (removed tables) |
| 1 | Frontmatter | ~300 chars | 15 | ENHANCED (triggers added) |
| 1 | GETTING_STARTED.md | 2 KB | 60 | NEW (quick start) |
| 2 | SCENARIOS/*.md | 2.5 KB | 100 | NEW (workflow examples) |
| 2 | QUICK_REFERENCE.md | 3 KB | 90 | NEW (lookup focused) |
| 2 | TEMPLATES.md | 2 KB | 50 | NEW (copy-paste) |
| 2 | adf_guide.md | 1.6 KB | 84 | UNCHANGED (good) |
| 3 | DEEP_DIVES/*.md | 25 KB | 500 | REFACTORED (organized by topic) |
| 3 | Scripts | 51 KB | ~440 | UNCHANGED (good) |

**Median read time to use skill:** ~5 minutes (new user reads GETTING_STARTED + one scenario)

**Cognitive load reduction:** 67% (from 15 min to 5 min critical path)

---

## Migration Path

### Week 1: Foundation (Phase 1)
- Day 1-2: Create doc structure in git
- Day 3-4: Extract & refactor best practices
- Day 5: Test navigation, gather feedback

### Week 2: Optimization (Phase 2)
- Day 1-2: Update SKILL.md frontmatter & structure
- Day 3-4: Create SCRIPT_OPTIONS.md reference
- Day 5: Update examples section with cross-links

### Week 3: Hierarchy (Phase 3)
- Day 1: Create INDEX.md navigation guide
- Day 2-3: Add breadcrumbs to all Level 3 docs
- Day 4: Create COMMENT_FORMATS.md advanced reference
- Day 5: Final validation & README update

### Success Metrics
- [ ] SKILL.md under 6KB (remove consolidated table)
- [ ] BEST_PRACTICES.md broken into 5 focused <10KB documents
- [ ] New user can perform first workflow in <5 minutes
- [ ] Every Level 2+ doc has breadcrumb navigation
- [ ] INDEX.md correctly routes users to appropriate docs
- [ ] No content duplication between documents

---

## Risk Assessment

### Risk 1: Content Fragmentation
**Issue:** Splitting 1 comprehensive guide into 5 documents may scatter information users need together.

**Mitigation:**
- Cross-link heavily with clear "See also" sections
- INDEX.md guides users to related documents
- DEEP_DIVES keep topical cohesion (all comment etiquette in one file)

### Risk 2: Maintenance Burden
**Issue:** More files means more places to keep in sync.

**Mitigation:**
- Document sync points (e.g., "templates in 3 places: TEMPLATES.md, DEEP_DIVES/*, QUICK_REFERENCE.md")
- Establish CI check: "ensure no duplicate template definitions"
- Use cross-references instead of duplication where possible

### Risk 3: User Confusion in Migration
**Issue:** Existing users bookmarked BEST_PRACTICES.md link.

**Mitigation:**
- Keep BEST_PRACTICES.md with redirect: "This guide has been reorganized. See INDEX.md"
- Create 301-style anchors: `[BEST_PRACTICES.md](docs/INDEX.md#best-practices-and-etiquette)`

---

## Code Example: Scenario Template (Reference)

Each scenario file follows this structure:

```markdown
# Scenario: [Title]

**Use this guide when:** [1 sentence trigger]

## The Situation

[2-3 sentences describing the context]

## Quick Template

\`\`\`bash
[Copy-paste ready command]
\`\`\`

## Example

[Real-world example output/usage]

## Related Scripts

- `add_comment.py` - [why relevant]
- `manage_watchers.py` - [why relevant]

## Pro Tips

- Tip 1
- Tip 2

---

[← Back to GETTING_STARTED.md](../GETTING_STARTED.md)
```

---

## Appendix: Files to Create

**Phase 1 Deliverables:**
```
docs/GETTING_STARTED.md
docs/QUICK_REFERENCE.md
docs/TEMPLATES.md
docs/scenarios/starting_work.md
docs/scenarios/progress_update.md
docs/scenarios/blocker_escalation.md
docs/scenarios/handoff.md
docs/scenarios/sharing_evidence.md
docs/DEEP_DIVES/COMMENT_ETIQUETTE.md
docs/DEEP_DIVES/ATTACHMENT_STRATEGY.md
docs/DEEP_DIVES/NOTIFICATION_MANAGEMENT.md
docs/DEEP_DIVES/TEAM_COMMUNICATION.md
docs/DEEP_DIVES/ACTIVITY_TRACKING.md
docs/BEST_PRACTICES.md → moved to DEEP_DIVES/ (with redirect)
```

**Phase 2 Deliverables:**
```
references/SCRIPT_OPTIONS.md
SKILL.md (updated with frontmatter & consolidated tables)
```

**Phase 3 Deliverables:**
```
docs/INDEX.md
docs/DEEP_DIVES/*.md (with breadcrumbs)
references/COMMENT_FORMATS.md
```

---

## Conclusion

The jira-collaborate skill's BEST_PRACTICES.md guide (50KB, 1,685 lines) violates every progressive disclosure principle. While content quality is excellent, organization is the critical failure point.

**The 3-phase reorganization:**
1. **Phase 1** breaks the monolithic guide into modular topic-specific documents
2. **Phase 2** optimizes SKILL.md metadata and consolidates redundant tables
3. **Phase 3** establishes clear navigation hierarchy with INDEX.md

**Expected outcome:** New users go from 15-minute discovery path to 5-minute quick-start path, with deeper content available at Level 3 when needed.

**Success criteria:** All documents follow 3-level progressive disclosure, no file exceeds 10KB at Levels 1-2, and user navigation is explicit with INDEX.md routing.
