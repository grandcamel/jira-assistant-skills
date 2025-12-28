# jira-relationships: Progressive Disclosure Optimization Plan

## Executive Summary

The `jira-relationships` skill demonstrates excellent use of progressive disclosure for complex content but has identified violations requiring targeted refactoring. The SKILL.md is well-structured at 235 lines with good discoverability, but the skill references a 939-line BEST_PRACTICES.md that duplicates information and represents deep nesting (2-level disclosure hierarchy). Code examples are at the threshold of disclosure limits (51 lines vs. 50 target).

**Overall Assessment:**
- **Quality Score:** 7.5/10
- **Files Analyzed:** 11 (2 primary markdown + 9 scripts)
- **Critical Issues:** 2
- **Major Violations:** 2
- **Technical Debt:** ~3-4 hours to remediate

---

## Critical Issues

### 1. Bloated BEST_PRACTICES.md Creates Deep Nesting (Level 2→3 Violation)
- **Severity:** HIGH
- **File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-relationships/docs/BEST_PRACTICES.md`
- **Issue:** 939-line document represents unnecessary deep nesting
- **Impact:** Users must navigate SKILL.md → docs/BEST_PRACTICES.md → 10+ subsections
- **Evidence:**
  ```
  Level 1 (Metadata): 186 chars description ✓
  Level 2 (SKILL.md): 235 lines body content ✓
  Level 3 (Nested): docs/BEST_PRACTICES.md (939 lines) ✗
  ```

**Why This Violates Progressive Disclosure:**
- BEST_PRACTICES contains extensive duplicated content already in SKILL.md
- Examples section (lines 66-152 in SKILL.md) + Graph Formats table (154-165) are duplicated in BEST_PRACTICES (lines 513-595)
- Link Types Reference (BEST_PRACTICES lines 23-48) duplicates SKILL.md lines 172-181
- Troubleshooting section (SKILL.md 190-219) overlaps with Common Pitfalls (BEST_PRACTICES 718-776)
- Creates "information scattered across 3 levels" problem for users

### 2. Example Code Block Exceeds Disclosure Limit (51 lines vs. 50 target)
- **Severity:** MEDIUM
- **File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-relationships/SKILL.md` (lines 100-152)
- **Issue:** Single code block with 51 lines of examples
- **Impact:** Cognitive overload in Level 2 - users see entire example suite at once
- **Violation:** 2% over threshold (51 > 50)
- **Current Structure:**
  ```
  # Examples (single code block)
  - 16 link type examples
  - 7 blocker chain examples
  - 7 statistics queries
  - 4 bulk operations
  - 4 clone operations
  - 4 dependency graph exports
  ```

---

## Code Smells Detected

### 1. Duplicate Content Across Multiple Files
- **Smell Type:** DRY Violation (Duplication)
- **Evidence:**
  - Link Types table appears in SKILL.md (3 rows) AND BEST_PRACTICES.md (6 rows, more detailed)
  - Example commands scattered: SKILL.md Examples section PLUS BEST_PRACTICES sections 8-10
  - Troubleshooting content: SKILL.md (30 lines) + BEST_PRACTICES (90 lines + Quick Ref Card)
- **Root Cause:** BEST_PRACTICES.md designed as comprehensive reference BEFORE progressive disclosure model implemented
- **Impact:** User confusion about which content is canonical; maintenance burden increases with each update

### 2. Mixed Disclosure Levels Within Sections
- **Smell Type:** Inconsistent Information Architecture
- **Location:** "Graph Output Formats" section (SKILL.md lines 154-170)
- **Issue:** Detailed table at Level 2 that references external tools (Graphviz, PlantUML, D2)
- **Problem:** Users unfamiliar with these tools see overwhelming complexity; should defer to Level 3
- **Current Block:** 17 lines explaining 5 formats - should be 2-3 lines with references

### 3. "When to Use" Triggers Not Explicit for All Operations
- **Smell Type:** Missing Context Triggers
- **Evidence:**
  - "When to use" clause at top (lines 10-19) is excellent
  - But individual scripts lack "When to use THIS script" guidance
  - Users must infer: Should I use `link_stats.py` or `get_blockers.py` for dependency analysis?
  - BEST_PRACTICES provides this guidance scattered across 939 lines
