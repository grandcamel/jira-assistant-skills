#!/usr/bin/env python3
"""
Transition a JIRA issue to a new status.

Usage:
    python transition_issue.py PROJ-123 --name "In Progress"
    python transition_issue.py PROJ-123 --id 31
    python transition_issue.py PROJ-123 --name "Done" --resolution "Fixed"
    python transition_issue.py PROJ-123 --name "In Progress" --sprint 42
"""

import sys
import argparse
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared' / 'scripts' / 'lib'))

from config_manager import get_jira_client
from error_handler import print_error, JiraError, ValidationError
from validators import validate_issue_key, validate_transition_id
from formatters import print_success, print_info, format_transitions
from adf_helper import text_to_adf
from transition_helpers import find_transition_by_name


def transition_issue(issue_key: str, transition_id: str = None,
                    transition_name: str = None, resolution: str = None,
                    comment: str = None, fields: dict = None,
                    sprint_id: int = None, profile: str = None,
                    dry_run: bool = False) -> dict:
    """
    Transition an issue to a new status.

    Args:
        issue_key: Issue key (e.g., PROJ-123)
        transition_id: Transition ID
        transition_name: Transition name (alternative to ID)
        resolution: Resolution to set (for Done transitions)
        comment: Comment to add
        fields: Additional fields to set
        sprint_id: Sprint ID to move issue to after transition
        profile: JIRA profile to use
        dry_run: If True, preview changes without making them

    Returns:
        Dictionary with transition details
    """
    issue_key = validate_issue_key(issue_key)

    if not transition_id and not transition_name:
        raise ValidationError("Either --id or --name must be specified")

    client = get_jira_client(profile)

    transitions = client.get_transitions(issue_key)

    if not transitions:
        raise ValidationError(f"No transitions available for {issue_key}")

    if transition_name:
        transition = find_transition_by_name(transitions, transition_name)
        transition_id = transition['id']
    else:
        transition_id = validate_transition_id(transition_id)
        matching = [t for t in transitions if t['id'] == transition_id]
        if not matching:
            available = format_transitions(transitions)
            raise ValidationError(
                f"Transition ID '{transition_id}' not available.\n\n{available}"
            )
        transition = matching[0]

    transition_fields = fields or {}

    if resolution:
        transition_fields['resolution'] = {'name': resolution}

    if comment:
        transition_fields['comment'] = text_to_adf(comment)

    # Get current status for dry-run display
    issue = client.get_issue(issue_key, fields=['status'])
    current_status = issue.get('fields', {}).get('status', {}).get('name', 'Unknown')
    target_status = transition.get('to', {}).get('name', transition.get('name', 'Unknown'))

    result = {
        'issue_key': issue_key,
        'transition': transition.get('name'),
        'transition_id': transition_id,
        'current_status': current_status,
        'target_status': target_status,
        'resolution': resolution,
        'comment': comment is not None,
        'sprint_id': sprint_id,
        'dry_run': dry_run
    }

    if dry_run:
        print_info(f"[DRY RUN] Would transition {issue_key}:")
        print(f"  Current status: {current_status}")
        print(f"  Target status: {target_status}")
        print(f"  Transition: {transition.get('name')}")
        if resolution:
            print(f"  Resolution: {resolution}")
        if comment:
            print(f"  Comment: (would add comment)")
        if sprint_id:
            print(f"  Sprint: Would move to sprint {sprint_id}")
        client.close()
        return result

    client.transition_issue(issue_key, transition_id, fields=transition_fields if transition_fields else None)

    # Move to sprint if specified
    if sprint_id:
        client.move_issues_to_sprint(sprint_id, [issue_key])

    client.close()
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Transition a JIRA issue to a new status',
        epilog='Example: python transition_issue.py PROJ-123 --name "In Progress"'
    )

    parser.add_argument('issue_key',
                       help='Issue key (e.g., PROJ-123)')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--id',
                      help='Transition ID')
    group.add_argument('--name', '-n',
                      help='Transition name (e.g., "In Progress", "Done")')

    parser.add_argument('--resolution', '-r',
                       help='Resolution (for Done transitions): Fixed, Won\'t Fix, Duplicate, etc.')
    parser.add_argument('--comment', '-c',
                       help='Comment to add during transition')
    parser.add_argument('--sprint', '-s', type=int,
                       help='Sprint ID to move issue to after transition')
    parser.add_argument('--fields',
                       help='Additional fields as JSON string')
    parser.add_argument('--dry-run',
                       action='store_true',
                       help='Preview changes without making them')
    parser.add_argument('--profile',
                       help='JIRA profile to use (default: from config)')

    args = parser.parse_args()

    try:
        fields = json.loads(args.fields) if args.fields else None

        result = transition_issue(
            issue_key=args.issue_key,
            transition_id=args.id,
            transition_name=args.name,
            resolution=args.resolution,
            comment=args.comment,
            fields=fields,
            sprint_id=args.sprint,
            profile=args.profile,
            dry_run=args.dry_run
        )

        if args.dry_run:
            # Dry-run output handled in function
            pass
        else:
            target = args.name or f"transition {args.id}"
            msg = f"Transitioned {args.issue_key} to {target}"
            if args.sprint:
                msg += f" and moved to sprint {args.sprint}"
            print_success(msg)

    except JiraError as e:
        print_error(e)
        sys.exit(1)
    except Exception as e:
        print_error(e, debug=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
