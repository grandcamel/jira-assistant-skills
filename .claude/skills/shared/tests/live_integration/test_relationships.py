"""
Live Integration Tests: Issue Relationships

Tests for issue linking operations against a real JIRA instance.
"""

import pytest
import uuid


class TestLinkTypes:
    """Tests for link type operations."""

    def test_get_link_types(self, jira_client):
        """Test fetching available link types."""
        link_types = jira_client.get_link_types()

        assert isinstance(link_types, list)
        assert len(link_types) > 0

        # Verify structure
        for lt in link_types:
            assert 'id' in lt
            assert 'name' in lt
            assert 'inward' in lt
            assert 'outward' in lt

    def test_common_link_types_exist(self, jira_client):
        """Test that common link types are available."""
        link_types = jira_client.get_link_types()
        type_names = [lt['name'].lower() for lt in link_types]

        # At least one of these should exist
        common_types = ['blocks', 'duplicate', 'relates', 'cloners']
        found = any(ct in ' '.join(type_names) for ct in common_types)
        assert found, f"No common link types found. Available: {type_names}"


class TestLinkCreation:
    """Tests for creating issue links."""

    def test_create_blocks_link(self, jira_client, test_project):
        """Test creating a 'blocks' link between issues."""
        # Create two issues
        blocker = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Blocker Issue {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })
        blocked = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Blocked Issue {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })

        # Create link: blocker blocks blocked
        jira_client.create_link(
            link_type='Blocks',
            inward_key=blocked['key'],   # is blocked by
            outward_key=blocker['key']   # blocks
        )

        # Verify link exists
        links = jira_client.get_issue_links(blocker['key'])
        assert len(links) >= 1

        linked_keys = []
        for link in links:
            if 'inwardIssue' in link:
                linked_keys.append(link['inwardIssue']['key'])
            if 'outwardIssue' in link:
                linked_keys.append(link['outwardIssue']['key'])

        assert blocked['key'] in linked_keys

        # Cleanup
        jira_client.delete_issue(blocker['key'])
        jira_client.delete_issue(blocked['key'])

    def test_create_relates_link(self, jira_client, test_project):
        """Test creating a 'relates to' link."""
        issue1 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Related Issue 1 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })
        issue2 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Related Issue 2 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })

        # Create relates link
        jira_client.create_link(
            link_type='Relates',
            inward_key=issue2['key'],
            outward_key=issue1['key']
        )

        # Verify from both sides
        links1 = jira_client.get_issue_links(issue1['key'])
        links2 = jira_client.get_issue_links(issue2['key'])

        assert len(links1) >= 1
        assert len(links2) >= 1

        # Cleanup
        jira_client.delete_issue(issue1['key'])
        jira_client.delete_issue(issue2['key'])

    def test_create_duplicate_link(self, jira_client, test_project):
        """Test creating a 'duplicate' link."""
        original = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Original Issue {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Bug'}
        })
        duplicate = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Duplicate Issue {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Bug'}
        })

        # Create duplicate link
        jira_client.create_link(
            link_type='Duplicate',
            inward_key=duplicate['key'],   # is duplicated by
            outward_key=original['key']    # duplicates
        )

        # Verify link
        links = jira_client.get_issue_links(original['key'])
        assert len(links) >= 1

        # Cleanup
        jira_client.delete_issue(original['key'])
        jira_client.delete_issue(duplicate['key'])


class TestLinkRetrieval:
    """Tests for retrieving issue links."""

    def test_get_issue_links(self, jira_client, test_project):
        """Test getting all links for an issue."""
        # Create linked issues
        issue1 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Link Test 1 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })
        issue2 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Link Test 2 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })
        issue3 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Link Test 3 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })

        # Create multiple links
        jira_client.create_link('Blocks', issue2['key'], issue1['key'])
        jira_client.create_link('Relates', issue3['key'], issue1['key'])

        # Get links for issue1
        links = jira_client.get_issue_links(issue1['key'])

        assert len(links) >= 2

        # Cleanup
        jira_client.delete_issue(issue1['key'])
        jira_client.delete_issue(issue2['key'])
        jira_client.delete_issue(issue3['key'])

    def test_get_link_by_id(self, jira_client, test_project):
        """Test getting a specific link by ID."""
        # Create linked issues
        issue1 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Link ID Test 1 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })
        issue2 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Link ID Test 2 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })

        # Create link
        jira_client.create_link('Relates', issue2['key'], issue1['key'])

        # Get link ID from issue
        links = jira_client.get_issue_links(issue1['key'])
        link_id = links[0]['id']

        # Get link by ID
        link = jira_client.get_link(link_id)

        assert link['id'] == link_id
        assert 'type' in link

        # Cleanup
        jira_client.delete_issue(issue1['key'])
        jira_client.delete_issue(issue2['key'])


class TestLinkDeletion:
    """Tests for deleting issue links."""

    def test_delete_link(self, jira_client, test_project):
        """Test deleting an issue link."""
        # Create linked issues
        issue1 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Delete Link Test 1 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })
        issue2 = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Delete Link Test 2 {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })

        # Create link
        jira_client.create_link('Relates', issue2['key'], issue1['key'])

        # Get link ID
        links = jira_client.get_issue_links(issue1['key'])
        assert len(links) >= 1
        link_id = links[0]['id']

        # Delete link
        jira_client.delete_link(link_id)

        # Verify link is gone
        links_after = jira_client.get_issue_links(issue1['key'])
        link_ids_after = [l['id'] for l in links_after]
        assert link_id not in link_ids_after

        # Cleanup
        jira_client.delete_issue(issue1['key'])
        jira_client.delete_issue(issue2['key'])

    def test_delete_all_links(self, jira_client, test_project):
        """Test deleting all links from an issue."""
        # Create issues
        main_issue = jira_client.create_issue({
            'project': {'key': test_project['key']},
            'summary': f'Main Issue {uuid.uuid4().hex[:8]}',
            'issuetype': {'name': 'Task'}
        })
        related = []
        for i in range(3):
            issue = jira_client.create_issue({
                'project': {'key': test_project['key']},
                'summary': f'Related {i} {uuid.uuid4().hex[:8]}',
                'issuetype': {'name': 'Task'}
            })
            related.append(issue)
            jira_client.create_link('Relates', issue['key'], main_issue['key'])

        # Verify links exist
        links = jira_client.get_issue_links(main_issue['key'])
        assert len(links) >= 3

        # Delete all links
        for link in links:
            jira_client.delete_link(link['id'])

        # Verify all gone
        links_after = jira_client.get_issue_links(main_issue['key'])
        assert len(links_after) == 0

        # Cleanup
        jira_client.delete_issue(main_issue['key'])
        for issue in related:
            jira_client.delete_issue(issue['key'])
