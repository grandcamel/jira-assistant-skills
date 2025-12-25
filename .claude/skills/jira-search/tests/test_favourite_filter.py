"""
Tests for favourite_filter.py - Manage filter favourites.
"""

import pytest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestFavouriteFilter:
    """Tests for managing filter favourites."""

    def test_add_to_favourites(self, mock_jira_client, sample_filter):
        """Test adding filter to favourites."""
        sample_filter['favourite'] = True
        mock_jira_client.add_filter_favourite.return_value = sample_filter

        from favourite_filter import add_favourite

        result = add_favourite(mock_jira_client, '10042')

        assert result['favourite'] is True
        mock_jira_client.add_filter_favourite.assert_called_once_with('10042')

    def test_remove_from_favourites(self, mock_jira_client):
        """Test removing filter from favourites."""
        mock_jira_client.remove_filter_favourite.return_value = None

        from favourite_filter import remove_favourite

        remove_favourite(mock_jira_client, '10042')

        mock_jira_client.remove_filter_favourite.assert_called_once_with('10042')

    def test_already_favourite(self, mock_jira_client, sample_filter):
        """Test handling already favourited filter."""
        sample_filter['favourite'] = True
        mock_jira_client.add_filter_favourite.return_value = sample_filter

        from favourite_filter import add_favourite

        # Should still succeed (idempotent)
        result = add_favourite(mock_jira_client, '10042')
        assert result['favourite'] is True

    def test_not_favourite(self, mock_jira_client):
        """Test handling non-favourited filter removal."""
        # JIRA typically returns 204 even if not favourited
        mock_jira_client.remove_filter_favourite.return_value = None

        from favourite_filter import remove_favourite

        # Should not raise
        remove_favourite(mock_jira_client, '10042')

    def test_filter_not_found(self, mock_jira_client):
        """Test error when filter doesn't exist."""
        from error_handler import NotFoundError
        mock_jira_client.add_filter_favourite.side_effect = NotFoundError(
            "Filter 99999 not found"
        )

        from favourite_filter import add_favourite

        with pytest.raises(NotFoundError):
            add_favourite(mock_jira_client, '99999')
