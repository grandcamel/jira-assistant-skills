# JIRA Operations Skill - Progressive Disclosure Optimization Plan

## Executive Summary

**Analysis Date:** December 28, 2025
**Skill:** jira-ops (Cache management and operational utilities)

**Overall Assessment:** The jira-ops skill violates the 3-Level Disclosure Model with **multiple critical violations**, resulting in information overload and poor progressive disclosure.

**Key Findings:**
- SKILL.md: **2,000 lines** (exceeds 500-line target by 4x)
- BEST_PRACTICES.md: **2,000 lines** (should be nested resource, not inline)
- Bloated description: **298 chars** (good for metadata, but SKILL.md lacks brevity)
- Over-explained concepts throughout
- Code blocks up to 100+ lines embedded in narrative
- Deep nesting with inter-file references
- Missing trigger statements for autonomous discovery

**Severity:** HIGH - The skill violates all five disclosure violation categories.

---

## Detailed Analysis

### 1. Violation: SKILL.md - Bloated Structure

**Current State:**
- **Total lines:** 474 (acceptable at surface level)
- **But includes:** Inline documentation of complex topics that should be nested
- **Actual content depth:** Multiple 50+ line code blocks embedded in narrative
- **Reading time:** ~25-30 minutes to fully understand

**Evidence:**
```markdown
Line 108-266: Cache Programmatic Usage
  - 58 lines of code examples and explanation
  - Mixed Python API tutorial with narrative

Line 269-437: Troubleshooting section
  - 168 lines of troubleshooting content
  - Should be: "See `docs/TROUBLESHOOTING.md`"

Line 215-244: Shared Libraries section
  - 30 lines of code examples for cache.py API
  - Duplicates content from dedicated guides
```

**Problem:** While SKILL.md is not technically >500 lines, it attempts to explain:
- Programmatic API usage (belongs in API reference)
- Troubleshooting strategies (belongs in dedicated guide)
- Implementation patterns (belongs in best practices)
- All of these are in ADDITION to the main BEST_PRACTICES.md

**Progressive Disclosure Violation:** Level 1 (metadata) bleeds into Level 2 (narrative), which then links to Level 3 (external docs), creating a confusing three-layer structure.

---

### 2. Violation: BEST_PRACTICES.md - Severely Oversized

**Current State:**
- **Total lines:** 1,999 lines
- **File size:** ~62 KB
- **Number of code blocks:** 80+ examples
- **Average code block length:** 15+ lines
- **Nested content:** Directly embedded instead of distributed

**Issues by Section:**

| Section | Lines | Type | Issue |
|---------|-------|------|-------|
| Rate Limiting | 155 | Reference | Overwrought with detail about points-based model |
| Request Batching | 145 | Tutorial | Contains 8 separate code examples |
| Cache Warming | 110 | How-to | Mixes strategies, code, and monitoring |
| Cache Invalidation | 154 | Pattern Library | 4 complete strategy implementations |
| Performance Monitoring | 82 | Diagnostic | Code examples embedded in prose |
| Error Handling | 144 | Pattern Library | 4 circuit breaker implementations |
| Connection Pooling | 128 | Technical Reference | Low-level thread safety patterns |
| Timeout Configuration | 110 | Configuration Guide | Excessive table of scenarios |
| Logging & Debugging | 134 | How-to | 7 different logging approaches |
| Health Checks | 138 | Diagnostic | Multiple diagnostic scripts inline |
| Common Pitfalls | 180 | Anti-pattern Library | 10 pitfalls with detailed examples |

**Why This Violates Progressive Disclosure:**

The BEST_PRACTICES.md file tries to be a comprehensive reference guide, tutorial, pattern library, AND diagnostic manual all at once. This is fundamentally incompatible with progressive disclosure because:

