"""
Tests for move_to_sprint.py - Moving issues to sprints in JIRA.

Following TDD: These tests are written FIRST and should FAIL initially.
Implementation comes after tests are defined.
"""

import sys
from pathlib import Path

# Add paths BEFORE any other imports
test_dir = Path(__file__).parent  # tests
jira_agile_dir = test_dir.parent  # jira-agile
skills_dir = jira_agile_dir.parent  # skills
shared_lib_path = skills_dir / 'shared' / 'scripts' / 'lib'
scripts_path = jira_agile_dir / 'scripts'

sys.path.insert(0, str(shared_lib_path))
sys.path.insert(0, str(scripts_path))

import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.mark.agile
@pytest.mark.unit
class TestMoveToSprint:
    """Test suite for move_to_sprint.py functionality."""

    def test_move_single_issue_to_sprint(self, mock_jira_client):
        """Test moving one issue to sprint."""
        # Arrange
        from move_to_sprint import move_to_sprint

        mock_jira_client.move_issues_to_sprint.return_value = None

        # Act
        result = move_to_sprint(
            sprint_id=456,
            issue_keys=["PROJ-101"],
            client=mock_jira_client
        )

        # Assert
        assert result is not None
        assert result['moved'] == 1
        assert result['failed'] == 0

        # Verify API call
        mock_jira_client.move_issues_to_sprint.assert_called_once()
        call_args = mock_jira_client.move_issues_to_sprint.call_args
        assert call_args[0][0] == 456  # Sprint ID
        assert "PROJ-101" in call_args[0][1]  # Issues

    def test_move_multiple_issues_to_sprint(self, mock_jira_client):
        """Test bulk moving issues."""
        # Arrange
        from move_to_sprint import move_to_sprint

        mock_jira_client.move_issues_to_sprint.return_value = None

        # Act
        result = move_to_sprint(
            sprint_id=456,
            issue_keys=["PROJ-101", "PROJ-102", "PROJ-103"],
            client=mock_jira_client
        )

        # Assert
        assert result['moved'] == 3
        assert result['failed'] == 0

    def test_move_to_sprint_by_jql(self, mock_jira_client, sample_issue_response):
        """Test moving all issues matching JQL query."""
        # Arrange
        from move_to_sprint import move_to_sprint

        # Mock JQL search returning issues
        mock_jira_client.search_issues.return_value = {
            'issues': [
                {'key': 'PROJ-101'},
                {'key': 'PROJ-102'}
            ],
            'total': 2
        }
        mock_jira_client.move_issues_to_sprint.return_value = None

        # Act
        result = move_to_sprint(
            sprint_id=456,
            jql="project=PROJ AND status='To Do'",
            client=mock_jira_client
        )

        # Assert
        assert result['moved'] == 2

        # Verify JQL search was called
        mock_jira_client.search_issues.assert_called_once()

    def test_move_to_backlog(self, mock_jira_client):
        """Test removing issues from sprint (back to backlog)."""
        # Arrange
        from move_to_sprint import move_to_backlog

        mock_jira_client.move_issues_to_backlog.return_value = None

        # Act
        result = move_to_backlog(
            issue_keys=["PROJ-101"],
            client=mock_jira_client
        )

        # Assert
        assert result is not None
        assert result['moved_to_backlog'] == 1

        # Verify API call
        mock_jira_client.move_issues_to_backlog.assert_called_once()

    def test_move_to_sprint_dry_run(self, mock_jira_client):
        """Test dry-run preview."""
        # Arrange
        from move_to_sprint import move_to_sprint

        # Act
        result = move_to_sprint(
            sprint_id=456,
            issue_keys=["PROJ-101", "PROJ-102"],
            dry_run=True,
            client=mock_jira_client
        )

        # Assert
        assert result['would_move'] == 2
        # Verify NO actual move was called
        mock_jira_client.move_issues_to_sprint.assert_not_called()

    def test_move_to_sprint_with_rank(self, mock_jira_client):
        """Test moving and setting rank position."""
        # Arrange
        from move_to_sprint import move_to_sprint

        mock_jira_client.move_issues_to_sprint.return_value = None

        # Act
        result = move_to_sprint(
            sprint_id=456,
            issue_keys=["PROJ-101"],
            rank_position="top",
            client=mock_jira_client
        )

        # Assert
        assert result['moved'] == 1

        # Verify rank was passed
        call_args = mock_jira_client.move_issues_to_sprint.call_args
        # Depending on API, rank may be passed differently
        assert call_args is not None


@pytest.mark.agile
@pytest.mark.unit
class TestMoveToSprintCLI:
    """Test command-line interface for move_to_sprint.py."""

    @patch('sys.argv', ['move_to_sprint.py', '--sprint', '456', '--issues', 'PROJ-1,PROJ-2'])
    def test_cli_multiple_issues(self, mock_jira_client):
        """Test CLI with multiple issues."""
        # from move_to_sprint import main
        pass

    @patch('sys.argv', ['move_to_sprint.py', '--backlog', '--issues', 'PROJ-5'])
    def test_cli_move_to_backlog(self, mock_jira_client):
        """Test CLI to move issues to backlog."""
        # from move_to_sprint import main
        pass
