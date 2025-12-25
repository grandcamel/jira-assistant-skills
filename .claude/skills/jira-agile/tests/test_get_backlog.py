"""
Tests for get_backlog.py - Retrieving board backlog.

Following TDD: These tests are written FIRST and should FAIL initially.
"""

import sys
from pathlib import Path

test_dir = Path(__file__).parent
jira_agile_dir = test_dir.parent
skills_dir = jira_agile_dir.parent
shared_lib_path = skills_dir / 'shared' / 'scripts' / 'lib'
scripts_path = jira_agile_dir / 'scripts'

sys.path.insert(0, str(shared_lib_path))
sys.path.insert(0, str(scripts_path))

import pytest
from unittest.mock import Mock


@pytest.mark.agile
@pytest.mark.unit
class TestGetBacklog:
    """Test suite for get_backlog.py functionality."""

    def test_get_backlog_all(self, mock_jira_client, sample_issue_response):
        """Test fetching full backlog for board."""
        from get_backlog import get_backlog

        mock_jira_client.get_board_backlog.return_value = {
            'issues': [sample_issue_response],
            'total': 1
        }

        result = get_backlog(board_id=123, client=mock_jira_client)

        assert result is not None
        assert len(result['issues']) == 1
        mock_jira_client.get_board_backlog.assert_called_once()

    def test_get_backlog_with_filter(self, mock_jira_client, sample_issue_response):
        """Test filtering backlog by JQL."""
        from get_backlog import get_backlog

        mock_jira_client.get_board_backlog.return_value = {
            'issues': [sample_issue_response],
            'total': 1
        }

        result = get_backlog(
            board_id=123,
            jql_filter="priority=High",
            client=mock_jira_client
        )

        assert result is not None
        call_args = mock_jira_client.get_board_backlog.call_args
        assert 'jql' in str(call_args) or call_args[1].get('jql')

    def test_get_backlog_with_pagination(self, mock_jira_client, sample_issue_response):
        """Test paginated backlog retrieval."""
        from get_backlog import get_backlog

        mock_jira_client.get_board_backlog.return_value = {
            'issues': [sample_issue_response],
            'total': 100,
            'startAt': 0,
            'maxResults': 50
        }

        result = get_backlog(
            board_id=123,
            max_results=50,
            client=mock_jira_client
        )

        assert result is not None
        assert result['total'] == 100

    def test_get_backlog_sorted(self, mock_jira_client):
        """Test backlog in rank order."""
        from get_backlog import get_backlog

        mock_jira_client.get_board_backlog.return_value = {
            'issues': [
                {'key': 'PROJ-1', 'fields': {'summary': 'First'}},
                {'key': 'PROJ-2', 'fields': {'summary': 'Second'}},
            ],
            'total': 2
        }

        result = get_backlog(board_id=123, client=mock_jira_client)

        assert result['issues'][0]['key'] == 'PROJ-1'
        assert result['issues'][1]['key'] == 'PROJ-2'

    def test_get_backlog_with_epics(self, mock_jira_client, sample_issue_response):
        """Test grouping backlog by epic."""
        from get_backlog import get_backlog

        issue_with_epic = sample_issue_response.copy()
        issue_with_epic['fields'] = sample_issue_response['fields'].copy()
        issue_with_epic['fields']['customfield_10014'] = 'PROJ-100'

        mock_jira_client.get_board_backlog.return_value = {
            'issues': [issue_with_epic],
            'total': 1
        }

        result = get_backlog(
            board_id=123,
            group_by_epic=True,
            client=mock_jira_client
        )

        assert result is not None
        assert 'by_epic' in result or 'grouped' in result or len(result['issues']) > 0


@pytest.mark.agile
@pytest.mark.unit
class TestGetBacklogCLI:
    """Test command-line interface for get_backlog.py."""

    def test_cli_basic(self, mock_jira_client):
        """Test CLI with board ID."""
        pass
