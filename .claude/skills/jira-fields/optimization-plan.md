# jira-fields Skill: Progressive Disclosure Optimization Plan

## Executive Summary

The jira-fields skill exhibits **moderate disclosure violations** in the BEST_PRACTICES.md documentation (967 lines). While the SKILL.md (275 lines) is well-structured and follows best practices, the nested best practices guide violates the 3-Level Model by over-explaining concepts and inlining massive reference content.

**Overall Assessment:**
- Level 1 (Metadata): Well-optimized (200 chars, clear description)
- Level 2 (SKILL.md body): Well-structured (275 lines, 1-10KB target met)
- Level 3+ (Nested resources): BLOATED - Single 967-line monolithic document violates progressive disclosure

---

## Critical Findings

### Violation 1: Monolithic Best Practices Document (967 lines)

**Location:** `/SKILL.md` → `docs/BEST_PRACTICES.md` (line 274 reference)

**Issue:** Single 967-line document attempts to cover:
- Field type reference tables (42 lines)
- Design principles and guidelines (75 lines)
- Naming conventions (50 lines)
- Field context management (65 lines)
- Screen configuration (100 lines)
- Agile field configuration (110 lines)
- Validation and constraints (60 lines)
- Performance optimization (160 lines)
- Field governance and cleanup (83 lines)
- Common pitfalls and troubleshooting (100 lines)
- Quick reference card (80 lines)
- External resource links (50 lines)

**Impact:**
- Users looking for quick field type reference must scroll through 967 lines
- Governance team guidance buried among field type specs
- Performance optimization tips scattered across document
- No progressive disclosure from tactical to strategic content

**Severity:** HIGH

---

### Violation 2: Over-Explained Voodoo Constants (Field Type Mappings)

**Location:** `scripts/create_field.py` (lines 26-76)

**Issue:** 51-line FIELD_TYPES dictionary with cryptic Atlassian plugin identifiers documented inline:

```python
FIELD_TYPES = {
    'text': {
        'type': 'com.atlassian.jira.plugin.system.customfieldtypes:textfield',
        'searcher': 'com.atlassian.jira.plugin.system.customfieldtypes:textsearcher'
    },
    # ... repeats 11 more times ...
}
```

**Problems:**
1. Field type IDs (e.g., `com.atlassian.jira.plugin.system.customfieldtypes:textfield`) are cryptic "voodoo constants"
2. No inline documentation explaining WHY these specific type/searcher pairs
3. No reference to where these constants come from
4. Difficult to debug when types fail
5. Impossible to extend without understanding the pattern

**Suggestion:** Extract to external reference with link:
- Create `.claude/skills/jira-fields/assets/field-types-reference.md` with full type mappings
- Inline simple comment: `# See assets/field-types-reference.md for complete type mapping`
- Link from create_field.py to reference doc

**Severity:** MEDIUM

---

### Violation 3: Redundant Field Configuration Content

**Location:** Multiple sections in BEST_PRACTICES.md

**Redundancy Examples:**
1. Lines 47-52: Agile field IDs listed
2. Lines 167-176 (SKILL.md): Same Agile field IDs repeated
3. Lines 366-381 (BEST_PRACTICES.md): Same IDs repeated again with instance type
4. Lines 838-849 (BEST_PRACTICES.md Quick Reference): Fourth repetition

**Impact:** Users unsure which source is authoritative; updates must occur in 4 places.

**Suggestion:** Single source of truth with links from SKILL.md and BEST_PRACTICES.md.

**Severity:** MEDIUM

---

### Violation 4: Deep Nesting (3-Level) in Guidance Path

**Current Structure:**
```
SKILL.md (Metadata)
  └── docs/BEST_PRACTICES.md (Reference guide)
      └── Embedded Atlassian documentation links (external)
      └── Quick Reference Card (summary)
```

