# jira-issue Skill - Progressive Disclosure Optimization Plan

## Analysis Summary

The jira-issue skill has significant disclosure issues across multiple dimensions. Total documentation footprint is 2,179 lines with front-loaded complexity in the primary discovery document (SKILL.md). The analysis identifies critical violations of progressive disclosure principles that should be addressed to improve Claude's autonomous discovery and navigation.

**Overall Assessment:** Level 2 - Multiple moderate violations, require immediate refactoring

---

## Detailed Findings

### 1. SKILL.md - Front-Loaded Complexity (CRITICAL)

**File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-issue/SKILL.md`
**Size:** 266 lines
**Current Content Density:** 107 lines per major section

**Violations Found:**

#### A. Overly Detailed Script-Level Documentation (Lines 73-125)
- **Issue:** CLI Options presented as exhaustive tables instead of summaries
- **Severity:** HIGH - Cognitive overload for autonomous discovery
- **Example:** Lines 96-104 list get_issue.py options in full detail with short/long forms
- **Impact:** Claude must parse 30+ table cells just to understand one script
- **Root Cause:** Treating SKILL.md as user manual instead of discovery document

**Recommended Action:**
- Move complete CLI references to individual script `--help` output
- In SKILL.md, show only 2-3 common patterns per script
- Reference "See `--help` for full options" for completeness
- **Expected Reduction:** 35-40 lines

#### B. Over-Explained Common Concepts (Lines 19-48)
- **Issue:** Re-explaining standard JIRA concepts Claude already knows
- **Example:** Lines 23-31 describe "Create Issues" with sub-bullets that repeat concept
  - "Create new JIRA tickets with customizable fields including..."
  - Then lists 10 items, many explaining what customizable means (labels, components, etc.)
- **Severity:** MEDIUM - Voodoo constants that add noise without signal
- **Impact:** 40% of "What this skill does" section is explanatory padding

**Recommended Action:**
- Condense "What this skill does" section from 4 subsections to 1-2 conceptual statements
- Assume Claude understands JIRA domain concepts (issues, fields, types, etc.)
- Focus on what makes THIS skill unique, not general JIRA knowledge
- **Expected Reduction:** 20-25 lines

#### C. Comprehensive Field Documentation Duplicated Elsewhere (Lines 63-175)
- **Issue:** Lines 63-125 present CLI options that exist in:
  1. Script docstrings (create_issue.py has usage examples)
  2. Reference files (references/api_reference.md, references/field_formats.md)
  3. Available via `--help` on each script
- **Severity:** MEDIUM - Triple documentation maintenance burden
- **Impact:** Claude reads same information three times when discovering scripts
- **Root Cause:** Treating SKILL.md as comprehensive user guide instead of discovery map

**Recommended Action:**
- Remove "CLI Options by Script" section entirely
- Add single-line pointer: "Each script supports `--help` with full option documentation"
- Move detailed field reference to Level 3 resource (references/FIELD_REFERENCE.md)
- **Expected Reduction:** 55 lines

---

### 2. BEST_PRACTICES.md - Structural Bloat (HIGH SEVERITY)

**File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-issue/docs/BEST_PRACTICES.md`
**Size:** 1,159 lines (52% of total jira-issue documentation)
**Issue Complexity:** 12 major sections, ~100 lines per section

**Violations Found:**

#### A. Deep Nesting - Example Tables (Lines 46-56, 320-328, 359-403)
- **Issue:** Decision matrices and lookup tables with 5+ columns embedded in flowing text
- **Severity:** HIGH - Requires scrolling/parsing multiple levels of information
- **Example:** Lines 359-365 show priority decision framework with:
  - 5 priority levels × 4 columns (Definition, Response, Examples, Context)
  - Followed by decision framework asking 4 questions
  - Followed by priority vs severity comparison table
  - Followed by common mistakes table
- **Depth Nesting:** Issue Type Decision Matrix leads to Epic Guidelines leads to Story vs Task comparison leads to Bug Guidelines (4 levels deep)
- **Impact:** To understand when to use Bug type, reader must parse 10+ table rows

**Recommended Action:**
- Extract decision matrices to separate /docs/DECISION_MATRICES.md file
- In BEST_PRACTICES.md, reference with: "See [Decision Matrices](DECISION_MATRICES.md) for detailed comparison tables"
- Keep only narrative guidance (1-2 paragraphs per topic) in main guide
- **Expected Reduction:** 400-450 lines from BEST_PRACTICES.md