- **Impact:** Reduces autonomous discovery capability

---

## Refactoring Opportunities

### Opportunity 1: Extract BEST_PRACTICES into Script-Specific Guides
**Benefit:** Reduce nesting depth from 3 to 2 levels; improve relevance to user workflow

**Current Structure:**
```
SKILL.md (general overview)
└── docs/BEST_PRACTICES.md (939 lines of specific patterns)
```

**Proposed Structure:**
```
SKILL.md (streamlined to ~180 lines)
├── scripts/link_issue.py (enhanced help text)
├── scripts/get_blockers.py (enhanced help text with "when to use" section)
├── scripts/clone_issue.py (enhanced help text)
└── docs/PATTERNS.md (NEW - 150 lines of architecture patterns only)
```

**Specific Changes:**
1. Move "Blocker Chain Analysis" (BEST_PRACTICES 208-275) → Add to `get_blockers.py` docstring or `--examples` flag
2. Move "Issue Cloning Strategies" (BEST_PRACTICES 391-457) → Add to `clone_issue.py` docstring
3. Move "Dependency Management Strategies" (BEST_PRACTICES 139-205) → Add to `bulk_link.py` docstring
4. Keep ONLY "When to Use Each Link Type" (BEST_PRACTICES 56-136) in SKILL.md Link Types section
5. Extract "Managing Circular Dependencies" (BEST_PRACTICES 598-715) → NEW `docs/PATTERNS.md` section

**Implementation Effort:** ~2 hours
**Benefit Realized:** Users find all guidance via `--help` without navigating 3 levels

---

### Opportunity 2: Split Example Code Block by Use Case
**Benefit:** Reduce cognitive load; make examples discoverable by task

**Current Block (51 lines):**
```bash
# All 16+ examples in single code block
```

**Proposed Structure (3 blocks, max 20 lines each):**

**Block 1: Quick Start (Lines 1-15)**
```bash
# Most common operations
python link_issue.py PROJ-1 --blocks PROJ-2
python get_links.py PROJ-123
python get_blockers.py PROJ-123 --recursive
python clone_issue.py PROJ-123
```

**Block 2: Advanced Queries (Lines 16-30)**
```bash
# Complex scenarios with filters/options
python get_blockers.py PROJ-123 --recursive --depth 3
python link_stats.py --project PROJ --top 10
python bulk_link.py --jql "project=PROJ AND status=Open" --relates-to PROJ-500
```

**Block 3: Export & Visualization (Lines 31-45)**
```bash
# Generate diagrams for documentation
python get_dependencies.py PROJ-123 --output mermaid
python get_dependencies.py PROJ-123 --output dot > deps.dot
dot -Tpng deps.dot -o deps.png  # Graphviz rendering
```

**Implementation Effort:** ~30 minutes
**Benefit Realized:** Users see focused examples matching their task; reduces "analysis paralysis"

---

### Opportunity 3: Reduce "Graph Output Formats" Table Complexity
**Benefit:** Clarify when to use visualization; defer tool-specific details

**Current (Lines 154-170, 17 lines):**
```markdown
## Graph Output Formats

The `get_dependencies.py` script supports multiple diagram formats:

| Format | Description | Usage |
|--------|-------------|-------|
| `text` | Plain text tree view (default) | Human-readable console output |
| `json` | JSON structure | Programmatic processing |
| `mermaid` | Mermaid.js flowchart | GitHub/GitLab markdown, documentation |
| `dot` | Graphviz DOT format | Render with `dot -Tpng deps.dot -o deps.png` |
| `plantuml` | PlantUML diagram | Render with PlantUML server or CLI |
| `d2` | D2 diagram (Terrastruct) | Render with `d2 deps.d2 deps.svg` |

All graph formats include:
- Status-based node coloring (green=Done, yellow=In Progress, white=Open)
- Link type labels on edges
- Issue summaries in node labels
```