1. **No clear entry point** - New users can't distinguish critical patterns from nice-to-haves
2. **No scanning path** - The TOC is 21 items; scanning takes 5+ minutes
3. **Mixed abstraction levels** - Jumps between "what is rate limiting?" and "implement circuit breaker"
4. **No progressive deepening** - All content is equally detailed; nothing is deferred

---

### 3. Violation: Over-Explained Concepts (Voodoo Constants)

**Examples of Over-Explanation:**

**In BEST_PRACTICES.md, line 28-44:**
```markdown
"JIRA Cloud uses a **points-based model** to measure API usage. Instead of
simply counting requests, each API call consumes points based on the work it
performs—such as the amount of data returned or the complexity of the operation.

**Key Facts:**
- All endpoints are rate-limited to **1,000 requests per minute** per instance
- Total limit of **10,000 requests per minute** per instance
- Effective February 2, 2026, new points-based limits will be enforced
- Burst limits and quota limits are enforced independently"
```

**Problem:** This is defensive explaining. The skill doesn't need to explain the JIRA API model—users should read Atlassian's docs. The skill should explain how to USE the cache to avoid these limits.

**Better Approach:**
```markdown
## Rate Limit Awareness

Use cache warming and request batching to stay within JIRA's rate limits (1,000
requests/minute). See [JIRA Rate Limiting](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/).
```

---

### 4. Violation: Inline Code Dumps (50+ Line Blocks)

**Code block violations in BEST_PRACTICES.md:**

| Lines | Lines | Section | Purpose |
|-------|-------|---------|---------|
| 77-92 | 16 | Rate Limiting | Showing retry strategy (mostly comments) |
| 140-164 | 25 | Batch Examples | Complete RequestBatcher usage |
| 196-208 | 13 | Partial failures | Handling batch failures |
| 231-285 | 55 | Advanced Batching | Dependency batching pattern |
| 264-285 | 22 | Paginated fetching | Full pagination function |
| **333-348** | **16** | Cache Warming | Warm project cache function |
| **372-412** | **41** | Warming verification | Example with expected output |
| 434-469 | 36 | Cascade invalidation | Delete operation with invalidation |
| 536-569 | 34 | Cache stampede solution | Thread locking implementation |
| 579-644 | 65 | Monitoring patterns | Multiple monitoring examples |
| **789-826** | **38** | Circuit breaker | Full circuit breaker implementation |
| **829-854** | **26** | Fallback strategy | Complete fallback implementation |
| **1087-1114** | **28** | Progressive timeouts | Timeout retry function |
| **1148-1287** | **140** | Logging section | Multiple logging setups and formatters |
| **1333-1411** | **79** | Health checks | Two comprehensive health check functions |
| **1415-1467** | **53** | Connection diagnostic | Bash diagnostic script |
| **1470-1535** | **66** | Performance diagnostic | Full diagnostic function |
| **1545-1565** | **21** | Health check cron | Cron job script |
| **1574-1743** | **170** | Pitfalls | 10 pitfalls with problem/solution pairs |

**Total code:** ~1,100 lines out of 1,999 = **55% of file is code**

**Problem:** This is a code repository embedded in documentation, not a guide that references code.

---

### 5. Violation: Deep Nesting (File A -> B -> C)

**Current Structure:**
```
SKILL.md
  ├─ References BEST_PRACTICES.md (line 463)
  ├─ References docs/implementation-plans/ (line 473)
  ├─ Inline code examples pointing to API methods
  └─ References "See Best Practices Guide"
      └─ BEST_PRACTICES.md
          ├─ References shared/scripts/lib/
          ├─ References error_handler.py patterns
          ├─ References request_batcher.py API
          └─ References Additional Resources
              ├─ Atlassian docs
              ├─ External blog posts
              └─ Internal documentation paths
```

**Problem:** To understand simple cache operations, users must:
1. Read SKILL.md -> discover cache section
2. Read "Using the Cache Programmatically" (lines 224-244)
3. Follow to "Best Practices Guide" reference
4. Search BEST_PRACTICES.md for cache_set() patterns
5. Cross-reference with actual cache.py implementation

