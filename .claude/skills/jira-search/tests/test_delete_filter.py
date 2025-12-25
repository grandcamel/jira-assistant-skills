"""
Tests for delete_filter.py - Delete saved filters.
"""

import pytest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestDeleteFilter:
    """Tests for deleting filters."""

    def test_delete_filter(self, mock_jira_client):
        """Test deleting a filter."""
        mock_jira_client.delete_filter.return_value = None

        from delete_filter import delete_filter

        delete_filter(mock_jira_client, '10042')

        mock_jira_client.delete_filter.assert_called_once_with('10042')

    def test_delete_filter_not_owner(self, mock_jira_client):
        """Test error when not filter owner."""
        from error_handler import PermissionError
        mock_jira_client.delete_filter.side_effect = PermissionError(
            "You are not the owner of this filter"
        )

        from delete_filter import delete_filter

        with pytest.raises(PermissionError):
            delete_filter(mock_jira_client, '10042')

    def test_delete_filter_not_found(self, mock_jira_client):
        """Test error when filter doesn't exist."""
        from error_handler import NotFoundError
        mock_jira_client.delete_filter.side_effect = NotFoundError(
            "Filter 99999 not found"
        )

        from delete_filter import delete_filter

        with pytest.raises(NotFoundError):
            delete_filter(mock_jira_client, '99999')

    def test_delete_with_confirmation(self, mock_jira_client, sample_filter):
        """Test confirmation prompt."""
        mock_jira_client.get_filter.return_value = sample_filter

        from delete_filter import get_filter_info

        filter_info = get_filter_info(mock_jira_client, '10042')

        assert filter_info['name'] == 'My Bugs'
        assert filter_info['jql'] is not None

    def test_delete_dry_run(self, mock_jira_client, sample_filter):
        """Test dry-run mode."""
        mock_jira_client.get_filter.return_value = sample_filter

        from delete_filter import dry_run_delete

        result = dry_run_delete(mock_jira_client, '10042')

        assert 'Would delete filter' in result
        assert '10042' in result
        # delete_filter should NOT be called
        mock_jira_client.delete_filter.assert_not_called()