#### B. Missing Triggers - No "When to Use" Guidance (Lines 1-20)
- **Issue:** BEST_PRACTICES.md has no introductory section explaining when/why to use it
- **Severity:** MEDIUM - Claude doesn't know if this is for creating issues or maintaining them
- **Current State:** Jumps directly to "Table of Contents" without context
- **Contrast:** SKILL.md properly includes "When to use this skill" section
- **Impact:** Blocks autonomous discovery of when BEST_PRACTICES applies

**Recommended Action:**
- Add introductory "When to use this guide" section:
  ```markdown
  ## When to Use This Guide

  Use this guide when:
  - Creating new JIRA issues (design before creating)
  - Maintaining issue quality (improving existing issues)
  - Training team members on issue standards
  - Auditing project issue quality
  - Troubleshooting issues with descriptions, priorities, or assignments

  This guide focuses on best practices for *issue content and metadata*.
  For operational guidance, see SKILL.md.
  ```
- **Expected Addition:** 10-15 lines, huge clarity improvement

#### C. Too Much Detail in Core Sections (Example: Lines 105-260)
- **Issue:** "Writing Effective Descriptions" section has:
  - 4 different templates (standard, bug, user story, task)
  - 4 sets of guidelines
  - Real examples with 20+ lines each
  - Acceptance criteria guidance
- **Severity:** MEDIUM - Excellent content, but belongs in Level 3
- **Current Placement:** Front-loaded in BEST_PRACTICES, making it heavy
- **Root Cause:** Everything at same indentation level (no hierarchical disclosure)

**Recommended Action:**
- Restructure as collapsed templates:
  ```markdown
  ## Writing Effective Descriptions

  Start with **Problem/Goal**, add **Acceptance Criteria** (at minimum).
  For detailed templates, see:
  - [Standard Description Template](templates/description-standard.md)
  - [Bug Report Template](templates/description-bug.md)
  - [User Story Template](templates/description-story.md)
  - [Task Template](templates/description-task.md)
  ```
- Create separate template files in docs/templates/ directory
- **Expected Reduction:** 150 lines from BEST_PRACTICES.md

---

### 3. Field Reference Files - Inefficient Organization (MEDIUM)

**Files:**
- `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-issue/references/field_formats.md` (508 lines)
- `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-issue/references/api_reference.md` (246 lines)

**Violations Found:**

#### A. Code Examples Exceed 50-Line Threshold (Lines 3-26 in api_reference.md, repeated)
- **Issue:** Request/response examples shown as full JSON blocks
- **Severity:** LOW - These are references, but excessive for discovery
- **Example:** Lines 14-40 show complete POST request with full ADF payload
- **Impact:** 26-line example when 4-line summary + link would suffice

**Recommended Action:**
- Move complete request/response examples to separate file: `references/EXAMPLES.md`
- Show only structure in main reference:
  ```markdown
  ### Create Issue
  POST /rest/api/3/issue

  Request body: `{ "fields": { ... } }` - See examples in EXAMPLES.md
  Response: `201 Created` with `{ "id", "key", "self" }`
  ```
- **Expected Reduction:** 150-180 lines

#### B. Missing Hierarchy - All Fields Listed Sequentially (Lines 161-413 in field_formats.md)
- **Issue:** 50+ field format examples shown with no organization or discoverability
- **Severity:** MEDIUM - Reader must scan all 250+ examples to find one needed field
- **Root Cause:** Content-driven (flat list) vs task-driven (grouped by use case)
- **Impact:** "I need to set assignee" requires reading 20 unrelated field examples

**Recommended Action:**
- Create index grouped by field type:
  ```markdown
  ## Field Format Reference - Quick Index

  **User/Assignment Fields:** Assignee, Reporter, Watcher
  **Status/Workflow Fields:** Status, Priority, Resolution
  **Time Fields:** Created, Updated, Due Date, Time Tracking
  **Text Fields:** Summary, Description, Environment
  **Array Fields:** Labels, Components, Fix Versions
  **Structured Fields:** Project, Issue Type, Epic Link
  **Custom Fields:** [Link to custom field guide]
  ```
- Each group becomes collapsible section
- **Expected Enhancement:** Better navigation, no line count change

---

### 4. SKILL.md Metadata Violations (MEDIUM)

