import click
from jira_assistant_skills.utils import SKILLS_ROOT_DIR, run_skill_script_subprocess


@click.group()
def relationships():
    """Commands for managing issue links and dependencies."""
    pass


@relationships.command(name="link")
@click.argument('source_issue')
@click.argument('target_issue')
@click.option('--type', '-t', 'link_type', default='Relates', help='Link type (Blocks, Relates, Duplicate, etc.)')
@click.option('--comment', '-c', help='Add comment with the link')
@click.pass_context
def relationships_link(ctx, source_issue: str, target_issue: str, link_type: str, comment: str):
    """Create a link between two issues."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "link_issue.py"

    script_args = [source_issue, target_issue, "--type", link_type]
    if comment:
        script_args.extend(["--comment", comment])

    run_skill_script_subprocess(script_path, script_args, ctx)


@relationships.command(name="unlink")
@click.argument('source_issue')
@click.argument('target_issue')
@click.option('--type', '-t', 'link_type', help='Link type to remove (removes all if not specified)')
@click.pass_context
def relationships_unlink(ctx, source_issue: str, target_issue: str, link_type: str):
    """Remove a link between two issues."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "unlink_issue.py"

    script_args = [source_issue, target_issue]
    if link_type:
        script_args.extend(["--type", link_type])

    run_skill_script_subprocess(script_path, script_args, ctx)


@relationships.command(name="get-links")
@click.argument('issue_key')
@click.option('--type', '-t', 'link_type', help='Filter by link type')
@click.option('--direction', '-d', type=click.Choice(['inward', 'outward', 'both']),
              default='both', help='Link direction')
@click.pass_context
def relationships_get_links(ctx, issue_key: str, link_type: str, direction: str):
    """Get all links for an issue."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "get_links.py"

    script_args = [issue_key]
    if link_type:
        script_args.extend(["--type", link_type])
    if direction != 'both':
        script_args.extend(["--direction", direction])

    run_skill_script_subprocess(script_path, script_args, ctx)


@relationships.command(name="get-blockers")
@click.argument('issue_key')
@click.option('--recursive', '-r', is_flag=True, help='Show full blocker chain')
@click.option('--include-done', is_flag=True, help='Include completed blockers')
@click.pass_context
def relationships_get_blockers(ctx, issue_key: str, recursive: bool, include_done: bool):
    """Get issues blocking this issue."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "get_blockers.py"

    script_args = [issue_key]
    if recursive:
        script_args.append("--recursive")
    if include_done:
        script_args.append("--include-done")

    run_skill_script_subprocess(script_path, script_args, ctx)


@relationships.command(name="get-dependencies")
@click.argument('issue_key')
@click.option('--depth', '-d', type=int, default=3, help='Maximum depth to traverse')
@click.option('--include-done', is_flag=True, help='Include completed issues')
@click.pass_context
def relationships_get_dependencies(ctx, issue_key: str, depth: int, include_done: bool):
    """Get dependency tree for an issue."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "get_dependencies.py"

    script_args = [issue_key, "--depth", str(depth)]
    if include_done:
        script_args.append("--include-done")

    run_skill_script_subprocess(script_path, script_args, ctx)


@relationships.command(name="link-types")
@click.pass_context
def relationships_link_types(ctx):
    """List available link types."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "get_link_types.py"
    run_skill_script_subprocess(script_path, [], ctx)


@relationships.command(name="clone")
@click.argument('issue_key')
@click.option('--project', '-p', help='Target project key (defaults to same project)')
@click.option('--prefix', help='Prefix for cloned issue summary')
@click.option('--clone-links', '-l', is_flag=True, help='Clone issue links')
@click.option('--clone-subtasks', '-s', is_flag=True, help='Clone subtasks')
@click.pass_context
def relationships_clone(ctx, issue_key: str, project: str, prefix: str,
                        clone_links: bool, clone_subtasks: bool):
    """Clone an issue with optional links and subtasks."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "clone_issue.py"

    script_args = [issue_key]
    if project:
        script_args.extend(["--project", project])
    if prefix:
        script_args.extend(["--prefix", prefix])
    if clone_links:
        script_args.append("--clone-links")
    if clone_subtasks:
        script_args.append("--clone-subtasks")

    run_skill_script_subprocess(script_path, script_args, ctx)


@relationships.command(name="bulk-link")
@click.argument('jql')
@click.argument('target_issue')
@click.option('--type', '-t', 'link_type', default='Relates', help='Link type')
@click.option('--dry-run', '-n', is_flag=True, help='Show what would be linked')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def relationships_bulk_link(ctx, jql: str, target_issue: str, link_type: str,
                            dry_run: bool, force: bool):
    """Link multiple issues matching JQL to a target issue."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "bulk_link.py"

    script_args = [jql, target_issue, "--type", link_type]
    if dry_run:
        script_args.append("--dry-run")
    if force:
        script_args.append("--force")

    run_skill_script_subprocess(script_path, script_args, ctx)


@relationships.command(name="stats")
@click.argument('project_key')
@click.option('--type', '-t', 'link_type', help='Filter by link type')
@click.pass_context
def relationships_stats(ctx, project_key: str, link_type: str):
    """Get link statistics for a project."""
    script_path = SKILLS_ROOT_DIR / "jira-relationships" / "scripts" / "link_stats.py"

    script_args = [project_key]
    if link_type:
        script_args.extend(["--type", link_type])

    run_skill_script_subprocess(script_path, script_args, ctx)
