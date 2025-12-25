"""
Tests for filter_subscriptions.py - View filter subscriptions.
"""

import pytest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestFilterSubscriptions:
    """Tests for viewing filter subscriptions."""

    def test_get_subscriptions(self, mock_jira_client, sample_filter_with_subscriptions):
        """Test fetching filter subscriptions."""
        mock_jira_client.get_filter.return_value = sample_filter_with_subscriptions

        from filter_subscriptions import get_subscriptions

        result = get_subscriptions(mock_jira_client, '10042')

        assert len(result['subscriptions']['items']) == 2
        assert result['subscriptions']['items'][0]['user']['displayName'] == 'Alice'
        mock_jira_client.get_filter.assert_called_once()

    def test_subscriptions_empty(self, mock_jira_client, sample_filter):
        """Test handling filter with no subscriptions."""
        # sample_filter has empty subscriptions
        mock_jira_client.get_filter.return_value = sample_filter

        from filter_subscriptions import get_subscriptions

        result = get_subscriptions(mock_jira_client, '10042')

        assert result['subscriptions']['size'] == 0
        assert len(result['subscriptions']['items']) == 0

    def test_subscription_details(self, mock_jira_client):
        """Test showing subscription schedule details."""
        filter_with_schedule = {
            'id': '10042',
            'name': 'My Bugs',
            'jql': 'project = PROJ AND type = Bug',
            'viewUrl': 'https://test.atlassian.net/issues/?filter=10042',
            'subscriptions': {
                'size': 1,
                'items': [
                    {
                        'id': 789,
                        'user': {
                            'displayName': 'Alice',
                            'emailAddress': 'alice@company.com'
                        },
                        'group': None
                    }
                ]
            }
        }
        mock_jira_client.get_filter.return_value = filter_with_schedule

        from filter_subscriptions import get_subscriptions

        result = get_subscriptions(mock_jira_client, '10042')

        subscription = result['subscriptions']['items'][0]
        assert subscription['id'] == 789
        assert subscription['user']['emailAddress'] == 'alice@company.com'

    def test_filter_not_found(self, mock_jira_client):
        """Test error when filter doesn't exist."""
        from error_handler import NotFoundError
        mock_jira_client.get_filter.side_effect = NotFoundError(
            "Filter 99999 not found"
        )

        from filter_subscriptions import get_subscriptions

        with pytest.raises(NotFoundError):
            get_subscriptions(mock_jira_client, '99999')