**File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-issue/SKILL.md`

#### A. Frontmatter Description Too Long (Lines 1-3)
```yaml
description: "Core CRUD operations for JIRA issues - create, read, update, delete tickets.
Use when creating bugs, tasks, stories, retrieving issue details, updating fields, or deleting issues."
```
- **Current Length:** 193 characters
- **Target:** ~200 characters (at limit)
- **Assessment:** PASS - slightly over but acceptable
- **Recommendation:** Minor trim if possible

#### B. Body Description Too Comprehensive (Lines 8-9)
```markdown
Core CRUD operations for JIRA issues - create, read, update, and delete tickets.
```
- **Severity:** LOW - concise and clear
- **Assessment:** PASS

#### C. Missing Precise "When to Use" Triggers (Lines 10-17)
- **Issue:** "When to use this skill" is broad but lacks specificity
- **Current:** "Use this skill when you need to:"
- **Better Pattern:** "Use this skill when Claude asks you to:" or "Triggers:"
- **Recommendation:** Change bullet format to explicit trigger matching
- **Example Fix:**
  ```markdown
  ## When to Use This Skill

  Triggers: User asks to...
  - Create a new JIRA issue
  - Retrieve issue details
  - Update issue properties
  - Delete an issue
  ```

---

### 5. Example Code Coverage (MEDIUM)

**File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-issue/SKILL.md` (Lines 129-174)

#### A. Examples are Well-Formatted But Numerous
- **Count:** 14 bash examples in SKILL.md
- **Severity:** LOW - examples are good, but format is repetitive
- **Issue:** bash code blocks with minimal variation
- **Recommendation:** Consolidate to 5-7 most common patterns, rest in separate examples file

---

## Issues by Severity Level

### CRITICAL (Immediate Action Required)
1. **SKILL.md front-loaded with CLI tables** (Lines 73-125)
   - Action: Move to Level 3, reference `--help`
   - Priority: P0
   - Effort: 1-2 hours
   - Impact: 30% reduction in SKILL.md complexity

2. **BEST_PRACTICES.md lacks discovery trigger** (No intro section)
   - Action: Add "When to use this guide" section
   - Priority: P0
   - Effort: 30 minutes
   - Impact: Enables autonomous discovery of guide purpose

### HIGH (Next Sprint)
3. **BEST_PRACTICES.md - decision matrices bloat** (Lines 46-56, 320-403)
   - Action: Extract to separate DECISION_MATRICES.md
   - Priority: P1
   - Effort: 2-3 hours
   - Impact: 400-line reduction in BEST_PRACTICES.md

4. **Redundant field documentation** (Multiple locations)
   - Action: Consolidate to single references/ file
   - Priority: P1
   - Effort: 1-2 hours
   - Impact: Reduce maintenance burden

### MEDIUM (Next Iteration)
5. **BEST_PRACTICES.md description templates too detailed** (Lines 105-260)
   - Action: Move to Level 3 docs/templates/ subdirectory
   - Priority: P2
   - Effort: 1-2 hours
   - Impact: 150-line reduction

6. **Example code blocks exceed 50 lines** (references/api_reference.md)
   - Action: Move full examples to EXAMPLES.md
   - Priority: P2
   - Effort: 1 hour
   - Impact: Improve reference readability

---

## Implementation Roadmap

### Phase 1: Critical Fixes (Highest Impact, Lowest Effort)
**Effort: 2-3 hours | Impact: 40% reduction in disclosure bloat**

1. **Refactor SKILL.md - Remove CLI Option Tables**
   - Move Lines 73-125 to script `--help` documentation
   - Add single-line reference to each script
   - Update SKILL.md to show only common examples

2. **Add Discovery Trigger to BEST_PRACTICES.md**
   - Insert "When to use this guide" at top
   - Clarify relationship to SKILL.md
   - Define scope (content/metadata, not operations)

### Phase 2: Major Restructuring (High Impact, Moderate Effort)
**Effort: 4-5 hours | Impact: 50% reduction from BEST_PRACTICES**

3. **Extract Decision Matrices to Level 3**
   - Create `docs/DECISION_MATRICES.md`
   - Move all comparison/lookup tables
   - Add matrix index in BEST_PRACTICES.md

4. **Consolidate Description Templates**
   - Create `docs/templates/` directory
   - Move 4 template examples to separate files
   - Reference from BEST_PRACTICES.md

