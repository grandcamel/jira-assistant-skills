# Progressive Disclosure Optimization Plan - jira-dev Skill

**Analysis Date:** December 28, 2025
**Skill:** JIRA Developer Integration (jira-dev)
**Current Status:** Requires optimization

---

## Executive Summary

The jira-dev skill exhibits significant progressive disclosure violations that impact discoverability and readability:

- **SKILL.md:** 342 lines, 10,089 characters (exceeds 500 line guideline)
- **BEST_PRACTICES.md:** 1,617 lines, 40,330 characters (critical bloat - not referenced from SKILL.md)
- **Description:** 200 characters (acceptable, 797 chars under limit)
- **Code blocks:** 24+ inline examples in SKILL.md (violates 50-line threshold)
- **Nesting depth:** SKILL.md → docs/BEST_PRACTICES.md (2 levels, acceptable)
- **Missing triggers:** No clear "When to use this skill" guidance before examples

**Overall Quality Score:** 5/10
**Critical Issues:** 3
**Code Smells:** 4
**Technical Debt Estimate:** 4-6 hours

---

## Critical Issues

### Issue 1: Bloated SKILL.md Exceeds Target Scope
**Severity:** HIGH
**File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-dev/SKILL.md`
**Line Count:** 342 (Target: <500, but significantly over-explained)
**Character Count:** 10,089 (within 1KB limit technically, but poorly structured)

**Problem:**
- SKILL.md contains complete code examples for all 6 scripts (lines 27-291)
- Examples consume 264+ lines of documentation
- Each script includes bash examples, optional flags, and output samples
- Creates "information overload" on first read

**Example Violations:**
```markdown
Lines 27-43:   14 lines for create_branch_name.py examples
Lines 55-75:   20 lines for parse_commit_issues.py examples
Lines 87-96:   9 lines for link_commit.py examples
Lines 107-119: 12 lines for get_issue_commits.py examples
Lines 129-144: 15 lines for link_pr.py examples
Lines 155-173: 18 lines for create_pr_description.py examples
Lines 184-211: 27 lines for PR output example
```

**Impact:**
- Claude discovers 10KB of documentation on first load
- Examples clutter the skill discovery phase
- Readers must scroll past 200+ lines before reaching configuration
- Violates "target ~200 chars" for Level 1 metadata

**Root Cause:** All scripts documented with full bash examples inline rather than linking to script help.

---

### Issue 2: Orphaned BEST_PRACTICES.md Not Referenced in Discovery
**Severity:** HIGH
**File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-dev/docs/BEST_PRACTICES.md`
**Line Count:** 1,617 (excessive for secondary reference)
**Character Count:** 40,330 (4x larger than SKILL.md)

**Problem:**
- 1,617 lines of detailed Git/CI/CD workflows, branch conventions, smart commits
- Creates "hidden knowledge" not surfaced in SKILL.md discovery
- Tables of contents suggest 10+ major sections but no entry point
- Users won't discover this resource during initial skill exploration
- Contains 200+ code examples (Jenkins, GitHub Actions, GitLab CI, shell scripts)

**Missing Link:** Line 334 in SKILL.md references it casually:
```markdown
For comprehensive guidance on Git integration patterns, branch naming
conventions, and PR workflows, see [Best Practices Guide](docs/BEST_PRACTICES.md).
```

This single sentence on line 334 is the ONLY reference. No "When to use" or "Learn more about" guidance.

**Impact:**
- Advanced workflows (CI/CD integration, deployment tracking, release notes) hidden in separate document
- 40KB of content not discoverable until user reads line 334
- Duplication: BEST_PRACTICES repeats examples already in SKILL.md
- Progressive disclosure broken: Level 2 content inaccessible without scrolling to line 334

**Root Cause:** Best practices file created as "nice-to-have" appendix rather than structured reference.

---