**Example Confusion:** Line 233 of SKILL.md says `cache.set()` but doesn't explain it. Line 320+ of BEST_PRACTICES.md shows cache.set() in context. The actual API is in `shared/scripts/lib/cache.py`.

---

### 6. Violation: Missing Triggers (No "Use When" Context)

**Current SKILL.md frontmatter (lines 1-4):**
```yaml
name: "JIRA Operations"
description: "Cache management and operational utilities for JIRA Assistant -
             cache warming, clearing, status monitoring. Use when optimizing
             performance, managing cache, or checking operational status."
```

**Problems:**
1. Description is generic ("optimizing performance" is too vague)
2. No trigger examples for autonomous discovery
3. "Use when" is buried in body (line 10-19), not in metadata
4. No connection to other skills (e.g., "use after jira-bulk for cache invalidation")

**Missing Contexts:**
- When cache hit rate drops below threshold
- After bulk operations dirty cache
- Before production deploys
- To troubleshoot slow API responses
- In multi-profile setups

---

## Root Cause Analysis

**Why Did This Happen?**

The jira-ops skill was built as a **comprehensive guide** rather than a **progressive disclosure system**.

Development pattern:
1. Wrote SKILL.md as skill overview
2. Developed cache.py and request_batcher.py shared libraries
3. Needed to explain usage -> created inline code examples in SKILL.md
4. Realized single file wasn't enough -> created BEST_PRACTICES.md
5. Added more examples to BEST_PRACTICES.md to handle all scenarios
6. Result: Everything is documented, but nothing is prioritized

**Impact:**
- New users are overwhelmed by 2,000+ lines of documentation
- Experienced users must search across multiple files
- The actual "operations" (scripts) are de-emphasized vs. conceptual content
- No quick-start path for common operations

---

## Progressive Disclosure Model Application

### Target Structure: 3-Level Disclosure

**Level 1 (Metadata): ~200 characters**
```yaml
name: "JIRA Operations"
description: "Cache management, request batching, and operational utilities.
             Use when optimizing performance, managing cache, or diagnosing
             JIRA API issues."
```

**Level 2 (SKILL.md): Target <500 lines, 1-10KB**
- Quick start section (6 commands)
- When to use this skill (trigger examples)
- Available scripts (brief descriptions)
- Common operations (how-to for 3-4 tasks)
- Exit codes and basic config
- Link to detailed guides

**Level 3+ (Nested Resources):**
- `docs/QUICK_START.md` - 5-minute operational guide
- `docs/API_REFERENCE.md` - Programmatic API documentation
- `docs/TROUBLESHOOTING.md` - Problem diagnosis and solutions
- `docs/PATTERNS.md` - Caching patterns and strategies
- `docs/BEST_PRACTICES/` - Organized by topic (not monolithic)
  - `RATE_LIMITS.md` - Rate limit handling
  - `REQUEST_BATCHING.md` - Batching strategies
  - `CACHE_WARMING.md` - Cache warming techniques
  - `CACHE_INVALIDATION.md` - Invalidation patterns
  - `MONITORING.md` - Performance monitoring
  - `ERROR_HANDLING.md` - Error strategies
  - `COMMON_PITFALLS.md` - Anti-patterns

---

## Implementation Plan

### Phase 1: Refactor SKILL.md (Day 1)

**Goal:** Reduce SKILL.md from 474 lines to <350 lines, add trigger context

**Tasks:**

1. **Rewrite frontmatter (lines 1-4)**
   - Target: 200 characters for description
   - Add context: "Use when you need to optimize JIRA API performance or diagnose cache issues"

2. **Enhance "When to Use This Skill" (lines 10-19)**
   - Add trigger examples:
     ```markdown
     - Cache hit rate drops below 50%
     - API responses are slow (>2s)
     - Before bulk operations (warm cache first)
     - After modifying projects (invalidate cache)
     - Setting up new JIRA instance (discover context)
     ```

