"""
Tests for create_component.py - Create a project component.
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add script path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))


class TestCreateComponent:
    """Tests for creating project components."""

    @patch('create_component.get_jira_client')
    def test_create_basic_component(self, mock_get_client, mock_jira_client, sample_component):
        """Test creating a basic component with name only."""
        mock_get_client.return_value = mock_jira_client
        mock_jira_client.create_component.return_value = sample_component

        from create_component import create_component

        result = create_component(
            project='PROJ',
            name='Backend API',
            profile=None
        )

        assert result['name'] == 'Backend API'
        assert result['project'] == 'PROJ'
        mock_jira_client.create_component.assert_called_once()

    @patch('create_component.get_jira_client')
    def test_create_component_with_description(self, mock_get_client, mock_jira_client):
        """Test creating component with description."""
        mock_get_client.return_value = mock_jira_client
        component_with_desc = {
            'id': '10001',
            'name': 'Frontend UI',
            'description': 'User interface components',
            'project': 'PROJ',
            'projectId': 10000
        }
        mock_jira_client.create_component.return_value = component_with_desc

        from create_component import create_component

        result = create_component(
            project='PROJ',
            name='Frontend UI',
            description='User interface components',
            profile=None
        )

        assert result['description'] == 'User interface components'

    @patch('create_component.get_jira_client')
    def test_create_component_with_lead(self, mock_get_client, mock_jira_client):
        """Test creating component with component lead."""
        mock_get_client.return_value = mock_jira_client
        component_with_lead = {
            'id': '10002',
            'name': 'Database',
            'project': 'PROJ',
            'lead': {
                'accountId': '5b10a2844c20165700ede21g',
                'displayName': 'Alice Smith'
            }
        }
        mock_jira_client.create_component.return_value = component_with_lead

        from create_component import create_component

        result = create_component(
            project='PROJ',
            name='Database',
            lead_account_id='5b10a2844c20165700ede21g',
            profile=None
        )

        assert result['lead']['accountId'] == '5b10a2844c20165700ede21g'

    @patch('create_component.get_jira_client')
    def test_create_component_with_assignee_type(self, mock_get_client, mock_jira_client):
        """Test creating component with default assignee type."""
        mock_get_client.return_value = mock_jira_client
        component_with_assignee = {
            'id': '10003',
            'name': 'Infrastructure',
            'project': 'PROJ',
            'assigneeType': 'COMPONENT_LEAD'
        }
        mock_jira_client.create_component.return_value = component_with_assignee

        from create_component import create_component

        result = create_component(
            project='PROJ',
            name='Infrastructure',
            assignee_type='COMPONENT_LEAD',
            profile=None
        )

        assert result['assigneeType'] == 'COMPONENT_LEAD'

    @patch('create_component.get_jira_client')
    def test_create_component_full(self, mock_get_client, mock_jira_client):
        """Test creating component with all fields."""
        mock_get_client.return_value = mock_jira_client
        full_component = {
            'id': '10004',
            'name': 'Security',
            'description': 'Security and authentication',
            'project': 'PROJ',
            'lead': {
                'accountId': '5b10a2844c20165700ede22h',
                'displayName': 'Bob Jones'
            },
            'assigneeType': 'PROJECT_LEAD'
        }
        mock_jira_client.create_component.return_value = full_component

        from create_component import create_component

        result = create_component(
            project='PROJ',
            name='Security',
            description='Security and authentication',
            lead_account_id='5b10a2844c20165700ede22h',
            assignee_type='PROJECT_LEAD',
            profile=None
        )

        assert result['name'] == 'Security'
        assert result['description'] == 'Security and authentication'
        assert result['assigneeType'] == 'PROJECT_LEAD'

    @patch('create_component.get_jira_client')
    def test_create_component_dry_run(self, mock_get_client, mock_jira_client):
        """Test dry-run mode shows what would be created."""
        mock_get_client.return_value = mock_jira_client

        from create_component import create_component_dry_run

        result = create_component_dry_run(
            project='PROJ',
            name='Testing',
            description='QA and testing',
            lead_account_id='5b10a2844c20165700ede21g',
            assignee_type='COMPONENT_LEAD'
        )

        # Dry run should return data without calling API
        assert result['project'] == 'PROJ'
        assert result['name'] == 'Testing'
        assert result['description'] == 'QA and testing'
        mock_jira_client.create_component.assert_not_called()
