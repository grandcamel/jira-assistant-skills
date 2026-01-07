"""
Tests for list_sprints.py - Listing sprints for boards and projects.
"""

import json
import sys
from pathlib import Path

# Add paths BEFORE any other imports
test_dir = Path(__file__).parent  # tests
jira_agile_dir = test_dir.parent  # jira-agile
skills_dir = jira_agile_dir.parent  # skills
shared_lib_path = skills_dir / "shared" / "scripts" / "lib"
scripts_path = jira_agile_dir / "scripts"

sys.path.insert(0, str(shared_lib_path))
sys.path.insert(0, str(scripts_path))

import pytest


@pytest.fixture
def sample_boards_response():
    """Sample JIRA Agile API response for boards list."""
    return {
        "values": [
            {
                "id": 123,
                "self": "https://test.atlassian.net/rest/agile/1.0/board/123",
                "name": "PROJ Scrum Board",
                "type": "scrum",
                "location": {"projectKey": "PROJ", "projectName": "Test Project"},
            },
            {
                "id": 124,
                "self": "https://test.atlassian.net/rest/agile/1.0/board/124",
                "name": "PROJ Kanban Board",
                "type": "kanban",
                "location": {"projectKey": "PROJ", "projectName": "Test Project"},
            },
        ],
        "total": 2,
    }


@pytest.fixture
def sample_sprints_response():
    """Sample JIRA Agile API response for sprints list."""
    return {
        "values": [
            {
                "id": 456,
                "self": "https://test.atlassian.net/rest/agile/1.0/sprint/456",
                "state": "active",
                "name": "Sprint 42",
                "startDate": "2025-01-20T00:00:00.000Z",
                "endDate": "2025-02-03T00:00:00.000Z",
                "originBoardId": 123,
                "goal": "Launch MVP",
            },
            {
                "id": 455,
                "self": "https://test.atlassian.net/rest/agile/1.0/sprint/455",
                "state": "closed",
                "name": "Sprint 41",
                "startDate": "2025-01-06T00:00:00.000Z",
                "endDate": "2025-01-20T00:00:00.000Z",
                "originBoardId": 123,
                "goal": "Complete alpha",
            },
        ],
        "total": 2,
    }


@pytest.mark.agile
@pytest.mark.unit
class TestListSprints:
    """Test suite for list_sprints.py functionality."""

    def test_list_sprints_by_board_id(self, mock_jira_client, sample_sprints_response):
        """Test listing sprints by board ID."""
        # Arrange
        from list_sprints import list_sprints

        mock_jira_client.get_board_sprints.return_value = sample_sprints_response

        # Act
        result = list_sprints(board_id=123, client=mock_jira_client)

        # Assert
        assert result is not None
        assert "sprints" in result
        assert len(result["sprints"]) == 2
        assert result["sprints"][0]["name"] == "Sprint 42"
        assert result["sprints"][1]["name"] == "Sprint 41"
        assert result["total"] == 2

        # Verify API call
        mock_jira_client.get_board_sprints.assert_called_once_with(
            123, state=None, max_results=50
        )

    def test_list_sprints_by_project_key(
        self, mock_jira_client, sample_boards_response, sample_sprints_response
    ):
        """Test listing sprints by project key (finds board automatically)."""
        # Arrange
        from list_sprints import list_sprints

        mock_jira_client.get_all_boards.return_value = sample_boards_response
        mock_jira_client.get_board_sprints.return_value = sample_sprints_response

        # Act
        result = list_sprints(project_key="PROJ", client=mock_jira_client)

        # Assert
        assert result is not None
        assert "sprints" in result
        assert len(result["sprints"]) == 2
        assert result["board"]["id"] == 123  # Should prefer Scrum board

        # Verify board lookup used project key
        mock_jira_client.get_all_boards.assert_called_once_with(project_key="PROJ")
        # Verify sprints fetched from the Scrum board
        mock_jira_client.get_board_sprints.assert_called_once_with(
            123, state=None, max_results=50
        )

    def test_list_sprints_with_state_filter(self, mock_jira_client):
        """Test filtering sprints by state."""
        # Arrange
        from list_sprints import list_sprints

        mock_jira_client.get_board_sprints.return_value = {
            "values": [
                {
                    "id": 456,
                    "state": "active",
                    "name": "Sprint 42",
                    "startDate": "2025-01-20T00:00:00.000Z",
                    "endDate": "2025-02-03T00:00:00.000Z",
                }
            ],
            "total": 1,
        }

        # Act
        result = list_sprints(board_id=123, state="active", client=mock_jira_client)

        # Assert
        assert result is not None
        assert len(result["sprints"]) == 1
        assert result["sprints"][0]["state"] == "active"
        assert result["state_filter"] == "active"

        # Verify state filter passed to API
        mock_jira_client.get_board_sprints.assert_called_once_with(
            123, state="active", max_results=50
        )

    def test_list_sprints_no_board_found(self, mock_jira_client):
        """Test error when project has no boards."""
        # Arrange
        from list_sprints import list_sprints

        from jira_assistant_skills_lib import ValidationError

        mock_jira_client.get_all_boards.return_value = {"values": [], "total": 0}

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            list_sprints(project_key="EMPTY", client=mock_jira_client)

        assert "No board found for project EMPTY" in str(exc_info.value)

    def test_list_sprints_requires_board_or_project(self, mock_jira_client):
        """Test error when neither board nor project provided."""
        # Arrange
        from list_sprints import list_sprints

        from jira_assistant_skills_lib import ValidationError

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            list_sprints(client=mock_jira_client)

        assert "Either --board or --project is required" in str(exc_info.value)

    def test_list_sprints_prefers_scrum_board(
        self, mock_jira_client, sample_sprints_response
    ):
        """Test that Scrum boards are preferred over Kanban for sprint listing."""
        # Arrange
        from list_sprints import list_sprints

        # Return Kanban first, then Scrum
        mock_jira_client.get_all_boards.return_value = {
            "values": [
                {"id": 124, "name": "Kanban Board", "type": "kanban"},
                {"id": 123, "name": "Scrum Board", "type": "scrum"},
            ],
            "total": 2,
        }
        mock_jira_client.get_board_sprints.return_value = sample_sprints_response

        # Act
        list_sprints(project_key="PROJ", client=mock_jira_client)

        # Assert - should use Scrum board (id=123) not Kanban
        mock_jira_client.get_board_sprints.assert_called_once_with(
            123, state=None, max_results=50
        )