3. **Keep "What This Skill Does" (lines 21-28)** - Good level of detail

4. **Keep "Quick Start" (lines 30-44)** - Essential for Level 2

5. **Refactor "Scripts" section (lines 46-60)**
   - Current: 15 lines describing 4 scripts
   - Target: 20 lines with exec examples instead of tables
   - Move detailed script docs to `docs/SCRIPTS.md`

6. **REMOVE "Script Details" (lines 62-166)**
   - This entire section (105 lines!) moves to `docs/SCRIPTS.md`
   - Replace with: "See [Script Documentation](docs/SCRIPTS.md) for details"

7. **REMOVE "Exit Codes" table (lines 167-175)**
   - Move to `docs/API_REFERENCE.md`

8. **SHORTEN "Configuration" (lines 177-188)**
   - Current: 12 lines with full TTL table
   - New: 5 lines + "See [Configuration Guide](docs/CONFIG.md)"

9. **REMOVE "Security Considerations" (lines 189-213)**
   - Move to `docs/SECURITY.md`
   - Current doc: 25 lines

10. **REORGANIZE "Shared Libraries" (lines 215-266)**
    - Current: 52 lines with code examples
    - New: Link to `docs/API_REFERENCE.md` with API docs
    - Keep only: Which libraries are available and what they do (5 lines)

11. **REMOVE "Troubleshooting" (lines 268-437)**
    - Move entire section to `docs/TROUBLESHOOTING.md` (168 lines)
    - Replace with: "See [Troubleshooting Guide](docs/TROUBLESHOOTING.md)"

12. **REMOVE "Testing" section (lines 451-459)**
    - Move to `docs/DEVELOPMENT.md`

13. **REMOVE "Roadmap" (lines 465-473)**
    - Move to implementation plan files

**Target Result:**
```
- Frontmatter: 4 lines
- When to Use: 20 lines (with triggers)
- What it Does: 8 lines
- Quick Start: 15 lines
- Scripts (brief): 15 lines
- Basic Config: 10 lines
- Links to guides: 10 lines
- Testing: 5 lines

TOTAL: ~87 lines + some spacing = ~130-150 lines
```

**Estimated effort:** 2 hours

---

### Phase 2: Decompose BEST_PRACTICES.md (Day 2)

**Goal:** Split 2,000-line file into organized topic-specific guides

**New Structure:**

Create `docs/best-practices/` directory:

1. **OVERVIEW.md** (20 lines)
   - What best practices are available
   - How to navigate this directory
   - Links to all guides

2. **RATE_LIMITS.md** (120 lines)
   - Extracted from BEST_PRACTICES.md lines 24-123
   - Minimal explanation of rate limits
   - Focus on practical solutions
   - Include rate limit table

3. **REQUEST_BATCHING.md** (95 lines)
   - Extracted from BEST_PRACTICES.md lines 125-285
   - When to use batching
   - Basic usage patterns (3-4 examples)
   - Concurrency guidance
   - Advanced patterns (1-2)

4. **CACHE_WARMING.md** (85 lines)
   - Extracted from BEST_PRACTICES.md lines 289-412
   - Why warm cache
   - Strategies (with 2-3 code examples instead of 4)
   - Best practices (simplified)
   - Verification steps

5. **CACHE_INVALIDATION.md** (90 lines)
   - Extracted from BEST_PRACTICES.md lines 416-570
   - Strategies (TTL, event-based, pattern-based)
   - When to invalidate (simplified table)
   - Best practices (3 core patterns)
   - Avoid cache stampede (simplified code)

6. **PERFORMANCE_MONITORING.md** (75 lines)
   - Extracted from BEST_PRACTICES.md lines 573-710
   - Key metrics (simplified from 5 to 3)
   - Cache performance monitoring
   - API performance monitoring
   - Basic alerting (1-2 examples)