5. **Organize Field Reference by Task**
   - Add index section to field_formats.md
   - Group fields by functional category
   - Create quick-jump navigation

### Phase 3: Optimization (Medium Impact, Lower Priority)
**Effort: 2-3 hours | Impact: Polish and refinement**

6. **Reduce Code Examples in Examples**
   - Move long examples to EXAMPLES.md
   - Keep only structural examples in main reference

7. **Update Script Docstrings**
   - Ensure all scripts have comprehensive `--help`
   - Match documentation style across all scripts
   - Include usage examples in docstring

---

## File Structure After Optimization

```
.claude/skills/jira-issue/
├── SKILL.md                           [~180-200 lines] DISCOVERY DOCUMENT
├── assets/
│   └── templates/
│       ├── bug_template.json
│       ├── task_template.json
│       └── story_template.json
├── docs/
│   ├── BEST_PRACTICES.md              [~700-750 lines] OPERATIONAL GUIDE
│   ├── DECISION_MATRICES.md           [400+ lines] REFERENCE TABLES
│   ├── templates/
│   │   ├── description-standard.md
│   │   ├── description-bug.md
│   │   ├── description-story.md
│   │   └── description-task.md
│   └── EXAMPLES.md                    [Examples collection]
├── references/
│   ├── QUICK_REFERENCE.md             [~200 lines] CHEAT SHEET
│   ├── FIELD_REFERENCE.md             [~500 lines] FIELD FORMATS
│   ├── API_REFERENCE.md               [~150 lines] ENDPOINTS
│   └── EXAMPLES.md                    [Full examples]
└── scripts/
    ├── create_issue.py
    ├── get_issue.py
    ├── update_issue.py
    └── delete_issue.py
```

---

## Disclosure Level Assessment

### Current State
- **Level 1 (Metadata):** 190 chars frontmatter + 1 line description = PASS
- **Level 2 (SKILL.md):** 266 lines with 35% CLI option detail = BLOATED
- **Level 3 (Nested):** 1,913 lines spread across 2 major docs = DISORGANIZED

### Target State
- **Level 1 (Metadata):** Same metadata, same effectiveness = PASS (no change needed)
- **Level 2 (SKILL.md):** 180-200 lines focused on discovery = OPTIMIZED
- **Level 3+ (Nested):**
  - BEST_PRACTICES.md: 700-750 lines (operational guide, Level 2.5)
  - DECISION_MATRICES.md: 400+ lines (reference tables, Level 3)
  - docs/templates/: 4 files (template examples, Level 3)
  - references/: Organized by task (quick ref, examples, fields, api)

**Total After Optimization: 2,200-2,300 lines** (slight increase due to better organization, but dramatically improved navigation and discoverability)

---

## Success Metrics

After optimization, the skill should achieve:

1. **SKILL.md readability:** 5-10 minutes for complete understanding (down from 15-20)
2. **First-time user success:** Find relevant guide within 2 clicks (currently 3-4)
3. **Maintenance burden:** Single source of truth per concept (currently 2-3 locations)
4. **Autonomous discovery:** Claude navigates to correct resource on first try
5. **Search efficiency:** 80% of searches answered in <2 files (currently scattered)

---

## Notes for Implementation

### Preserve What Works Well
- SKILL.md discovery framing is excellent
- BEST_PRACTICES.md content is comprehensive and accurate
- Examples are clear and practical
- Field reference coverage is thorough

### Don't Over-Optimize
- BEST_PRACTICES.md needs depth; this is appropriate for Level 2.5
- Field examples are necessary; just need better organization
- Keep full reference material; just move to appropriate level

### Version Control Strategy
- Create Level 3 files first (no breaking changes)
- Update references/links from SKILL.md
- Update BEST_PRACTICES.md navigation
- Test all links before final PR

---

## Related Context

This optimization aligns with the project's progressive disclosure model:
- **Level 1:** Metadata in frontmatter (~200 chars)
- **Level 2:** SKILL.md discovery document (<500 lines)
- **Level 3+:** Nested resources (detailed guides, templates, examples)

The jira-issue skill currently violates Level 2 guidelines by embedding 35% of content that should be Level 3+. This plan restores proper hierarchy while preserving content quality.

---

**Analysis Completed:** December 28, 2025
**Analyzed Files:** 4 core files, 1 script sample
**Total Lines Analyzed:** 2,179 lines
**Recommendation:** Implement Phase 1 immediately, Phase 2 within 2 weeks