**Better Progressive Disclosure:**
```
SKILL.md (Level 1: Metadata)
  ├── scripts/ with --help (Level 2: Tactical)
  ├── docs/QUICK_START.md (Level 2: Getting Started, ~500 chars)
  ├── docs/AGILE_SETUP_GUIDE.md (Level 3: Workflow-based, ~1KB)
  ├── docs/FIELD_TYPES_REFERENCE.md (Level 3: Reference, ~1KB)
  ├── docs/GOVERNANCE_GUIDE.md (Level 3: Strategic, ~1.5KB)
  └── docs/TROUBLESHOOTING.md (Level 3: Support, ~1KB)
```

**Current issue:** Users must read entire 967-line doc to find specific guidance.

**Severity:** HIGH

---

### Violation 5: Missing "Use When" Triggers in SKILL.md

**Location:** SKILL.md lines 10-18

**Issue:** "When to use this skill" section is feature-focused but lacks decision triggers:

Current:
```markdown
Use this skill when you need to:
- List available custom fields in a JIRA instance
- Check Agile field availability for a specific project
- Create custom fields (requires admin permissions)
```

**Missing:** Trigger-based discovery cues like:
- "When fields are missing from issue create screen..."
- "When Agile board shows 'Field not configured' error..."
- "When migrating from team-managed to company-managed projects..."

**Suggestion:** Add problem-based triggers to improve autonomous discovery.

**Severity:** LOW

---

## Detailed Violation Analysis

### Line Count Breakdown

| Component | Lines | Target | Status | Notes |
|-----------|-------|--------|--------|-------|
| SKILL.md | 275 | <500 | ✓ Good | Clear structure, examples included |
| BEST_PRACTICES.md | 967 | N/A | ✗ Bloated | Should be 2-4 focused docs (~500 lines each) |
| Total nested docs | 967 | <1000 | ✗ Exceeds | Single monolithic reference violates disclosure |
| Code with inline docs | 150 | <50 per file | ✓ Good | Scripts are clean, under-commented |

---

## Implementation Plan

### Phase 1: Decompose BEST_PRACTICES.md (Priority: HIGH)

Break 967-line document into 5 focused guides:

#### 1.1 Create `docs/FIELD_TYPES_REFERENCE.md` (~300 lines)
- Move: Lines 23-65 (Field Type Reference section)
- Move: Lines 803-816 (Field Type Cheat Sheet)
- Move: Lines 909-926 (Common JQL examples)
- Add: Description of when to use each type
- Add: Example values and use cases
- Keep link in SKILL.md line 274

**Target Size:** 300 lines

#### 1.2 Create `docs/AGILE_FIELD_GUIDE.md` (~250 lines)
- Move: Lines 335-437 (Agile Field Configuration)
- Move: Lines 838-849 (Common Agile Field IDs)
- Move: SKILL.md lines 167-176 (deduplicate to single source)
- Add: Decision tree for Scrum vs Kanban
- Add: Board configuration visual
- Link from SKILL.md and troubleshooting

**Target Size:** 250 lines

#### 1.3 Create `docs/GOVERNANCE_GUIDE.md` (~280 lines)
- Move: Lines 617-720 (Field Governance and Cleanup)
- Move: Lines 724-761 (Common Pitfalls)
- Add: Field request template
- Add: Audit checklist (keep but link)
- Add: Cleanup decision flowchart

**Target Size:** 280 lines

#### 1.4 Create `docs/QUICK_START.md` (~150 lines)
- Move: Lines 817-836 (Essential Scripts)
- Rewrite with 3 common scenarios:
  1. "I need to add Story Points to my project"
  2. "I need to list all custom fields"
  3. "I need to understand what fields my project has"
- Link to detailed guides for each
- Keep Quick Reference Card from BEST_PRACTICES

**Target Size:** 150 lines

