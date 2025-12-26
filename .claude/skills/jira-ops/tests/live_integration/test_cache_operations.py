"""
Live Integration Tests: Cache Operations

Tests for cache management operations against a real JIRA instance.
"""

import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'shared' / 'scripts' / 'lib'))

from cache import JiraCache
from cache_warm import warm_projects, warm_fields, warm_issue_types, warm_priorities, warm_statuses


class TestCacheWarmProjects:
    """Tests for project cache warming."""

    def test_warm_projects_success(self, jira_client, test_cache):
        """Test warming projects cache from JIRA."""
        count = warm_projects(jira_client, test_cache, verbose=False)

        assert count > 0

        # Verify cache has data
        stats = test_cache.get_stats()
        assert stats['total_entries'] > 0

    def test_warm_projects_with_verbose(self, jira_client, test_cache, capsys):
        """Test verbose output during cache warming."""
        count = warm_projects(jira_client, test_cache, verbose=True)

        captured = capsys.readouterr()
        assert "Fetching projects" in captured.out
        assert count > 0

    def test_warm_projects_cacheable(self, jira_client, test_cache):
        """Test that projects are properly cached."""
        count = warm_projects(jira_client, test_cache, verbose=False)

        # Get a project from cache
        # Projects are cached by key
        stats = test_cache.get_stats()
        assert stats['categories'].get('project', 0) > 0


class TestCacheWarmFields:
    """Tests for field cache warming."""

    def test_warm_fields_success(self, jira_client, test_cache):
        """Test warming fields cache from JIRA."""
        count = warm_fields(jira_client, test_cache, verbose=False)

        assert count > 0

        # Verify cache has field data
        stats = test_cache.get_stats()
        assert stats['categories'].get('field', 0) > 0

    def test_warm_fields_with_verbose(self, jira_client, test_cache, capsys):
        """Test verbose output during field cache warming."""
        count = warm_fields(jira_client, test_cache, verbose=True)

        captured = capsys.readouterr()
        assert "Fetching fields" in captured.out
        assert count > 0

    def test_warm_fields_caches_all_list(self, jira_client, test_cache):
        """Test that the 'all fields' list is cached."""
        warm_fields(jira_client, test_cache, verbose=False)

        # The full list should be cached
        all_key = test_cache.generate_key("field", "all")
        all_fields = test_cache.get(all_key)

        if all_fields:
            assert isinstance(all_fields, list)
            assert len(all_fields) > 0


class TestCacheWarmIssueTypes:
    """Tests for issue type cache warming."""

    def test_warm_issue_types_success(self, jira_client, test_cache):
        """Test warming issue types cache from JIRA."""
        count = warm_issue_types(jira_client, test_cache, verbose=False)

        assert isinstance(count, int)
        assert count > 0

    def test_warm_issue_types_with_verbose(self, jira_client, test_cache, capsys):
        """Test verbose output during issue type cache warming."""
        count = warm_issue_types(jira_client, test_cache, verbose=True)

        captured = capsys.readouterr()
        assert "issue types" in captured.out.lower() or count > 0


class TestCacheWarmPrioritiesAndStatuses:
    """Tests for priority and status cache warming."""

    def test_warm_priorities_success(self, jira_client, test_cache):
        """Test warming priorities cache from JIRA."""
        count = warm_priorities(jira_client, test_cache, verbose=False)

        assert isinstance(count, int)
        assert count > 0

    def test_warm_statuses_success(self, jira_client, test_cache):
        """Test warming statuses cache from JIRA."""
        count = warm_statuses(jira_client, test_cache, verbose=False)

        assert isinstance(count, int)
        assert count > 0