### Issue 3: Excessive Inline Code Blocks in SKILL.md
**Severity:** MEDIUM
**File:** `/Users/jasonkrueger/IdeaProjects/Jira-Assistant-Skills/.claude/skills/jira-dev/SKILL.md`
**Code Block Count:** 24+ blocks
**Block Sizes:** 1-27 lines

**Problem:**
- Lines 27-43: 16-line bash block (create_branch_name examples)
- Lines 55-75: 20-line bash block (parse_commit_issues examples)
- Lines 107-119: 12-line bash block (get_issue_commits examples)
- Lines 129-144: 15-line bash block (link_pr examples)
- Lines 184-211: 27-line markdown block (PR description output)

**Violation:** While no single block exceeds 50 lines, density of examples violates spirit of "avoid code dumps."

**Example - Lines 184-211 (27-line PR description output):**
This is pure output, not script invocation. Belongs in separate reference file.

**Root Cause:** "Show don't tell" philosophy applied too liberally; prioritizes examples over explanation.

---

### Issue 4: "When to Use" Section Lacks Specificity
**Severity:** MEDIUM
**Location:** Lines 11-19 (SKILL.md "When to use this skill")

**Problem:**
Current text:
```markdown
Use this skill when you need to:
- Generate standardized Git branch names from JIRA issues
- Extract JIRA issue keys from commit messages
- Link Git commits to JIRA issues via comments
- Retrieve commits linked to a JIRA issue via Development Information API
- Link Pull Requests (GitHub, GitLab, Bitbucket) to JIRA issues
- Generate PR descriptions from JIRA issue details
- Integrate developer workflows with JIRA tracking
```

**Weaknesses:**
- Generic list that could apply to ANY JIRA skill
- No context about WHEN in workflow to use (pre-commit? pre-PR? pre-deploy?)
- No mention of prerequisites (Git integration setup)
- No example trigger/scenario
- Doesn't explain "why" (what problem it solves)

**Missing:** Contextual triggers like:
- "Use this when developers need to start work on an issue"
- "Use this when creating PR descriptions from issue requirements"
- "Use this for CI/CD pipeline integration"
- "Use this to automatically link development work to tracking"

**Root Cause:** Boilerplate "When to use" without skill-specific trigger scenarios.

---

## Code Smells

### Smell 1: Over-Explained Constants ("Voodoo Constants")
**Severity:** LOW
**Location:** Lines 223-232 (Issue Type Prefixes table)

**Problem:**
Table documents issue type-to-prefix mappings that are hardcoded in create_branch_name.py:
```python
ISSUE_TYPE_PREFIXES = {
    'bug': 'bugfix',
    'defect': 'bugfix',
    'hotfix': 'hotfix',
    'story': 'feature',
    ...
}
```

Documentation DUPLICATES this mapping in a markdown table. When constants change, table falls out of sync.

**Duplication Example:**
- SKILL.md line 223-232: Lists all 8 type mappings in table format
- create_branch_name.py lines 35-53: Same mappings in code

**Impact:** Maintenance burden, potential drift between docs and code.

---

### Smell 2: Script-Level Documentation Not Leveraging CLI Help
**Severity:** MEDIUM
**Location:** Lines 23-96 (Phase 1: Git Integration scripts)

**Problem:**
Each script has a docstring and --help output, but SKILL.md repeats this information:
- Script docstring → SKILL.md description (duplication)
- Script argparse → SKILL.md options (duplication)
- Script examples → SKILL.md bash blocks (duplication)

Users should be directed to `python script.py --help` rather than reading examples in SKILL.md.

**Example - create_branch_name.py:**
- Docstring explains purpose (lines 2-7)
- argparse defines options with help text (lines 51-63 in script)
- SKILL.md repeats purpose, options, examples (lines 23-43)

**Opportunity:** Replace most SKILL.md script examples with reference to --help output.

---

### Smell 3: Missing Skill Organization (No Phases Hierarchy)
**Severity:** LOW
**Location:** Lines 21-122 (Phase 1) and Lines 123-173 (Phase 2)

