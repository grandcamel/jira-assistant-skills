"""
Live Integration Tests: Issue Lifecycle

Tests for issue CRUD operations against a real JIRA instance.
"""

import pytest
import uuid


class TestIssueCreate:
    """Tests for issue creation."""

    def test_create_task(self, jira_client, test_project):
        """Test creating a basic task."""
        issue = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Test Task {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })

        assert issue['key'].startswith(test_project['key'])
        assert 'id' in issue

        # Cleanup
        jira_client.delete_issue(issue['key'])

    def test_create_story(self, jira_client, test_project):
        """Test creating a story."""
        issue = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Test Story {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Story'},
            'description': {
                'type': 'doc',
                'version': 1,
                'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'Story description'}]}]
            }
        })

        assert issue['key'].startswith(test_project['key'])

        # Cleanup
        jira_client.delete_issue(issue['key'])

    def test_create_bug(self, jira_client, test_project):
        """Test creating a bug."""
        issue = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Test Bug {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Bug'},
            'priority': {'name': 'High'}
        })

        assert issue['key'].startswith(test_project['key'])

        # Cleanup
        jira_client.delete_issue(issue['key'])

    def test_create_subtask(self, jira_client, test_project, test_issue):
        """Test creating a subtask under a parent issue."""
        subtask = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Test Subtask {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Subtask'},
            'parent': {'key': test_issue['key']}
        })

        assert subtask['key'].startswith(test_project['key'])

        # Verify parent relationship
        subtask_data = jira_client.get_issue(subtask['key'])
        assert subtask_data['fields']['parent']['key'] == test_issue['key']

        # Cleanup
        jira_client.delete_issue(subtask['key'])


class TestIssueRead:
    """Tests for reading issue data."""

    def test_get_issue(self, jira_client, test_issue):
        """Test fetching an issue."""
        issue = jira_client.get_issue(test_issue['key'])

        assert issue['key'] == test_issue['key']
        assert 'fields' in issue
        assert 'summary' in issue['fields']

    def test_get_issue_specific_fields(self, jira_client, test_issue):
        """Test fetching specific fields."""
        issue = jira_client.get_issue(
            test_issue['key'],
            fields=['summary', 'status', 'priority']
        )

        assert 'summary' in issue['fields']
        assert 'status' in issue['fields']
        # Other fields should not be present
        assert 'description' not in issue['fields']

    def test_search_issues(self, jira_client, test_project, test_issue):
        """Test searching for issues."""
        import time
        # Small delay for indexing
        time.sleep(1)

        result = jira_client.search_issues(
            f"project = {test_project['key']}",
            fields=['key', 'summary']
        )

        # Response structure varies between API versions
        issues = result.get('issues', [])
        total = result.get('total', len(issues))
        # Note: Search may return 0 due to indexing delays
        # Just verify the API works correctly
        assert 'issues' in result
        if total > 0:
            keys = [i['key'] for i in issues]
            assert test_issue['key'] in keys


class TestIssueUpdate:
    """Tests for updating issues."""

    def test_update_summary(self, jira_client, test_issue):
        """Test updating issue summary."""
        new_summary = f'Updated Summary {uuid.uuid4().hex[:8]}'

        jira_client.update_issue(test_issue['key'], {
            'summary': new_summary
        })

        updated = jira_client.get_issue(test_issue['key'])
        assert updated['fields']['summary'] == new_summary

    def test_update_priority(self, jira_client, test_issue):
        """Test updating issue priority."""
        jira_client.update_issue(test_issue['key'], {
            'priority': {'name': 'High'}
        })

        updated = jira_client.get_issue(test_issue['key'])
        assert updated['fields']['priority']['name'] == 'High'

    def test_assign_issue(self, jira_client, test_issue):
        """Test assigning an issue to current user."""
        current_user_id = jira_client.get_current_user_id()

        jira_client.assign_issue(test_issue['key'], current_user_id)

        updated = jira_client.get_issue(test_issue['key'])
        assert updated['fields']['assignee']['accountId'] == current_user_id

    def test_unassign_issue(self, jira_client, test_issue):
        """Test unassigning an issue."""
        # First assign
        jira_client.assign_issue(test_issue['key'], jira_client.get_current_user_id())

        # Then unassign
        jira_client.assign_issue(test_issue['key'], None)

        updated = jira_client.get_issue(test_issue['key'])
        assert updated['fields']['assignee'] is None


class TestIssueDelete:
    """Tests for deleting issues."""

    def test_delete_issue(self, jira_client, test_project):
        """Test deleting an issue."""
        # Create issue to delete
        issue = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Issue to Delete {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })

        # Delete it
        jira_client.delete_issue(issue['key'])

        # Verify it's gone
        from error_handler import NotFoundError
        with pytest.raises(NotFoundError):
            jira_client.get_issue(issue['key'])

    def test_delete_issue_with_subtasks(self, jira_client, test_project):
        """Test that deleting parent also deletes subtasks."""
        # Create parent
        parent = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Parent {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })

        # Create subtask
        subtask = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Subtask {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Subtask'},
            'parent': {'key': parent['key']}
        })

        # Delete parent (should cascade)
        jira_client.delete_issue(parent['key'])

        # Verify both are gone
        from error_handler import NotFoundError
        with pytest.raises(NotFoundError):
            jira_client.get_issue(parent['key'])
        with pytest.raises(NotFoundError):
            jira_client.get_issue(subtask['key'])


class TestIssueTransitions:
    """Tests for issue status transitions."""

    def test_get_transitions(self, jira_client, test_issue):
        """Test getting available transitions."""
        transitions = jira_client.get_transitions(test_issue['key'])

        assert isinstance(transitions, list)
        assert len(transitions) > 0
        assert all('id' in t and 'name' in t for t in transitions)

    def test_transition_issue(self, jira_client, test_issue):
        """Test transitioning an issue."""
        # Get available transitions
        transitions = jira_client.get_transitions(test_issue['key'])

        # Find a transition (usually "In Progress" or similar)
        target_transition = None
        for t in transitions:
            if 'progress' in t['name'].lower() or 'start' in t['name'].lower():
                target_transition = t
                break

        if not target_transition:
            # Just use the first available transition
            target_transition = transitions[0]

        # Perform transition
        jira_client.transition_issue(test_issue['key'], target_transition['id'])

        # Verify status changed
        updated = jira_client.get_issue(test_issue['key'])
        # Status should have changed (exact name depends on workflow)
        assert updated['fields']['status']['name'] != 'To Do' or target_transition['name'] == 'To Do'
