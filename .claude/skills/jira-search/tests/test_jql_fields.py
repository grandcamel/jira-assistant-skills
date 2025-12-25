"""
Tests for jql_fields.py - List JQL searchable fields and operators.
"""

import pytest
import json
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestGetAllFields:
    """Tests for fetching all searchable fields."""

    def test_get_all_fields(self, mock_jira_client, sample_autocomplete_data):
        """Test fetching all searchable fields."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_fields import get_fields

        fields = get_fields(mock_jira_client)

        assert len(fields) == 7
        assert any(f['value'] == 'assignee' for f in fields)
        assert any(f['value'] == 'status' for f in fields)
        mock_jira_client.get_jql_autocomplete.assert_called_once()

    def test_filter_fields_by_name(self, mock_jira_client, sample_autocomplete_data):
        """Test filtering fields by name pattern."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_fields import get_fields

        fields = get_fields(mock_jira_client, name_filter='status')

        assert len(fields) == 1
        assert fields[0]['value'] == 'status'

    def test_get_custom_fields_only(self, mock_jira_client, sample_autocomplete_data):
        """Test filtering to only custom fields."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_fields import get_fields

        fields = get_fields(mock_jira_client, custom_only=True)

        assert len(fields) == 1
        assert fields[0]['value'] == 'customfield_10016'
        assert fields[0]['cfid'] == '10016'

    def test_get_system_fields_only(self, mock_jira_client, sample_autocomplete_data):
        """Test filtering to only system fields."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_fields import get_fields

        fields = get_fields(mock_jira_client, system_only=True)

        assert len(fields) == 6
        assert all(f['cfid'] is None for f in fields)

    def test_format_text_output(self, mock_jira_client, sample_autocomplete_data, capsys):
        """Test human-readable table output."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_fields import format_fields_text

        fields = sample_autocomplete_data['visibleFieldNames']
        output = format_fields_text(fields)

        assert 'Field' in output
        assert 'Display Name' in output
        assert 'Operators' in output
        assert 'assignee' in output
        assert 'Assignee' in output

    def test_format_json_output(self, mock_jira_client, sample_autocomplete_data):
        """Test JSON output format."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_fields import format_fields_json

        fields = sample_autocomplete_data['visibleFieldNames']
        output = format_fields_json(fields)

        # Should be valid JSON
        parsed = json.loads(output)
        assert isinstance(parsed, list)
        assert len(parsed) == 7
        assert parsed[0]['value'] == 'assignee'
