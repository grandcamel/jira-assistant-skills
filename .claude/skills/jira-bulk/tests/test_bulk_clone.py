"""
Tests for bulk_clone.py - TDD approach (Phase 2).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared' / 'scripts' / 'lib'))


class TestBulkCloneBasic:
    """Test cloning multiple issues."""

    def test_bulk_clone_basic(self, mock_jira_client, sample_issues):
        """Test cloning multiple issues."""
        from bulk_clone import bulk_clone

        # Setup mock
        mock_jira_client.get_issue.side_effect = lambda key, **kwargs: next(
            (i for i in sample_issues if i['key'] == key), sample_issues[0]
        )
        mock_jira_client.create_issue.side_effect = [
            {'key': 'PROJ-101', 'id': '10101'},
            {'key': 'PROJ-102', 'id': '10102'},
            {'key': 'PROJ-103', 'id': '10103'},
        ]

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-1', 'PROJ-2', 'PROJ-3'],
            dry_run=False
        )

        # Verify
        assert result['success'] == 3
        assert result['failed'] == 0
        assert len(result['created_issues']) == 3


class TestBulkCloneWithSubtasks:
    """Test including subtasks in clone."""

    def test_bulk_clone_with_subtasks(self, mock_jira_client, sample_issue_with_subtasks):
        """Test including subtasks in clone."""
        from bulk_clone import bulk_clone

        # Setup mock
        mock_jira_client.get_issue.return_value = sample_issue_with_subtasks
        mock_jira_client.create_issue.side_effect = [
            {'key': 'PROJ-101', 'id': '10101'},  # Parent clone
            {'key': 'PROJ-102', 'id': '10102'},  # Subtask 1 clone
            {'key': 'PROJ-103', 'id': '10103'},  # Subtask 2 clone
        ]

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-1'],
            include_subtasks=True,
            dry_run=False
        )

        # Verify parent and subtasks were created
        assert result['success'] == 1
        assert mock_jira_client.create_issue.call_count >= 1


class TestBulkCloneWithLinks:
    """Test copying issue links."""

    def test_bulk_clone_with_links(self, mock_jira_client, sample_issue_with_subtasks):
        """Test copying issue links."""
        from bulk_clone import bulk_clone

        # Setup mock
        mock_jira_client.get_issue.return_value = sample_issue_with_subtasks
        mock_jira_client.create_issue.return_value = {'key': 'PROJ-101', 'id': '10101'}
        mock_jira_client.post.return_value = {}  # For link creation

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-1'],
            include_links=True,
            dry_run=False
        )

        # Verify
        assert result['success'] == 1


class TestBulkCloneWithPrefix:
    """Test adding prefix to cloned summaries."""

    def test_bulk_clone_with_prefix(self, mock_jira_client, sample_issues):
        """Test adding prefix to cloned summaries."""
        from bulk_clone import bulk_clone

        # Setup mock
        mock_jira_client.get_issue.return_value = sample_issues[0]
        mock_jira_client.create_issue.return_value = {'key': 'PROJ-101', 'id': '10101'}

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-1'],
            prefix='[Clone]',
            dry_run=False
        )

        # Verify prefix was added
        call_args = mock_jira_client.create_issue.call_args
        fields = call_args[0][0] if call_args[0] else call_args[1].get('fields', {})
        assert '[Clone]' in fields.get('summary', '')


class TestBulkCloneToProject:
    """Test cloning to different project."""

    def test_bulk_clone_to_project(self, mock_jira_client, sample_issues):
        """Test cloning to different project."""
        from bulk_clone import bulk_clone

        # Setup mock
        mock_jira_client.get_issue.return_value = sample_issues[0]
        mock_jira_client.create_issue.return_value = {'key': 'NEWPROJ-1', 'id': '20001'}

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-1'],
            target_project='NEWPROJ',
            dry_run=False
        )

        # Verify project was changed
        call_args = mock_jira_client.create_issue.call_args
        fields = call_args[0][0] if call_args[0] else call_args[1].get('fields', {})
        assert fields.get('project', {}).get('key') == 'NEWPROJ'


class TestBulkCloneStripValues:
    """Test stripping certain fields (status, assignee)."""

    def test_bulk_clone_strip_values(self, mock_jira_client, sample_issues):
        """Test stripping certain fields (status, assignee)."""
        from bulk_clone import bulk_clone

        # Setup mock - issue has assignee
        issue = sample_issues[1].copy()  # Has assignee
        mock_jira_client.get_issue.return_value = issue
        mock_jira_client.create_issue.return_value = {'key': 'PROJ-101', 'id': '10101'}

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-2'],
            dry_run=False
        )

        # Verify - cloned issue should not have status or assignee
        # (these are reset on new issues)
        call_args = mock_jira_client.create_issue.call_args
        fields = call_args[0][0] if call_args[0] else call_args[1].get('fields', {})
        # Status is not set on create - it uses default
        assert 'status' not in fields


class TestBulkCloneDryRun:
    """Test dry-run preview."""

    def test_bulk_clone_dry_run(self, mock_jira_client, sample_issues):
        """Test dry-run preview doesn't make changes."""
        from bulk_clone import bulk_clone

        # Setup mock
        mock_jira_client.get_issue.side_effect = lambda key, **kwargs: next(
            (i for i in sample_issues if i['key'] == key), sample_issues[0]
        )

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-1', 'PROJ-2'],
            dry_run=True
        )

        # Verify no actual creates made
        assert result['would_create'] == 2
        mock_jira_client.create_issue.assert_not_called()


