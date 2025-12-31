import click
from jira_assistant_skills.utils import SKILLS_ROOT_DIR, run_skill_script_subprocess


@click.group()
def time():
    """Commands for time tracking and worklogs."""
    pass


@time.command(name="log")
@click.argument('issue_key')
@click.argument('time_spent')
@click.option('--comment', '-c', help='Worklog comment')
@click.option('--started', '-s', help='Start time (YYYY-MM-DD or ISO datetime)')
@click.option('--adjust', '-a', type=click.Choice(['auto', 'leave', 'new', 'manual']),
              default='auto', help='How to adjust remaining estimate')
@click.option('--new-estimate', help='New remaining estimate (when adjust=new or manual)')
@click.pass_context
def time_log(ctx, issue_key: str, time_spent: str, comment: str, started: str,
             adjust: str, new_estimate: str):
    """Log time worked on an issue."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "add_worklog.py"

    script_args = [issue_key, time_spent]
    if comment:
        script_args.extend(["--comment", comment])
    if started:
        script_args.extend(["--started", started])
    if adjust != 'auto':
        script_args.extend(["--adjust", adjust])
    if new_estimate:
        script_args.extend(["--new-estimate", new_estimate])

    run_skill_script_subprocess(script_path, script_args, ctx)


@time.command(name="worklogs")
@click.argument('issue_key')
@click.option('--since', '-s', help='Show worklogs since date (YYYY-MM-DD)')
@click.option('--author', '-a', help='Filter by author')
@click.pass_context
def time_worklogs(ctx, issue_key: str, since: str, author: str):
    """Get worklogs for an issue."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "get_worklogs.py"

    script_args = [issue_key]
    if since:
        script_args.extend(["--since", since])
    if author:
        script_args.extend(["--author", author])

    run_skill_script_subprocess(script_path, script_args, ctx)


@time.command(name="update-worklog")
@click.argument('issue_key')
@click.argument('worklog_id')
@click.option('--time-spent', '-t', help='New time spent')
@click.option('--comment', '-c', help='New comment')
@click.option('--started', '-s', help='New start time')
@click.pass_context
def time_update_worklog(ctx, issue_key: str, worklog_id: str, time_spent: str,
                        comment: str, started: str):
    """Update an existing worklog."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "update_worklog.py"

    script_args = [issue_key, worklog_id]
    if time_spent:
        script_args.extend(["--time-spent", time_spent])
    if comment:
        script_args.extend(["--comment", comment])
    if started:
        script_args.extend(["--started", started])

    run_skill_script_subprocess(script_path, script_args, ctx)


@time.command(name="delete-worklog")
@click.argument('issue_key')
@click.argument('worklog_id')
@click.option('--adjust', '-a', type=click.Choice(['auto', 'leave', 'new', 'manual']),
              default='auto', help='How to adjust remaining estimate')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def time_delete_worklog(ctx, issue_key: str, worklog_id: str, adjust: str, force: bool):
    """Delete a worklog."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "delete_worklog.py"

    script_args = [issue_key, worklog_id]
    if adjust != 'auto':
        script_args.extend(["--adjust", adjust])
    if force:
        script_args.append("--force")

    run_skill_script_subprocess(script_path, script_args, ctx)


@time.command(name="estimate")
@click.argument('issue_key')
@click.argument('estimate')
@click.option('--remaining', '-r', help='Remaining estimate (updates both if not specified)')
@click.pass_context
def time_estimate(ctx, issue_key: str, estimate: str, remaining: str):
    """Set time estimate for an issue."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "set_estimate.py"

    script_args = [issue_key, estimate]
    if remaining:
        script_args.extend(["--remaining", remaining])

    run_skill_script_subprocess(script_path, script_args, ctx)


@time.command(name="tracking")
@click.argument('issue_key')
@click.pass_context
def time_tracking(ctx, issue_key: str):
    """Get time tracking information for an issue."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "get_time_tracking.py"
    run_skill_script_subprocess(script_path, [issue_key], ctx)


@time.command(name="report")
@click.option('--project', '-p', help='Project key')
@click.option('--user', '-u', help='User (account ID or email)')
@click.option('--since', '-s', help='Start date (YYYY-MM-DD)')
@click.option('--until', help='End date (YYYY-MM-DD)')
@click.option('--format', '-f', 'output_format', type=click.Choice(['text', 'csv', 'json']),
              default='text', help='Output format')
@click.pass_context
def time_report(ctx, project: str, user: str, since: str, until: str, output_format: str):
    """Generate a time report."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "time_report.py"

    script_args = []
    if project:
        script_args.extend(["--project", project])
    if user:
        script_args.extend(["--user", user])
    if since:
        script_args.extend(["--since", since])
    if until:
        script_args.extend(["--until", until])
    if output_format != 'text':
        script_args.extend(["--format", output_format])

    run_skill_script_subprocess(script_path, script_args, ctx)


@time.command(name="export")
@click.option('--project', '-p', help='Project key')
@click.option('--user', '-u', help='User (account ID or email)')
@click.option('--since', '-s', help='Start date (YYYY-MM-DD)')
@click.option('--until', help='End date (YYYY-MM-DD)')
@click.option('--format', '-f', 'output_format', type=click.Choice(['csv', 'xlsx']),
              default='csv', help='Export format')
@click.option('--output', '-o', 'output_file', help='Output file path')
@click.pass_context
def time_export(ctx, project: str, user: str, since: str, until: str,
                output_format: str, output_file: str):
    """Export timesheets to CSV or Excel."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "export_timesheets.py"

    script_args = []
    if project:
        script_args.extend(["--project", project])
    if user:
        script_args.extend(["--user", user])
    if since:
        script_args.extend(["--since", since])
    if until:
        script_args.extend(["--until", until])
    if output_format:
        script_args.extend(["--format", output_format])
    if output_file:
        script_args.extend(["--output", output_file])

    run_skill_script_subprocess(script_path, script_args, ctx)


@time.command(name="bulk-log")
@click.argument('jql')
@click.argument('time_spent')
@click.option('--comment', '-c', help='Worklog comment')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be logged')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def time_bulk_log(ctx, jql: str, time_spent: str, comment: str, dry_run: bool, force: bool):
    """Log time on multiple issues matching JQL."""
    script_path = SKILLS_ROOT_DIR / "jira-time" / "scripts" / "bulk_log_time.py"

    script_args = [jql, time_spent]
    if comment:
        script_args.extend(["--comment", comment])
    if dry_run:
        script_args.append("--dry-run")
    if force:
        script_args.append("--force")

    run_skill_script_subprocess(script_path, script_args, ctx)
