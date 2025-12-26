"""
Live Integration Tests: Service Desk Management

Tests for service desk CRUD operations and configuration against a real JIRA instance.
"""

import pytest
import uuid


@pytest.mark.jsm
class TestServiceDeskRead:
    """Tests for reading service desk information."""

    def test_list_service_desks(self, jira_client):
        """Test listing all service desks."""
        result = jira_client.get_service_desks()

        assert 'values' in result
        assert isinstance(result['values'], list)
        # At minimum, we should have our test service desk
        assert len(result['values']) >= 1

    def test_get_service_desk(self, jira_client, test_service_desk):
        """Test fetching a specific service desk."""
        service_desk = jira_client.get_service_desk(test_service_desk['id'])

        assert service_desk['id'] == test_service_desk['id']
        assert service_desk['projectKey'] == test_service_desk['projectKey']
        assert 'projectName' in service_desk

    def test_service_desk_has_required_fields(self, jira_client, test_service_desk):
        """Test that service desk has all required fields."""
        service_desk = jira_client.get_service_desk(test_service_desk['id'])

        required_fields = ['id', 'projectId', 'projectKey', 'projectName']
        for field in required_fields:
            assert field in service_desk, f"Missing required field: {field}"


@pytest.mark.jsm
class TestRequestTypes:
    """Tests for request type management."""

    def test_list_request_types(self, jira_client, test_service_desk):
        """Test listing request types for a service desk."""
        result = jira_client.get_request_types(test_service_desk['id'])

        assert 'values' in result
        assert isinstance(result['values'], list)
        # Service desks should have at least one request type
        assert len(result['values']) >= 1

    def test_request_type_has_required_fields(self, jira_client, test_service_desk):
        """Test that request types have required fields."""
        result = jira_client.get_request_types(test_service_desk['id'])
        request_type = result['values'][0]

        required_fields = ['id', 'name', 'description']
        for field in required_fields:
            assert field in request_type, f"Missing required field: {field}"

    def test_get_request_type(self, jira_client, test_service_desk, default_request_type):
        """Test getting a specific request type."""
        request_type = jira_client.get_request_type(
            test_service_desk['id'],
            default_request_type['id']
        )

        assert request_type['id'] == default_request_type['id']
        assert request_type['name'] == default_request_type['name']

    def test_get_request_type_fields(self, jira_client, test_service_desk, default_request_type):
        """Test getting fields for a request type."""
        result = jira_client.get_request_type_fields(
            test_service_desk['id'],
            default_request_type['id']
        )

        assert 'requestTypeFields' in result
        fields = result['requestTypeFields']
        assert isinstance(fields, list)

        # Should have at least summary field
        field_ids = [f.get('fieldId') for f in fields]
        assert 'summary' in field_ids


@pytest.mark.jsm
class TestPortalSettings:
    """Tests for portal configuration."""

    def test_get_portal_url(self, jira_client, test_service_desk):
        """Test getting portal URL information."""
        service_desk = jira_client.get_service_desk(test_service_desk['id'])

        # Portal URL should be in _links
        assert '_links' in service_desk or 'portal' in str(service_desk).lower()


@pytest.mark.jsm
class TestServiceDeskAgents:
    """Tests for agent management."""

    def test_list_agents(self, jira_client, test_service_desk):
        """Test listing agents for a service desk."""
        try:
            result = jira_client.get_service_desk_agents(test_service_desk['id'])

            assert 'values' in result
            assert isinstance(result['values'], list)
            # Should have at least the current user as agent
            assert len(result['values']) >= 1
        except Exception as e:
            if '403' in str(e) or 'permission' in str(e).lower():
                pytest.skip("Insufficient permissions to list agents")
            raise

    def test_current_user_is_agent(self, jira_client, test_service_desk, current_user):
        """Test that the current user is an agent on the service desk."""
        try:
            result = jira_client.get_service_desk_agents(test_service_desk['id'])
            agent_ids = [a.get('accountId') for a in result.get('values', [])]

            # Current user should be in agents list
            assert current_user['accountId'] in agent_ids
        except Exception as e:
            if '403' in str(e) or 'permission' in str(e).lower():
                pytest.skip("Insufficient permissions to list agents")
            raise