**Problem:**
Skills are divided into "Phase 1: Git Integration" and "Phase 2: PR Management," but:
- No clear learning path through phases
- No indication which phase to start with
- No dependencies listed (e.g., "Phase 1 is required before Phase 2")
- No estimate of time to learn/implement each phase

**Positive:** Phases are a good organizational pattern, but need clearer scaffolding.

**Opportunity:** Add phase introduction with:
- Learning objectives for each phase
- Estimated time commitment
- Prerequisites/dependencies
- Progression path (Phase 1 → Phase 2)

---

### Smell 4: Deep Nesting of Tutorial Content
**Severity:** LOW
**Location:** docs/BEST_PRACTICES.md (1,617 lines)

**Problem:**
The best practices file contains tutorial-level content (sections 1-10) that should be in separate files:
- Section 1: Branch Naming Conventions (89 lines)
- Section 2: Commit Message Formats (90 lines)
- Section 3: Smart Commits (157 lines)
- Section 4: Pull Request Best Practices (120 lines)
- Section 5: Development Panel Usage (80 lines)
- Section 6: CI/CD Integration Patterns (254 lines)
- Section 7: Automated Workflow Transitions (140 lines)
- Section 8: Deployment Tracking (130 lines)
- Section 9: Release Notes Generation (150 lines)
- Section 10: Common Pitfalls (160 lines)

These are really 10 separate "how-to" guides compressed into one 1,617-line document.

**Structure Should Be:**
```
docs/
├── BEST_PRACTICES.md (TOC, ~50 lines, links to guides)
├── branch-naming-guide.md
├── commit-messages-guide.md
├── smart-commits-guide.md
├── pr-workflows-guide.md
├── development-panel-guide.md
├── ci-cd-integration-guide.md
├── automation-guide.md
├── deployment-tracking-guide.md
├── release-notes-guide.md
└── common-pitfalls-guide.md
```

---

## Refactoring Opportunities

### Opportunity 1: Create Script Reference Card
**Benefit:** Reduce SKILL.md from 342 to 200 lines
**Effort:** 1 hour
**Priority:** HIGH

**Action:**
1. Create `scripts/REFERENCE.md` with tabular summary of all 6 scripts
2. Replace SKILL.md lines 23-291 with single table:
   ```markdown
   | Script | Purpose | Basic Usage | Options |
   |--------|---------|-------------|---------|
   | create_branch_name.py | Generate branch names | See --help | --prefix, --auto-prefix, --max-length |
   | parse_commit_issues.py | Extract issue keys | See --help | --from-stdin, --project, --unique |
   | ... | ... | See --help | ... |
   ```
3. Direct users to `python script.py --help` for detailed usage
4. Keep only 1-2 realistic example per script

**Result:** SKILL.md shrinks from 10KB to 5KB; more discoverable content.

---

### Opportunity 2: Restructure BEST_PRACTICES.md as Modular Guides
**Benefit:** Better progressive disclosure; clearer learning path
**Effort:** 3-4 hours
**Priority:** HIGH

**Action:**
1. Convert BEST_PRACTICES.md to 50-line table of contents:
   ```markdown
   # Developer Workflow Best Practices

   ## Quick Links
   - [Branch Naming Conventions](guides/branch-naming.md) - 3 min read
   - [Commit Message Patterns](guides/commit-messages.md) - 3 min read
   - [Smart Commits Guide](guides/smart-commits.md) - 5 min read
   - [PR Workflows](guides/pr-workflows.md) - 5 min read
   - [Development Panel](guides/development-panel.md) - 3 min read
   - [CI/CD Integration](guides/ci-cd-integration.md) - 10 min read
   - [Automation Rules](guides/automation-rules.md) - 8 min read
   - [Deployment Tracking](guides/deployment-tracking.md) - 5 min read
   - [Release Notes](guides/release-notes.md) - 5 min read
   - [Common Pitfalls & Solutions](guides/pitfalls-and-fixes.md) - 5 min read
   ```