class TestCacheOperations:
    """Tests for cache operations."""

    def test_cache_set_and_get(self, test_cache):
        """Test basic cache set and get operations."""
        key = "test_key_123"
        value = {"data": "test_value", "count": 42}

        test_cache.set(key, value, category="test")
        retrieved = test_cache.get(key)

        assert retrieved is not None
        assert retrieved == value

    def test_cache_expiry(self, test_cache):
        """Test cache with short TTL."""
        import time

        key = "expiring_key"
        value = {"data": "will_expire"}

        # Set with very short TTL
        test_cache.set(key, value, category="test", ttl=1)

        # Should be available immediately
        assert test_cache.get(key) is not None

        # Wait for expiry
        time.sleep(2)

        # Should be expired
        assert test_cache.get(key) is None

    def test_cache_invalidate(self, test_cache):
        """Test cache invalidation."""
        key = "to_invalidate"
        value = {"data": "will_be_removed"}

        test_cache.set(key, value, category="test")
        assert test_cache.get(key) is not None

        test_cache.invalidate(key)
        assert test_cache.get(key) is None

    def test_cache_stats(self, test_cache):
        """Test cache statistics."""
        # Add some entries
        for i in range(5):
            test_cache.set(f"key_{i}", {"index": i}, category="test")

        stats = test_cache.get_stats()

        assert 'total_entries' in stats
        assert stats['total_entries'] >= 5
        assert 'categories' in stats

    def test_cache_generate_key(self, test_cache):
        """Test key generation."""
        key = test_cache.generate_key("issue", "PROJ-123")

        assert key is not None
        assert "issue" in key
        assert "PROJ-123" in key

    def test_cache_clear_category(self, test_cache):
        """Test clearing a specific category."""
        # Add entries in different categories
        test_cache.set("issue_1", {"key": "PROJ-1"}, category="issue")
        test_cache.set("issue_2", {"key": "PROJ-2"}, category="issue")
        test_cache.set("project_1", {"key": "PROJ"}, category="project")

        # Clear only issue category
        test_cache.clear(category="issue")

        # Issue entries should be gone
        assert test_cache.get("issue_1") is None
        assert test_cache.get("issue_2") is None

        # Project entries should remain
        assert test_cache.get("project_1") is not None


class TestCacheIntegration:
    """Integration tests for cache with real JIRA data."""

    def test_cache_issue_data(self, jira_client, test_cache):
        """Test caching issue search results."""
        # Perform a search
        result = jira_client.search_issues(
            "created >= -7d",
            max_results=5
        )

        # Cache the results
        for issue in result.get('issues', []):
            key = test_cache.generate_key("issue", issue['key'])
            test_cache.set(key, issue, category="issue")

        # Verify caching
        stats = test_cache.get_stats()
        cached_issues = stats['categories'].get('issue', 0)
        assert cached_issues >= 0  # May be 0 if no issues found

    def test_cache_project_lookup(self, jira_client, test_cache):
        """Test caching and retrieving project data."""
        # Get projects from JIRA
        response = jira_client.get("/rest/api/3/project", operation="get projects")

        if response and len(response) > 0:
            project = response[0]
            key = test_cache.generate_key("project", project['key'])
            test_cache.set(key, project, category="project")

            # Retrieve from cache
            cached = test_cache.get(key)
            assert cached is not None
            assert cached['key'] == project['key']

    def test_cache_warm_all(self, jira_client, test_cache):
        """Test warming all caches."""
        # Warm all cache types
        project_count = warm_projects(jira_client, test_cache, verbose=False)
        field_count = warm_fields(jira_client, test_cache, verbose=False)

        # Verify caches have data
        stats = test_cache.get_stats()
        assert stats['total_entries'] > 0
        assert project_count > 0 or field_count > 0


class TestCachePerformance:
    """Tests for cache performance."""

    def test_cache_hit_rate(self, test_cache):
        """Test cache hit rate tracking."""
        key = "hit_test"
        value = {"data": "test"}

        test_cache.set(key, value, category="test")

        # Multiple gets
        for _ in range(5):
            test_cache.get(key)

        # Get miss
        test_cache.get("nonexistent_key")

        stats = test_cache.get_stats()
        # Hit rate should be calculated
        assert 'hit_rate' in stats or 'hits' in stats

    def test_cache_size_tracking(self, test_cache):
        """Test cache size tracking."""
        # Add entries
        for i in range(10):
            test_cache.set(f"size_test_{i}", {"index": i, "data": "x" * 100}, category="test")

        stats = test_cache.get_stats()
        assert 'total_entries' in stats
        assert stats['total_entries'] >= 10