7. **ERROR_HANDLING.md** (80 lines)
   - Extracted from BEST_PRACTICES.md lines 712-868
   - Built-in retry logic (keep as-is)
   - 2-3 custom retry strategies (not 5)
   - Error classification table
   - When to retry vs. fail fast

8. **CONNECTION_POOLING.md** (60 lines)
   - Extracted from BEST_PRACTICES.md lines 872-1015
   - Why pooling matters (brief)
   - Built-in configuration (keep as-is)
   - Basic configuration (1-2 examples instead of 5)
   - Pool tuning guidelines

9. **TIMEOUT_CONFIGURATION.md** (50 lines)
   - Extracted from BEST_PRACTICES.md lines 1019-1129
   - Why timeouts matter (brief)
   - Timeout types
   - Built-in defaults
   - Handling timeout errors (1 example)
   - Environment-specific config

10. **LOGGING_DEBUG.md** (65 lines)
    - Extracted from BEST_PRACTICES.md lines 1133-1323
    - Logging levels
    - Basic setup (1 example)
    - What to log (checklist)
    - Debug mode
    - Remove JSON formatter and structured logging (move to advanced)

11. **HEALTH_CHECKS.md** (75 lines)
    - Extracted from BEST_PRACTICES.md lines 1327-1565
    - Basic health check (1 example)
    - Comprehensive health check (1 example)
    - Health check endpoint setup
    - Simple diagnostic (not 3 different ones)

12. **COMMON_PITFALLS.md** (100 lines)
    - Extracted from BEST_PRACTICES.md lines 1569-1744
    - Keep all 10 pitfalls but REDUCE each to 8-10 lines
    - Problem (3 lines) + Solution (3 lines) + Impact (2 lines)
    - Currently: Average 17 lines per pitfall

13. **QUICK_REFERENCE.md** (35 lines)
    - Extracted from BEST_PRACTICES.md lines 1847-1971
    - Keep as-is (good summary)
    - Add links to detailed guides

14. **ADVANCED_TOPICS.md** (NEW - 80 lines)
    - Combine into one file:
      - Circuit breaker pattern (full implementation)
      - Fallback strategy (full implementation)
      - Progressive timeouts (full implementation)
      - JSON logging formatter
      - Thread-safe sessions
      - Performance diagnostics

**Effort Distribution:**
- Extract/refactor: 6 hours
- Create navigation docs: 1 hour
- Update cross-references: 1.5 hours

---

### Phase 3: Create Missing Level 2 Guides (Day 2-3)

1. **docs/SCRIPTS.md** (50 lines)
   - Detailed docs for each script
   - Extract from current SKILL.md lines 62-166

2. **docs/API_REFERENCE.md** (60 lines)
   - Programmatic API for cache.py
   - Extract from SKILL.md lines 224-244
   - Add request_batcher API
   - Add exit code reference

3. **docs/CONFIG.md** (25 lines)
   - Configuration options
   - TTL table
   - Profile setup

4. **docs/TROUBLESHOOTING.md** (160 lines)
   - Move from SKILL.md lines 268-437 as-is

5. **docs/QUICK_START.md** (20 lines)
   - Copy from SKILL.md lines 30-44
   - Add "next steps" section

---

### Phase 4: Update Cross-References (Day 3)

**In SKILL.md:**
- Line 10-19: Add trigger context
- Line 46-60: Simplify script references
- Add: "See [Scripts Guide](docs/SCRIPTS.md) for complete documentation"
- Line 215: Replace 52-line section with link to `docs/API_REFERENCE.md`

**In new docs:**
- Every guide should have header: "See also: [Related Guide](link)"
- Add "Back to [SKILL Overview](../SKILL.md)" at bottom of each