#### 1.5 Refactor `docs/BEST_PRACTICES.md` (~350 lines)
- Keep: Design Principles (lines 68-121)
- Keep: Naming Conventions (lines 123-170)
- Keep: Screen Configuration (lines 240-331)
- Keep: Validation section (lines 464-521)
- Trim: Performance section (point to GOVERNANCE_GUIDE)
- Add: Links to all new documents
- Add: Table of contents with progressive depth labels

**Target Size:** 350 lines (66% reduction)

### Phase 2: Extract Field Type Constants (Priority: MEDIUM)

#### 2.1 Create `assets/field-types-reference.json`

```json
{
  "field_types": {
    "text": {
      "display_name": "Text Field",
      "type": "com.atlassian.jira.plugin.system.customfieldtypes:textfield",
      "searcher": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher",
      "description": "Single-line text input (max 255 chars)",
      "use_cases": ["Product name", "Ticket number", "Customer ID"],
      "examples": ["API-123", "Feature request"],
      "validation_options": ["max_length", "regex_pattern"]
    },
    ...
  }
}
```

#### 2.2 Update `scripts/create_field.py`

Replace hardcoded FIELD_TYPES with:
```python
import json
from pathlib import Path

# Load field types from reference
ref_file = Path(__file__).parent.parent / 'assets' / 'field-types-reference.json'
with open(ref_file) as f:
    FIELD_TYPES_REF = json.load(f)
    FIELD_TYPES = {k: v for k, v in FIELD_TYPES_REF['field_types'].items()}

# Document the reference:
# Field type mappings sourced from assets/field-types-reference.json
# See that file for complete documentation and examples
```

Add comment to script:
```python
# Field type plugin IDs are Atlassian internal identifiers.
# See assets/field-types-reference.json for full reference with descriptions.
```

### Phase 3: Eliminate Redundant Content (Priority: MEDIUM)

#### 3.1 Single Source of Truth for Agile Field IDs

Create `assets/agile-field-ids.md`:
```markdown
# Agile Field IDs Reference

These IDs vary by JIRA instance. Always verify with:
```bash
python list_fields.py --agile
```

## Typical Cloud Field IDs
- Sprint: customfield_10020
- Story Points: customfield_10016
- Epic Link: customfield_10014
...
```

#### 3.2 Update SKILL.md (lines 167-176)

Replace with:
```markdown
## Common Agile Field IDs

See [assets/agile-field-ids.md](../assets/agile-field-ids.md) for the most up-to-date list.

Always run `python list_fields.py --agile` to verify IDs for your instance.
```

#### 3.3 Update BEST_PRACTICES.md

Lines 366-381: Replace with link
```markdown
See [Agile Field IDs Reference](../assets/agile-field-ids.md) for current field ID mappings.
```

Lines 838-849: Point to QUICK_START.md instead

### Phase 4: Improve SKILL.md Triggers (Priority: LOW)

#### 4.1 Expand "When to use this skill" section

Add problem-based triggers:
```markdown
## When to use this skill

**Use when you need to:**
- List available custom fields in a JIRA instance
- Check Agile field availability for a specific project
- Create custom fields (requires admin permissions)
- Configure projects for Agile workflows

**Use when troubleshooting:**
- "Field not found" or "field not available" errors
- Agile board shows "Story Points field not configured"
- Missing fields on issue create screen
- Setting up Scrum in a company-managed project
- Understanding why team-managed projects behave differently

**Use when planning:**
- Migrating from team-managed to company-managed projects
- Setting up a new Scrum/Kanban board
- Discovering instance field configuration
```

---

## Metrics & Impact

### Before Optimization

| Metric | Value | Issue |
|--------|-------|-------|
| Single nested doc size | 967 lines | Violates progressive disclosure |
| Redundancy | 4 copies of field IDs | High maintenance burden |
| Voodoo constants | 51 lines unexplained | Difficult to debug/extend |
| Navigation depth | 3 levels | Users skip intermediate docs |
| File count | 2 docs | Low discoverability |

### After Optimization

