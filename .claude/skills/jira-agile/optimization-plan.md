# jira-agile Skill: Progressive Disclosure Optimization Plan

**Analysis Date:** December 28, 2025
**Current Status:** Requires Significant Restructuring
**Priority:** High

---

## Executive Summary

The jira-agile skill exhibits **critical violations** of the 3-Level Disclosure Model. The primary documentation has grown to 626 lines with an extensive companion guide (1,265 lines), creating cognitive overload. Key issues:

- **Level 2 bloat:** SKILL.md is 17.7 KB (target: <10 KB), ~125% over budget
- **Missing Level 3 delegation:** All content lives in SKILL.md instead of nested resources
- **Inline code dumps:** 40+ line code blocks with full example outputs
- **Deep nesting:** Complex explanations with multiple header levels (H4, H5) that should be separate documents
- **Missing trigger phrases:** Several sections lack clear "use when" guidance

**Estimated improvement potential:** 50% reduction in SKILL.md length while improving discoverability.

---

## Detailed Analysis

### 1. Violation: Bloated Metadata Description

**Current State:**
```yaml
description: "Agile and Scrum workflow management - epics, sprints, backlogs, story points. Use when creating epics, managing sprints, ranking backlog items, or estimating issues."
```

**Metrics:**
- Length: 181 characters (target: ~200 chars max, so this is acceptable)
- However: The "use when" clause is vague and doesn't include all skill purposes

**Issue:** The trigger phrase doesn't mention:
- Subtask management
- Story point estimation beyond the brief mention
- Sprint lifecycle operations (start/close)
- Epic progress tracking
- Issue ranking operations

**Impact:** Users may miss applicable scenarios for this skill.

---

### 2. Violation: Over-Explained Main Documentation

**Current State:**
- SKILL.md: 626 lines, 17.7 KB
- Includes exhaustive usage examples with full output demonstrations
- Every feature has detailed description in main file
- Custom field IDs explained inline
- Integration with other skills documented in-line
- Troubleshooting guide (28 lines) in main file
- Notes, common workflows, best practices references all in main file

**Specific Problems:**

**2a. Level 2 Content Size**
- Lines 24-114: Feature descriptions (90 lines) - too detailed for Level 2
- Lines 115-138: Script listings (24 lines) - acceptable
- Lines 139-199: Common options (61 lines) - should be moved to separate file
- Lines 200-503: Usage examples (304 lines) - **VIOLATES 3-LEVEL MODEL**
- Lines 504-517: Custom field IDs (14 lines) - should reference jira-fields skill
- Lines 518-544: Integration notes (27 lines) - acceptable
- Lines 545-626: Common workflows, troubleshooting, best practices (82 lines) - should move to docs/

**Assessment:** Lines 200-626 (427 lines, 67% of content) should be in Level 3 resources.

**2b. Over-Explained Concepts**
Examples of voodoo constants and unnecessary detail:

- Lines 30-47: Epic Name/Color field IDs explained with default values and instance-variance caveats. Better approach: Reference jira-fields skill for field discovery.
- Lines 35-40: Epic field descriptions mix with script behavior. Separable into: (a) What Epic Name is; (b) How scripts use it.
- Lines 104-114: Story points & estimation section duplicates BEST_PRACTICES.md content extensively.

---

### 3. Violation: Inline Code Dumps

**Current State:**

Lines 200-503 contain 40+ line code blocks with:
- Full command examples
- Full output demonstrations
- Multi-step workflow examples

**Examples:**

```markdown
Lines 257-271: Example output of 24+ lines
Lines 375-388: Example output of 14+ lines
Lines 428-445: Example output of 18+ lines
Lines 488-502: Example output of 15+ lines
```

**Problem:** Each script section (Epic, Subtask, Sprint, Backlog, Estimation) includes:
1. Description
2. Multiple command examples (3-5 variations per script)
3. Example output
4. Repeat for 8 scripts = massive duplication

**Assessment:** 150+ lines of examples should move to separate files:
- `.claude/skills/jira-agile/examples/epic-workflows.md`
- `.claude/skills/jira-agile/examples/sprint-management.md`
- `.claude/skills/jira-agile/examples/estimation-workflow.md`

---

### 4. Violation: Deep Nesting and Missing Links