class TestBulkClonePartialFailure:
    """Test partial failure handling."""

    def test_bulk_clone_partial_failure(self, mock_jira_client, sample_issues):
        """Test partial failure handling."""
        from bulk_clone import bulk_clone
        from error_handler import JiraError

        # Setup mock
        mock_jira_client.get_issue.side_effect = lambda key, **kwargs: next(
            (i for i in sample_issues if i['key'] == key), sample_issues[0]
        )

        def create_side_effect(fields):
            if 'Second' in fields.get('summary', ''):
                raise JiraError("Create failed")
            return {'key': 'PROJ-101', 'id': '10101'}

        mock_jira_client.create_issue.side_effect = create_side_effect

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-1', 'PROJ-2', 'PROJ-3'],
            dry_run=False
        )

        # Verify partial success
        assert result['success'] == 2
        assert result['failed'] == 1


class TestBulkCloneByJql:
    """Test cloning issues from JQL."""

    def test_bulk_clone_by_jql(self, mock_jira_client, sample_issues):
        """Test cloning issues from JQL query."""
        from bulk_clone import bulk_clone

        # Setup mock
        mock_jira_client.search_issues.return_value = {
            'issues': sample_issues,
            'total': 3
        }
        mock_jira_client.get_issue.side_effect = lambda key, **kwargs: next(
            (i for i in sample_issues if i['key'] == key), sample_issues[0]
        )
        mock_jira_client.create_issue.return_value = {'key': 'PROJ-101', 'id': '10101'}

        # Execute
        result = bulk_clone(
            client=mock_jira_client,
            jql="sprint=123",
            dry_run=False
        )

        # Verify
        assert result['success'] == 3
        mock_jira_client.search_issues.assert_called_once()


class TestBulkCloneProgressCallback:
    """Test progress reporting."""

    def test_bulk_clone_progress_callback(self, mock_jira_client, sample_issues):
        """Test progress reporting during operation."""
        from bulk_clone import bulk_clone

        # Setup mock
        mock_jira_client.get_issue.side_effect = lambda key, **kwargs: next(
            (i for i in sample_issues if i['key'] == key), sample_issues[0]
        )
        mock_jira_client.create_issue.return_value = {'key': 'PROJ-101', 'id': '10101'}

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
        result = bulk_clone(
            client=mock_jira_client,
            issue_keys=['PROJ-1', 'PROJ-2'],
            dry_run=False,
            progress_callback=progress_callback
        )

        # Verify progress was reported
        assert len(progress_calls) == 2