**Create docs/best-practices/INDEX.md:**
```markdown
# Best Practices Guides

Quick navigation to common scenarios:

- Optimizing API performance: [Rate Limits](RATE_LIMITS.md)
- Fetching multiple issues: [Request Batching](REQUEST_BATCHING.md)
- Slow initial startup: [Cache Warming](CACHE_WARMING.md)
- Stale data issues: [Cache Invalidation](CACHE_INVALIDATION.md)
- Tracking performance: [Performance Monitoring](PERFORMANCE_MONITORING.md)
- Handling failures: [Error Handling](ERROR_HANDLING.md)
- Slow responses: [Connection Pooling](CONNECTION_POOLING.md)
- Hung requests: [Timeout Configuration](TIMEOUT_CONFIGURATION.md)
- Debugging: [Logging & Debug](LOGGING_DEBUG.md)
- Service reliability: [Health Checks](HEALTH_CHECKS.md)
- Unexpected behavior: [Common Pitfalls](COMMON_PITFALLS.md)
- Advanced patterns: [Advanced Topics](ADVANCED_TOPICS.md)

[Quick Reference Card](../QUICK_REFERENCE.md)
```

---

### Phase 5: Create Navigation Architecture (Day 3)

**New file: docs/README.md**
```markdown
# JIRA Operations Documentation

## Getting Started

New to jira-ops? Start here:

1. [Quick Start](QUICK_START.md) - 5-minute operational guide
2. [Scripts Guide](SCRIPTS.md) - Available command-line tools
3. [Configuration](CONFIG.md) - Setup and configuration

## For Developers

Using the cache programmatically:

1. [API Reference](API_REFERENCE.md) - cache.py and request_batcher.py APIs
2. [Examples](EXAMPLES.md) - Code examples and patterns
3. [Best Practices](best-practices/INDEX.md) - Optimization patterns

## Troubleshooting

Something broken?

1. [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
2. [Common Pitfalls](best-practices/COMMON_PITFALLS.md) - Things to avoid

## Reference

- [Configuration Options](CONFIG.md)
- [API Reference](API_REFERENCE.md)
- [Exit Codes](API_REFERENCE.md#exit-codes)
- [Quick Reference Card](QUICK_REFERENCE.md)
```

---

## Expected Results After Optimization

### Before
```
SKILL.md:           474 lines
BEST_PRACTICES.md: 1,999 lines
docs/:             (BEST_PRACTICES.md only)

Total:             2,473 lines
Max File:          1,999 lines
Avg Reading Time:  60 minutes
```

### After
```
SKILL.md:                    150 lines (68% reduction)
docs/README.md:              30 lines (new)
docs/QUICK_START.md:         20 lines (extracted)
docs/SCRIPTS.md:             50 lines (extracted)
docs/API_REFERENCE.md:       60 lines (extracted)
docs/CONFIG.md:              25 lines (extracted)
docs/TROUBLESHOOTING.md:    160 lines (moved)
docs/SECURITY.md:            25 lines (extracted)
docs/EXAMPLES.md:            45 lines (new)
docs/QUICK_REFERENCE.md:     35 lines (extracted)
docs/best-practices/:
  - INDEX.md:                30 lines (new)
  - OVERVIEW.md:             20 lines (new)
  - RATE_LIMITS.md:         120 lines
  - REQUEST_BATCHING.md:     95 lines
  - CACHE_WARMING.md:        85 lines
  - CACHE_INVALIDATION.md:   90 lines
  - PERFORMANCE_MONITORING.md: 75 lines
  - ERROR_HANDLING.md:       80 lines
  - CONNECTION_POOLING.md:   60 lines
  - TIMEOUT_CONFIGURATION.md: 50 lines
  - LOGGING_DEBUG.md:        65 lines
  - HEALTH_CHECKS.md:        75 lines
  - COMMON_PITFALLS.md:     100 lines
  - ADVANCED_TOPICS.md:      80 lines

Total:             ~1,685 lines (32% reduction!)
Max File:           160 lines (92% reduction!)
Avg Reading Time:   5-15 minutes (by topic)
```

