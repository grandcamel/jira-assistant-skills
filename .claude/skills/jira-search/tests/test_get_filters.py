"""
Tests for get_filters.py - List and search filters.
"""

import pytest
import json
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestGetFilters:
    """Tests for getting and searching filters."""

    def test_get_my_filters(self, mock_jira_client, sample_filter_list):
        """Test fetching user's own filters."""
        mock_jira_client.get_my_filters.return_value = sample_filter_list

        from get_filters import get_my_filters

        filters = get_my_filters(mock_jira_client)

        assert len(filters) == 3
        assert filters[0]['id'] == '10042'
        mock_jira_client.get_my_filters.assert_called_once()

    def test_get_favourite_filters(self, mock_jira_client, sample_filter_list):
        """Test fetching favourite filters."""
        favourites = [f for f in sample_filter_list if f.get('favourite')]
        mock_jira_client.get_favourite_filters.return_value = favourites

        from get_filters import get_favourite_filters

        filters = get_favourite_filters(mock_jira_client)

        assert len(filters) == 2
        assert all(f.get('favourite') for f in filters)
        mock_jira_client.get_favourite_filters.assert_called_once()

    def test_search_filters_by_name(self, mock_jira_client, sample_filter_search_response):
        """Test searching filters by name."""
        mock_jira_client.search_filters.return_value = sample_filter_search_response

        from get_filters import search_filters

        result = search_filters(mock_jira_client, filter_name='bugs')

        assert len(result['values']) == 2
        mock_jira_client.search_filters.assert_called_once()

    def test_search_filters_by_owner(self, mock_jira_client, sample_filter_search_response):
        """Test filtering by owner account ID."""
        mock_jira_client.search_filters.return_value = sample_filter_search_response

        from get_filters import search_filters

        result = search_filters(mock_jira_client, account_id='5b10a2844c20165700ede21g')

        assert len(result['values']) == 2

    def test_search_filters_by_project(self, mock_jira_client, sample_filter_search_response):
        """Test filtering by project."""
        mock_jira_client.search_filters.return_value = sample_filter_search_response

        from get_filters import search_filters

        result = search_filters(mock_jira_client, project_key='PROJ')

        mock_jira_client.search_filters.assert_called_once()

    def test_get_filter_by_id(self, mock_jira_client, sample_filter):
        """Test fetching specific filter by ID."""
        mock_jira_client.get_filter.return_value = sample_filter

        from get_filters import get_filter_by_id

        filter_data = get_filter_by_id(mock_jira_client, '10042')

        assert filter_data['id'] == '10042'
        assert filter_data['name'] == 'My Bugs'
        mock_jira_client.get_filter.assert_called_once_with('10042', expand=None)

    def test_format_text_output(self, mock_jira_client, sample_filter_list):
        """Test table output with filter details."""
        from get_filters import format_filters_text

        output = format_filters_text(sample_filter_list)

        assert 'ID' in output
        assert 'Name' in output
        assert '10042' in output
        assert 'My Bugs' in output

    def test_format_json_output(self, mock_jira_client, sample_filter_list):
        """Test JSON output."""
        from get_filters import format_filters_json

        output = format_filters_json(sample_filter_list)

        parsed = json.loads(output)
        assert isinstance(parsed, list)
        assert len(parsed) == 3