**Current State:**
- Section "Common Workflows" (lines 545-584) discusses Epic-Driven Development and Sprint Planning
- Contains example commands but lacks structure
- References jira-issue skill without clear links
- Best practices are mentioned but delegated to BEST_PRACTICES.md without clear when-to-use guidance

**Problem:** Users encounter:
- "For common workflows, see COMMON_WORKFLOWS section below" (implicit reference)
- "For comprehensive guidance... see [Best Practices Guide](docs/BEST_PRACTICES.md)" (external link)
- No clear progressive disclosure: What's the minimal workflow? What's advanced?

**Assessment:**
- Create `.claude/skills/jira-agile/docs/QUICK_START.md` for 3-5 essential workflows
- Create `.claude/skills/jira-agile/docs/WORKFLOWS.md` for detailed workflow examples
- Reduce SKILL.md to essential metadata + brief examples

---

### 5. Violation: Missing "Use When" Triggers

**Current State:**

The metadata description and SKILL.md "When to use this skill" section is generic:

```
Use this skill when you need to:
- Create and manage epics for organizing large features
- Link issues to epics for hierarchical planning
- ...
```

**Problem:**
- No guidance on **which skill to choose** when:
  - User wants to create a story that's part of epic → Use jira-issue or jira-agile?
  - User wants to move story to different project → Use jira-issue or jira-agile?
  - User wants to find unestimated stories → Use jira-search or jira-agile?

