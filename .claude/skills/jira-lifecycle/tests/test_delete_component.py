"""
Tests for delete_component.py - Delete a project component.
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestDeleteComponent:
    """Tests for deleting project components."""

    @patch('delete_component.get_jira_client')
    def test_delete_component_by_id(self, mock_get_client, mock_jira_client):
        """Test deleting a component by ID."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.delete_component.return_value = None

        from delete_component import delete_component

        delete_component(component_id='10000', profile=None)

        mock_jira_client.delete_component.assert_called_once_with('10000')

    @patch('delete_component.get_jira_client')
    def test_delete_component_with_confirmation(self, mock_get_client, mock_jira_client, sample_component, monkeypatch):
        """Test deleting component with confirmation prompt."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_component.return_value = sample_component
        mock_jira_client.delete_component.return_value = None

        # Simulate user confirming with 'yes'
        monkeypatch.setattr('builtins.input', lambda _: 'yes')

        from delete_component import delete_component_with_confirmation

        result = delete_component_with_confirmation(
            component_id='10000',
            profile=None
        )

        assert result is True
        mock_jira_client.delete_component.assert_called_once()

    @patch('delete_component.get_jira_client')
    def test_delete_component_cancelled(self, mock_get_client, mock_jira_client, sample_component, monkeypatch):
        """Test cancelling component deletion."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_component.return_value = sample_component

        # Simulate user declining with 'no'
        monkeypatch.setattr('builtins.input', lambda _: 'no')

        from delete_component import delete_component_with_confirmation

        result = delete_component_with_confirmation(
            component_id='10000',
            profile=None
        )

        assert result is False
        mock_jira_client.delete_component.assert_not_called()

    @patch('delete_component.get_jira_client')
    def test_delete_component_move_issues(self, mock_get_client, mock_jira_client):
        """Test deleting component with move-to option."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.delete_component.return_value = None

        from delete_component import delete_component

        delete_component(
            component_id='10000',
            move_issues_to='10001',
            profile=None
        )

        call_args = mock_jira_client.delete_component.call_args
        assert call_args[0][0] == '10000'
        assert call_args[1].get('moveIssuesTo') == '10001'

    @patch('delete_component.get_jira_client')
    def test_delete_component_dry_run(self, mock_get_client, mock_jira_client, sample_component):
        """Test dry-run mode shows what would be deleted."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.get_component.return_value = sample_component

        from delete_component import delete_component_dry_run

        result = delete_component_dry_run(
            component_id='10000',
            profile=None
        )

        # Dry run should return component info without deleting
        assert result['id'] == '10000'
        assert result['name'] == 'Backend API'
        mock_jira_client.delete_component.assert_not_called()

    @patch('delete_component.get_jira_client')
    def test_delete_component_skip_confirmation(self, mock_get_client, mock_jira_client):
        """Test deleting component with --yes flag (skip confirmation)."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.delete_component.return_value = None

        from delete_component import delete_component

        # Should not prompt, should delete directly
        delete_component(component_id='10000', profile=None)

        mock_jira_client.delete_component.assert_called_once()
