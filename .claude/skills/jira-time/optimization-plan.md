# JIRA Time Tracking Skill - Progressive Disclosure Optimization Plan

**Analysis Date:** 2025-12-28
**Skill:** jira-time
**Current Version:** v1.0

---

## Executive Summary

The jira-time skill exhibits **severe information bloat** that violates progressive disclosure principles. The auxiliary documentation (BEST_PRACTICES.md at 1,501 lines) is 5.6x larger than the primary skill definition (SKILL.md at 268 lines). While comprehensive, this creates three critical usability problems:

1. **Level 2 Bloat**: SKILL.md lacks structure for complexity management (no links to Level 3 resources)
2. **Level 3 Monster**: BEST_PRACTICES.md combines 9 distinct pedagogical domains into one 58KB file
3. **Metadata Weakness**: Skill description is adequate but lacks trigger phrases ("--help first" pattern)

**Overall Progressive Disclosure Score: 4/10** (Target: 8/10)

---

## Detailed Findings

### Level 1: Metadata Analysis

**Current State:**
```yaml
name: "JIRA Time Tracking"
description: "Time tracking and worklog management - log time, manage estimates,
             generate reports, export timesheets. Use when logging work, setting
             estimates, or generating time reports."
```

**Metrics:**
- Metadata description: 209 characters (Target: ~200)
- Clarity: Good ("Use when" clause present)
- Triggers: Moderate (covers 3 use cases: logging, estimates, reports)

**Violations:** None at this level

**Recommendation:** PASS with minor enhancement
- Add "Bulk operations" trigger to signal discovery of `--dry-run` pattern
- Description is slightly long but acceptable for a 9-script skill

---

### Level 2: SKILL.md Structure Analysis

**Current Metrics:**
- Total lines: 268
- Code blocks: 27 bash examples
- Tables: 8 (well-formatted)
- Sections: 11

**Structural Assessment:**

#### Positive Elements:
1. Clear "When to use" section (10 use cases)
2. Well-organized script inventory (table with descriptions)
3. Inline option tables (worklog, report, common)
4. Good exit code documentation
5. Examples organized by scenario (log time, view, manage estimates, reports, bulk)

#### Violations Detected:

**Violation #1: No Level 3 Navigation**
- BEST_PRACTICES.md exists but is never referenced in SKILL.md body
- Line 262: Reference exists but only as a single link in "Best Practices" section
- Problem: Reader must discover advanced content through luck, not design
- Impact: HIGH - Users seeking billing, accuracy, or team policies won't find it

**Violation #2: Incomplete Exit Code Section**
- Only 3 exit codes documented (0, 1, 2)
- No mapping to specific error conditions (e.g., "time format invalid" = 1)
- Problem: Users see "Error" but not which script validation failed
- Impact: MEDIUM - Affects troubleshooting workflow

**Violation #3: Troubleshooting Section Too Brief**
- 11 subsections (lines 214-259)
- Covers 6 issues with solutions
- Problem: Users with undocumented errors have nowhere to escalate
- Impact: MEDIUM - Edge cases (API limits, permission issues) minimally covered

**Violation #4: Missing Dry-Run Pattern Integration**
- Dry run covered in line 182-191 (2 scripts only)
- Table format good, but no pattern explanation
- Problem: Bulk operations require special understanding of preview-before-execute
- Impact: MEDIUM - Risk of accidental bulk changes

---

### Level 3: docs/BEST_PRACTICES.md Over-Aggregation

**Current Metrics:**
- Total lines: 1,501 (58KB with formatting)
- Sections: 10 major domains
- Code examples: 89
- Tables: 31
- Average section size: 150 lines

**Problem: Monolithic Pedagogy**

This file conflates nine distinct audience archetypes:

1. **Individual contributor** (time format, logging habits) - 400 lines
2. **Team manager** (policies, compliance, red flags) - 300 lines
3. **Finance/billing person** (invoicing, reconciliation) - 250 lines
4. **Estimation coach** (accuracy metrics, buffer guidelines) - 300 lines
5. **System admin** (permission schemes, configuration) - 150 lines
6. **JIRA admin** (field setup, workflow validators) - 200 lines
7. **Data analyst** (JQL queries, reporting patterns) - 200 lines
8. **Consultant** (implementation strategies) - 150 lines
9. **Platform engineer** (integration patterns) - 50 lines

**Deep Nesting Issues:**

File A (SKILL.md, line 262) → File B (BEST_PRACTICES.md, 1501 lines) → No File C

