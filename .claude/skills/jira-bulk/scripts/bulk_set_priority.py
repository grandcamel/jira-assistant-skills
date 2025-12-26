#!/usr/bin/env python3
"""
Bulk set priority on multiple JIRA issues.

Sets priority on multiple issues, with support for:
- Issue keys or JQL queries
- Standard priority values
- Dry-run preview
- Progress tracking

Usage:
    python bulk_set_priority.py --issues PROJ-1,PROJ-2 --priority High
    python bulk_set_priority.py --jql "project=PROJ AND type=Bug" --priority Blocker
    python bulk_set_priority.py --jql "labels=urgent" --priority Highest --dry-run
"""

import sys
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared' / 'scripts' / 'lib'))

from config_manager import get_jira_client
from error_handler import print_error, JiraError, ValidationError
from validators import validate_issue_key, validate_jql
from formatters import print_success, print_warning, print_info


# Standard JIRA priorities
STANDARD_PRIORITIES = ['Highest', 'High', 'Medium', 'Low', 'Lowest', 'Blocker', 'Critical', 'Major', 'Minor', 'Trivial']


def validate_priority(priority: str) -> str:
    """
    Validate and normalize priority name.

    Args:
        priority: Priority name

    Returns:
        Normalized priority name

    Raises:
        ValidationError: If priority is not valid
    """
    # Case-insensitive match
    for std in STANDARD_PRIORITIES:
        if std.lower() == priority.lower():
            return std

    raise ValidationError(
        f"Invalid priority: '{priority}'. "
        f"Valid priorities: {', '.join(STANDARD_PRIORITIES)}"
    )


def bulk_set_priority(
    client=None,
    issue_keys: List[str] = None,
    jql: str = None,
    priority: str = None,
    dry_run: bool = False,
    max_issues: int = 100,
    delay_between_ops: float = 0.1,
    progress_callback: Callable = None,
    profile: str = None
) -> Dict[str, Any]:
    """
    Set priority on multiple issues.

    Args:
        client: JiraClient instance (optional, created if not provided)
        issue_keys: List of issue keys to update
        jql: JQL query to find issues (alternative to issue_keys)
        priority: Priority name to set
        dry_run: If True, preview without making changes
        max_issues: Maximum number of issues to process
        delay_between_ops: Delay between operations (seconds)
        progress_callback: Optional callback(current, total, issue_key, status)
        profile: JIRA profile to use

    Returns:
        Dict with success, failed, errors, etc.
    """
    # Validate priority first
    priority = validate_priority(priority)

    close_client = False
    if client is None:
        client = get_jira_client(profile)
        close_client = True

    try:
        # Get issues to process
        if issue_keys:
            issues = [{'key': validate_issue_key(k)} for k in issue_keys[:max_issues]]
        elif jql:
            jql = validate_jql(jql)
            result = client.search_issues(jql, fields=['key', 'summary', 'priority'], max_results=max_issues)
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
            print_info(f"[DRY RUN] Would set priority to '{priority}' on {total} issue(s):")
            for issue in issues:
                key = issue.get('key')
                current = issue.get('fields', {}).get('priority')
                current_name = current.get('name', 'None') if current else 'None'
                print(f"  - {key} ({current_name} -> {priority})")
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
                client.update_issue(
                    issue_key,
                    fields={'priority': {'name': priority}},
                    notify_users=False
                )
                success += 1
                processed.append(issue_key)

                if progress_callback:
                    progress_callback(i, total, issue_key, 'success')
                else:
                    print_success(f"[{i}/{total}] Set {issue_key} priority to '{priority}'")

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
        description='Bulk set priority on JIRA issues',
        epilog='Example: python bulk_set_priority.py --issues PROJ-1,PROJ-2 --priority High'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--issues', '-i',
                       help='Comma-separated issue keys (e.g., PROJ-1,PROJ-2)')
    group.add_argument('--jql', '-q',
                       help='JQL query to find issues')

    parser.add_argument('--priority', '-p', required=True,
                        help=f'Priority to set ({", ".join(STANDARD_PRIORITIES[:5])})')
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

        result = bulk_set_priority(
            issue_keys=issue_keys,
            jql=args.jql,
            priority=args.priority,
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