@pytest.mark.agile
@pytest.mark.unit
class TestFormatSprintList:
    """Test suite for sprint list formatting."""

    def test_format_text_output(self, sample_sprints_response):
        """Test text format output."""
        # Arrange
        from list_sprints import format_sprint_list

        data = {
            "board": {"id": 123, "name": "Test Board"},
            "sprints": sample_sprints_response["values"],
            "state_filter": None,
            "total": 2,
        }

        # Act
        output = format_sprint_list(data, "text")

        # Assert
        assert "Test Board" in output
        assert "Sprint 42" in output
        assert "Sprint 41" in output
        assert "active" in output
        assert "closed" in output
        assert "Total: 2 sprint(s)" in output

    def test_format_json_output(self, sample_sprints_response):
        """Test JSON format output."""
        # Arrange
        from list_sprints import format_sprint_list

        data = {
            "board": {"id": 123, "name": "Test Board"},
            "sprints": sample_sprints_response["values"],
            "state_filter": "active",
            "total": 2,
        }

        # Act
        output = format_sprint_list(data, "json")

        # Assert
        parsed = json.loads(output)
        assert parsed["board"]["id"] == 123
        assert len(parsed["sprints"]) == 2
        assert parsed["state_filter"] == "active"

    def test_format_empty_sprints(self):
        """Test formatting when no sprints found."""
        # Arrange
        from list_sprints import format_sprint_list

        data = {
            "board": {"id": 123, "name": "Empty Board"},
            "sprints": [],
            "state_filter": "future",
            "total": 0,
        }

        # Act
        output = format_sprint_list(data, "text")

        # Assert
        assert "No sprints found" in output
        assert "state: future" in output


@pytest.mark.agile
@pytest.mark.unit
class TestGetBoardForProject:
    """Test suite for get_board_for_project helper."""

    def test_get_board_for_project_success(
        self, mock_jira_client, sample_boards_response
    ):
        """Test finding board by project key."""
        # Arrange
        from list_sprints import get_board_for_project

        mock_jira_client.get_all_boards.return_value = sample_boards_response

        # Act
        board = get_board_for_project("PROJ", client=mock_jira_client)

        # Assert
        assert board is not None
        assert board["id"] == 123  # Scrum board preferred
        assert board["type"] == "scrum"

    def test_get_board_for_project_no_boards(self, mock_jira_client):
        """Test when project has no boards."""
        # Arrange
        from list_sprints import get_board_for_project

        mock_jira_client.get_all_boards.return_value = {"values": [], "total": 0}

        # Act
        board = get_board_for_project("EMPTY", client=mock_jira_client)

        # Assert
        assert board is None

    def test_get_board_for_project_only_kanban(self, mock_jira_client):
        """Test fallback to Kanban board when no Scrum board exists."""
        # Arrange
        from list_sprints import get_board_for_project

        mock_jira_client.get_all_boards.return_value = {
            "values": [{"id": 124, "name": "Kanban", "type": "kanban"}],
            "total": 1,
        }

        # Act
        board = get_board_for_project("PROJ", client=mock_jira_client)

        # Assert
        assert board is not None
        assert board["id"] == 124
        assert board["type"] == "kanban"