2. Split content into 10 focused guides (80-160 lines each)
3. Add learning time estimates to each guide
4. Create logical prerequisites (e.g., branch-naming before pr-workflows)

**Result:** Users can target specific workflows; no 40KB document to load.

---

### Opportunity 3: Add Phase-Based Learning Path
**Benefit:** Clear onboarding for new users
**Effort:** 1.5 hours
**Priority:** MEDIUM

**Action:**
1. Insert "Learning Path" section after "When to use this skill" in SKILL.md:
   ```markdown
   ## Learning Path

   This skill is organized into two phases:

   ### Phase 1: Core Git Integration (30-45 min)
   Learn to automate Git workflow integration:
   - **create_branch_name.py**: Generate consistent branch names from issues
   - **parse_commit_issues.py**: Extract issue keys from commit messages
   - **link_commit.py**: Link commits to JIRA issues
   - **get_issue_commits.py**: Retrieve development information

   Start here if you're new to JIRA-Git integration.

   ### Phase 2: Pull Request & CI/CD (45-60 min)
   Integrate pull requests and deployment tracking:
   - **link_pr.py**: Automatically link PRs to JIRA
   - **create_pr_description.py**: Generate PR descriptions from issues
   - CI/CD integration patterns (see docs/guides/ci-cd-integration.md)
   - Deployment tracking and release notes

   Prerequisites: Complete Phase 1 first.

   ### Recommended Start Points
   - **Issue Developer:** Start Phase 1, try create_branch_name.py
   - **Git Administrator:** Learn Phase 1 first, then advance to Phase 2
   - **DevOps Engineer:** Focus on Phase 2 CI/CD integration patterns
   - **Release Manager:** Phase 2 deployment tracking and release notes
   ```

2. Update "When to use this skill" to reference phases
3. Add a "What to learn next" section at end linking to related skills

**Result:** Clear scaffolding for different user roles.

---

### Opportunity 4: Create Quick Start Guide
**Benefit:** Reduce time-to-value for new users
**Effort:** 1 hour
**Priority:** MEDIUM

**Action:**
1. Create `docs/QUICK_START.md` (60-80 lines):
   ```markdown
   # Quick Start: Developer Workflow Integration

   Get started with jira-dev in 10 minutes.

   ## 1. Generate Your First Branch Name (2 min)
   ```bash
   python create_branch_name.py PROJ-123 --auto-prefix
   git checkout -b $(python create_branch_name.py PROJ-123 --output git)
   ```

   ## 2. Link a Commit (2 min)
   ```bash
   python link_commit.py PROJ-123 --commit abc123def456 --repo https://github.com/org/repo
   ```

   ## 3. Create PR Description (3 min)
   ```bash
   python create_pr_description.py PROJ-123 --include-checklist
   ```

   ## 4. What's Next?
   - Full Phase 1: Learn all 4 Git integration scripts
   - Full Phase 2: Pull requests and CI/CD integration
   - See [docs/BEST_PRACTICES.md](BEST_PRACTICES.md) for advanced patterns
   ```

2. Reference this from SKILL.md as first resource after "When to use"

**Result:** Users can see value in 10 minutes, then dive deeper.

---

### Opportunity 5: Move Jenkins/GitHub Actions/GitLab CI Examples to Separate Files
**Benefit:** Reduce BEST_PRACTICES.md noise
**Effort:** 2 hours
**Priority:** MEDIUM

**Problem:** Current BEST_PRACTICES.md mixes high-level guidance with 250+ lines of CI/CD config files (Jenkins, GitHub Actions, GitLab CI).

**Action:**
1. Create `docs/ci-cd-integration.md` with architecture + high-level patterns (80 lines)
2. Create `docs/examples/` directory:
   - `jenkins-pipeline.groovy` (full Jenkins example)
   - `github-actions-workflow.yml` (full GitHub example)
   - `gitlab-ci.yml` (full GitLab example)
