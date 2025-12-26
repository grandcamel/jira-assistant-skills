"""
Tests for bulk_transition.py - TDD approach.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, call
import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared' / 'scripts' / 'lib'))


class TestBulkTransitionByKeys:
    """Test transitioning multiple issues by key list."""

    def test_bulk_transition_by_keys_success(self, mock_jira_client, sample_issues, sample_transitions):
        """Test transitioning multiple issues by key list."""
        from bulk_transition import bulk_transition

        # Setup mock
        mock_jira_client.get_transitions.return_value = sample_transitions
        mock_jira_client.transition_issue.return_value = None

        # Execute
        result = bulk_transition(
            client=mock_jira_client,
            issue_keys=['PROJ-1', 'PROJ-2', 'PROJ-3'],
            target_status='Done',
            dry_run=False
        )

        # Verify
        assert result['success'] == 3
        assert result['failed'] == 0
        assert mock_jira_client.get_transitions.call_count == 3
        assert mock_jira_client.transition_issue.call_count == 3


class TestBulkTransitionByJql:
    """Test transitioning all issues matching JQL query."""

    def test_bulk_transition_by_jql_success(self, mock_jira_client, sample_issues, sample_transitions):
        """Test transitioning all issues matching JQL query."""
        from bulk_transition import bulk_transition

        # Setup mock
        mock_jira_client.search_issues.return_value = {
            'issues': sample_issues,
            'total': 3
        }
        mock_jira_client.get_transitions.return_value = sample_transitions
        mock_jira_client.transition_issue.return_value = None

        # Execute
        result = bulk_transition(
            client=mock_jira_client,
            jql="project=PROJ AND status='In Progress'",
            target_status='Done',
            dry_run=False
        )

        # Verify
        assert result['success'] == 3
        assert result['failed'] == 0
        mock_jira_client.search_issues.assert_called_once()


class TestBulkTransitionWithResolution:
    """Test setting resolution during transition."""

    def test_bulk_transition_with_resolution(self, mock_jira_client, sample_transitions):
        """Test setting resolution during transition."""
        from bulk_transition import bulk_transition

        # Setup mock
        mock_jira_client.get_transitions.return_value = sample_transitions
        mock_jira_client.transition_issue.return_value = None

        # Execute
        result = bulk_transition(
            client=mock_jira_client,
            issue_keys=['PROJ-1'],
            target_status='Done',
            resolution='Fixed',
            dry_run=False
        )

        # Verify resolution was passed
        assert result['success'] == 1
        call_args = mock_jira_client.transition_issue.call_args
        assert 'resolution' in call_args[1].get('fields', {}) or \
               'resolution' in (call_args[0][2] if len(call_args[0]) > 2 else {})


class TestBulkTransitionWithComment:
    """Test adding comment during transition."""

    def test_bulk_transition_with_comment(self, mock_jira_client, sample_transitions):
        """Test adding comment during transition."""
        from bulk_transition import bulk_transition

        # Setup mock
        mock_jira_client.get_transitions.return_value = sample_transitions
        mock_jira_client.transition_issue.return_value = None

        # Execute
        result = bulk_transition(
            client=mock_jira_client,
            issue_keys=['PROJ-1'],
            target_status='Done',
            comment='Bulk transition complete',
            dry_run=False
        )

        # Verify
        assert result['success'] == 1


class TestBulkTransitionDryRun:
    """Test dry-run mode shows preview without changes."""

    def test_bulk_transition_dry_run(self, mock_jira_client, sample_issues, sample_transitions):
        """Test dry-run mode shows preview without changes."""
        from bulk_transition import bulk_transition

        # Setup mock
        mock_jira_client.search_issues.return_value = {
            'issues': sample_issues,
            'total': 3
        }
        mock_jira_client.get_transitions.return_value = sample_transitions

        # Execute
        result = bulk_transition(
            client=mock_jira_client,
            jql="project=PROJ",
            target_status='Done',
            dry_run=True
        )

        # Verify no actual transitions made
        assert result['success'] == 0
        assert result['would_process'] == 3
        mock_jira_client.transition_issue.assert_not_called()


class TestBulkTransitionRateLimiting:
    """Test rate limiting and throttling."""

    def test_bulk_transition_respects_rate_limit(self, mock_jira_client, sample_transitions):
        """Test rate limiting delays between operations."""
        from bulk_transition import bulk_transition
        import time

        # Setup mock
        mock_jira_client.get_transitions.return_value = sample_transitions
        mock_jira_client.transition_issue.return_value = None

        # Execute with many issues
        issue_keys = [f'PROJ-{i}' for i in range(10)]
        start_time = time.time()

        result = bulk_transition(
            client=mock_jira_client,
            issue_keys=issue_keys,
            target_status='Done',
            dry_run=False,
            delay_between_ops=0.01  # Small delay for testing
        )

        elapsed = time.time() - start_time

        # Verify some delay occurred (at least 9 delays of 0.01s)
        assert result['success'] == 10
        assert elapsed >= 0.05  # At least some delay


class TestBulkTransitionPartialFailure:
    """Test handling when some issues fail to transition."""

    def test_bulk_transition_partial_failure(self, mock_jira_client, sample_transitions):
        """Test handling when some issues fail to transition."""
        from bulk_transition import bulk_transition
        from error_handler import JiraError

        # Setup mock - fail on second issue
        mock_jira_client.get_transitions.return_value = sample_transitions

        def transition_side_effect(issue_key, transition_id, fields=None):
            if issue_key == 'PROJ-2':
                raise JiraError("Permission denied for PROJ-2")
            return None

        mock_jira_client.transition_issue.side_effect = transition_side_effect

        # Execute
        result = bulk_transition(
            client=mock_jira_client,
            issue_keys=['PROJ-1', 'PROJ-2', 'PROJ-3'],
            target_status='Done',
            dry_run=False
        )

        # Verify partial success
        assert result['success'] == 2
        assert result['failed'] == 1
        assert 'PROJ-2' in result['errors']


class TestBulkTransitionInvalidTransition:
    """Test error when transition not available for issue status."""

    def test_bulk_transition_invalid_transition(self, mock_jira_client):
        """Test error when transition not available for issue status."""
        from bulk_transition import bulk_transition

        # Setup mock - no matching transition
        mock_jira_client.get_transitions.return_value = [
            {'id': '21', 'name': 'In Progress', 'to': {'name': 'In Progress'}}
        ]

        # Execute - trying to transition to 'Done' which isn't available
        result = bulk_transition(
            client=mock_jira_client,
            issue_keys=['PROJ-1'],
            target_status='Done',
            dry_run=False
        )

        # Verify failure due to invalid transition
        assert result['success'] == 0
        assert result['failed'] == 1
        assert 'PROJ-1' in result['errors']


class TestBulkTransitionProgressCallback:
    """Test progress reporting during operation."""

    def test_bulk_transition_progress_callback(self, mock_jira_client, sample_transitions):
        """Test progress reporting during operation."""
        from bulk_transition import bulk_transition

        # Setup mock
        mock_jira_client.get_transitions.return_value = sample_transitions
        mock_jira_client.transition_issue.return_value = None

        # Track progress calls
        progress_calls = []

        def progress_callback(current, total, issue_key, status):
            progress_calls.append({
                'current': current,
                'total': total,
                'issue_key': issue_key,
                'status': status
            })

        # Execute
        result = bulk_transition(
            client=mock_jira_client,
            issue_keys=['PROJ-1', 'PROJ-2', 'PROJ-3'],
            target_status='Done',
            dry_run=False,
            progress_callback=progress_callback
        )

        # Verify progress was reported
        assert len(progress_calls) == 3
        assert progress_calls[0]['current'] == 1
        assert progress_calls[2]['current'] == 3


class TestBulkTransitionNoIssuesFound:
    """Test when no issues match the criteria."""

    def test_bulk_transition_no_issues(self, mock_jira_client):
        """Test when no issues are found."""
        from bulk_transition import bulk_transition

        # Setup mock - empty results
        mock_jira_client.search_issues.return_value = {
            'issues': [],
            'total': 0
        }

        # Execute
        result = bulk_transition(
            client=mock_jira_client,
            jql="project=NONEXISTENT",
            target_status='Done',
            dry_run=False
        )

        # Verify
        assert result['success'] == 0
        assert result['failed'] == 0
        assert result['total'] == 0


class TestBulkTransitionMaxIssues:
    """Test respecting max_issues limit."""

    def test_bulk_transition_max_issues_limit(self, mock_jira_client, sample_issues, sample_transitions):
        """Test respecting max_issues limit."""
        from bulk_transition import bulk_transition

        # Setup mock - return only 2 issues (simulating API respecting maxResults)
        # The implementation passes max_issues to search_issues, which returns limited results
        mock_jira_client.search_issues.return_value = {
            'issues': sample_issues[:2],  # Only 2 issues returned by API
            'total': 100  # Total is higher
        }
        mock_jira_client.get_transitions.return_value = sample_transitions
        mock_jira_client.transition_issue.return_value = None

        # Execute with limit
        result = bulk_transition(
            client=mock_jira_client,
            jql="project=PROJ",
            target_status='Done',
            dry_run=False,
            max_issues=2
        )

        # Verify only 2 were processed
        assert result['success'] == 2
        assert mock_jira_client.transition_issue.call_count == 2
        # Verify search was called with max_results
        mock_jira_client.search_issues.assert_called_once()
