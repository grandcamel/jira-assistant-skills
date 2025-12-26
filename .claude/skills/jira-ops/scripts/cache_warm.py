#!/usr/bin/env python3
"""
Pre-warm JIRA cache with commonly accessed data.

Fetches and caches project metadata, field definitions, and other
frequently accessed data to improve performance of subsequent operations.

Usage:
    python cache_warm.py --projects          # Cache project list
    python cache_warm.py --fields            # Cache field definitions
    python cache_warm.py --users             # Cache user list
    python cache_warm.py --all               # Cache everything
    python cache_warm.py --profile production

Examples:
    # Warm project and field caches
    python cache_warm.py --projects --fields

    # Warm all caches for production profile
    python cache_warm.py --all --profile production
"""

import argparse
import sys
from pathlib import Path

# Add shared lib to path
shared_lib_path = str(Path(__file__).parent.parent.parent / 'shared' / 'scripts' / 'lib')
if shared_lib_path not in sys.path:
    sys.path.insert(0, shared_lib_path)

from cache import JiraCache

try:
    from config_manager import get_jira_client
    HAS_CONFIG_MANAGER = True
except ImportError:
    HAS_CONFIG_MANAGER = False


def warm_projects(client, cache, verbose=False):
    """Fetch and cache project list."""
    if verbose:
        print("Fetching projects...")

    try:
        response = client.get("/rest/api/3/project", operation="fetch projects")

        for project in response:
            key = cache.generate_key("project", project["key"])
            cache.set(key, project, category="project")

        count = len(response) if isinstance(response, list) else 1
        if verbose:
            print(f"  Cached {count} projects")
        return count
    except Exception as e:
        if verbose:
            print(f"  Error fetching projects: {e}")
        return 0


def warm_fields(client, cache, verbose=False):
    """Fetch and cache field definitions."""
    if verbose:
        print("Fetching fields...")

    try:
        response = client.get("/rest/api/3/field", operation="fetch fields")

        for field in response:
            key = cache.generate_key("field", field["id"])
            cache.set(key, field, category="field")

        # Also cache the full list
        all_fields_key = cache.generate_key("field", "all")
        cache.set(all_fields_key, response, category="field")

        count = len(response) if isinstance(response, list) else 1
        if verbose:
            print(f"  Cached {count} fields")
        return count
    except Exception as e:
        if verbose:
            print(f"  Error fetching fields: {e}")
        return 0


def warm_issue_types(client, cache, verbose=False):
    """Fetch and cache issue type definitions."""
    if verbose:
        print("Fetching issue types...")

    try:
        response = client.get("/rest/api/3/issuetype", operation="fetch issue types")

        for issue_type in response:
            key = cache.generate_key("field", "issuetype", issue_type["id"])
            cache.set(key, issue_type, category="field")

        # Also cache the full list
        all_types_key = cache.generate_key("field", "issuetypes", "all")
        cache.set(all_types_key, response, category="field")

        count = len(response) if isinstance(response, list) else 1
        if verbose:
            print(f"  Cached {count} issue types")
        return count
    except Exception as e:
        if verbose:
            print(f"  Error fetching issue types: {e}")
        return 0


def warm_priorities(client, cache, verbose=False):
    """Fetch and cache priority definitions."""
    if verbose:
        print("Fetching priorities...")

    try:
        response = client.get("/rest/api/3/priority", operation="fetch priorities")

        for priority in response:
            key = cache.generate_key("field", "priority", priority["id"])
            cache.set(key, priority, category="field")

        # Also cache the full list
        all_key = cache.generate_key("field", "priorities", "all")
        cache.set(all_key, response, category="field")

        count = len(response) if isinstance(response, list) else 1
        if verbose:
            print(f"  Cached {count} priorities")
        return count
    except Exception as e:
        if verbose:
            print(f"  Error fetching priorities: {e}")
        return 0


def warm_statuses(client, cache, verbose=False):
    """Fetch and cache status definitions."""
    if verbose:
        print("Fetching statuses...")

    try:
        response = client.get("/rest/api/3/status", operation="fetch statuses")

        for status in response:
            key = cache.generate_key("field", "status", status["id"])
            cache.set(key, status, category="field")

        # Also cache the full list
        all_key = cache.generate_key("field", "statuses", "all")
        cache.set(all_key, response, category="field")

        count = len(response) if isinstance(response, list) else 1
        if verbose:
            print(f"  Cached {count} statuses")
        return count
    except Exception as e:
        if verbose:
            print(f"  Error fetching statuses: {e}")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Pre-warm JIRA cache",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python cache_warm.py --projects --fields
    python cache_warm.py --all --profile production
        """
    )
    parser.add_argument(
        "--projects",
        action="store_true",
        help="Cache project list"
    )
    parser.add_argument(
        "--fields",
        action="store_true",
        help="Cache field definitions"
    )
    parser.add_argument(
        "--users",
        action="store_true",
        help="Cache assignable users (requires project)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Cache all available metadata"
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="JIRA profile to use"
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default=None,
        help="Custom cache directory"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Check if any warming option is selected
    if not any([args.projects, args.fields, args.users, args.all]):
        parser.print_help()
        print("\nError: At least one warming option is required", file=sys.stderr)
        sys.exit(1)

    if not HAS_CONFIG_MANAGER:
        print("Error: config_manager not available. Cannot connect to JIRA.", file=sys.stderr)
        sys.exit(1)

    try:
        client = get_jira_client(profile=args.profile)
        cache = JiraCache(cache_dir=args.cache_dir)

        total_cached = 0

        if args.all or args.projects:
            total_cached += warm_projects(client, cache, args.verbose)

        if args.all or args.fields:
            total_cached += warm_fields(client, cache, args.verbose)
            total_cached += warm_issue_types(client, cache, args.verbose)
            total_cached += warm_priorities(client, cache, args.verbose)
            total_cached += warm_statuses(client, cache, args.verbose)

        if args.users:
            print("User caching requires a project context. Use search scripts instead.")

        print(f"\nCache warming complete. Cached {total_cached} items.")

        stats = cache.get_stats()
        print(f"Total cache size: {stats.total_size_bytes / (1024*1024):.1f} MB")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
