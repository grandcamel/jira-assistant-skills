import click
from jira_assistant_skills.utils import SKILLS_ROOT_DIR, run_skill_script_subprocess


@click.group()
def agile():
    """Commands for Agile/Scrum workflows (epics, sprints, backlog)."""
    pass


# Epic commands
@agile.group()
def epic():
    """Manage epics."""
    pass


@epic.command(name="create")
@click.option('--project', '-p', required=True, help='Project key')
@click.option('--name', '-n', required=True, help='Epic name')
@click.option('--summary', '-s', required=True, help='Epic summary')
@click.option('--description', '-d', help='Epic description')
@click.option('--priority', help='Priority')
@click.option('--labels', '-l', help='Comma-separated labels')
@click.pass_context
def epic_create(ctx, project: str, name: str, summary: str, description: str,
                priority: str, labels: str):
    """Create a new epic."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "create_epic.py"

    script_args = ["--project", project, "--name", name, "--summary", summary]
    if description:
        script_args.extend(["--description", description])
    if priority:
        script_args.extend(["--priority", priority])
    if labels:
        script_args.extend(["--labels", labels])

    run_skill_script_subprocess(script_path, script_args, ctx)


@epic.command(name="get")
@click.argument('epic_key')
@click.option('--include-issues', '-i', is_flag=True, help='Include issues in epic')
@click.pass_context
def epic_get(ctx, epic_key: str, include_issues: bool):
    """Get epic details."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "get_epic.py"

    script_args = [epic_key]
    if include_issues:
        script_args.append("--include-issues")

    run_skill_script_subprocess(script_path, script_args, ctx)


@epic.command(name="add-issues")
@click.argument('epic_key')
@click.argument('issue_keys', nargs=-1, required=True)
@click.pass_context
def epic_add_issues(ctx, epic_key: str, issue_keys: tuple):
    """Add issues to an epic."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "add_to_epic.py"
    run_skill_script_subprocess(script_path, [epic_key] + list(issue_keys), ctx)


# Sprint commands
@agile.group()
def sprint():
    """Manage sprints."""
    pass


@sprint.command(name="create")
@click.argument('board_id', type=int)
@click.argument('name')
@click.option('--goal', '-g', help='Sprint goal')
@click.option('--start-date', help='Start date (YYYY-MM-DD)')
@click.option('--end-date', help='End date (YYYY-MM-DD)')
@click.pass_context
def sprint_create(ctx, board_id: int, name: str, goal: str, start_date: str, end_date: str):
    """Create a new sprint."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "create_sprint.py"

    script_args = [str(board_id), name]
    if goal:
        script_args.extend(["--goal", goal])
    if start_date:
        script_args.extend(["--start-date", start_date])
    if end_date:
        script_args.extend(["--end-date", end_date])

    run_skill_script_subprocess(script_path, script_args, ctx)


@sprint.command(name="get")
@click.argument('sprint_id', type=int)
@click.option('--include-issues', '-i', is_flag=True, help='Include issues in sprint')
@click.pass_context
def sprint_get(ctx, sprint_id: int, include_issues: bool):
    """Get sprint details."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "get_sprint.py"

    script_args = [str(sprint_id)]
    if include_issues:
        script_args.append("--include-issues")

    run_skill_script_subprocess(script_path, script_args, ctx)


@sprint.command(name="manage")
@click.argument('sprint_id', type=int)
@click.option('--start', is_flag=True, help='Start the sprint')
@click.option('--complete', is_flag=True, help='Complete the sprint')
@click.option('--name', '-n', help='Update sprint name')
@click.option('--goal', '-g', help='Update sprint goal')
@click.option('--move-to', type=int, help='Move incomplete issues to sprint ID')
@click.pass_context
def sprint_manage(ctx, sprint_id: int, start: bool, complete: bool, name: str,
                  goal: str, move_to: int):
    """Manage sprint lifecycle (start, complete, update)."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "manage_sprint.py"

    script_args = [str(sprint_id)]
    if start:
        script_args.append("--start")
    if complete:
        script_args.append("--complete")
    if name:
        script_args.extend(["--name", name])
    if goal:
        script_args.extend(["--goal", goal])
    if move_to:
        script_args.extend(["--move-to", str(move_to)])

    run_skill_script_subprocess(script_path, script_args, ctx)


@sprint.command(name="move-issues")
@click.argument('sprint_id', type=int)
@click.argument('issue_keys', nargs=-1, required=True)
@click.pass_context
def sprint_move_issues(ctx, sprint_id: int, issue_keys: tuple):
    """Move issues to a sprint."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "move_to_sprint.py"
    run_skill_script_subprocess(script_path, [str(sprint_id)] + list(issue_keys), ctx)


# Backlog commands
@agile.command(name="backlog")
@click.argument('board_id', type=int)
@click.option('--max-results', '-m', type=int, default=50, help='Maximum results')
@click.pass_context
def agile_backlog(ctx, board_id: int, max_results: int):
    """Get backlog issues for a board."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "get_backlog.py"
    run_skill_script_subprocess(script_path, [str(board_id), "--max-results", str(max_results)], ctx)


# Ranking
@agile.command(name="rank")
@click.argument('issue_key')
@click.option('--before', '-b', help='Rank before this issue')
@click.option('--after', '-a', help='Rank after this issue')
@click.pass_context
def agile_rank(ctx, issue_key: str, before: str, after: str):
    """Rank an issue in the backlog."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "rank_issue.py"

    script_args = [issue_key]
    if before:
        script_args.extend(["--before", before])
    if after:
        script_args.extend(["--after", after])

    run_skill_script_subprocess(script_path, script_args, ctx)


# Estimation
@agile.command(name="estimate")
@click.argument('issue_key')
@click.argument('story_points', type=float)
@click.pass_context
def agile_estimate(ctx, issue_key: str, story_points: float):
    """Set story points for an issue."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "estimate_issue.py"
    run_skill_script_subprocess(script_path, [issue_key, str(story_points)], ctx)


@agile.command(name="estimates")
@click.argument('jql')
@click.option('--summary', '-s', is_flag=True, help='Show summary statistics')
@click.pass_context
def agile_estimates(ctx, jql: str, summary: bool):
    """Get estimates for issues matching JQL."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "get_estimates.py"

    script_args = [jql]
    if summary:
        script_args.append("--summary")

    run_skill_script_subprocess(script_path, script_args, ctx)


# Subtasks
@agile.command(name="subtask")
@click.argument('parent_key')
@click.option('--summary', '-s', required=True, help='Subtask summary')
@click.option('--description', '-d', help='Subtask description')
@click.option('--assignee', '-a', help='Assignee')
@click.pass_context
def agile_subtask(ctx, parent_key: str, summary: str, description: str, assignee: str):
    """Create a subtask under a parent issue."""
    script_path = SKILLS_ROOT_DIR / "jira-agile" / "scripts" / "create_subtask.py"

    script_args = [parent_key, "--summary", summary]
    if description:
        script_args.extend(["--description", description])
    if assignee:
        script_args.extend(["--assignee", assignee])

    run_skill_script_subprocess(script_path, script_args, ctx)