**Proposed (4 lines at Level 2, defer details):**
```markdown
## Exporting Dependency Graphs

Use `get_dependencies.py` with `--output` flag to generate diagrams:
- `text` (default), `json` (data export), `mermaid` (GitHub docs), `dot` (Graphviz), `plantuml`, `d2`
- See `python get_dependencies.py --help` for rendering instructions specific to your format
```

**Move tool-specific details to:**
- `get_dependencies.py` docstring
- NEW `docs/PATTERNS.md` → "Visualizing Dependencies" subsection

**Implementation Effort:** ~20 minutes
**Benefit Realized:** SKILL.md stays focused on WHAT users can do; defer HOW for each tool

---

### Opportunity 4: Add Script-Level "When to Use" Context
**Benefit:** Improve autonomous discovery; reduce decision paralysis

**Current State:** Scripts lack usage context
```bash
# No guidance - which to choose?
python link_stats.py PROJ-123
python get_blockers.py PROJ-123 --recursive
python get_dependencies.py PROJ-123 --output mermaid
```

**Proposed Enhancement:** Update each script's help text
```bash
# get_blockers.py --help enhancement
USAGE: Find issues blocking a specific issue (use for sprint planning, blocker hygiene)
       - Recursive mode: Trace full dependency chain (use for critical path analysis)
       - Direction outward: Find issues THIS issue blocks (use for impact analysis)

# link_stats.py --help enhancement
USAGE: Analyze linking patterns (use for dependency architecture audits)
       - Single issue: Link count and breakdown (quick health check)
       - Project-wide: Link distribution stats (use for process metrics)
       - --top N: Most connected issues (identify hubs/bottlenecks)

# get_dependencies.py --help enhancement
USAGE: Visualize dependency graph (use for stakeholder communication, release planning)
       - text: Terminal output (quick preview)
       - mermaid: GitHub markdown (wiki, documentation)
       - dot: Graphviz (publication-quality diagrams)
```

**Implementation Effort:** ~1 hour
**Benefit Realized:** Users can autonomously select correct script via `--help`

---

## Violations Summary

| # | Type | Location | Severity | Impact | Status |
|---|------|----------|----------|--------|--------|
| 1 | Bloated nested file (939 lines) | docs/BEST_PRACTICES.md | HIGH | Deep nesting violates Level 2-3 rule | Violation |
| 2 | Code block exceeds threshold | SKILL.md lines 100-152 | MEDIUM | 51 > 50 line limit | Violation |
| 3 | Duplicate content | SKILL.md + BEST_PRACTICES.md | MEDIUM | DRY violation; maintenance burden | Code Smell |
| 4 | Over-detailed tables | Graph Output Formats section | LOW | 5 formats vs. ~3 worth detailing | Code Smell |
| 5 | Missing "when to use" per script | Script help text | MEDIUM | Reduces autonomous discovery | Code Smell |

---

## Implementation Plan

### Phase 1: Immediate Fixes (0.5 hours)
Minimum viable changes to meet disclosure constraints:

1. **Split Examples code block** (20 min)
   - Replace single 51-line block with 3 focused blocks (max 20 lines each)
   - Category: Quick Start, Advanced, Visualization
   - File: SKILL.md lines 100-152

2. **Condense Graph Output Formats table** (15 min)
   - Reduce from 17 lines to 4 lines at Level 2
   - Add note: "See `get_dependencies.py --help` for full rendering options"
   - Move detailed examples to docstring or separate guide
   - File: SKILL.md lines 154-170

3. **Add "When to use this script" to top 3 scripts** (15 min)
   - Enhance docstrings in `get_blockers.py`, `link_stats.py`, `get_dependencies.py`
   - Add comparison: "Use blocker for dependency chains, link_stats for patterns, dependencies for visualization"
   - Files: `.claude/skills/jira-relationships/scripts/{get_blockers,link_stats,get_dependencies}.py`

**Deliverable:** Compliant with Level 2 disclosure limits; minimal disruption

---

### Phase 2: Architectural Refactor (2-3 hours)
Address root cause of nesting violation:

