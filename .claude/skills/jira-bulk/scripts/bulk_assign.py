#!/usr/bin/env python3
"""
Bulk assign multiple JIRA issues.

Assigns multiple issues to a user, with support for:
- Issue keys or JQL queries
- Assignment by account ID or email
- Self-assignment using 'self' keyword
- Unassigning issues
- Dry-run preview
- Progress tracking

Usage:
    python bulk_assign.py --issues PROJ-1,PROJ-2 --assignee "john.doe"
    python bulk_assign.py --jql "project=PROJ AND status=Open" --assignee self
    python bulk_assign.py --jql "project=PROJ" --unassign
    python bulk_assign.py --issues PROJ-1 --assignee "john@company.com" --dry-run
"""

import sys
import argparse
import time
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared' / 'scripts' / 'lib'))

from config_manager import get_jira_client
from error_handler import print_error, JiraError, ValidationError
from validators import validate_issue_key, validate_jql
from formatters import print_success, print_warning, print_info


def resolve_user_id(client, user_identifier: str) -> Optional[str]:
    """
    Resolve a user identifier to an account ID.

    Args:
        client: JiraClient instance
        user_identifier: Account ID, email, or 'self'

    Returns:
        Account ID string or None for unassign
    """
    if user_identifier is None:
        return None

    if user_identifier.lower() == 'self':
        return client.get_current_user_id()

    # Check if it looks like an email
    if '@' in user_identifier:
        # Try to find user by email
        try:
            users = client.get(
                '/rest/api/3/user/search',
                params={'query': user_identifier},
                operation='search users'
            )
            if users and len(users) > 0:
                # Find exact email match
                for user in users:
                    if user.get('emailAddress', '').lower() == user_identifier.lower():
                        return user['accountId']
                # Fall back to first result
                return users[0]['accountId']
        except JiraError:
            pass

    # Assume it's already an account ID
    return user_identifier


def bulk_assign(
    client=None,
    issue_keys: List[str] = None,
    jql: str = None,
    assignee: str = None,
    unassign: bool = False,
    dry_run: bool = False,
    max_issues: int = 100,
    delay_between_ops: float = 0.1,
    progress_callback: Callable = None,
    profile: str = None
) -> Dict[str, Any]:
    """
    Assign multiple issues to a user.

    Args:
        client: JiraClient instance (optional, created if not provided)
        issue_keys: List of issue keys to assign
        jql: JQL query to find issues (alternative to issue_keys)
        assignee: User to assign (account ID, email, or 'self')
        unassign: If True, remove assignee
        dry_run: If True, preview without making changes
        max_issues: Maximum number of issues to process
        delay_between_ops: Delay between operations (seconds)
        progress_callback: Optional callback(current, total, issue_key, status)
        profile: JIRA profile to use

    Returns:
        Dict with success, failed, errors, etc.
    """
    close_client = False
    if client is None:
        client = get_jira_client(profile)
        close_client = True

    try:
        # Resolve assignee ID
        account_id = None
        if unassign:
            account_id = None
            action = "unassign"
        elif assignee:
            account_id = resolve_user_id(client, assignee)
            if account_id is None and assignee.lower() != 'self':
                raise ValidationError(f"Could not resolve user: {assignee}")
            action = f"assign to {assignee}"
        else:
            raise ValidationError("Either --assignee or --unassign must be provided")

        # Get issues to process
        if issue_keys:
            issues = [{'key': validate_issue_key(k)} for k in issue_keys[:max_issues]]
        elif jql:
            jql = validate_jql(jql)
            result = client.search_issues(jql, fields=['key', 'summary', 'assignee'], max_results=max_issues)
            issues = result.get('issues', [])
        else:
            raise ValidationError("Either --issues or --jql must be provided")

        total = len(issues)

        if total == 0:
            return {
                'success': 0,
                'failed': 0,
                'total': 0,
                'errors': {},
                'processed': []
            }

        if dry_run:
            print_info(f"[DRY RUN] Would {action} {total} issue(s):")
            for issue in issues:
                key = issue.get('key')
                current = issue.get('fields', {}).get('assignee')
                current_name = current.get('displayName', 'Unassigned') if current else 'Unassigned'
                print(f"  - {key} (current: {current_name})")
            return {
                'dry_run': True,
                'success': 0,
                'failed': 0,
                'would_process': total,
                'total': total,
                'errors': {},
                'processed': []
            }

        success = 0
        failed = 0
        errors = {}
        processed = []

        for i, issue in enumerate(issues, 1):
            issue_key = issue.get('key')

            try:
                client.assign_issue(issue_key, account_id)
                success += 1
                processed.append(issue_key)

                if progress_callback:
                    progress_callback(i, total, issue_key, 'success')
                else:
                    print_success(f"[{i}/{total}] {action.capitalize()}d {issue_key}")

            except Exception as e:
                failed += 1
                errors[issue_key] = str(e)

                if progress_callback:
                    progress_callback(i, total, issue_key, 'failed')
                else:
                    print_warning(f"[{i}/{total}] Failed {issue_key}: {e}")

            # Rate limiting delay
            if i < total and delay_between_ops > 0:
                time.sleep(delay_between_ops)

        return {
            'success': success,
            'failed': failed,
            'total': total,
            'errors': errors,
            'processed': processed
        }

    finally:
        if close_client:
            client.close()


def main():
    parser = argparse.ArgumentParser(
        description='Bulk assign JIRA issues to a user',
        epilog='Example: python bulk_assign.py --issues PROJ-1,PROJ-2 --assignee self'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--issues', '-i',
                       help='Comma-separated issue keys (e.g., PROJ-1,PROJ-2)')
    group.add_argument('--jql', '-q',
                       help='JQL query to find issues')

    assign_group = parser.add_mutually_exclusive_group(required=True)
    assign_group.add_argument('--assignee', '-a',
                              help='User to assign (account ID, email, or "self")')
    assign_group.add_argument('--unassign', '-u',
                              action='store_true',
                              help='Remove assignee from issues')

    parser.add_argument('--max-issues',
                        type=int,
                        default=100,
                        help='Maximum issues to process (default: 100)')
    parser.add_argument('--dry-run',
                        action='store_true',
                        help='Preview changes without making them')
    parser.add_argument('--profile',
                        help='JIRA profile to use')

    args = parser.parse_args()

    try:
        issue_keys = None
        if args.issues:
            issue_keys = [k.strip() for k in args.issues.split(',')]

        result = bulk_assign(
            issue_keys=issue_keys,
            jql=args.jql,
            assignee=args.assignee,
            unassign=args.unassign,
            dry_run=args.dry_run,
            max_issues=args.max_issues,
            profile=args.profile
        )

        print(f"\nSummary: {result['success']} succeeded, {result['failed']} failed")

        if result['failed'] > 0:
            sys.exit(1)

    except JiraError as e:
        print_error(e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled")
        sys.exit(130)
    except Exception as e:
        print_error(e, debug=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
