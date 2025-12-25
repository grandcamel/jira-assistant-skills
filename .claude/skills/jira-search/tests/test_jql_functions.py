"""
Tests for jql_functions.py - List JQL functions with examples.
"""

import pytest
import json
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestGetFunctions:
    """Tests for fetching JQL functions."""

    def test_get_all_functions(self, mock_jira_client, sample_autocomplete_data):
        """Test fetching all JQL functions."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_functions import get_functions

        functions = get_functions(mock_jira_client)

        assert len(functions) == 6
        assert any(f['value'] == 'currentUser()' for f in functions)
        assert any(f['value'] == 'startOfDay()' for f in functions)
        mock_jira_client.get_jql_autocomplete.assert_called_once()

    def test_filter_functions_by_name(self, mock_jira_client, sample_autocomplete_data):
        """Test filtering functions by name."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_functions import get_functions

        functions = get_functions(mock_jira_client, name_filter='user')

        assert len(functions) == 1
        assert functions[0]['value'] == 'currentUser()'

    def test_get_list_functions(self, mock_jira_client, sample_autocomplete_data):
        """Test functions that return lists (for IN operator)."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_functions import get_functions

        functions = get_functions(mock_jira_client, list_only=True)

        assert len(functions) == 1
        assert functions[0]['value'] == 'membersOf(group)'
        assert functions[0]['isList'] == 'true'

    def test_get_functions_by_type(self, mock_jira_client, sample_autocomplete_data):
        """Test filtering by return type."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_functions import get_functions

        functions = get_functions(mock_jira_client, type_filter='Date')

        # startOfDay, startOfWeek, endOfMonth, now all return Date
        assert len(functions) == 4
        assert all('Date' in str(f.get('types', [])) for f in functions)

    def test_format_with_examples(self, mock_jira_client, sample_autocomplete_data):
        """Test showing usage examples."""
        mock_jira_client.get_jql_autocomplete.return_value = sample_autocomplete_data

        from jql_functions import format_functions_text

        functions = sample_autocomplete_data['visibleFunctionNames']
        output = format_functions_text(functions, show_examples=True)

        assert 'Function' in output
        assert 'currentUser()' in output
        # Examples section should be present
        assert 'Example' in output or 'assignee = currentUser()' in output
