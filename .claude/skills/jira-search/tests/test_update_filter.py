"""
Tests for update_filter.py - Update saved filters.
"""

import pytest
import json
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestUpdateFilter:
    """Tests for updating filters."""

    def test_update_filter_name(self, mock_jira_client, sample_filter):
        """Test updating filter name."""
        sample_filter['name'] = 'My Open Bugs'
        mock_jira_client.update_filter.return_value = sample_filter

        from update_filter import update_filter

        result = update_filter(mock_jira_client, '10042', name='My Open Bugs')

        assert result['name'] == 'My Open Bugs'
        mock_jira_client.update_filter.assert_called_once()

    def test_update_filter_jql(self, mock_jira_client, sample_filter):
        """Test updating filter JQL."""
        new_jql = 'project = PROJ AND type = Bug AND status != Done'
        sample_filter['jql'] = new_jql
        mock_jira_client.update_filter.return_value = sample_filter

        from update_filter import update_filter

        result = update_filter(mock_jira_client, '10042', jql=new_jql)

        assert result['jql'] == new_jql

    def test_update_filter_description(self, mock_jira_client, sample_filter):
        """Test updating filter description."""
        sample_filter['description'] = 'Updated description'
        mock_jira_client.update_filter.return_value = sample_filter

        from update_filter import update_filter

        result = update_filter(mock_jira_client, '10042',
                              description='Updated description')

        assert result['description'] == 'Updated description'

    def test_update_multiple_fields(self, mock_jira_client, sample_filter):
        """Test updating multiple fields at once."""
        sample_filter['name'] = 'New Name'
        sample_filter['jql'] = 'project = TEST'
        mock_jira_client.update_filter.return_value = sample_filter

        from update_filter import update_filter

        result = update_filter(
            mock_jira_client, '10042',
            name='New Name',
            jql='project = TEST'
        )

        assert result['name'] == 'New Name'
        assert result['jql'] == 'project = TEST'

    def test_update_not_owner(self, mock_jira_client):
        """Test error when not filter owner."""
        from error_handler import PermissionError
        mock_jira_client.update_filter.side_effect = PermissionError(
            "You are not the owner of this filter"
        )

        from update_filter import update_filter

        with pytest.raises(PermissionError):
            update_filter(mock_jira_client, '10042', name='New Name')

    def test_update_filter_not_found(self, mock_jira_client):
        """Test error when filter doesn't exist."""
        from error_handler import NotFoundError
        mock_jira_client.update_filter.side_effect = NotFoundError(
            "Filter 99999 not found"
        )

        from update_filter import update_filter

        with pytest.raises(NotFoundError):
            update_filter(mock_jira_client, '99999', name='New Name')

    def test_validate_new_jql(self, mock_jira_client, sample_filter):
        """Test JQL validation on update."""
        # If JQL is invalid, JIRA returns an error
        from error_handler import ValidationError
        mock_jira_client.update_filter.side_effect = ValidationError(
            "JQL parse error"
        )

        from update_filter import update_filter

        with pytest.raises(ValidationError):
            update_filter(mock_jira_client, '10042', jql='invalid jql syntax')