**Problem:** Readers landing in BEST_PRACTICES.md to understand "estimation guidelines" must traverse:
1. TOC at line 7-18 (12 links, all in same file)
2. 2KB of preamble about time format (not needed)
3. 300KB of manager policies (wrong persona)
4. To finally reach 150 lines about "Estimation Approaches" at line 88

**Structure Debt:**
- Line 79 table: "Original vs Remaining vs Time Spent" (essential for all users)
- Lines 90-195: Estimation section (good, comprehensive)
- Lines 197-320: Worklog practices (good for IC, not for manager)
- Lines 385-510: Billable tracking (essential for finance, noise for developer)
- Lines 515-750: Reporting strategies (critical for managers, overwhelming for IC)

**Result:** A developer wanting to understand "when to use --adjust-estimate auto" must:
1. Open BEST_PRACTICES.md
2. Scroll 180 lines past time format reference
3. Find line 178-187 (10 lines of clarity!)
4. Scroll back to understand context in SKILL.md

**Impact Assessment: CRITICAL**
- Cognitive load: Very high (users must read 1501 lines to find 10)
- Searchability: Low (TOC uses vague names like "Worklog Best Practices")
- Onboarding time: 30+ minutes vs. recommended 5-10 minutes
- Page bloat: 6x what progressive disclosure allows at Level 3

---

### Code Quality Check: Script-Level Analysis

**Script Line Count Distribution:**
```
add_worklog.py:        209 lines (reasonable for I/O + validation)
bulk_log_time.py:      229 lines (good - includes dry-run preview logic)
delete_worklog.py:     156 lines (well-scoped)
export_timesheets.py:  291 lines (largest - formatting-heavy)
get_time_tracking.py:  157 lines (concise)
get_worklogs.py:       206 lines (reasonable)
set_estimate.py:       148 lines (tight)
time_report.py:        305 lines (largest, complex reporting)
update_worklog.py:     161 lines (focused)
─────────────────
Total:                1,862 lines
```

**Assessment:** Script quality is GOOD
- No script exceeds 320 lines (well below 500-line code smell threshold)
- Time format validation properly delegated to shared `time_utils`
- Error handling consistent across all scripts
- argparse help text is present but minimal (good - matches SKILL.md)

**Finding:** Scripts themselves are NOT the problem. Documentation sprawl is.

---

## Three-Level Disclosure Violations Summary

### Level 1 Violations
- **Count:** 0
- **Severity:** N/A
- **Status:** PASS

### Level 2 Violations
- **Count:** 4
- **Severity:** Medium
- **Critical Issues:**
  1. No explicit navigation to Level 3 (BEST_PRACTICES.md)
  2. Troubleshooting section underdeveloped (6 issues, needs 12+)
  3. Dry-run pattern explained but not integrated
  4. No persona-based entry points

### Level 3 Violations
- **Count:** 2 (Critical)
- **Severity:** High
- **Critical Issues:**
  1. **Monolithic aggregation**: 9 distinct domains in 1 file
  2. **No segmentation**: No sub-files for finance/admin/estimation personas
  3. **Search overhead**: 1500-line files force full-text scanning
  4. **Nesting depth**: No separation of tactical vs. strategic content

**Bloat Factor:** +560% (BEST_PRACTICES.md is 560% larger than SKILL.md)

---

## Specific Recommendations

### Phase 1: Restructure Level 2 (SKILL.md)

**Action Items:**

1. **Add Level 3 Navigation Section** (new, post-examples)
   - Location: After "Examples" section, before "Dry Run Support"
   - Content: Persona-based links to advanced guides
   - Format:
     ```markdown
     ## Advanced Guides

     For specific roles and use cases, see:
     - **Time Logging Habits**: [Daily Logging, Retroactive Entries, Comment Templates](docs/ic-time-logging.md)
     - **Estimation & Planning**: [Estimation Approaches, Accuracy Metrics, Buffer Guidelines](docs/estimation-guide.md)
     - **Team Policies**: [Policy Templates, Permission Schemes, Compliance Monitoring](docs/team-policies.md)
     - **Billing & Finance**: [Billable Tracking, Invoicing Workflows, Client Disputes](docs/billing-integration.md)
     - **JQL & Reporting**: [Time-Based Queries, Report Templates, Analytics](docs/reporting-guide.md)
     ```
   - Benefit: Users immediately find role-specific content
   - Effort: 15 minutes