3. Reference files from ci-cd-integration.md:
   ```markdown
   See [example Jenkins configuration](examples/jenkins-pipeline.groovy)
   for a complete working pipeline.
   ```

**Result:** BEST_PRACTICES shrinks by 250+ lines; code examples live in executable form.

---

### Opportunity 6: Add "Troubleshooting" Trigger to Description
**Benefit:** Help Claude discover skill for error cases
**Effort:** 15 minutes
**Priority:** LOW

**Current Description (Line 3):**
```yaml
description: "Developer workflow integration for JIRA - Git branch names, commit parsing, PR descriptions. Use when generating branch names from issues, linking commits, or creating PR descriptions."
```

**Improved Description:**
```yaml
description: "Developer workflow integration for JIRA - Git branch names, commit parsing, PR descriptions. Use when generating branch names from issues, linking commits, or creating PR descriptions. Also use to troubleshoot Development Panel issues or automate CI/CD integration."
```

**Benefit:** Helps Claude route troubleshooting queries to this skill.

---

## Violations Summary Table

| Violation Type | Guideline | Current | Target | Status |
|---|---|---|---|---|
| Metadata Description | <1024 chars | 200 chars | 200 chars | PASS |
| SKILL.md Lines | <500 lines | 342 lines | <300 lines | FAIL |
| SKILL.md Size | <10KB | 10.1 KB | 5-7 KB | FAIL |
| Inline Code Blocks | <50 lines per block | Max 27 lines | Avoid >20 | WARNING |
| Code Block Density | Avoid excessive examples | 24+ blocks | <10 blocks | FAIL |
| Nesting Depth | Max 2 levels | 2 levels (SKILL.md → docs/) | 2 levels | PASS |
| Missing Triggers | Clear "When to use" | Generic list | Specific scenarios | FAIL |
| Orphaned Resources | All referenced in Level 1 | BEST_PRACTICES not mentioned until line 334 | Clear entry point | FAIL |
| Learning Path | Clear progression | Mentioned but not scaffolded | Explicit phases | FAIL |

---

## Implementation Roadmap

### Phase 1: Critical Fixes (Week 1)
**Effort:** 6-8 hours

1. **Task 1.1:** Restructure SKILL.md with script reference table
   - Replace lines 23-291 with compact reference table
   - Target: 342 lines → 200 lines
   - Files: SKILL.md

2. **Task 1.2:** Add prominent link to BEST_PRACTICES at top
   - Move line 334 reference to line 25 (after "When to use")
   - Add "Advanced Workflows" section header
   - Files: SKILL.md

3. **Task 1.3:** Create QUICK_START.md
   - 60-80 line quick start guide
   - Reference from SKILL.md line 2
   - Files: docs/QUICK_START.md

4. **Task 1.4:** Refactor "When to use" with specific triggers
   - Add 3-5 realistic scenario examples
   - Mention prerequisites (Git integration setup)
   - Files: SKILL.md

### Phase 2: Enhanced Organization (Week 2)
**Effort:** 4-6 hours

