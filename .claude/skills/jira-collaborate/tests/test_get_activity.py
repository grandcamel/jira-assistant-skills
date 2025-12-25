"""
Tests for get_activity.py - Get issue activity/changelog.
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestGetActivity:
    """Tests for getting issue activity/changelog."""

    @patch('get_activity.get_jira_client')
    def test_get_all_activity(self, mock_get_client, mock_jira_client, sample_changelog):
        """Test getting all activity for an issue."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_changelog.return_value = sample_changelog

        from get_activity import get_activity

        result = get_activity('PROJ-123', profile=None)

        assert result['total'] == 3
        assert len(result['values']) == 3
        mock_jira_client.get_changelog.assert_called_once()

    @patch('get_activity.get_jira_client')
    def test_activity_pagination(self, mock_get_client, mock_jira_client, sample_changelog):
        """Test pagination of activity."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_changelog.return_value = sample_changelog

        from get_activity import get_activity

        result = get_activity('PROJ-123', limit=2, offset=1, profile=None)

        call_args = mock_jira_client.get_changelog.call_args
        assert call_args[1]['max_results'] == 2
        assert call_args[1]['start_at'] == 1

    @patch('get_activity.get_jira_client')
    def test_parse_status_change(self, mock_get_client, mock_jira_client, sample_changelog):
        """Test parsing status change in activity."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_changelog.return_value = sample_changelog

        from get_activity import parse_changelog

        parsed = parse_changelog(sample_changelog)

        # First change is status change
        status_change = parsed[0]
        assert status_change['type'] == 'status'
        assert status_change['field'] == 'status'
        assert status_change['from'] == 'To Do'
        assert status_change['to'] == 'In Progress'

    @patch('get_activity.get_jira_client')
    def test_parse_assignee_change(self, mock_get_client, mock_jira_client, sample_changelog):
        """Test parsing assignee change in activity."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_changelog.return_value = sample_changelog

        from get_activity import parse_changelog

        parsed = parse_changelog(sample_changelog)

        # Second change is assignee change
        assignee_change = parsed[1]
        assert assignee_change['type'] == 'assignee'
        assert assignee_change['field'] == 'assignee'
        assert assignee_change['from'] == 'Alice Smith'
        assert assignee_change['to'] == 'Bob Jones'

    @patch('get_activity.get_jira_client')
    def test_parse_priority_change(self, mock_get_client, mock_jira_client, sample_changelog):
        """Test parsing priority change in activity."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_changelog.return_value = sample_changelog

        from get_activity import parse_changelog

        parsed = parse_changelog(sample_changelog)

        # Third change is priority change
        priority_change = parsed[2]
        assert priority_change['type'] == 'priority'
        assert priority_change['field'] == 'priority'
        assert priority_change['from'] == 'Medium'
        assert priority_change['to'] == 'High'

    @patch('get_activity.get_jira_client')
    def test_filter_by_change_type(self, mock_get_client, mock_jira_client, sample_changelog):
        """Test filtering activity by change type."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_changelog.return_value = sample_changelog

        from get_activity import get_activity, parse_changelog

        result = get_activity('PROJ-123', profile=None)
        parsed = parse_changelog(result)

        # Filter only status changes
        status_changes = [c for c in parsed if c['type'] == 'status']
        assert len(status_changes) == 1
        assert status_changes[0]['field'] == 'status'

    @patch('get_activity.get_jira_client')
    def test_activity_table_output(self, mock_get_client, mock_jira_client, sample_changelog, capsys):
        """Test table output format for activity."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_changelog.return_value = sample_changelog

        from get_activity import display_activity_table, parse_changelog

        parsed = parse_changelog(sample_changelog)
        display_activity_table(parsed)

        captured = capsys.readouterr()
        assert 'status' in captured.out
        assert 'To Do' in captured.out
        assert 'In Progress' in captured.out

    @patch('get_activity.get_jira_client')
    def test_activity_json_output(self, mock_get_client, mock_jira_client, sample_changelog):
        """Test JSON output format for activity."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_changelog.return_value = sample_changelog

        from get_activity import parse_changelog
        import json

        parsed = parse_changelog(sample_changelog)
        json_output = json.dumps(parsed, indent=2)

        # Should be valid JSON
        parsed_json = json.loads(json_output)
        assert len(parsed_json) == 3
        assert parsed_json[0]['field'] == 'status'
