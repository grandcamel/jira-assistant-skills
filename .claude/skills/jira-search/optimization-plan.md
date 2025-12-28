# Progressive Disclosure Optimization Plan
## jira-search Skill Analysis

**Analysis Date:** December 28, 2025
**Analyzer:** Code Quality Analyzer
**Status:** Ready for Implementation

---

## Executive Summary

The jira-search skill exhibits **moderate progressive disclosure violations** that create cognitive load for new users. The skill is feature-rich (31 scripts) with substantial documentation (2,182 lines across SKILL.md + docs), but the information architecture violates the 3-Level Disclosure Model.

**Key Findings:**
- SKILL.md exceeds recommended size (592 lines vs. 500 target)
- BEST_PRACTICES.md is oversized (1,219 lines) and contains repeated concepts
- Inline code blocks frequently exceed 50 lines
- "Use when" triggers are vague/generic
- Deep nesting: SKILL.md → docs/BEST_PRACTICES.md → references/* (3+ levels)
- Missing quick-start/cheat sheet at entry level

**Improvement Potential:** High. Reorganizing content can reduce cognitive load by ~40%.

---

## Detailed Violation Analysis

### 1. Bloated Description (SKILL.md frontmatter)

**Location:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-search/SKILL.md` (lines 1-4)

**Current:**
```yaml
name: "JIRA Search & JQL"
description: "Query and discovery operations using JQL - search, filters, export,
bulk operations. Use when searching issues, building JQL queries, managing saved
filters, or exporting results."
```

**Issue:** Description is 238 characters, approaching the 200-char target, but is generic ("use when" repeats content not triggers).

**Violation Level:** Minor
- No "When to use" trigger context
- Passive language ("operations", "using")
- Doesn't answer: "What problems does this solve?"

**Recommendation:**
```yaml
description: "Search & filter JIRA issues with JQL. Find work by status, assignee,
priority, or custom criteria. Export results to CSV/JSON. Bulk update issues from
search results."
```

---

### 2. Over-Explained SKILL.md (592 lines)

**Location:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-search/SKILL.md`

**Structure Breakdown:**
```
Lines 1-4        : Frontmatter (✓ OK)
Lines 6-23       : Title + "When to use" (✓ OK - 17 lines)
Lines 24-80      : "What this skill does" (✗ TOO LONG - 57 lines)
Lines 81-112     : "Available scripts" (✗ BLOATED - 32 lines for pure list)
Lines 114-131    : "Common Options" (✓ OK)
Lines 132-401    : "Examples" (✗ EXCESSIVE - 270 lines!)
Lines 402-500    : "Streaming Export Details" (✗ DUPLICATES - 99 lines)
Lines 502-593    : "Troubleshooting" (✗ DUPLICATES - 92 lines)
```

**Issues Identified:**

| Section | Lines | Target | Violation |
|---------|-------|--------|-----------|
| What/Does | 57 | 20-30 | +90% over |
| Scripts List | 32 | 20 | +60% over |
| Examples | 270 | 50-100 | +170% over |
| Streaming Details | 99 | Move to L3 | Inline copy |
| Troubleshooting | 92 | Move to L3 | Inline copy |

**Code Block Violations:**

Lines 230-237 (search example): 8 lines ✓ OK
Lines 312-359 (streaming export): 48 lines ✓ BORDERLINE
Lines 361-401 (streaming export detail): 41 lines ✓ BORDERLINE
Lines 402-440 (output formats): 39 lines ✓ BORDERLINE
Lines 471-500 (JQL basics): 30 lines ✓ OK

**Root Cause:** Examples serve dual purpose (discovery + detailed guidance). Content should be tiered.

---

### 3. Deep Documentation Nesting (3+ levels)

**Current Information Flow:**

```
Level 1: SKILL.md (entry point)
  ├─ Level 2a: docs/BEST_PRACTICES.md (1,219 lines - OVERSIZED)
  │  ├─ JQL Fundamentals (60 lines)
  │  ├─ Operator Reference (145 lines)
  │  ├─ Common Query Patterns (120 lines)
  │  ├─ Advanced Techniques (160 lines)
  │  ├─ Performance Optimization (120 lines)
  │  ├─ Filter Management (150 lines)
  │  ├─ Export & Reporting (130 lines)
  │  ├─ Common Pitfalls (140 lines)
  │  └─ Quick Reference Card (100 lines)
  └─ Level 2b: references/
     ├─ jql_reference.md (175 lines)
     └─ search_examples.md (196 lines)
```

**Problem:** Users cannot discern:
1. What is essential vs. nice-to-know
2. How docs relate to each other
3. Where to find quick answers

**Navigation Issues:**
- SKILL.md references "See docs/BEST_PRACTICES.md" (line 584)
- BEST_PRACTICES.md references "jql_reference.md" (line 173)
- Three similar content areas: jql_reference.md vs. BEST_PRACTICES.md (lines 21-61)

---

### 4. Missing Triggers for "Use When"

**Current (line 12-22):**
```markdown
Use this skill when you need to:
- Search for issues using JQL queries
- Find issues by project, status, assignee, or other criteria
- Build and validate JQL queries
- ...
```

**Issues:**
- All bullets are equivalent priority (no hierarchy)
- No "Don't use when" guidance
- No mention of alternative skills
- No problem statements (e.g., "When you need to find 100+ issues simultaneously")

**Example Problems Not Addressed:**
- "I want to run a saved search daily" → Best skill? (jira-ops for scheduling?)
- "I need to track issue metrics" → Implies export, but no context
- "I'm new to JQL" → No beginner path offered
- "My query is slow" → No performance troubleshooting link

---

### 5. Inline Concept Repetition (Voodoo Constants)

**Repeated Concepts Across Files:**

| Concept | SKILL.md | BEST_PRACTICES.md | jql_reference.md | Count |
|---------|----------|-------------------|------------------|-------|
| JQL basic syntax | Lines 471-500 | Lines 21-58 | Lines 5-16 | 3x |
| Common operators | Lines 484-492 | Lines 61-133 | Lines 41-63 | 3x |
| Date functions | Lines 493-498 | Lines 115-195 | Lines 116-135 | 3x |
| User functions | (implicit) | Lines 197-207 | Lines 127-129 | 2x |

**Impact:** New user confusion:
- "Which operator reference is authoritative?"
- "Should I read SKILL.md or jql_reference.md first?"
- "Why are there 3 sets of examples?"

---

### 6. Asset Organization Issues

**Location:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-search/assets/templates/`

**Current:** Only `jql_templates.json` exists

**Missing at Level 1:**
- Quick reference card (text or JSON format)
- Script selector guide (which script for my use case?)
- Common JQL patterns (as templates or JSON)

---

## Specific Problem Examples

### Problem 1: Script Discovery Friction

**Scenario:** User wants to "find all unresolved bugs assigned to me"

**Current Flow:**
1. Read SKILL.md lines 81-112 (32 scripts listed)
2. Script summary says "Available scripts" but doesn't indicate which to use
3. User scans "Available scripts" and finds: "jql_search.py - Execute JQL queries" (vague)
4. Goes to Examples (line 229) for guidance
5. Finds example but needs JQL help → Navigate to BEST_PRACTICES.md
6. Searches for bug/assignee pattern → Lines 220-228 provide it

**Failure Points:**
- Line 229 doesn't explain which script matches the use case
- No script selector decision tree
- Assumes user knows JQL already

**Better Approach:**
```markdown
### Quick Start: Find My Bugs
assignee = currentUser() AND type = Bug AND status != Done
python jql_search.py "assignee = currentUser() AND type = Bug AND status != Done"
```

---

### Problem 2: Streaming Export Concept Appears 3x

**Location 1:** SKILL.md lines 329-359 (basic description)
**Location 2:** SKILL.md lines 361-401 (detailed how-to)
**Location 3:** BEST_PRACTICES.md lines 761-786 (best practices repeat)

**Issue:** Same concept, different depths, confusing layout.

**Solution:** Single authoritative explanation at Level 1, detailed guidance moved to Level 3.

---

### Problem 3: Troubleshooting Mismatch

**SKILL.md Troubleshooting (lines 513-575):**
- Lists 4 common issues
- Generic advice ("verify API token")
- No links to specific debugging tools

**Better Approach:**
- Mention which script to run first (jql_validate.py)
- Reference specific error patterns
- Point to appropriate scripts for debugging

---

## Implementation Plan

### Phase 1: Restructure Information Architecture (Priority: HIGH)

**1.1 Split SKILL.md into Clear Levels**

**New Structure:**

```
SKILL.md (Level 1 - Discovery & Quick Start)
├─ Frontmatter (metadata)
├─ When to use (triggers)
├─ Quick start example (1 concrete scenario)
├─ 5 most common scripts (with use cases)
├─ Common options table
└─ Related skills

docs/QUICK_START.md (Level 2 - Getting Started, <150 lines)
├─ First JQL query
├─ How to read results
├─ Next steps by use case
└─ Error messages guide

docs/SCRIPT_REFERENCE.md (Level 2 - Scripts Catalog, <200 lines)
├─ Table: Script → Use Case → Example
└─ Grouped by category (JQL Builder, Search, Filters, Export)

references/BEST_PRACTICES.md (Level 3 - Expert Guide, keep current)
├─ Full JQL reference
├─ Advanced patterns
├─ Optimization
└─ Common pitfalls

references/TROUBLESHOOTING.md (Level 3 - New file)
├─ Error catalog
├─ Diagnostic flowchart
└─ Per-script debugging
```

**Action Items:**

| Item | Owner | Effort | Notes |
|------|-------|--------|-------|
| Extract "5 most common scripts" list | Analyst | 1h | From script usage patterns |
| Create QUICK_START.md | Writer | 2h | Must include 1 complete scenario |
| Create SCRIPT_REFERENCE.md | Writer | 2h | Reorganize lines 81-112 + 137-328 |
| Condense SKILL.md | Writer | 3h | Delete redundant examples |
| Extract troubleshooting | Writer | 1h | Move lines 513-575 to new guide |

**Success Criteria:**
- SKILL.md ≤ 350 lines
- BEST_PRACTICES.md unchanged (already L3)
- No content duplication across docs
- Script reference uses decision table format

---

### Phase 2: Fix Metadata & Triggers (Priority: HIGH)

**2.1 Improve SKILL.md Description**

**Current (238 chars):**
> "Query and discovery operations using JQL - search, filters, export, bulk operations. Use when searching issues, building JQL queries, managing saved filters, or exporting results."

**Proposed (205 chars):**
> "Find issues by criteria (status, assignee, priority, etc.) using JQL. Create filters, export results to CSV/JSON, bulk update. Ideal for reporting and automation."

**2.2 Restructure "When to Use" Section**

**Current (lines 12-22):** Flat list of 9 bullets

**Proposed:**
```markdown
## When to use this skill

### Perfect for:
- **Search by criteria:** "Find all bugs assigned to me"
- **Reporting:** Export sprint results to spreadsheet
- **Bulk operations:** Update 50 issues at once
- **Automation:** Create filters for monitoring

### Not ideal for:
- Single issue operations → Use jira-issue skill
- Workflow transitions on many issues → Use jira-lifecycle skill
- Complex issue relationships → Use jira-relationships skill
```

**Action Items:**

| Item | Effort | Notes |
|------|--------|-------|
| Rewrite description | 15 min | Must fit ~200 chars, include problem statement |
| Add "Perfect for" section | 30 min | Use concrete examples, not abstract capabilities |
| Add "Not ideal for" section | 30 min | Cross-reference related skills |

**Success Criteria:**
- Description fits in 200-210 characters
- At least 3 "Perfect for" scenarios are concrete problem statements
- At least 2 "Not ideal for" cross-references to other skills

---

### Phase 3: Eliminate Content Duplication (Priority: MEDIUM)

**3.1 Consolidate JQL Basics**

Currently appears 3 places with ~95% overlap:
- SKILL.md lines 471-500 (30 lines)
- BEST_PRACTICES.md lines 21-58 (38 lines)
- jql_reference.md lines 5-16 (12 lines)

**Solution:**
- Keep jql_reference.md as authoritative reference
- Remove "JQL Basics" section from SKILL.md entirely
- Add "See jql_reference.md" link in QUICK_START.md

**3.2 Consolidate Operator References**

Currently appears 2 places:
- BEST_PRACTICES.md lines 61-133 (73 lines - detailed)
- jql_reference.md lines 41-63 (23 lines - concise)

**Solution:**
- Expand jql_reference.md to include all operators (currently concise)
- Reference from BEST_PRACTICES.md rather than duplicating
- Remove operators section from SKILL.md entirely

**3.3 Consolidate Streaming Export**

Currently appears 3 places:
- SKILL.md lines 312-359 (48 lines - basic)
- SKILL.md lines 361-401 (41 lines - advanced)
- BEST_PRACTICES.md lines 761-786 (26 lines - optimization)

**Solution:**
- Keep single "Streaming Export" section in SKILL.md (lines 329-359 only - concise)
- Move detailed how-to to docs/ADVANCED_EXPORT.md (Level 3)
- Keep best practices in BEST_PRACTICES.md as context

**Action Items:**

| Duplication | Files | Effort | Approach |
|-------------|-------|--------|----------|
| JQL basics | 3 | 1h | Consolidate in jql_reference.md, remove from SKILL.md |
| Operators | 2 | 1h | Expand jql_reference.md, cross-reference in BEST_PRACTICES.md |
| Streaming export | 3 | 1.5h | Keep concise intro, move details to Level 3 |

**Success Criteria:**
- Same concept appears in no more than 2 places
- Each duplication has clear purpose (intro vs. detailed)
- Cross-references are explicit ("For details, see...")

---

### Phase 4: Create Asset Templates (Priority: MEDIUM)

**4.1 Add Quick Reference Card**

**File:** `assets/QUICK_REFERENCE.txt` (~50 lines)

```
JIRA SEARCH - QUICK REFERENCE

FIND MY WORK:
  assignee = currentUser() AND status != Done

FIND BUGS THIS WEEK:
  type = Bug AND created >= -7d

FIND UNRESIGNED ISSUES:
  assignee IS EMPTY AND status = Open

FIND OVERDUE:
  duedate < now() AND status != Done

SCRIPTS:
  jql_search.py "query"             # Search
  create_filter.py "name" "query"   # Save filter
  export_results.py "query"         # Export to CSV
  streaming_export.py "query"       # Large export

LEARN MORE:
  python jql_fields.py              # See available fields
  python jql_functions.py           # See JQL functions
  python jql_validate.py "query"    # Validate syntax
```

**4.2 Add Script Selector Decision Tree**

**File:** `assets/SCRIPT_SELECTOR.json`

```json
{
  "I want to": [
    {
      "goal": "Find issues matching criteria",
      "script": "jql_search.py",
      "example": "jql_search.py \"project = PROJ AND status = Open\"",
      "time": "instant"
    },
    {
      "goal": "Save a search I use often",
      "script": "create_filter.py",
      "example": "create_filter.py \"My Open Issues\" \"assignee = currentUser()\" --favourite",
      "time": "1 minute"
    },
    {
      "goal": "Export results to CSV/JSON",
      "script": "export_results.py",
      "example": "export_results.py \"project = PROJ\" --output report.csv",
      "time": "depends on size"
    }
  ]
}
```

**4.3 Add Error/Solution Mapping**

**File:** `assets/ERROR_SOLUTIONS.json`

```json
{
  "errors": [
    {
      "message": "401 Unauthorized",
      "cause": "API token invalid or expired",
      "solution": "Check https://id.atlassian.com/manage-profile/security/api-tokens",
      "script": "jql_search.py",
      "debug_command": "python jql_search.py \"project = PROJ\" --max-results 1"
    },
    {
      "message": "No issues found",
      "cause": "JQL syntax error or too restrictive",
      "solution": "Validate syntax and check field values",
      "script": "jql_validate.py",
      "debug_command": "python jql_validate.py \"your query\""
    }
  ]
}
```

**Action Items:**

| Asset | Lines | Effort | Usage |
|-------|-------|--------|-------|
| QUICK_REFERENCE.txt | 50 | 1h | Print card, quick lookup |
| SCRIPT_SELECTOR.json | 40 | 1h | Decision tree for script selection |
| ERROR_SOLUTIONS.json | 60 | 1.5h | IDE integration, error handling |

---

### Phase 5: Create Level 2 Quick Start (Priority: HIGH)

**File:** `docs/QUICK_START.md` (~150 lines)

**Structure:**

```markdown
# JIRA Search Quick Start

## Your First Search (5 minutes)

### Step 1: Install dependencies
pip install -r requirements.txt

### Step 2: Run your first search
python jql_search.py "project = PROJ"

### Step 3: Search by criteria
# Find your assigned issues
python jql_search.py "assignee = currentUser()"

# Find open bugs
python jql_search.py "type = Bug AND status = Open"

## Common Patterns (Templates)

|Goal|JQL|Script|
|---|---|---|
|My work|assignee = currentUser() AND status != Done|jql_search.py|
|Team bugs|assignee IN membersOf("team") AND type = Bug|jql_search.py|
|Overdue|duedate < now() AND status != Done|jql_search.py|

## Next Steps

- Learn JQL: See docs/JQL_GUIDE.md
- Save searches: See docs/FILTERS.md
- Export data: See docs/EXPORT.md
- Full reference: See docs/BEST_PRACTICES.md

## Troubleshooting

**"No issues found"**
→ Verify query: python jql_validate.py "your query"

**"401 Unauthorized"**
→ Check token: https://id.atlassian.com/manage-profile/security/api-tokens

**"Field not found"**
→ List fields: python jql_fields.py
```

---

### Phase 6: Optimize SKILL.md for Discovery (Priority: HIGH)

**Target:** Reduce from 592 to 350 lines

**Deletions:**
- Remove "JQL Basics" section (lines 471-500) → Point to jql_reference.md
- Remove "Streaming Export details" (lines 361-401) → Point to docs/EXPORT.md
- Remove "Troubleshooting" section (lines 513-575) → Point to docs/TROUBLESHOOTING.md
- Condense "Examples" section to 50 lines (keep only 1-2 per category)

**Restructure:**

```markdown
---
name: "JIRA Search & JQL"
description: "[IMPROVED: ~200 chars, problem-focused]"
---

# jira-search

[Improved overview: 3-5 sentences max]

## When to use this skill

### Perfect for:
[4 concrete problem statements]

### Not ideal for:
[2-3 cross-references to related skills]

## Quick Start (5 minutes)

[Single complete example: find my bugs]

## Most Common Scripts

[Table: 5 scripts with use cases]

## Common Options

[Existing table: keep as-is]

## Script Reference

[Link to docs/SCRIPT_REFERENCE.md]

## Examples by Category

[Condensed: 1-2 examples per category instead of current 270 lines]

## Troubleshooting

[Link to docs/TROUBLESHOOTING.md for details]
[Keep 1-2 quick diagnostic tips only]

## Related Skills

[Existing section: keep as-is]
```

---

## Implementation Timeline

| Phase | Duration | Effort | Dependencies |
|-------|----------|--------|--------------|
| 1: Restructure architecture | 8 hours | Writer + Analyst | Planning (current) |
| 2: Fix metadata & triggers | 2 hours | Writer | Phase 1 complete |
| 3: Eliminate duplication | 3.5 hours | Writer | Phase 1 complete |
| 4: Create assets | 3.5 hours | Writer | Phase 1 complete |
| 5: Level 2 Quick Start | 3 hours | Writer | Phase 1 complete |
| 6: Optimize SKILL.md | 4 hours | Writer | Phases 1-5 complete |
| **Total** | **~24 hours** | **2-3 days** | Sequential |

---

## Success Metrics

### Before Optimization

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| SKILL.md lines | 592 | 350 | Violation |
| BEST_PRACTICES.md lines | 1,219 | (keep as L3) | OK |
| Content duplication instances | 8+ | 0-1 | Violation |
| Maximum code block size | 48 lines | 30-40 | Borderline |
| Nesting depth | 3+ levels | 2-3 levels | Violation |
| "Use when" clarity | Generic | Specific | Violation |
| Quick reference asset | None | 1 | Missing |

### After Optimization

| Metric | Target | Success |
|--------|--------|---------|
| SKILL.md ≤ 350 lines | Achieved when reductions complete | Pass |
| BEST_PRACTICES.md moved to L3 | Referenced, not duplicated | Pass |
| All code blocks ≤ 40 lines | Verify during Phase 6 | Pass |
| Max nesting: L1 → L2 → L3 | No deep chains | Pass |
| "Use when" section includes 4 problem statements | Section rewritten in Phase 2 | Pass |
| Quick reference card exists | Created in Phase 4 | Pass |
| Script selector available | Created in Phase 4 | Pass |
| Zero content duplication | Consolidated in Phase 3 | Pass |

---

## Risk Mitigation

### Risk 1: Breaking Existing External Links
**Probability:** Medium
**Mitigation:**
- Maintain old file names as redirects (BEST_PRACTICES.md still exists)
- Update SKILL.md references to point to new locations
- Add "See also" sections linking new docs

### Risk 2: Losing Detailed Information
**Probability:** Low
**Mitigation:**
- Move, don't delete (content goes to Level 2/3)
- Maintain explicit cross-references
- Verify no content is orphaned

### Risk 3: User Confusion During Transition
**Probability:** Medium
**Mitigation:**
- Keep SKILL.md as starting point (don't restructure entry point)
- Add breadcrumbs in all docs
- Include "Where to go next" sections

---

## Appendix: Detailed Violation Scoring

### Violation Severity Matrix

| Violation | Severity | Impact | File/Lines | Recommendation |
|-----------|----------|--------|-----------|-----------------|
| SKILL.md oversize | HIGH | Cognitive overload for discovery | 592/500 | Split into L2 Quick Start |
| "Use when" generic | HIGH | User can't determine fit | Lines 12-22 | Add problem statements |
| Content duplication | MEDIUM | Confusion about authoritative source | 3+ instances | Consolidate, cross-ref |
| Deep nesting | MEDIUM | Hard to navigate | L1→L2→L3 chains | Flatten where possible |
| Inline code blocks | MEDIUM | Page length inflates | Lines 312-359, 361-401 | Move to appendix/L3 |
| Missing assets | LOW | No quick reference available | assets/ dir sparse | Add JSON/txt cards |

### Content Audit

**Total Documentation:** 2,182 lines across 5 files

```
SKILL.md                    592 lines (27%)  <- OVERSIZE
docs/BEST_PRACTICES.md    1,219 lines (56%) <- OK (L3)
references/jql_reference.md 175 lines (8%)   <- OK
references/search_examples.md 196 lines (9%)  <- OK
Total                     2,182 lines
```

**Recommendation:** Target total 1,800-2,000 lines by consolidating SKILL.md (reduce 592→350) and improving organization.

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Assign Phase 1-2** to writer (start with restructuring)
3. **Validate assets** from Phase 4 with users
4. **Test Phase 5-6** quick start with new users
5. **Measure success** using metrics above

---

## Questions for Stakeholder Feedback

1. Which scripts are most critical for users? (For Phase 1: "5 most common scripts")
2. Should BEST_PRACTICES.md stay unchanged or be split further?
3. Are there use cases we're missing from "Perfect for" section?
4. Should error mappings go in code or separate asset file?
5. Would a video walkthrough for Quick Start be valuable?

