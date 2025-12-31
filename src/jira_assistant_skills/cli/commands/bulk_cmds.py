import click
from jira_assistant_skills.utils import SKILLS_ROOT_DIR, run_skill_script_subprocess


@click.group()
def bulk():
    """Commands for bulk operations on multiple issues."""
    pass


@bulk.command(name="transition")
@click.argument('jql')
@click.argument('status')
@click.option('--comment', '-c', help='Add comment with transition')
@click.option('--resolution', '-r', help='Resolution for Done transitions')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be changed without making changes')
@click.option('--max-issues', '-m', type=int, default=50, help='Maximum issues to process')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def bulk_transition(ctx, jql: str, status: str, comment: str, resolution: str,
                    dry_run: bool, max_issues: int, force: bool):
    """Transition multiple issues matching JQL to a new status."""
    script_path = SKILLS_ROOT_DIR / "jira-bulk" / "scripts" / "bulk_transition.py"

    script_args = [jql, status]
    if comment:
        script_args.extend(["--comment", comment])
    if resolution:
        script_args.extend(["--resolution", resolution])
    if dry_run:
        script_args.append("--dry-run")
    if max_issues:
        script_args.extend(["--max-issues", str(max_issues)])
    if force:
        script_args.append("--force")

    run_skill_script_subprocess(script_path, script_args, ctx)


@bulk.command(name="assign")
@click.argument('jql')
@click.argument('assignee')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be changed without making changes')
@click.option('--max-issues', '-m', type=int, default=50, help='Maximum issues to process')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def bulk_assign(ctx, jql: str, assignee: str, dry_run: bool, max_issues: int, force: bool):
    """Assign multiple issues matching JQL to a user."""
    script_path = SKILLS_ROOT_DIR / "jira-bulk" / "scripts" / "bulk_assign.py"

    script_args = [jql, assignee]
    if dry_run:
        script_args.append("--dry-run")
    if max_issues:
        script_args.extend(["--max-issues", str(max_issues)])
    if force:
        script_args.append("--force")

    run_skill_script_subprocess(script_path, script_args, ctx)


@bulk.command(name="set-priority")
@click.argument('jql')
@click.argument('priority')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be changed without making changes')
@click.option('--max-issues', '-m', type=int, default=50, help='Maximum issues to process')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def bulk_set_priority(ctx, jql: str, priority: str, dry_run: bool, max_issues: int, force: bool):
    """Set priority for multiple issues matching JQL."""
    script_path = SKILLS_ROOT_DIR / "jira-bulk" / "scripts" / "bulk_set_priority.py"

    script_args = [jql, priority]
    if dry_run:
        script_args.append("--dry-run")
    if max_issues:
        script_args.extend(["--max-issues", str(max_issues)])
    if force:
        script_args.append("--force")

    run_skill_script_subprocess(script_path, script_args, ctx)


@bulk.command(name="clone")
@click.argument('jql')
@click.option('--target-project', '-t', help='Target project key for clones')
@click.option('--prefix', '-p', help='Prefix for cloned issue summaries')
@click.option('--clone-links', '-l', is_flag=True, help='Clone issue links')
@click.option('--clone-subtasks', '-s', is_flag=True, help='Clone subtasks')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be changed without making changes')
@click.option('--max-issues', '-m', type=int, default=50, help='Maximum issues to process')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def bulk_clone(ctx, jql: str, target_project: str, prefix: str, clone_links: bool,
               clone_subtasks: bool, dry_run: bool, max_issues: int, force: bool):
    """Clone multiple issues matching JQL."""
    script_path = SKILLS_ROOT_DIR / "jira-bulk" / "scripts" / "bulk_clone.py"

    script_args = [jql]
    if target_project:
        script_args.extend(["--target-project", target_project])
    if prefix:
        script_args.extend(["--prefix", prefix])
    if clone_links:
        script_args.append("--clone-links")
    if clone_subtasks:
        script_args.append("--clone-subtasks")
    if dry_run:
        script_args.append("--dry-run")
    if max_issues:
        script_args.extend(["--max-issues", str(max_issues)])
    if force:
        script_args.append("--force")

    run_skill_script_subprocess(script_path, script_args, ctx)