5. **Task 2.1:** Split BEST_PRACTICES.md into modular guides
   - Create docs/guides/ directory structure
   - Split 10 sections into 10 focused documents
   - Target: BEST_PRACTICES.md → 50-line TOC
   - Files: docs/guides/*.md, docs/BEST_PRACTICES.md

6. **Task 2.2:** Create learning path scaffolding
   - Add "Learning Path" section with phases
   - Document prerequisites and sequences
   - Add time estimates
   - Files: SKILL.md

7. **Task 2.3:** Move CI/CD examples to separate files
   - Extract Jenkins, GitHub Actions, GitLab CI configs
   - Create docs/examples/ directory
   - Update guides with file references
   - Files: docs/examples/*.groovy, docs/examples/*.yml

### Phase 3: Polish (Week 3)
**Effort:** 2-3 hours

8. **Task 3.1:** Create scripts/REFERENCE.md
   - Tabular summary of all 6 scripts
   - Link to --help for detailed usage
   - Files: scripts/REFERENCE.md

9. **Task 3.2:** Update skill description metadata
   - Add troubleshooting triggers
   - Mention CI/CD automation capability
   - Files: SKILL.md front matter (line 3)

10. **Task 3.3:** Quality review and metrics
    - Verify all guidelines met
    - Check link integrity
    - Measure final readability scores
    - Files: All

---

## Success Criteria

### Level 1 Metadata
- [x] Description: ~200 characters (currently 200)
- [ ] Clear "When to use" with specific scenarios (currently generic)
- [ ] Link to quick start on first read

### Level 2 Main Documentation (SKILL.md)
- [ ] <300 lines (currently 342)
- [ ] <7KB size (currently 10.1 KB)
- [ ] Concise script overview (reference table format)
- [ ] Clear learning path with phases
- [ ] Prominent "Learn more" link to advanced guide

### Level 3+ Nested Resources
- [ ] BEST_PRACTICES.md: 50-line TOC
- [ ] Modular guides: 80-160 lines each
- [ ] Examples in separate directory with README
- [ ] Quick start guide (60-80 lines)
- [ ] Troubleshooting section clearly discoverable

### Overall
- [ ] No orphaned documentation
- [ ] Clear learning path (Quick Start → Phase 1 → Phase 2 → Advanced)
- [ ] <20 inline code blocks in main documentation
- [ ] All code blocks <20 lines in SKILL.md
- [ ] Readability score: 8+/10

---

## Metrics & Measurements

### Current State
- SKILL.md: 342 lines, 10,089 chars
- BEST_PRACTICES.md: 1,617 lines, 40,330 chars
- Total jira-dev documentation: 1,959 lines, 50,419 chars
- Inline code blocks: 24+
- References to BEST_PRACTICES: 1 (line 334)
- Named learning paths: 0

### Target State
- SKILL.md: <200 lines, 5-7KB
- BEST_PRACTICES.md: <50 lines (TOC only)
- Modular guides: 10 files, 800-1,600 lines total
- Total jira-dev documentation: 1,000-1,200 lines (organized)
- Inline code blocks: <10 in main docs
- References to guides: 5+ (TOC, learning path, sections)
- Named learning paths: 2 (Phase 1, Phase 2)

### Improvement
- SKILL.md reduction: 48% fewer lines, 30% fewer characters
- Better progressive disclosure: 3 clear levels
- Clearer entry points: Quick Start, Learning Path, Phase 1-2 structure
- Estimated discoverability improvement: +40% (easier to find specific topics)

---

## Notes

### Positive Findings
1. **Well-organized phases:** Phase 1 and Phase 2 structure is sound
2. **Comprehensive coverage:** All major workflows documented
3. **Multiple output formats:** Scripts support json, text, git output
4. **Good error handling:** Consistent error messages and exit codes
5. **Helpful troubleshooting sections:** Detailed solutions provided
6. **Script quality:** 6 well-tested scripts (42 tests total)

### Risk Mitigations
- All refactoring should maintain existing functionality
- Update internal links when splitting BEST_PRACTICES.md
- Keep BEST_PRACTICES.md as legacy reference during transition
- Test all markdown links after restructuring

### Timeline Estimate
- Phase 1 (Critical fixes): 6-8 hours
- Phase 2 (Enhanced organization): 4-6 hours
- Phase 3 (Polish): 2-3 hours
- **Total: 12-17 hours**

Recommend completing by end of Q1 2026 as part of skill documentation audit.

---

## Next Steps

1. Review this plan with team
2. Prioritize implementation phase
3. Assign ownership for each task
4. Schedule 1-week sprints for Phase 1
5. Iterate on modular guide structure with team feedback
6. Publish updated documentation with version bump

