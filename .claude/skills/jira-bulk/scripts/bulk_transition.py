#!/usr/bin/env python3
"""
Bulk transition multiple JIRA issues.

Transitions multiple issues to a new status, with support for:
- Issue keys or JQL queries
- Resolution setting
- Comments during transition
- Dry-run preview
- Progress tracking
- Rate limiting

Usage:
    python bulk_transition.py --issues PROJ-1,PROJ-2 --to "Done"
    python bulk_transition.py --jql "project=PROJ AND status='In Progress'" --to "Done"
    python bulk_transition.py --jql "project=PROJ" --to "Done" --resolution "Fixed"
    python bulk_transition.py --issues PROJ-1 --to "In Review" --comment "Ready for review"
    python bulk_transition.py --jql "project=PROJ" --to "Done" --dry-run
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
from adf_helper import text_to_adf


def find_transition(transitions: List[Dict], target_status: str) -> Optional[Dict]:
    """
    Find a transition that leads to the target status.

    Args:
        transitions: List of available transitions
        target_status: Target status name (case-insensitive)

    Returns:
        Matching transition dict or None
    """
    target_lower = target_status.lower()

    # First try exact match on transition name
    for t in transitions:
        if t['name'].lower() == target_lower:
            return t

    # Then try matching target status name
    for t in transitions:
        to_status = t.get('to', {}).get('name', '').lower()
        if to_status == target_lower:
            return t

    # Finally try partial match
    for t in transitions:
        if target_lower in t['name'].lower() or target_lower in t.get('to', {}).get('name', '').lower():
            return t

    return None


def bulk_transition(
    client=None,
    issue_keys: List[str] = None,
    jql: str = None,
    target_status: str = None,
    resolution: str = None,
    comment: str = None,
    dry_run: bool = False,
    max_issues: int = 100,
    delay_between_ops: float = 0.1,
    progress_callback: Callable = None,
    profile: str = None
) -> Dict[str, Any]:
    """
    Transition multiple issues to a new status.

    Args:
        client: JiraClient instance (optional, created if not provided)
        issue_keys: List of issue keys to transition
        jql: JQL query to find issues (alternative to issue_keys)
        target_status: Target status name
        resolution: Optional resolution to set
        comment: Optional comment to add during transition
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
        # Get issues to process
        if issue_keys:
            issues = [{'key': validate_issue_key(k)} for k in issue_keys[:max_issues]]
        elif jql:
            jql = validate_jql(jql)
            result = client.search_issues(jql, fields=['key', 'summary', 'status'], max_results=max_issues)
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
            print_info(f"[DRY RUN] Would transition {total} issue(s) to '{target_status}':")
            for issue in issues:
                key = issue.get('key', issue.get('key'))
                current_status = issue.get('fields', {}).get('status', {}).get('name', 'Unknown')
                print(f"  - {key} ({current_status} -> {target_status})")
            return {
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
                # Get available transitions
                transitions = client.get_transitions(issue_key)

                # Find matching transition
                transition = find_transition(transitions, target_status)

                if not transition:
                    available = [t['name'] for t in transitions]
                    raise ValidationError(
                        f"Transition to '{target_status}' not available. "
                        f"Available: {', '.join(available)}"
                    )

                # Build fields for transition
                fields = {}
                if resolution:
                    fields['resolution'] = {'name': resolution}

                # Execute transition
                client.transition_issue(issue_key, transition['id'], fields=fields if fields else None)

                # Add comment if provided
                if comment:
                    client.add_comment(issue_key, text_to_adf(comment))

                success += 1
                processed.append(issue_key)

                if progress_callback:
                    progress_callback(i, total, issue_key, 'success')
                else:
                    print_success(f"[{i}/{total}] Transitioned {issue_key} to '{target_status}'")

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
        description='Bulk transition JIRA issues to new status',
        epilog='Example: python bulk_transition.py --issues PROJ-1,PROJ-2 --to "Done"'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--issues', '-i',
                       help='Comma-separated issue keys (e.g., PROJ-1,PROJ-2)')
    group.add_argument('--jql', '-q',
                       help='JQL query to find issues')

    parser.add_argument('--to', '-t', required=True,
                        dest='target_status',
                        help='Target status name (e.g., "Done", "In Progress")')
    parser.add_argument('--resolution', '-r',
                        help='Resolution to set (e.g., Fixed, Won\'t Fix)')
    parser.add_argument('--comment', '-c',
                        help='Comment to add during transition')
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

        result = bulk_transition(
            issue_keys=issue_keys,
            jql=args.jql,
            target_status=args.target_status,
            resolution=args.resolution,
            comment=args.comment,
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