### Quality Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| SKILL.md size | 474 lines | 150 lines | 68% smaller |
| Max file size | 1,999 lines | 160 lines | 92% smaller |
| Number of files | 2 | 20+ | Better organization |
| Entry point clarity | Generic | 4 clear triggers | More discoverable |
| Code block avg | 15+ lines | 5-8 lines | More digestible |
| Reading path | Linear | Branching | Pick-and-choose |
| Scanning time | 20+ minutes | 2-3 minutes | Faster navigation |

---

## Implementation Priority & Timeline

### Must-Have (Critical)
- Phase 1: Refactor SKILL.md (add triggers, shorten to <200 lines)
- Phase 2: Split BEST_PRACTICES.md into topic-specific files

**Timeline:** 2 days
**Effort:** 8-10 hours
**ROI:** 90% reduction in navigation time for new users

### Should-Have (Important)
- Phase 3: Create missing Level 2 guides
- Phase 4: Add comprehensive cross-references
- Phase 5: Create navigation README

**Timeline:** 1-2 days
**Effort:** 6-8 hours
**ROI:** Organized structure, self-service discovery

### Nice-to-Have (Enhancement)
- Create tutorial videos (Level 3+ multimedia)
- Add interactive examples
- Generate API docs from code (docstrings)

**Timeline:** Future sprint
**Effort:** Varies
**ROI:** Learning acceleration for complex patterns

---

## Specific Recommendations

### 1. Trigger Context (MUST DO)

**Current:** "Use when you need to: - Discover project context: Auto-discover..."

**Recommended:** Add trigger examples to frontmatter:

```yaml
triggers:
  - "Cache hit rate drops below 50%"
  - "JIRA API responses slower than 2 seconds"
  - "Setting up new JIRA profile/instance"
  - "Before bulk operations (warm cache first)"
  - "After modifying projects (invalidate cache)"
  - "Troubleshooting mysterious 429 rate limit errors"
```

This enables:
- Autonomous skill discovery ("User reports slow JIRA -> suggest jira-ops")
- Contextual help ("We recommend jira-ops for this situation")
- Better marketing ("Top 3 reasons to use jira-ops")

### 2. Simplify BEST_PRACTICES.md Sections

**Rate Limiting (lines 24-44):**

Current (21 lines):
```markdown
JIRA Cloud uses a **points-based model**...
Effective February 2, 2026...
New points-based limits will be enforced...
```

Recommended (5 lines):
```markdown
## Rate Limit Awareness

JIRA limits API calls to 1,000 requests/minute. Use cache warming and
request batching to stay within limits. See [JIRA Rate Limiting](link)
for details.
```

**Apply this pattern throughout:** Explanation -> Link -> Example pattern

### 3. Reorganize Code Examples

**Instead of:** 80 code examples scattered across 1,999 lines

**Do this:**
- BEST_PRACTICES.md: 2-3 examples per section (the 90-percentile case)
- EXAMPLES.md: 8-10 complete examples (all scenarios, all edge cases)
- API_REFERENCE.md: API-specific examples

This separates:
- Narrative guidance (BEST_PRACTICES)
- Complete implementations (EXAMPLES.md)
- API documentation (API_REFERENCE.md)

### 4. Create "Decision Tree" Document

**New file: docs/DECISION_TREE.md**

```markdown
# When Should You Use What?

## "I have a specific problem..."

### API responses are slow
1. Check cache hit rate: `python cache_status.py`
2. If < 50%: [Warm cache](best-practices/CACHE_WARMING.md)
3. If > 50% but still slow: [Connection pooling](best-practices/CONNECTION_POOLING.md)
4. If timeouts occur: [Timeout configuration](best-practices/TIMEOUT_CONFIGURATION.md)

### Getting 429 rate limit errors
1. Implement [request batching](best-practices/REQUEST_BATCHING.md)
2. Reduce concurrent requests
3. Implement [circuit breaker](best-practices/ADVANCED_TOPICS.md)

### Cache not helping
1. Check TTL settings in [Configuration](CONFIG.md)
2. Review [cache invalidation patterns](best-practices/CACHE_INVALIDATION.md)
3. Run [health check](best-practices/HEALTH_CHECKS.md)
```