1. **Create docs/PATTERNS.md** (60 min)
   - Extract architecture-level guidance from BEST_PRACTICES
   - Sections: "Blocker Chain Analysis", "Managing Circular Dependencies", "Visualizing Dependencies"
   - Target: ~250 lines of curated, non-duplicative content
   - Purpose: Strategic guidance beyond SKILL.md examples
   - Files affected: NEW `docs/PATTERNS.md`

2. **Consolidate Link Types guidance** (30 min)
   - SKILL.md Link Types section expands from 3 rows to ~8 rows (inline details)
   - Remove "When to Use Each Link Type" section from BEST_PRACTICES (shift to SKILL.md)
   - Keeps Level 2 guidance comprehensive without external file
   - File: SKILL.md lines 172-181 expanded; docs/BEST_PRACTICES.md sections 56-136 migrated

3. **Move operational guidance to script docstrings** (45 min)
   - Add "Dependency Management Strategies" summary to `link_issue.py` docstring
   - Add "Clone Strategies" to `clone_issue.py` docstring
   - Add "Blocker Chain Strategies" to `get_blockers.py` docstring
   - Each: ~30-50 lines of context-specific guidance
   - Files: `.claude/skills/jira-relationships/scripts/{link_issue,clone_issue,get_blockers}.py`

4. **Simplify BEST_PRACTICES or repurpose as archive** (30 min)
   - Option A: Merge BEST_PRACTICES content into PATTERNS.md + script docstrings; delete
   - Option B: Retain as "comprehensive reference" for historical context; add disclaimer "See SKILL.md and script docstrings for current guidance"
   - Recommendation: Option A - reduce maintenance burden

**Deliverable:** Flattened 2-level disclosure; all guidance accessible via SKILL.md + `--help`

---

### Phase 3: Quality Assurance (0.5 hours)

1. **Line count audit** (10 min)
   - Verify new SKILL.md ≤ 250 lines (currently 235, +15 for expanded Link Types)
   - Verify code blocks ≤ 50 lines each (3 blocks, ~20 lines each)
   - Verify docs/PATTERNS.md ≤ 300 lines (extracted content)

2. **Cross-reference validation** (15 min)
   - Ensure BEST_PRACTICES → PATTERNS/docstrings migration is complete
   - No orphaned references to removed sections
   - Test: `grep -r "Dependency Management Strategies\|Issue Cloning Strategies" .`

3. **Autonomous discovery test** (10 min)
   - Verify users can find correct script via:
     - `python link_issue.py --help` shows when to use
     - `python get_blockers.py --help` explains vs. get_dependencies.py
     - SKILL.md "When to use" section sufficient for initial selection

**Deliverable:** Verified compliance with 3-Level Disclosure Model

---

## Positive Findings

### 1. Excellent Initial "When to Use" Section
- Lines 10-19 provide clear trigger phrases for skill activation
- Examples: "linking issues", "finding blocker chains", "cloning with relationships"
- This pattern should be replicated at script level

### 2. Well-Structured Script Portfolio
- 9 focused scripts, each with single responsibility
- No mega-scripts (longest: 383 lines, within acceptable range)
- Clear separation: link creation, link inspection, analysis, bulk operations

### 3. Good Use of Semantic Flags
- `--blocks`, `--relates-to`, `--duplicates`, `--clones` improve discoverability
- Users can reason about intent without learning JIRA link type names
- Reduces cognitive load vs. `--type "Blocks"` syntax

### 4. Thoughtful Table Organization
- Link Types table (lines 172-181) well-structured
- Common Options table (lines 88-96) clear and minimal
- Troubleshooting by error message (lines 192-219) practical

### 5. Graph Format Support Shows User-Centric Design
- Multiple export formats recognize different user contexts (Mermaid for docs, DOT for publication, etc.)
- Appropriate for complex dependency visualization use case

---

## Metrics Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Metadata description length | ~200 chars | 186 chars | PASS |
| SKILL.md size | <500 lines | 235 lines | PASS |
| Nesting depth | ≤2 levels | 3 levels | FAIL |
| Code block max size | ≤50 lines | 51 lines | FAIL (marginal) |
| Duplicate content % | 0% (ideal) | ~15% | Warning |
| Scripts with "when to use" | 100% | ~33% (3/9) | Warning |