| Metric | Target | Benefit |
|--------|--------|---------|
| Max doc size | 350 lines | 64% reduction in BEST_PRACTICES |
| Docs | 6 focused guides | Each under 300 lines |
| Navigation depth | 2 levels | Direct access to guides |
| Redundancy | 1 source of truth | Easier maintenance |
| Discovery | Problem-based triggers | Better autonomous agent usage |
| Constants | Externalized + documented | Self-documenting reference |

**Estimated reading time reduction:**
- Before: 20 minutes to find specific guidance in 967-line doc
- After: 3 minutes with 4-document navigation + quick reference

---

## Implementation Sequence

### Week 1: Foundation
1. Create `docs/QUICK_START.md` (scenario-based, unblocks users immediately)
2. Create `assets/agile-field-ids.md` (eliminate redundancy)
3. Create `assets/field-types-reference.json` (extract constants)

### Week 2: Extraction
4. Create `docs/FIELD_TYPES_REFERENCE.md` (reference consolidation)
5. Create `docs/AGILE_FIELD_GUIDE.md` (Agile-specific guidance)
6. Update `scripts/create_field.py` to load from JSON

### Week 3: Consolidation
7. Create `docs/GOVERNANCE_GUIDE.md` (strategic guidance)
8. Refactor `docs/BEST_PRACTICES.md` (consolidate + link)
9. Update SKILL.md with improved triggers and links

### Week 4: Validation
10. Add cross-document link validation
11. Update documentation index
12. Verify no broken references
13. Test script constant loading

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Broken links after decomposition | Medium | High | Implement link validation in tests |
| Maintenance burden increases | Low | Medium | Clear ownership of each document |
| Users miss guidance | Low | Medium | Add comprehensive index in SKILL.md |
| Field type constants fail to load | Low | High | Add fallback to hardcoded dict + logging |

---

## Success Criteria

1. **All nested docs < 350 lines** (except reference tables)
2. **Single source of truth for field IDs** (no redundancy)
3. **Field type constants externalized** (90% reduction in create_field.py comments)
4. **Problem-based triggers in SKILL.md** (added 5+ use-when scenarios)
5. **Navigation depth max 2 levels** (users reach specific guidance in < 3 clicks)
6. **All cross-document links functional** (tested in CI)
7. **Reading time for common scenarios < 5 minutes**

---

## File Structure After Optimization

```
.claude/skills/jira-fields/
├── SKILL.md (275 lines, optimized)
├── scripts/
│   ├── list_fields.py (clean)
│   ├── check_project_fields.py (clean)
│   ├── configure_agile_fields.py (clean)
│   └── create_field.py (loads from JSON)
├── assets/
│   ├── agile-field-ids.md (single source of truth)
│   └── field-types-reference.json (constants extracted)
├── docs/
│   ├── QUICK_START.md (~150 lines, NEW)
│   ├── FIELD_TYPES_REFERENCE.md (~300 lines, NEW)
│   ├── AGILE_FIELD_GUIDE.md (~250 lines, NEW)
│   ├── GOVERNANCE_GUIDE.md (~280 lines, NEW)
│   └── BEST_PRACTICES.md (~350 lines, refactored)
└── tests/
    └── (unchanged)
```

---

## Recommendation

**Implement Phases 1-3 immediately** (3 weeks of effort):
- High impact (64% size reduction in primary doc)
- Low risk (links validation catches errors early)
- Improves maintainability and discoverability significantly

**Phase 4** can be deferred but recommended for autonomous agent discovery.

---

## Notes for Implementation

1. **Preserve commit history:** Each decomposition is a separate commit for rollback safety
2. **Update references last:** After all docs created, bulk update links
3. **Add file headers:** Each new doc should reference parent and related docs
4. **Link validation:** Add test that checks all cross-document links resolve
5. **Staging:** Merge as single PR after validation to maintain coherent history

---

*Analysis completed: 2025-12-28*
*Model: Claude Haiku 4.5*
*Review framework: 3-Level Progressive Disclosure Model*