- Missing negative cases (don't use when):
  - Creating standard issues (use jira-issue)
  - Searching across projects (use jira-search)
  - Managing deployments (use jira-ops)

**Assessment:**
- Enhance metadata description with specific triggers
- Add "Don't use this skill when" section
- Create `.claude/skills/jira-agile/docs/SKILL_SELECTION.md` for disambiguation

---

## Root Causes

1. **Single-file architecture:** All documentation in SKILL.md
2. **Exhaustive approach:** Attempting to cover every use case in main file
3. **No content model:** No distinction between discovery, operation, and reference content
4. **Embedded best practices:** BEST_PRACTICES.md exists but isn't integrated into workflow

---

## Detailed Recommendations

### Phase 1: Restructure Level 2 (SKILL.md)

**Target:** Reduce from 626 to ~300 lines (48% reduction)

#### 1a. Extract Usage Examples (150 lines savings)

**Create:** `.claude/skills/jira-agile/examples/README.md`

```
examples/
├── README.md (index of all examples)
├── epic-management.md (50 lines: create, add-to, get-epic examples)
├── sprint-lifecycle.md (60 lines: create, start, close, move-to-sprint examples)
├── estimation.md (40 lines: story points, summaries)
└── backlog-management.md (35 lines: ranking, viewing)
```

**Action:**
- Move lines 200-271 (Epic examples) to `examples/epic-management.md`
- Move lines 299-356 (Sprint examples) to `examples/sprint-lifecycle.md`
- Move lines 409-445 (Backlog examples) to `examples/backlog-management.md`
- Move lines 447-502 (Estimation examples) to `examples/estimation.md`
- Move lines 545-584 (Common workflows) to `docs/WORKFLOWS.md`
- Update SKILL.md with cross-references: `See [Epic examples](examples/epic-management.md) for detailed usage.`

#### 1b. Extract Troubleshooting (28 lines savings)

**Create:** `.claude/skills/jira-agile/docs/TROUBLESHOOTING.md`

**Action:**
- Move lines 585-623 (Troubleshooting section) to `docs/TROUBLESHOOTING.md`
- Replace in SKILL.md with: `See [Troubleshooting Guide](docs/TROUBLESHOOTING.md) for common issues and solutions.`

#### 1c. Extract Common Options (50 lines savings)

**Create:** `.claude/skills/jira-agile/docs/OPTIONS.md`

**Action:**
- Move lines 139-199 (Profile, Output Format, Dry Run, Exit Codes) to `docs/OPTIONS.md`
- Keep one-line summary in SKILL.md: `All scripts support [common options](docs/OPTIONS.md): --profile, --output, --dry-run.`

#### 1d. Condense Feature Descriptions (40 lines savings)

**Current:** Lines 24-114 provide detailed explanations of each feature

**Action:**
- Reduce each feature section from ~20 lines to ~8 lines
- Example:

```markdown
# Current (20 lines)
### 1. Epic Management

**Create Epics**: Create epic issues with Agile-specific fields:
- Epic Name field (customfield_10011)
- Epic Color for visual organization
- Summary and description (supports Markdown via ADF conversion)
- Standard issue fields (priority, assignee, labels)

**Add Issues to Epics**: Link stories and tasks to epics:
- Single or bulk operations
- Add by issue keys or JQL query
- Remove issues from epics
- Dry-run mode for previewing changes
- Individual failure tracking for bulk operations

[Revised (8 lines)]
### 1. Epic Management

Create epics for organizing large features, link issues to epics for hierarchy, and track progress. Scripts:
- `create_epic.py` - New epic with Epic Name/Color
- `add_to_epic.py` - Bulk add/remove issues to epic
- `get_epic.py` - Epic progress with child issues and story points

See [examples](examples/epic-management.md) for detailed usage.
```

#### 1e. Remove Redundant Notes

**Current:** Lines 537-544 repeat information already in SKILL.md

**Action:**
- Remove lines 537-544
- Fold essentials into appropriate sections

---

### Phase 2: Enhance Level 1 Metadata

**Current:** Simple comma-separated use cases

**Proposed Enhancement:**

```yaml
name: "JIRA Agile Management"
description: "Epic, sprint, and backlog management - create/link epics, manage sprints, estimate with story points, rank backlog issues."
use_when:
  - Creating epics to organize large features
  - Adding issues to epics for hierarchical planning
  - Creating and managing sprints on Scrum boards
  - Setting story points for estimation
  - Ranking backlog items by priority
  - Tracking epic and sprint progress
  - Managing sprint lifecycle (start/close)
  - Breaking down stories into subtasks
do_not_use_when:
  - Creating individual stories/tasks without epic context (use jira-issue)
  - Searching across issues by JQL (use jira-search)
  - Transitioning issues through workflow (use jira-lifecycle)
  - Managing time tracking/worklogs (use jira-time)
  - Discovering field configurations (use jira-fields)
```

**Expected Benefit:**
- Clarifies when skill is applicable
- Reduces ambiguity between skills
- Improves autonomous Claude skill selection

---

### Phase 3: Create New Supporting Documents

#### 3a. Create `docs/QUICK_START.md` (100 lines)

**Content:**
- 3-5 essential workflows (Epic creation → Estimation, Sprint creation → Start)
- Minimal examples (5-line commands, no output)
- Links to detailed examples
- Prerequisites (permissions, JIRA setup)

**Example structure:**
```markdown
# Quick Start Guide

## Essential 5-Minute Workflows

### Workflow 1: Create and Estimate an Epic
1. `python create_epic.py ...`
2. `python add_to_epic.py ...`
3. `python get_epic.py ...`
See [detailed examples](../examples/epic-management.md).
```

#### 3b. Create `docs/SKILL_SELECTION.md` (50 lines)

**Content:**
- Skill comparison table: jira-agile vs jira-issue vs jira-search
- Decision tree: "What should I do?" flowchart
- Cross-references to other skills

**Example:**
```markdown
| Task | Skill | When to Use |
|------|-------|------------|
| Create story | jira-issue | Always for individual stories |
| Create epic | jira-agile | For organizing multiple stories |
| Add story to epic | jira-agile | After creating story with jira-issue |
| Find stories needing estimates | jira-search | Query unestimated items, then pipe to estimate_issue.py |
```

#### 3c. Create `docs/FIELD_REFERENCE.md` (30 lines)

**Current:** Lines 504-517 explain custom field IDs

**Action:**
- Move and condense to `FIELD_REFERENCE.md`
- Include: Default field IDs, how to discover instance-specific IDs, link to jira-fields skill

**Content:**
```markdown
# Agile Custom Fields Reference

This skill uses JIRA's standard Agile custom fields. If your instance uses different field IDs, use the jira-fields skill to discover them.

## Default Custom Field IDs

| Field | Default ID | Purpose |
|-------|-----------|---------|
| Epic Name | customfield_10011 | User-readable epic identifier |
| Epic Color | customfield_10012 | Visual organization |
| Epic Link | customfield_10014 | Links issues to epics |
| Story Points | customfield_10016 | Estimation metric |

## Discovering Your Field IDs

Use jira-fields skill:
```bash
python get_agile_fields.py
```

See [jira-fields skill](../../jira-fields/SKILL.md) for details.
```

#### 3d. Enhance `docs/BEST_PRACTICES.md`

**Current:** 1,265 lines - comprehensive but not well-integrated

**Action:**
- Link from SKILL.md with clear trigger: "For best practices on sprint planning, estimation strategies, and team velocity optimization, see [Agile Best Practices](docs/BEST_PRACTICES.md)."
- Keep as-is (don't reduce): This is appropriate Level 3 content
- Consider creating `.claude/skills/jira-agile/docs/CHECKLIST.md` with print-friendly sprint planning checklist extracted from BEST_PRACTICES.md

---

### Phase 4: Restructure jira-agile Directory

**Current Structure:**
```
jira-agile/
├── SKILL.md (626 lines)
├── docs/
│   └── BEST_PRACTICES.md (1,265 lines)
├── assets/
├── references/ (empty)
├── scripts/ (14 executable Python files)
└── tests/
```

**Proposed Structure:**
```
jira-agile/
├── SKILL.md (≈300 lines, 52% reduction)
├── docs/
│   ├── BEST_PRACTICES.md (unchanged, 1,265 lines - appropriate for Level 3)
│   ├── QUICK_START.md (new, 100 lines)
│   ├── SKILL_SELECTION.md (new, 50 lines)
│   ├── FIELD_REFERENCE.md (new, 30 lines)
│   ├── OPTIONS.md (new, 50 lines - moved from SKILL.md)
│   ├── TROUBLESHOOTING.md (new, 28 lines - moved from SKILL.md)
│   └── WORKFLOWS.md (new, 80 lines - moved from SKILL.md)
├── examples/ (new directory)
│   ├── README.md (index, 15 lines)
│   ├── epic-management.md (50 lines)
│   ├── sprint-lifecycle.md (60 lines)
│   ├── estimation.md (40 lines)
│   └── backlog-management.md (35 lines)
├── references/ (to-be-populated)
├── assets/
├── scripts/
└── tests/
```

**Benefit:** Clear progressive disclosure:
- Level 1 (Metadata): ~200 chars in SKILL.md frontmatter
- Level 2 (Skill overview): 300 lines in SKILL.md body
- Level 3 (Details): 300+ lines across docs/ and examples/

---

## Implementation Roadmap

### Task 1: Restructure SKILL.md (2 hours)

1. Create clean copy of SKILL.md with:
   - Metadata frontmatter (unchanged)
   - "When to use this skill" (enhanced with use_when/do_not_use_when)
   - "What this skill does" (condensed to 8-line summaries per feature)
   - "Available scripts" (unchanged)
   - Cross-references to docs/ and examples/
   - Exit codes table (unchanged, 12 lines)

2. Remove sections:
   - Usage Examples (304 lines) → examples/
   - Common Workflows (40 lines) → docs/WORKFLOWS.md
   - Troubleshooting (28 lines) → docs/TROUBLESHOOTING.md
   - Common Options (61 lines) → docs/OPTIONS.md
   - Notes (8 lines) → Remove or fold into appropriate section

3. Condense sections:
   - Feature descriptions: 90 → 35 lines (61% reduction)
   - Integration notes: Keep 18 lines, remove 9 lines of repetition

### Task 2: Create New Documentation (3 hours)

1. `docs/QUICK_START.md` (100 lines) - 1 hour
2. `docs/SKILL_SELECTION.md` (50 lines) - 30 min
3. `docs/FIELD_REFERENCE.md` (30 lines) - 30 min
4. `docs/OPTIONS.md` (move + edit from SKILL.md) (50 lines) - 30 min
5. `docs/TROUBLESHOOTING.md` (move from SKILL.md) (28 lines) - 15 min
6. `docs/WORKFLOWS.md` (move + reorganize from SKILL.md) (80 lines) - 30 min

### Task 3: Create Examples Directory (2 hours)

1. `examples/README.md` (index, 15 lines) - 15 min
2. `examples/epic-management.md` (extract from lines 200-271) (50 lines) - 30 min
3. `examples/sprint-lifecycle.md` (extract from lines 299-356) (60 lines) - 30 min
4. `examples/estimation.md` (extract from lines 447-502) (40 lines) - 30 min
5. `examples/backlog-management.md` (extract from lines 409-445) (35 lines) - 25 min

### Task 4: Update Cross-References (1 hour)

1. SKILL.md: Add cross-references to all extracted docs/examples
2. BEST_PRACTICES.md: Add "quick reference" section linking to QUICK_START.md
3. Create internal link map in examples/README.md

### Task 5: Verify and Test (1 hour)

1. Validate all markdown links work
2. Ensure no broken references
3. Test `--help` output doesn't reference moved content
4. Verify git commit follows conventional commits format

**Total Estimated Effort:** 9 hours (design + implementation)

---

## Expected Outcomes

### Before Optimization

| Metric | Value |
|--------|-------|
| SKILL.md size | 626 lines, 17.7 KB |
| Lines of examples in SKILL.md | 304 |
| Documentation files | 2 (SKILL.md, BEST_PRACTICES.md) |
| Max header depth | H4 |
| Code block examples | 40+ blocks |

### After Optimization

| Metric | Target |
|--------|--------|
| SKILL.md size | ~300 lines, ~8.5 KB |
| Lines of examples in SKILL.md | ~20 (quick reference only) |
| Documentation files | 8+ (SKILL.md + 6 docs/ + examples/ index) |
| Max header depth | H3 in SKILL.md, H4 in docs/ |
| Code block examples | 20 in examples/, 10 in docs/ |
| **Reduction** | **52% smaller SKILL.md** |

### User Experience Improvements

1. **Faster discovery:** Metadata description includes all use cases
2. **Shorter ramp-up:** QUICK_START.md covers 80% of use cases in 5 minutes
3. **Skill selection clarity:** SKILL_SELECTION.md prevents choosing wrong skill
4. **Detailed examples preserved:** examples/ directory contains all original examples with better organization
5. **Progressive learning:** 3 levels of complexity (metadata → SKILL.md → docs/ → BEST_PRACTICES.md)

---

## Validation Criteria

- [ ] SKILL.md < 350 lines (currently 626, target 300)
- [ ] Average lines per feature section < 10 (currently 15)
- [ ] All examples moved to separate files
- [ ] All links verified (markdown, internal)
- [ ] No duplicate content between SKILL.md and docs/
- [ ] Metadata includes complete use_when triggers
- [ ] examples/README.md provides navigation
- [ ] Git history clean (conventional commits per project standards)

---

## Risk Mitigation

### Risk 1: Users can't find examples

**Mitigation:** Create clear navigation:
- SKILL.md links to examples/README.md
- examples/README.md indexes all example files by workflow
- Each example file has cross-references back to SKILL.md

### Risk 2: Over-fragmentation (too many files)

**Mitigation:** Keep BEST_PRACTICES.md untouched; don't fragment further. Strict file count limit: 8 docs + examples only

### Risk 3: Losing important context

**Mitigation:** Add "See also" sections in moved content that reference related context in SKILL.md

### Risk 4: Broken relative links

**Mitigation:** Use full relative paths (e.g., `../examples/epic-management.md`), test all links before commit

---

## Future Considerations

### Post-Optimization Phase

1. **Dynamic examples generation:** Consider using a tool that generates examples from actual test outputs (ensures examples stay current)
2. **Video tutorials:** Create 3-5 minute video walkthroughs linked from QUICK_START.md
3. **Interactive playground:** Link to JIRA Cloud trial instances pre-populated with test data
4. **Checklist generation:** Auto-generate sprint planning checklists from BEST_PRACTICES.md
5. **Skill maturity levels:** Add difficulty tags to examples (Beginner, Intermediate, Advanced)

### Ongoing Maintenance

- Review QUICK_START.md quarterly based on user questions
- Update BEST_PRACTICES.md with new Agile trends (e.g., "Scaled Scrum", "SAFe")
- Monitor examples/ for divergence from actual script behavior
- Maintain examples/README.md as search index

---

## Summary

The jira-agile skill demonstrates comprehensive feature coverage but violates progressive disclosure by concentrating 626 lines in SKILL.md. This optimization plan restructures content into three clear levels:

1. **Metadata** (~180 chars) - Skill discovery with comprehensive use_when triggers
2. **SKILL.md** (~300 lines) - Overview, script listing, quick reference
3. **Supporting docs** (examples/, docs/) - Detailed examples, workflows, best practices, troubleshooting

The restructuring will reduce SKILL.md by 52% while preserving all content in more accessible locations. Implementation time: ~9 hours.

---

**Next Step:** Begin with Task 1 (SKILL.md restructuring) to establish the new document structure.