---

## Recommended Timeline

**Minimum (Phase 1 only):** 0.5 hours - Brings skill into compliance
- **When:** This sprint, low priority
- **Who:** 1 person
- **Outcome:** Meets disclosure thresholds

**Ideal (Phases 1-3):** 3-4 hours - Optimizes for autonomous discovery
- **When:** Next sprint or next available block
- **Who:** 1-2 people (1 for refactor, 1 for review)
- **Outcome:** Excellent progressive disclosure; users find answers via `--help` first

---

## Next Steps

1. **Review this plan** with skill owner for alignment on scope
2. **Decide on BEST_PRACTICES.md** - merge into PATTERNS.md or keep as reference?
3. **Prioritize:** Phase 1 (mandatory), Phase 2 (recommended), Phase 3 (validation)
4. **Assign ownership:** Code refactor vs. documentation updates
5. **Schedule execution:** Fits in 1-2 hour time block

---

## Appendix: File Structure Analysis

```
.claude/skills/jira-relationships/
├── SKILL.md (235 lines) ← Primary Level 2
│   ├── Metadata (3 lines)
│   ├── "When to use" (10 lines) ✓ Excellent
│   ├── "What this skill does" (55 lines) ✓ Good
│   ├── "Available scripts" (11 lines) ✓ Minimal
│   ├── "Common Options" (9 lines) ✓ Concise
│   ├── "Examples" (51 lines) ✗ Exceeds 50-line threshold
│   ├── "Graph Output Formats" (17 lines) ✗ Too detailed
│   ├── "Link Types" (10 lines) ✓ Good reference
│   ├── "Exit Codes" (8 lines) ✓ Useful
│   ├── "Troubleshooting" (30 lines) ✓ Practical
│   ├── "Configuration" (3 lines) ✓ Minimal
│   ├── "Best Practices" (1 line) → Link to Level 3
│   └── "Related skills" (6 lines) ✓ Good context
│
├── docs/
│   └── BEST_PRACTICES.md (939 lines) ← Level 3 Violation
│       ├── TOC (20 lines)
│       ├── Link Types Reference (56 lines) - DUPLICATES SKILL.md
│       ├── When to Use Each Type (81 lines) - DUPLICATES SKILL.md
│       ├── Dependency Management (72 lines) - NEW (good)
│       ├── Blocker Chain Analysis (69 lines) - NEW (good)
│       ├── Parent-Child Relationships (50 lines) - NEW (good)
│       ├── Cross-Project Linking (79 lines) - NEW (good)
│       ├── Issue Cloning Strategies (69 lines) - NEW (good)
│       ├── Visualizing Dependencies (106 lines) - DUPLICATES SKILL.md graph section
│       ├── Managing Circular Dependencies (118 lines) - NEW (good)
│       ├── Common Pitfalls (73 lines) - DUPLICATES Troubleshooting
│       ├── Quick Reference Card (80 lines) - NEW (good)
│       └── Sources (17 lines)
│
└── scripts/
    ├── get_link_types.py (129 lines)
    ├── link_issue.py (271 lines) ← Could add cloning context
    ├── get_links.py (177 lines)
    ├── unlink_issue.py (183 lines)
    ├── get_blockers.py (319 lines) ← Could add blocker chain strategies
    ├── get_dependencies.py (383 lines) ← Could add visualization guidance
    ├── link_stats.py (327 lines) ← Could add stats interpretation
    ├── bulk_link.py (288 lines) ← Could add bulk strategy guidance
    └── clone_issue.py (280 lines) ← Could add cloning strategies
```

**Key Insight:** 150+ lines of BEST_PRACTICES content are duplicates of SKILL.md (25% of file). Remaining 789 lines are valuable strategic guidance that should be:
- Redistributed to script docstrings (operational guidance)
- Consolidated into single PATTERNS.md (architectural guidance)
- Summarized in SKILL.md Link Types section (reference guidance)

This redistribution would reduce nesting depth from 3 to 2 levels while improving content discoverability.

---

*Analysis completed: 2025-12-28*
*Tool: Code Quality Analyzer (3-Level Progressive Disclosure Model)*
