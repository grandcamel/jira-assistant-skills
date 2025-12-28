# jira-jsm Progressive Disclosure Optimization Plan

## Executive Summary

**Overall Assessment**: The jira-jsm skill exhibits moderate progressive disclosure violations that impact scanning efficiency for Claude Code. While well-organized, the documentation violates 3 of 5 key constraints, requiring restructuring to follow the 3-Level Disclosure Model.

**Severity**: MEDIUM (impacts Claude discovery and context loading)
- **Files Analyzed**: 47 scripts + 2 major docs (SKILL.md: 1,203 lines, BEST_PRACTICES.md: 1,745 lines)
- **Key Issues Found**: 4 major violations
- **Estimated Refactoring Effort**: 6-8 hours
- **Priority**: High (applies to largest skill in project)

---

## Violation Analysis

### 1. Over-Extended SKILL.md (Level 2 Bloat)

**Issue**: SKILL.md contains 1,203 lines (target: <500 lines)
- **Violation Type**: Excessive Level 2 content
- **Current Structure**: 100 sections (## headers) crammed into single document
- **Impact**:
  - Increases scanning load by 2.4x
  - Makes skill auto-discovery harder ("when should I use this?")
  - Violates progressive disclosure model

**Breakdown by Section Type**:
```
Quick Start:              100 lines (Lines 223-322)
Usage Examples:           600 lines (Lines 290-545)
ITIL Workflows:           420 lines (Lines 546-699)
Integration with Other Skills: 220 lines (Lines 701-749)
Configuration:            130 lines (Lines 768-855)
Rate Limiting Guide:      180 lines (Lines 857-930)
API Reference:            100 lines (Lines 931-970)
Troubleshooting:          250 lines (Lines 971-1084)
Best Practices:            90 lines (Lines 1086-1151)
Performance Tips:          60 lines (Lines 1116-1150)
Licensing & Compatibility: 60 lines (Lines 1161-1200)
```

**Root Cause**: Everything documented in single file instead of being distributed across nested resources.

---

### 2. Duplicate Documentation (Cross-Level Pollution)

**Issue**: Content exists in both SKILL.md and docs/BEST_PRACTICES.md
- **File 1**: SKILL.md lines 1086-1151 (Best Practices section)
- **File 2**: docs/BEST_PRACTICES.md (dedicated 1,745-line guide)
- **Duplication**: ~120 lines of overlapping content

**Examples of Duplication**:
- SLA Management patterns (lines 1088-1091 in SKILL.md vs full section in BEST_PRACTICES.md)
- Customer Experience guidelines (lines 1093-1097 in SKILL.md)
- Asset Management practices (lines 1104-1107 in SKILL.md)

**Impact**:
- Doubles storage/memory footprint
- Creates maintenance nightmare
- Confuses users about source of truth

---

### 3. Oversized Usage Examples (Level 2 Sections)

**Issue**: 600+ lines of usage examples inline (Lines 290-545)
- **Violation**: Exceeds recommended 300 lines per section
- **Content Density**: 46 separate code blocks (average 11 lines each)
- **Nesting Problem**: Deep organization (Service Desk → Creating → Management → etc.)
- **Inline Code**: Largest block is 37 lines (create_request.py example)

**Example Block (Lines 592-625)**:
```bash
# Service Request Fulfillment example - 34 lines
python create_request.py...
python get_approvals.py...
python approve_request.py...
python add_participant.py...
python create_asset.py...
python link_asset.py...
python transition_request.py...
```

**Impact**:
- Makes scanning for "how do I use this?" slow
- Forces readers to scroll through all examples
- Example-heavy documentation suggests unclear API design

---

### 4. API Reference Inline (Should Be Nested)

**Issue**: JSM API Endpoints Reference (lines 931-970) contains raw API paths
- **Content**: Lists 8 API categories with endpoint paths
- **Location**: Middle of SKILL.md instead of separate reference
- **Usage**: Rarely needed during discovery - only for deep integration

**Example (lines 931-970)**:
```markdown
## JSM API Endpoints Reference

### Service Desk APIs
- `GET /rest/servicedeskapi/servicedesk` - List service desks
- `GET /rest/servicedeskapi/servicedesk/{serviceDeskId}` - Get service desk
[... 40+ more lines]
```

**Impact**:
- Takes up valuable Level 2 space
- Belongs in nested `references/` folder
- Blocks discovery of higher-priority information

---

### 5. Missing "When to Use" Triggers

**Issue**: Section lacks clear decision triggers for Claude
- **Current**: "When to use this skill" (lines 10-23) is generic
- **Missing**: Specific problem triggers (e.g., "When you encounter 'SLA breach' mention", "When user asks about change approvals")
- **Problem**: Claude can't easily pattern-match to this skill

**Current Text** (lines 12-22):
```
Use this skill when you need to:
- Create and manage service desk requests (incidents, service requests, changes)
- Track and monitor SLA compliance and breach detection
- [Generic list...]
```

**Better Approach** (example):
```
Use this skill when:
- User mentions "SLA", "service level", or "breach"
- Working with service desk requests (SD-* issue keys)
- Managing customer-facing support workflows
- Handling approvals/change management
- Searching for JSM-specific features in JIRA
```

---

## 3-Level Disclosure Model Violations

### Level 1 (Metadata) - SKILL.md Frontmatter

Status: **COMPLIANT**
```yaml
name: "JIRA Service Management"
description: "Complete ITSM/ITIL workflow support for JSM - service desks, requests, SLAs, customers, approvals, knowledge base. Use when managing service desk requests, tracking SLAs, or handling customer operations."
```
- Description: 203 characters (target: ~200) ✓
- Clear and concise ✓

---

### Level 2 (Discovery) - SKILL.md Body

Status: **VIOLATION - OVERSIZED**

**Current**: 1,203 lines
**Target**: <500 lines
**Overage**: 603 lines (120%)

**Content Distribution Analysis**:
```
Category                        Lines    Status
────────────────────────────────────────────────
When/What (essential)             25    OK
Scripts Index (lean)              40    OK
Quick Start (essential)           100   OK
Common Options (table)            30    OK
Exit Codes                        30    OK
────────────────────────────────────────────
Usage Examples (bloat)           300   TOO LONG (move to nested)
Common Workflows (bloat)         150   OPTIONAL (move to docs/)
Integration Patterns              50   OK (reference)
Configuration                     130   TOO LONG (move to references/)
Rate Limiting                     180   REFERENCE (move to nested)
Troubleshooting                   250   TOO DETAILED (move to nested)
API Reference                     100   WRONG PLACE (move to references/)
Best Practices                     90   DUPLICATE (consolidate in docs/)
Performance Tips                   60   REFERENCE (move to references/)
────────────────────────────────────────────
Total                          1,203   EXCEEDS LIMIT
```

---

### Level 3+ (Nested Resources) - Current Structure

Status: **PARTIAL - UNDERDEVELOPED**

**Current Nesting**:
```
.claude/skills/jira-jsm/
├── SKILL.md                          (Level 2 - currently overloaded)
├── docs/
│   ├── BEST_PRACTICES.md             (Level 3 - good, but duplicates SKILL.md)
│   └── integration_test_report.md    (Level 3 - test-focused, not user-facing)
├── references/                        (Level 3 - EXISTS BUT EMPTY)
│   └── [should contain API docs]
├── assets/templates/                 (Level 4 - exists but not referenced)
└── scripts/                          (45 scripts - no index/navigation)
```

**Missing Resources** (should be Level 3):
1. `docs/QUICK_START.md` - Dedicated quick start guide
2. `docs/USAGE_EXAMPLES.md` - All usage examples extracted
3. `docs/ITIL_WORKFLOWS.md` - Dedicated ITIL workflow guide
4. `docs/TROUBLESHOOTING.md` - Extracted troubleshooting guide
5. `references/API_REFERENCE.md` - JSM API endpoint reference
6. `references/RATE_LIMITS.md` - Rate limiting strategies
7. `references/INTEGRATION_GUIDE.md` - Integration with other skills

---

## Code Quality Issues

### 1. Script Documentation Consistency

**Status**: GOOD

- 45 scripts, all with consistent structure
- Average size: ~150 lines (appropriate)
- Docstrings present and helpful
- Examples: `create_request.py` (225 lines) has clear usage doc at top

**No changes needed** - script level is well-designed.

---

### 2. Inline Code Block Analysis

**Status**: ACCEPTABLE

- Total code blocks in SKILL.md: 46
- Average size: 11.3 lines
- Largest block: 37 lines (Service Request Fulfillment example)
- Largest bash example: 34 lines (acceptable for workflow)
- **Finding**: Code blocks are appropriately sized; the issue is TOO MANY of them (46) inline rather than too large

**Recommendation**: Keep code blocks as-is, but move entire "Usage Examples" section to nested docs.

---

### 3. Nesting Depth Analysis

**Status**: MODERATE CONCERN

Example traversal path:
1. User reads SKILL.md
2. Sees "Common ITIL Workflows" section
3. Expands "Service Request Fulfillment"
4. Sees multiple code examples
5. Wants more details → referred to docs/BEST_PRACTICES.md (separate file)

This is 1-level nesting, which is acceptable. However, the problem is that:
- Too many different topics in SKILL.md create cognitive load
- Users unsure whether to check BEST_PRACTICES.md or SKILL.md
- No clear navigation between documents

---

## Implementation Plan

### Phase 1: Audit and Planning (1 hour)

**Tasks**:
1. Identify content that belongs in nested docs
2. Audit duplication between SKILL.md and BEST_PRACTICES.md
3. Map script organization by category
4. Plan new document structure

**Deliverable**: This analysis document ✓ (COMPLETE)

---

### Phase 2: Core Restructuring (3-4 hours)

#### 2A. Refactor SKILL.md (target: 450-500 lines)

**Keep in SKILL.md** (Level 2):
```markdown
# jira-jsm

[Frontmatter]

## When to use this skill
- [Enhanced triggers]
- Link to nested docs for details

## What this skill does
- 6 core capability areas (brief descriptions)
- Link to detailed docs for each

## Quick Start
- 5 most common tasks (keep concise, ~80 lines)

## Available Scripts (45 total)
- [Organized by category with links to reference]

## Common Options
- [Common flags table]

## Getting Started
- Service Desk ID discovery methods (keep essential, move details to references/)
- Configuration overview with link to references/

## Next Steps
- Link to docs/QUICK_START.md for hands-on examples
- Link to docs/BEST_PRACTICES.md for workflow patterns
- Link to docs/TROUBLESHOOTING.md for error resolution
- Link to references/API_REFERENCE.md for integration
```

**Target Line Count**: 400-450 (currently 1,203)
**Content to Extract**:
- Usage Examples section (600 lines) → docs/USAGE_EXAMPLES.md
- ITIL Workflows section (150 lines) → docs/ITIL_WORKFLOWS.md
- Detailed Configuration (130 lines) → references/CONFIG_REFERENCE.md
- Rate Limiting guide (180 lines) → references/RATE_LIMITS.md
- API Endpoints (100 lines) → references/API_REFERENCE.md
- Extended Troubleshooting (150 lines) → docs/TROUBLESHOOTING.md

**Detailed Changes**:

1. **Lines 10-23** ("When to use this skill"):
   - Add specific problem triggers
   - Add "Not sure? Check this flowchart: references/DECISION_TREE.md"
   - Keep brief (expand to max 30 lines)

2. **Lines 290-545** (Usage Examples):
   - Reduce from 300 to ~40 lines
   - Keep only 2-3 essential examples
   - Add: "See docs/USAGE_EXAMPLES.md for 40+ additional examples organized by workflow"

3. **Lines 546-699** (Common ITIL Workflows):
   - Reduce from 150 to ~30 lines summary
   - Add: "See docs/ITIL_WORKFLOWS.md for detailed Incident Management, Change Management, Problem Management workflows"

4. **Lines 768-855** (Configuration):
   - Reduce from 130 to ~20 lines
   - Keep only essential env var setup
   - Link: "See references/CONFIG_REFERENCE.md for profiles, multi-instance setup, environment variable reference"

5. **Lines 857-930** (Rate Limiting):
   - Remove from SKILL.md entirely
   - Create: references/RATE_LIMITS.md
   - Reference: "See references/RATE_LIMITS.md if you encounter HTTP 429 errors"

6. **Lines 931-970** (API Endpoints):
   - Remove from SKILL.md entirely
   - Create: references/API_REFERENCE.md
   - Reference: "See references/API_REFERENCE.md for endpoint details (integration developers only)"

7. **Lines 971-1084** (Troubleshooting):
   - Reduce from 150 to ~40 lines (keep most common 3-4 errors)
   - Create: docs/TROUBLESHOOTING.md
   - Reference: "See docs/TROUBLESHOOTING.md for 15+ troubleshooting scenarios"

8. **Lines 1086-1151** (Best Practices):
   - Remove entirely - consolidate in docs/BEST_PRACTICES.md
   - This section duplicates what's in docs/BEST_PRACTICES.md
   - Verify consolidation in Phase 2B

---

#### 2B. Consolidate BEST_PRACTICES.md (deduplication)

**Current**: docs/BEST_PRACTICES.md (1,745 lines)

**Issues**:
- 120 lines overlap with SKILL.md section (lines 1086-1151)
- Some content is repetitive (e.g., "JSM vs JIRA Software" explained 2 ways)

**Action**:
1. Remove lines 1086-1151 from SKILL.md
2. Merge into docs/BEST_PRACTICES.md's existing sections
3. Add clear table of contents to BEST_PRACTICES.md
4. Verify no other duplication exists

**New BEST_PRACTICES.md structure**:
```markdown
# JSM Best Practices Guide

## Table of Contents
1. JSM vs JIRA Software
2. ITIL Process Implementation
3. Service Desk Setup
... [existing content + merged items from SKILL.md]
```

**Result**: Single authoritative source for best practices, referenced from SKILL.md

---

#### 2C. Create New Nested Documentation (3 new files)

**File 1: docs/QUICK_START.md** (150 lines)
- Extract lines 223-322 from SKILL.md
- Expand with more detailed step-by-step instructions
- Include prerequisite checks
- Add troubleshooting for common issues during first run

**File 2: docs/USAGE_EXAMPLES.md** (350 lines)
- Extract lines 290-545 from SKILL.md (all code examples)
- Organize by workflow category
- Add 10-15 new examples for edge cases
- Include expected output for each example

**File 3: docs/ITIL_WORKFLOWS.md** (200 lines)
- Extract lines 546-699 from SKILL.md
- Expand with detailed step-by-step for each workflow
- Add troubleshooting specific to each workflow
- Include timing/SLA considerations

**File 4: docs/TROUBLESHOOTING.md** (120 lines)
- Extract essential errors from lines 971-1084
- Add Q&A format for quick scanning
- Include decision tree for error diagnosis
- Cross-reference with other skills

**File 5: references/API_REFERENCE.md** (80 lines)
- Extract lines 931-970 from SKILL.md
- Organize by endpoint type
- Add request/response examples for each
- Include rate limit notes per endpoint

**File 6: references/RATE_LIMITS.md** (80 lines)
- Extract lines 857-930 from SKILL.md
- Add concrete examples of rate limit errors
- Include backoff calculation examples
- Compare JSM Cloud vs Data Center limits

**File 7: references/CONFIG_REFERENCE.md** (100 lines)
- Extract configuration details from lines 768-855
- Add config schema validation tips
- Include environment variable reference table
- Add examples for multi-instance setup

---

### Phase 3: Navigation and Cross-Linking (1-2 hours)

#### 3A. Update SKILL.md Navigation

Add section at end of SKILL.md:

```markdown
## Detailed Documentation

If you need more information on a specific topic, check these guides:

| Topic | Location | When to Read |
|-------|----------|--------------|
| Getting started hands-on | docs/QUICK_START.md | First time using jira-jsm |
| Usage examples by workflow | docs/USAGE_EXAMPLES.md | Looking for code examples |
| ITIL workflow patterns | docs/ITIL_WORKFLOWS.md | Implementing incident/change/problem workflows |
| Troubleshooting errors | docs/TROUBLESHOOTING.md | Encountering errors or unexpected behavior |
| Best practices guide | docs/BEST_PRACTICES.md | Want to improve service desk operations |
| Rate limiting strategies | references/RATE_LIMITS.md | Encountering HTTP 429 errors |
| API endpoint reference | references/API_REFERENCE.md | Building custom integrations |
| Configuration reference | references/CONFIG_REFERENCE.md | Managing multiple JIRA instances |
```

#### 3B. Create Navigation in Each Nested Doc

Add to top of each new doc:

```markdown
# [Document Title]

**Quick Navigation**:
- Need to get started? → [docs/QUICK_START.md](../QUICK_START.md)
- Looking for examples? → [docs/USAGE_EXAMPLES.md](../USAGE_EXAMPLES.md)
- Have an error? → [docs/TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
- Want best practices? → [docs/BEST_PRACTICES.md](../BEST_PRACTICES.md)
```

#### 3C. Update Each Script's Docstring

Add reference section to script modules:

```python
"""
[Existing docstring]

Related Documentation:
- Getting started: docs/QUICK_START.md
- Usage examples: docs/USAGE_EXAMPLES.md
- Workflows: docs/ITIL_WORKFLOWS.md
- API details: references/API_REFERENCE.md
"""
```

---

### Phase 4: Validation and Testing (1 hour)

**Checklist**:
- [ ] SKILL.md < 500 lines
- [ ] No code blocks > 50 lines in SKILL.md
- [ ] All extracted sections have dedicated nested files
- [ ] Cross-references between files work
- [ ] docs/BEST_PRACTICES.md consolidated (no duplication)
- [ ] All new files have navigation headers
- [ ] "When to use" section has clear triggers for Claude
- [ ] Level 3 resources organized in clear folder structure
- [ ] Run `grep -r "See docs/"` to verify all cross-links
- [ ] Verify no orphaned content

**Validation Script**:
```bash
# Check SKILL.md size
wc -l SKILL.md  # Should be 400-500

# Verify code blocks
python3 -c "
import re
with open('SKILL.md') as f:
    blocks = re.findall(r'\\`\\`\\`.+?\\n(.+?)\\n\\`\\`\\`', f.read(), re.DOTALL)
    sizes = [b.count('\\n') for b in blocks]
    print(f'Code blocks: {len(sizes)}, max size: {max(sizes) if sizes else 0} lines')
"

# Check for orphaned sections
grep "^##" SKILL.md | wc -l  # Should be ~15 (down from 100)

# Verify cross-links
grep -r "See docs/" .
grep -r "See references/" .
```

---

## Detailed Recommendations

### Recommendation 1: Enhance "When to Use" Triggers

**Current** (lines 10-23): Generic list approach
**Problem**: Claude can't pattern-match to business context

**Suggested Enhancement**:

```markdown
## When to use this skill

Use jira-jsm when you encounter:

### Problem Indicators
- Keywords: "SLA", "service level", "breach", "approval", "change request"
- Issue keys like: `SD-123`, `INC-456` (service desk format vs standard `PROJ-123`)
- Workflow needs: customer-facing requests, ITIL processes, service catalogs
- User questions about: incidents, problems, changes, service requests (not bugs/stories)

### Feature Triggers
- Need to track SLA compliance or generate SLA reports
- Managing approval workflows or CAB (Change Advisory Board) decisions
- Working with knowledge base integration for customer self-service
- Linking IT assets to requests or impact analysis
- Multi-tier support structure (agents, managers, customers)

### Integration Scenarios
- You've created a request in jira-jsm and want to update it (use jira-issue for updates)
- Need to transition a request through approval workflow (use jira-jsm for JSM-specific transitions)
- Searching for requests with complex criteria (use jira-search for JQL)

### NOT This Skill
- Creating bugs/stories in Agile → use **jira-issue**
- Sprint planning or backlog management → use **jira-agile**
- Developer workflow integration → use **jira-dev**
- Standard issue lifecycle management → use **jira-lifecycle**

**Still unsure?** Check the [decision tree](references/DECISION_TREE.md)
```

This gives Claude 4 concrete anchor points to pattern-match on.

---

### Recommendation 2: Create Script Index with Categories

**Current**: Lines 162-222 (list format)
**Problem**: Doesn't help users find what they need

**Suggested Enhancement**:

```markdown
## Available Scripts (45 total)

### Quick Navigation by Task

| What You Want to Do | Scripts | Examples |
|---|---|---|
| Create/manage requests | `create_request.py`, `list_requests.py` | Incident, change, service request |
| Handle approvals | `approve_request.py`, `list_pending_approvals.py` | CAB approval, purchase request approval |
| Track SLA | `get_sla.py`, `check_sla_breach.py`, `sla_report.py` | SLA compliance, at-risk detection |
| Manage customers | `create_customer.py`, `list_customers.py`, `add_to_organization.py` | Bulk add, customer organization |
| Work with assets | `create_asset.py`, `link_asset.py`, `find_affected_assets.py` | Laptop allocation, impact analysis |
| Search knowledge base | `search_kb.py`, `suggest_kb.py` | Self-service, AI suggestions |

### Full Script Reference (45 scripts)

[Existing organized list, but with links to example docs]
```

---

### Recommendation 3: Create a Decision Tree

**New file**: `references/DECISION_TREE.md`

```markdown
# JSM vs Other Skills - Decision Tree

Start here: What are you trying to do?

1. **Create/Update/Delete an issue** (standard fields like priority, assignee, status)
   → Use **jira-issue** (works for both standard issues and JSM requests)

2. **Transition an issue through workflow**
   → Standard JIRA workflow → Use **jira-lifecycle**
   → JSM-specific approval/transition → Use **jira-jsm**

3. **Search for issues with JQL**
   → Use **jira-search** (works for both standard and JSM requests)

4. **Customer-facing support** (approvals, SLAs, service catalog)
   → Use **jira-jsm**

5. **IT asset management** (laptops, servers, licenses)
   → If using JSM Assets → **jira-jsm**
   → If using standard custom fields → **jira-issue**

6. **Knowledge base integration**
   → Use **jira-jsm** for suggestions and search
```

---

### Recommendation 4: Reduce "Integration with Other Skills" Section

**Current** (lines 701-749): 50+ lines of copy-pasted examples
**Problem**: Examples are same as in "Usage Examples" section, just reorganized

**Action**:
- Reduce to ~15 lines
- Keep only unique integration patterns not covered elsewhere
- Add table showing which skills work together

```markdown
## Integration with Other Skills

jira-jsm requests (SD-* keys) are standard JIRA issues and work with all skills:

| Skill | Integration | Example |
|-------|----------|---------|
| jira-issue | CRUD operations on any request | Update priority, assignee, labels |
| jira-lifecycle | Workflow transitions | Transition request through approval workflow |
| jira-search | Query and filter requests | Find high-priority incidents, SLA breaches |
| jira-relationships | Link requests together | Link incident to problem, change to problem |
| jira-collaborate | Comments, attachments, notifications | Add rich comments, attach files, notify team |

See docs/USAGE_EXAMPLES.md for detailed integration examples.
```

---

### Recommendation 5: Refactor "Cloud vs Data Center" Section

**Current** (lines 1018-1084): 67 lines comparing APIs
**Problem**: Too detailed for Level 2; belongs in references or integration guide

**Action**:
1. Reduce in SKILL.md to ~10 lines warning
2. Create: `references/DATACENTER_GUIDE.md` (80 lines)

**New SKILL.md version**:
```markdown
## JIRA Cloud vs Data Center

This skill is optimized for **JIRA Cloud**. Data Center support is partial:
- Core API endpoints may differ
- Customer identification (email vs username)
- Assets/Insight integration may vary

See [Data Center Integration Guide](references/DATACENTER_GUIDE.md) if using Data Center.
```

---

## Success Metrics

### Before Optimization
- SKILL.md: 1,203 lines
- Sections: 100 subsections
- Nesting Level: 1 (SKILL.md → docs/)
- Discovery Time: ~5 minutes to find relevant example
- Duplication: 120 lines between SKILL.md and BEST_PRACTICES.md

### After Optimization (Target)
- SKILL.md: 450 lines (-63%)
- Sections: 15 subsections (-85%)
- Nesting Level: 2-3 (SKILL.md → docs/ → specific guides)
- Discovery Time: ~1-2 minutes (clear navigation)
- Duplication: 0 lines (single source of truth)

### Measurement
```bash
# Line count reduction
wc -l SKILL.md  # Target: 400-500 lines

# Section count reduction
grep "^##" SKILL.md | wc -l  # Target: 12-15

# Code block count
python3 -c "import re; print(len(re.findall(r'```', open('SKILL.md').read())) // 2)"  # Target: <20

# Nested documentation coverage
find docs/ references/ -name "*.md" | wc -l  # Target: 7+ new files
```

---

## Risk Assessment

### Low Risk Changes
- Extracting "Usage Examples" section → new docs/USAGE_EXAMPLES.md
- Moving "Rate Limiting" to references/ → no impact on core functionality
- Updating navigation links → straightforward regex replacement

### Medium Risk Changes
- Refactoring "When to Use" triggers → need review for accuracy
- Consolidating BEST_PRACTICES.md → verify no content is lost
- Reducing "Configuration" section → ensure essential info is preserved

### Mitigation
1. Create on feature branch before making changes
2. Validate all cross-references work
3. Test that `python script.py --help` still references correct documentation
4. Review consolidated BEST_PRACTICES.md with domain expert

---

## Implementation Timeline

| Phase | Task | Duration | Owner |
|-------|------|----------|-------|
| 1 | Complete analysis (this doc) | 1 hour | Complete |
| 2A | Refactor SKILL.md, update navigation | 2 hours | - |
| 2B | Consolidate BEST_PRACTICES.md | 1 hour | - |
| 2C | Create 7 new nested docs | 2 hours | - |
| 3 | Add cross-links and nav headers | 1.5 hours | - |
| 4 | Validate, test, measure | 1 hour | - |
| **Total** | - | **8.5 hours** | - |

---

## Appendix A: File Move Map

```
BEFORE:
.claude/skills/jira-jsm/SKILL.md                    (1,203 lines)
├── When to use (22 lines)
├── What this skill does (80 lines)
├── Quick Start (100 lines)
├── Usage Examples (300 lines)
├── ITIL Workflows (150 lines)
├── Configuration (130 lines)
├── Rate Limiting (180 lines)
├── API Reference (100 lines)
├── Troubleshooting (250 lines)
├── Best Practices (90 lines)
└── Performance Tips (60 lines)

AFTER:
.claude/skills/jira-jsm/SKILL.md                    (450 lines)
├── When to use (40 lines) [ENHANCED]
├── What this skill does (80 lines)
├── Quick Start (80 lines) [CONDENSED]
├── Available Scripts (30 lines) [LEAN]
├── Navigation Table (20 lines) [NEW]
└── Links to nested resources (10 lines) [NEW]

.claude/skills/jira-jsm/docs/
├── QUICK_START.md                                  (150 lines) [NEW]
├── USAGE_EXAMPLES.md                               (350 lines) [EXTRACTED]
├── ITIL_WORKFLOWS.md                               (200 lines) [EXTRACTED + EXPANDED]
├── TROUBLESHOOTING.md                              (120 lines) [EXTRACTED]
├── BEST_PRACTICES.md                               (1,745 lines) [CONSOLIDATED, NO DUPLICATION]
└── [Existing docs...]

.claude/skills/jira-jsm/references/
├── API_REFERENCE.md                                (80 lines) [EXTRACTED]
├── RATE_LIMITS.md                                  (80 lines) [EXTRACTED]
├── CONFIG_REFERENCE.md                             (100 lines) [EXTRACTED]
├── DATACENTER_GUIDE.md                             (80 lines) [NEW]
├── DECISION_TREE.md                                (40 lines) [NEW]
└── [Existing references...]
```

---

## Appendix B: Content Extraction Guide

### What to Move from SKILL.md Lines 290-545 → docs/USAGE_EXAMPLES.md

Keep in SKILL.md (brief):
```bash
# Keep: Single canonical example
python create_request.py \
  --service-desk 1 \
  --request-type 10 \
  --summary "Email service down"
```

Move to docs/USAGE_EXAMPLES.md (detailed):
```bash
### Service Desk Operations

#### List all service desks
python list_service_desks.py

#### Create new service desk
python create_service_desk.py --project-key FAC --name "Facilities Services"

#### Get service desk details
python get_service_desk.py --service-desk 1
python get_service_desk.py --project-key ITS  # By project key

[... 40+ more examples]
```

---

## Appendix C: Validation Checklist

- [ ] Verify SKILL.md < 500 lines with `wc -l`
- [ ] Check no code blocks > 50 lines in SKILL.md
- [ ] Verify 7 new nested docs created with content
- [ ] Check all cross-links between files work
- [ ] Review BEST_PRACTICES.md for duplicate content
- [ ] Verify "When to Use" section has concrete triggers
- [ ] Test that all scripts still work (they should - no code changes)
- [ ] Spot check navigation headers in each new doc
- [ ] Ensure API Reference has examples
- [ ] Verify Rate Limits doc has concrete error examples

---

## Conclusion

The jira-jsm skill demonstrates good organization at the script level but violates the 3-Level Progressive Disclosure Model at the documentation level. The proposed restructuring:

1. **Reduces scanning overhead** by cutting SKILL.md to 40% of current size
2. **Eliminates duplication** by consolidating BEST_PRACTICES.md
3. **Improves discoverability** with clear when-to-use triggers and decision trees
4. **Enables nested learning** for users who need depth without burdening beginners
5. **Maintains quality** by distributing content to appropriate nesting levels

Estimated effort: **6-8 hours** for complete restructuring with full validation.

Priority: **HIGH** - This is the largest skill in the project and a model for others.