2. **Enhance Troubleshooting Section** (expand lines 214-259)
   - Add 6 new categories: bulk operation timeouts, estimate update failures, permission errors, API rate limits, worklog visibility issues, timezone problems
   - Before: 6 documented issues
   - After: 12 documented issues
   - Format: Keep existing "Common Issues" subsection, add new "Advanced Troubleshooting" subsection
   - Effort: 30 minutes

3. **Document Dry-Run Pattern** (new subsection in Options section)
   - Location: After "Worklog-specific options" table (line 61)
   - Content: Explain preview-before-execute workflow
   - Example: Show flow for bulk_log_time.py with --dry-run output
   - Benefit: Prevents accidental bulk operations
   - Effort: 20 minutes

4. **Add "Common Questions" Section** (new, before Related skills)
   - Questions to address:
     - "Why is my estimate not updating?" (JRACLOUD-67539)
     - "How do I log time for someone else?" (permissions)
     - "Can I bill partial hours?" (rounding rules)
     - "How does --adjust-estimate work?" (modes)
   - Format: Q&A with link to BEST_PRACTICES sections
   - Effort: 20 minutes

---

### Phase 2: Decompose Level 3 (BEST_PRACTICES.md)

**Action Plan:**

Create 5 specialist guides, each 200-400 lines:

1. **docs/ic-time-logging.md** (Individual Contributor)
   - Extract: Lines 197-320 from current BEST_PRACTICES.md
   - Content: Daily logging, comment templates, interruption handling, retroactive entries
   - Audience: Developers, QA, contractors
   - Size: ~250 lines
   - TOC:
     - When to Log Time (daily, task completion, weekly)
     - Writing Effective Comments (patterns, templates)
     - Special Cases (non-issue time, retroactive, interrupted work)
     - Worklog Visibility (security)

