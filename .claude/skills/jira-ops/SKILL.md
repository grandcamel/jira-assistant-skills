# JIRA Operations Skill

Cache management, request batching, and operational utilities for JIRA Assistant.

## Quick Start

```bash
# Check cache status
python cache_status.py

# Clear cache
python cache_clear.py --force

# Warm cache with project/field data
python cache_warm.py --all --profile production
```

## Scripts

### Cache Management

| Script | Description |
|--------|-------------|
| `cache_status.py` | Display cache statistics (size, entries, hit rate) |
| `cache_clear.py` | Clear cache entries (all, by category, or by pattern) |
| `cache_warm.py` | Pre-warm cache with commonly accessed data |

## Script Details

### cache_status.py

Display JIRA cache statistics and status.

```bash
# Show cache status
python cache_status.py

# Output as JSON
python cache_status.py --json
```

**Output:**
```
Cache Statistics:
  Total Size: 12.5 MB / 100 MB
  Entries: 1,234
  Hit Rate: 78% (1000 hits, 234 misses)

By Category:
  issue: 800 entries, 8 MB
  project: 50 entries, 1 MB
  user: 200 entries, 2 MB
  field: 184 entries, 1.5 MB
```

### cache_clear.py

Clear JIRA cache entries.

```bash
# Clear all cache
python cache_clear.py --force

# Clear specific category
python cache_clear.py --category issue --force

# Clear by pattern
python cache_clear.py --pattern "PROJ-*" --category issue --force

# Dry run
python cache_clear.py --dry-run
```

### cache_warm.py

Pre-warm JIRA cache with commonly accessed data.

```bash
# Cache projects
python cache_warm.py --projects

# Cache field definitions
python cache_warm.py --fields

# Cache everything
python cache_warm.py --all --profile production --verbose
```

## Configuration

Cache is stored in `~/.jira-skills/cache/` with the following TTL defaults:

| Category | TTL | Description |
|----------|-----|-------------|
| `issue` | 5 minutes | Issue data (frequently updated) |
| `project` | 1 hour | Project metadata |
| `user` | 1 hour | User information |
| `field` | 1 day | Field definitions |
| `search` | 1 minute | Search results |

## Shared Libraries

This skill uses shared infrastructure from `.claude/skills/shared/scripts/lib/`:

| Library | Description |
|---------|-------------|
| `cache.py` | SQLite-based caching with TTL and LRU eviction |
| `request_batcher.py` | Parallel request batching for bulk operations |

### Using the Cache Programmatically

```python
from cache import JiraCache

# Create cache instance
cache = JiraCache()

# Cache an issue
cache.set("PROJ-123", issue_data, category="issue")

# Retrieve cached issue
issue = cache.get("PROJ-123", category="issue")

# Invalidate by pattern
cache.invalidate(pattern="PROJ-*", category="issue")

# Get statistics
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate * 100:.1f}%")
```

### Using Request Batching

```python
from request_batcher import RequestBatcher, batch_fetch_issues

# Option 1: Convenience function
issues = batch_fetch_issues(client, ["PROJ-1", "PROJ-2", "PROJ-3"])

# Option 2: Manual batching
batcher = RequestBatcher(client, max_concurrent=10)
id1 = batcher.add("GET", "/rest/api/3/issue/PROJ-1")
id2 = batcher.add("GET", "/rest/api/3/issue/PROJ-2")

results = batcher.execute_sync(progress_callback=lambda c, t: print(f"{c}/{t}"))

for request_id, result in results.items():
    if result.success:
        print(f"Got: {result.data['key']}")
    else:
        print(f"Error: {result.error}")
```

## Error Handling

All scripts provide meaningful error messages:

```bash
$ python cache_status.py
Error: Cannot open cache database

$ python cache_warm.py --all
Error: config_manager not available. Cannot connect to JIRA.
```

## Testing

Run tests with:

```bash
cd /path/to/Jira-Assistant-Skills
PYTHONPATH=".claude/skills/shared/scripts/lib:.claude/skills/jira-ops/scripts" \
  python -m pytest .claude/skills/jira-ops/tests/ -v
```

## Roadmap

Future enhancements planned:
- Rate limiting integration
- Offline mode support
- Audit logging
- Undo/redo capability

See `docs/implementation-plans/ROBUSTNESS_SCALE_IMPLEMENTATION_PLAN.md` for details.