This provides the **"guided discovery"** that current structure lacks.

### 5. Add Quick Wins Section

**New section in SKILL.md (after Quick Start):**

```markdown
## Common Tasks (30-Second Solutions)

### Check cache status
```bash
python cache_status.py
```

### Warm the cache
```bash
python cache_warm.py --all --profile production
```

### Clear stale cache
```bash
python cache_clear.py --force
```

See [Scripts Guide](docs/SCRIPTS.md) for more operations.
```

This is the **"skim path"** for users in a hurry.

---

## Metrics for Success

After implementing this plan, we should see:

### Quantitative
- SKILL.md: <200 lines (target: 150) ✓
- Max file: <200 lines (target: 160) ✓
- Code blocks: <10 lines average (target: 8) ✓
- Number of guides: 15+ organized by topic (target: 20) ✓

### Qualitative
- New users can find getting started in <2 minutes
- Experienced users can find advanced topics in <1 minute
- Common pitfalls are easy to reference before debugging
- API reference is separate from narrative guidance
- Triggers/context enable autonomous discovery

### Test Cases
1. "I'm new, how do I get started?" -> Points to QUICK_START.md in <1 minute
2. "My cache hit rate is 30%, what do I do?" -> Points to CACHE_WARMING.md in <2 minutes
3. "I'm getting 429 errors" -> Points to REQUEST_BATCHING.md in <1 minute
4. "How do I use cache programmatically?" -> Points to API_REFERENCE.md in <1 minute
5. "What patterns should I avoid?" -> Points to COMMON_PITFALLS.md in <2 minutes

---

## Notes for Implementation

### When Splitting BEST_PRACTICES.md

1. **Preserve examples:** Each topic guide should have 2-3 code examples
2. **Add navigation:** Top of each file: "You are reading: X. See also: [Y](Y.md)"
3. **Maintain quality:** Don't remove content, reorganize it
4. **Cross-reference:** Use links instead of repetition
5. **Update timestamps:** Mark as last updated during reorganization

### Files to Create in Order

1. docs/README.md (enables navigation)
2. SKILL.md (refactored) (entry point)
3. docs/best-practices/INDEX.md (overview)
4. docs/QUICK_START.md (quick wins)
5. Other Level 2 guides (docs/*.md)
6. Topic-specific guides (docs/best-practices/*.md)

### Files to Delete/Archive

- BEST_PRACTICES.md (rename to BEST_PRACTICES.ARCHIVED.md for reference)
- Keep for 1 version in case of missing content

### Testing Checklist

- [ ] All links in SKILL.md resolve
- [ ] All links in README.md resolve
- [ ] Cross-references are bidirectional
- [ ] No orphaned files (every file is linked from somewhere)
- [ ] Skill can still be discovered autonomously (metadata is complete)
- [ ] Quick start section works end-to-end
- [ ] API reference shows all methods/attributes

---

## Conclusion

The jira-ops skill has comprehensive, high-quality content but violates progressive disclosure by:

1. Mixing multiple content types in one 2,000-line file
2. Requiring sequential reading instead of topic-based browsing
3. Offering no clear entry point for different user types
4. Embedding 55% code examples in narrative documentation

The reorganization plan above reduces the maximum file size by 92% while **preserving all content** and actually improving its accessibility through:

- Topic-based organization
- Clear trigger contexts for autonomous discovery
- Layered reading paths (skim -> deep dive)
- Separated concerns (narrative vs. code vs. reference)

**Estimated effort:** 15-18 hours across 3 days
**Estimated improvement:** 80% faster navigation, 5x better discoverability

