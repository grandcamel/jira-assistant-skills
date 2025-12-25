"""
Tests for get_comments.py - Get comments on an issue.
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestGetComments:
    """Tests for getting comments on issues."""

    def test_get_all_comments(self, mock_jira_client, sample_comments_list):
        """Test fetching all comments on an issue."""
        mock_jira_client.get_comments.return_value = sample_comments_list

        from get_comments import get_comments

        result = get_comments('PROJ-123', profile=None)

        assert len(result['comments']) == 3
        assert result['total'] == 3
        assert result['comments'][0]['author']['displayName'] == 'Alice Smith'
        mock_jira_client.get_comments.assert_called_once_with('PROJ-123', max_results=50, start_at=0, order_by='-created')

    def test_get_comments_with_pagination(self, mock_jira_client, sample_comments_list):
        """Test paginated comment retrieval."""
        mock_jira_client.get_comments.return_value = sample_comments_list

        from get_comments import get_comments

        result = get_comments('PROJ-123', limit=10, offset=5, profile=None)

        mock_jira_client.get_comments.assert_called_once_with('PROJ-123', max_results=10, start_at=5, order_by='-created')

    def test_get_comments_order_by_created(self, mock_jira_client, sample_comments_list):
        """Test ordering comments by creation date."""
        mock_jira_client.get_comments.return_value = sample_comments_list

        from get_comments import get_comments

        # Default: newest first (-created)
        result = get_comments('PROJ-123', profile=None)
        mock_jira_client.get_comments.assert_called_with('PROJ-123', max_results=50, start_at=0, order_by='-created')

        # Oldest first (+created)
        result = get_comments('PROJ-123', order='asc', profile=None)
        assert mock_jira_client.get_comments.call_args[1]['order_by'] == '+created'

    def test_get_comments_empty(self, mock_jira_client):
        """Test handling issue with no comments."""
        mock_jira_client.get_comments.return_value = {
            'startAt': 0,
            'maxResults': 50,
            'total': 0,
            'comments': []
        }

        from get_comments import get_comments

        result = get_comments('PROJ-123', profile=None)

        assert result['total'] == 0
        assert len(result['comments']) == 0

    def test_get_single_comment(self, mock_jira_client, sample_comment):
        """Test fetching a specific comment by ID."""
        mock_jira_client.get_comment.return_value = sample_comment

        from get_comments import get_comment_by_id

        result = get_comment_by_id('PROJ-123', '10001', profile=None)

        assert result['id'] == '10001'
        assert result['author']['displayName'] == 'Alice Smith'
        mock_jira_client.get_comment.assert_called_once_with('PROJ-123', '10001')

    def test_format_text_output(self, mock_jira_client, sample_comments_list):
        """Test human-readable table output."""
        mock_jira_client.get_comments.return_value = sample_comments_list

        from get_comments import format_comments_table

        table = format_comments_table(sample_comments_list['comments'])

        # Should contain author, date, and body preview
        assert 'Alice Smith' in table
        assert 'Bob Jones' in table
        assert '10003' in table  # Comment ID

    def test_format_json_output(self, mock_jira_client, sample_comments_list):
        """Test JSON output format."""
        import json
        mock_jira_client.get_comments.return_value = sample_comments_list

        from get_comments import get_comments

        result = get_comments('PROJ-123', profile=None)

        # Should be JSON serializable
        json_str = json.dumps(result)
        assert json_str is not None
        assert 'comments' in result
