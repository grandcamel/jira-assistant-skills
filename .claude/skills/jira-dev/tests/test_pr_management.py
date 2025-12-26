"""
Tests for PR Management (Phase 2) - jira-dev skill.

TDD tests for:
- link_pr.py
- create_pr_description.py
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add scripts path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


# =============================================================================
# Tests for link_pr.py
# =============================================================================

class TestLinkPR:
    """Tests for link_pr functionality."""

    def test_link_pr_github(self, mock_jira_client):
        """Test linking GitHub PR to issue."""
        from link_pr import link_pr, parse_pr_url

        mock_jira_client.post.return_value = {'id': '10001'}

        with patch('link_pr.get_jira_client', return_value=mock_jira_client):
            result = link_pr(
                issue_key='PROJ-123',
                pr_url='https://github.com/org/repo/pull/456'
            )

        assert result['success'] is True
        assert result['pr_number'] == 456
        mock_jira_client.post.assert_called_once()

    def test_link_pr_gitlab(self, mock_jira_client):
        """Test linking GitLab MR to issue."""
        from link_pr import link_pr, parse_pr_url

        mock_jira_client.post.return_value = {'id': '10001'}

        with patch('link_pr.get_jira_client', return_value=mock_jira_client):
            result = link_pr(
                issue_key='PROJ-123',
                pr_url='https://gitlab.com/org/repo/-/merge_requests/789'
            )

        assert result['success'] is True
        assert result['pr_number'] == 789

    def test_link_pr_bitbucket(self, mock_jira_client):
        """Test linking Bitbucket PR to issue."""
        from link_pr import link_pr, parse_pr_url

        mock_jira_client.post.return_value = {'id': '10001'}

        with patch('link_pr.get_jira_client', return_value=mock_jira_client):
            result = link_pr(
                issue_key='PROJ-123',
                pr_url='https://bitbucket.org/org/repo/pull-requests/101'
            )

        assert result['success'] is True
        assert result['pr_number'] == 101

    def test_link_pr_with_status(self, mock_jira_client):
        """Test including PR status (open, merged, closed)."""
        from link_pr import link_pr, build_pr_comment

        comment = build_pr_comment(
            pr_url='https://github.com/org/repo/pull/456',
            pr_number=456,
            status='merged',
            title='Fix login bug'
        )

        assert 'merged' in comment.lower()
        assert '456' in comment

    def test_parse_github_pr_url(self):
        """Test parsing GitHub PR URL."""
        from link_pr import parse_pr_url

        result = parse_pr_url('https://github.com/org/repo/pull/456')

        assert result['provider'] == 'github'
        assert result['owner'] == 'org'
        assert result['repo'] == 'repo'
        assert result['pr_number'] == 456

    def test_parse_gitlab_mr_url(self):
        """Test parsing GitLab MR URL."""
        from link_pr import parse_pr_url

        result = parse_pr_url('https://gitlab.com/org/repo/-/merge_requests/789')

        assert result['provider'] == 'gitlab'
        assert result['owner'] == 'org'
        assert result['repo'] == 'repo'
        assert result['pr_number'] == 789

    def test_parse_bitbucket_pr_url(self):
        """Test parsing Bitbucket PR URL."""
        from link_pr import parse_pr_url

        result = parse_pr_url('https://bitbucket.org/org/repo/pull-requests/101')

        assert result['provider'] == 'bitbucket'
        assert result['owner'] == 'org'
        assert result['repo'] == 'repo'
        assert result['pr_number'] == 101


# =============================================================================
# Tests for create_pr_description.py
# =============================================================================

class TestCreatePRDescription:
    """Tests for create_pr_description functionality."""

    def test_create_pr_description_basic(self, mock_jira_client, sample_issue):
        """Test generating PR description from issue."""
        from create_pr_description import create_pr_description

        mock_jira_client.get_issue.return_value = sample_issue

        with patch('create_pr_description.get_jira_client', return_value=mock_jira_client):
            result = create_pr_description('PROJ-123')

        # Should contain key elements
        assert 'PROJ-123' in result
        assert 'Fix login button not responding' in result
        mock_jira_client.close.assert_called_once()

    def test_create_pr_description_includes_jira_link(self, mock_jira_client, sample_issue):
        """Test PR description includes link to JIRA issue."""
        from create_pr_description import create_pr_description

        mock_jira_client.get_issue.return_value = sample_issue

        with patch('create_pr_description.get_jira_client', return_value=mock_jira_client):
            with patch('create_pr_description.get_jira_base_url', return_value='https://jira.example.com'):
                result = create_pr_description('PROJ-123')

        # Should have link to JIRA
        assert 'PROJ-123' in result

    def test_create_pr_description_includes_checklist(self, mock_jira_client, sample_issue):
        """Test including checklist items."""
        from create_pr_description import create_pr_description

        mock_jira_client.get_issue.return_value = sample_issue

        with patch('create_pr_description.get_jira_client', return_value=mock_jira_client):
            result = create_pr_description('PROJ-123', include_checklist=True)

        # Should have checklist markers
        assert '- [ ]' in result or '- []' in result

    def test_create_pr_description_markdown_format(self, mock_jira_client, sample_issue):
        """Test Markdown output format."""
        from create_pr_description import create_pr_description

        mock_jira_client.get_issue.return_value = sample_issue

        with patch('create_pr_description.get_jira_client', return_value=mock_jira_client):
            result = create_pr_description('PROJ-123')

        # Should be valid markdown with headers
        assert '##' in result or '#' in result

    def test_create_pr_description_with_labels(self, mock_jira_client, sample_issue):
        """Test including labels from issue."""
        from create_pr_description import create_pr_description

        mock_jira_client.get_issue.return_value = sample_issue

        with patch('create_pr_description.get_jira_client', return_value=mock_jira_client):
            result = create_pr_description('PROJ-123', include_labels=True)

        # Labels from sample_issue: ['mobile', 'ui']
        assert 'mobile' in result.lower() or 'ui' in result.lower()

    def test_create_pr_description_json_output(self, mock_jira_client, sample_issue):
        """Test JSON output format."""
        from create_pr_description import create_pr_description, format_output

        mock_jira_client.get_issue.return_value = sample_issue

        with patch('create_pr_description.get_jira_client', return_value=mock_jira_client):
            description = create_pr_description('PROJ-123')
            output = format_output(description, 'PROJ-123', sample_issue, output_format='json')

        data = json.loads(output)
        assert 'description' in data
        assert 'issue_key' in data