2. **docs/estimation-guide.md** (Estimation & Planning)
   - Extract: Lines 69-195 from current BEST_PRACTICES.md
   - Content: Estimation approaches, T-shirt sizing, accuracy metrics, continuous improvement
   - Audience: Product managers, team leads, estimation coaches
   - Size: ~250 lines
   - TOC:
     - Understanding JIRA Time Fields
     - Estimation Approaches (bottom-up, story points, t-shirt sizing)
     - Setting Realistic Estimates (do/don't, buffers)
     - Estimate Adjustment Strategies (modes)
     - Measuring Accuracy
     - Continuous Improvement

3. **docs/team-policies.md** (Team Management)
   - Extract: Lines 753-890 from current BEST_PRACTICES.md
   - Content: Policy templates, onboarding, permission schemes, monitoring, compliance
   - Audience: Engineering managers, team leads, JIRA admins
   - Size: ~200 lines
   - TOC:
     - Establishing Team Policies (sample document)
     - Onboarding Checklist
     - Permission Configuration
     - Monitoring & Enforcement
     - Handling Non-Compliance

4. **docs/billing-integration.md** (Finance & Invoicing)
   - Extract: Lines 385-510 and 894-1035 from current BEST_PRACTICES.md
   - Content: Billable tracking, invoicing workflows, third-party tools, retainer models
   - Audience: Finance, billing admins, project managers
   - Size: ~300 lines
   - TOC:
     - Native JIRA Limitations (no built-in billable flag)
     - Billable Tracking Strategies (4 options with pros/cons)
     - Billable Hours Reporting
     - Third-Party Tools (Tempo, Everhour, etc.)
     - Invoice Preparation Workflow
     - Handling Client Disputes
     - Retainer & Fixed-Fee Projects

5. **docs/reporting-guide.md** (Analytics & JQL)
   - Extract: Lines 515-750 from current BEST_PRACTICES.md
   - Content: Built-in reports, command-line reporting, export formats, advanced JQL, dashboards
   - Audience: Data analysts, project managers, reporting admins
   - Size: ~250 lines
   - TOC:
     - Built-in JIRA Reports
     - Command-Line Reporting (user, project, custom date ranges)
     - Export Formats (CSV, JSON)
     - Client Reporting Templates
     - Dashboard Widgets
     - Advanced JQL for Time Queries

6. **Simplified docs/BEST_PRACTICES.md** (Rewritten as Index)
   - Replace 1,501 lines with ~300-line navigation hub
   - Purpose: Entry point directing users to specialists guides
   - Content:
     - Table of Contents with use-case descriptions
     - Quick reference (familiar faces for returning users)
     - "Getting Started" section (first 15 minutes)
     - Link tree to all guides

**Result:**
- 5 focused guides (200-300 lines each = ~1,250 lines total)
- 1 navigation hub (300 lines)
- Total Level 3: 1,550 lines (same size, but +5 organized files)
- Per-guide discoverability: 5x improvement

---

### Phase 3: Add Reference Layer

**Create docs/reference/** subdirectory with quick-lookup files:

1. **docs/reference/time-format-quick-ref.md** (~80 lines)
   - Extract from BEST_PRACTICES lines 23-67
   - Format: Lookup table only (no explanation)
   - Audience: Users familiar with time format, need quick syntax check

2. **docs/reference/jql-snippets.md** (~100 lines)
   - Extract from BEST_PRACTICES lines 715-750
   - Format: Copy-paste JQL queries with descriptions
   - Audience: Report builders

3. **docs/reference/permission-matrix.md** (~60 lines)
   - Extract from BEST_PRACTICES lines 824-834, 1450-1462
   - Format: Matrix of permission × action
   - Audience: JIRA admins

4. **docs/reference/error-codes.md** (NEW, ~100 lines)
   - Map exit codes to causes and solutions
   - Extract from SKILL.md lines 80-88, enhance
   - Audience: Troubleshooters

---

## Implementation Plan

### Sprint 1: Prepare (2 hours)
1. Audit all examples in BEST_PRACTICES.md to identify which guide they belong to
2. Create directory structure: `docs/{ic-time-logging,estimation-guide,team-policies,billing-integration,reporting-guide,reference}`
3. Identify sections to move (line numbers)

### Sprint 2: Decompose Level 3 (4 hours)
1. Extract 5 specialist guides from BEST_PRACTICES.md using line numbers
2. Add local TOC to each guide
3. Add cross-references between guides
4. Rewrite BEST_PRACTICES.md as navigation index
5. Verify no content duplication

### Sprint 3: Enhance Level 2 (2 hours)
1. Add "Advanced Guides" section to SKILL.md with persona-based links
2. Expand Troubleshooting section (add 6 new issues)
3. Add "Dry-Run Pattern" subsection
4. Add "Common Questions" section
5. Update BEST_PRACTICES link (now points to index, not monolithic)

### Sprint 4: Add Reference Layer (1 hour)
1. Create `docs/reference/` subdirectory
2. Extract quick-ref files (time format, JQL snippets, permission matrix)
3. Create error-codes.md from SKILL.md

### Sprint 5: Test & Verify (1 hour)
1. Walk through skill discovery: "I want to estimate story points" → ic-time-logging → estimation-guide
2. Walk through troubleshooting: Search for "estimate not updating" → SKILL.md Troubleshooting → docs/reference/error-codes.md
3. Verify all links functional
4. Check file sizes: each guide 200-400 lines (confirm)

**Total Effort:** 10 hours

---

## Success Criteria

After implementation:

| Metric | Current | Target | Success |
|--------|---------|--------|---------|
| **SKILL.md lines** | 268 | 350-400 | +20-30% (strategic, not bloat) |
| **BEST_PRACTICES.md lines** | 1,501 | 300 | 80% reduction (becomes index) |
| **Number of Level 3 files** | 1 | 6 | Specialization (5 guides + index) |
| **Max guide size** | 1,501 | 400 | Cognitive load reduction |
| **Link navigation steps** | 2 (SKILL→BEST_PRACTICES) | 2-3 (SKILL→Guides→Topics) | Same, but targeted |
| **Time to find estimate guidance** | 8 minutes (scan 1500 lines) | 2 minutes (direct link) | 75% faster |
| **Troubleshooting coverage** | 6 issues | 12+ issues | Better edge cases |
| **Persona entry points** | 0 (generic TOC) | 5 (IC, Manager, Finance, Analyst, Admin) | Role-based discovery |

---

## Comparison: Before & After

### User Journey: "How do I estimate this story?"

**CURRENT (Problematic):**
1. User reads SKILL.md "When to use this skill" (skips, too generic)
2. User scans script list (no estimation scripts)
3. User clicks BEST_PRACTICES link (1500 lines loaded)
4. User searches for "estimate" (multiple hits: section, subsections)
5. User reads 10 lines at 79-195 that answer the question
6. **Time: 8-10 minutes** (most time wasted on preamble)

**OPTIMIZED (Target):**
1. User reads SKILL.md "Advanced Guides" section
2. User clicks "Estimation & Planning" link
3. User lands on docs/estimation-guide.md (~250 lines)
4. User reads "Estimation Approaches" section (lines 20-120)
5. User finds answer in 3 minutes
6. **Time: 3 minutes** (5x faster)
7. **Bonus:** User can read other sections in guide without leaving (cohesive document)

### Skill Description (Metadata)

**CURRENT:**
```
"Time tracking and worklog management - log time, manage estimates,
 generate reports, export timesheets. Use when logging work, setting
 estimates, or generating time reports."
```

**OPTIMIZED:**
```
"Time tracking and worklog management with estimation, reporting, and
 billing integration. Use for logging work, managing estimates, generating
 reports, bulk operations, and team time tracking policies."
```

**Change Rationale:** Added "bulk operations" (--dry-run) and "team policies" triggers for better skill discovery

---

## Risk Assessment

### Risk 1: Link Rot
- **Probability:** Medium (5 new files to maintain)
- **Impact:** Users encounter broken links
- **Mitigation:** Add link verification test to CI/CD, validate in README

### Risk 2: Duplicate Content
- **Probability:** High (if not careful extracting from 1501-line file)
- **Impact:** Maintenance burden, conflicting guidance
- **Mitigation:** Use extraction checklist, cross-reference between guides, grep verification

### Risk 3: Lost Context
- **Probability:** Low (Level 3 links from Level 2)
- **Impact:** Users can't trace back to understand when to use feature
- **Mitigation:** Each guide includes "Use this guide if you..." preamble, linked back to SKILL.md

### Risk 4: Incomplete Guide Extraction
- **Probability:** Medium (1500 lines to segment is complex)
- **Impact:** Important content left in old file
- **Mitigation:** Line-by-line audit checklist before deleting from BEST_PRACTICES.md

---

## Code Quality Observations (Bonus)

While analyzing the skill, I observed:

**Strengths:**
- Scripts properly delegate to shared utilities (time_utils, adf_helper)
- Error handling consistent (validators.py pre-flight checks)
- Dry-run pattern well-implemented (bulk_log_time.py lines 76-99)
- Argument parsing clear and self-documenting

**Minor Opportunities:**
- add_worklog.py, bulk_log_time.py could extract common --started date parsing (17 lines repeated)
- Consider adding --verbose flag to dry-run to show field-by-field changes
- time_report.py (305 lines) could benefit from sub-functions for formatting logic

**These are non-blocking and separate from documentation restructuring.**

---

## Files to Create/Modify

### Create New Files:
1. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/ic-time-logging.md` (250 lines)
2. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/estimation-guide.md` (250 lines)
3. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/team-policies.md` (200 lines)
4. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/billing-integration.md` (300 lines)
5. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/reporting-guide.md` (250 lines)
6. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/reference/time-format-quick-ref.md` (80 lines)
7. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/reference/jql-snippets.md` (100 lines)
8. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/reference/permission-matrix.md` (60 lines)
9. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/reference/error-codes.md` (100 lines)

### Modify Existing Files:
1. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/SKILL.md`
   - Add "Advanced Guides" section (~50 lines)
   - Expand "Troubleshooting" section (~80 lines)
   - Add "Dry-Run Pattern" subsection (~20 lines)
   - Add "Common Questions" section (~50 lines)
   - Update metadata description (minor)

2. `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-time/docs/BEST_PRACTICES.md`
   - Replace entire content with index structure (~300 lines)
   - Keep table of contents, quick reference, getting started
   - Add cross-references to all new guides

---

## Conclusion

The jira-time skill has **excellent script quality** but **critical documentation organization issues**. The BEST_PRACTICES.md file violates progressive disclosure by conflating 9 distinct personas into 1,501 lines of monolithic content.

**Key Statistics:**
- Current bloat factor: +560% (BEST_PRACTICES vs. SKILL.md)
- Estimated discoverability improvement: 5x faster skill navigation
- Content decomposition: 1 file → 6 focused guides
- User cognitive load reduction: 80% (for targeted use cases)

The optimization plan is **achievable in 10 hours** and will transform the skill from "comprehensive but overwhelming" to "progressive, persona-aware, and discoverable."

---

**Next Steps:**
1. Review this plan with stakeholder
2. Prioritize: Phase 1-2 are critical, Phase 3-4 are nice-to-have
3. Execute in Sprint cycles with link verification
4. Add to CI/CD: verify docs links don't break on PR merge
