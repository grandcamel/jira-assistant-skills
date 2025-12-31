import click
import sys
import os
import importlib.util
from pathlib import Path
from jira_assistant_skills.utils import SKILLS_ROOT_DIR, run_skill_script_subprocess


@click.group()
def issue():
    """Commands for interacting with Jira issues."""
    pass


@issue.command(name="get")
@click.argument('issue_key')
@click.option('--fields', '-f', help='Comma-separated list of fields to retrieve')
@click.option('--detailed', '-d', is_flag=True, help='Show detailed information including description')
@click.option('--show-links', '-l', is_flag=True, help='Show issue links (blocks, relates to, etc.)')
@click.option('--show-time', '-t', is_flag=True, help='Show time tracking information')
@click.pass_context
def get_issue(ctx, issue_key: str, fields: str, detailed: bool, show_links: bool, show_time: bool):
    """Get the details of a specific issue."""
    script_module_path = SKILLS_ROOT_DIR / "jira-issue" / "scripts" / "get_issue.py"
    
    # Arguments for the script's main(argv)
    script_args = [issue_key]
    if fields: script_args.extend(["--fields", fields])
    if detailed: script_args.append("--detailed")
    if show_links: script_args.append("--show-links")
    if show_time: script_args.append("--show-time")
    # Global options are passed via env vars, so not explicitly added here

    try:
        # --- Primary: Direct call to callable API ---
        # Dynamically import the script as a module
        spec = importlib.util.spec_from_file_location(
            "jira_issue_get_script", str(script_module_path)
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        # Check if the preferred 'get_issue' function (aliased to execute_skill) exists
        if hasattr(module, 'get_issue') and callable(getattr(module, 'get_issue')):
            # The original get_issue function expects specific args, not an argparse namespace
            # We need to map CLI arguments to direct function arguments
            result = module.get_issue(
                issue_key=issue_key,
                fields=fields.split(',') if fields else None,
                profile=ctx.obj.get('PROFILE')
            )
            # The script logic inside get_issue.py already handles output formatting
            # We need to explicitly call the formatting if we are calling execute_skill directly
            # For simplicity for now, we'll let the main() function handle output.
            # If issue.get_issue() does not print, we need to handle it here.
            # For now, let's just make it simpler and call the main function with the mapped CLI arguments.
            # This is where the 'main(argv=...)' refactoring comes in handy.
            module.main(script_args + ["--output", ctx.obj['OUTPUT']]) # Call script's main with mapped args and global output
            ctx.exit(0)
        else:
            # Fallback to subprocess if execute_skill/get_issue is not found or not callable.
            raise ImportError("Callable 'get_issue' function not found in script.")

    except ImportError as e:
        # --- Fallback: Subprocess call to main(argv=...) ---
        click.echo(f"Warning: Falling back to subprocess for {script_module_path.name} ({e})", err=True)
        run_skill_script_subprocess(
            script_path=script_module_path,
            args=script_args + ["--output", ctx.obj['OUTPUT']],
            ctx=ctx
        )
    except Exception as e:
        click.echo(f"Error calling get_issue directly: {e}", err=True)
        ctx.exit(1)


@issue.command(name="create")
@click.option('--project', '-p', required=True, help='Project key (e.g., PROJ, DEV)')
@click.option('--type', '-t', required=True, help='Issue type (Bug, Task, Story, etc.)')
@click.option('--summary', '-s', required=True, help='Issue summary (title)')
@click.option('--description', '-d', help='Issue description (supports markdown)')
@click.option('--priority', help='Priority (Highest, High, Medium, Low, Lowest)')
@click.option('--assignee', '-a', help='Assignee (account ID, email, or "self")')
@click.option('--labels', '-l', help='Comma-separated labels')
@click.option('--components', '-c', help='Comma-separated component names')
@click.option('--template', help='Use a predefined template')
@click.option('--custom-fields', help='Custom fields as JSON string')
@click.option('--epic', '-e', help='Epic key to link this issue to (e.g., PROJ-100)')
@click.option('--sprint', type=int, help='Sprint ID to add this issue to')
@click.option('--story-points', type=float, help='Story point estimate')
@click.option('--blocks', help='Comma-separated issue keys this issue blocks')
@click.option('--relates-to', help='Comma-separated issue keys this issue relates to')
@click.option('--estimate', help='Original time estimate (e.g., 2d, 4h, 1w)')
@click.option('--no-defaults', is_flag=True, help='Disable project context defaults')
@click.pass_context
def create_issue(ctx, project: str, type: str, summary: str, description: str, priority: str,
                 assignee: str, labels: str, components: str, template: str, custom_fields: str,
                 epic: str, sprint: int, story_points: float, blocks: str, relates_to: str,
                 estimate: str, no_defaults: bool):
    """Create a new JIRA issue."""
    script_module_path = SKILLS_ROOT_DIR / "jira-issue" / "scripts" / "create_issue.py"

    script_args = [
        "--project", project,
        "--type", type,
        "--summary", summary
    ]
    if description: script_args.extend(["--description", description])
    if priority: script_args.extend(["--priority", priority])
    if assignee: script_args.extend(["--assignee", assignee])
    if labels: script_args.extend(["--labels", labels])
    if components: script_args.extend(["--components", components])
    if template: script_args.extend(["--template", template])
    if custom_fields: script_args.extend(["--custom-fields", custom_fields])
    if epic: script_args.extend(["--epic", epic])
    if sprint: script_args.extend(["--sprint", str(sprint)])
    if story_points: script_args.extend(["--story-points", str(story_points)])
    if blocks: script_args.extend(["--blocks", blocks])
    if relates_to: script_args.extend(["--relates-to", relates_to])
    if estimate: script_args.extend(["--estimate", estimate])
    if no_defaults: script_args.append("--no-defaults")

    try:
        spec = importlib.util.spec_from_file_location(
            "jira_issue_create_script", str(script_module_path)
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        if hasattr(module, 'create_issue') and callable(getattr(module, 'create_issue')):
            # The original create_issue function expects specific args
            # We need to map CLI arguments to direct function arguments
            # For simplicity and consistency, calling the main function with mapped CLI arguments
            module.main(script_args + ["--output", ctx.obj['OUTPUT']])
            ctx.exit(0)
        else:
            raise ImportError("Callable 'create_issue' function not found in script.")

    except ImportError as e:
        click.echo(f"Warning: Falling back to subprocess for {script_module_path.name} ({e})", err=True)
        run_skill_script_subprocess(
            script_path=script_module_path,
            args=script_args + ["--output", ctx.obj['OUTPUT']],
            ctx=ctx
        )
    except Exception as e:
        click.echo(f"Error calling create_issue directly: {e}", err=True)
        ctx.exit(1)


@issue.command(name="update")
@click.argument('issue_key')
@click.option('--summary', '-s', help='New summary (title)')
@click.option('--description', '-d', help='New description (supports markdown)')
@click.option('--priority', help='New priority (Highest, High, Medium, Low, Lowest)')
@click.option('--assignee', '-a', help='New assignee (account ID, email, "self", or "none")')
@click.option('--labels', '-l', help='Comma-separated labels (replaces existing)')
@click.option('--components', '-c', help='Comma-separated component names (replaces existing)')
@click.option('--custom-fields', help='Custom fields as JSON string')
@click.option('--no-notify', is_flag=True, help='Do not send notifications to watchers')
@click.pass_context
def update_issue(ctx, issue_key: str, summary: str, description: str, priority: str,
                 assignee: str, labels: str, components: str, custom_fields: str, no_notify: bool):
    """Update a JIRA issue."""
    script_module_path = SKILLS_ROOT_DIR / "jira-issue" / "scripts" / "update_issue.py"

    script_args = [issue_key]
    if summary: script_args.extend(["--summary", summary])
    if description: script_args.extend(["--description", description])
    if priority: script_args.extend(["--priority", priority])
    if assignee: script_args.extend(["--assignee", assignee])
    if labels: script_args.extend(["--labels", labels])
    if components: script_args.extend(["--components", components])
    if custom_fields: script_args.extend(["--custom-fields", custom_fields])
    if no_notify: script_args.append("--no-notify")
    
    try:
        spec = importlib.util.spec_from_file_location(
            "jira_issue_update_script", str(script_module_path)
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        if hasattr(module, 'update_issue') and callable(getattr(module, 'update_issue')):
            module.main(script_args + ["--output", ctx.obj['OUTPUT']])
            ctx.exit(0)
        else:
            raise ImportError("Callable 'update_issue' function not found in script.")

    except ImportError as e:
        click.echo(f"Warning: Falling back to subprocess for {script_module_path.name} ({e})", err=True)
        run_skill_script_subprocess(
            script_path=script_module_path,
            args=script_args + ["--output", ctx.obj['OUTPUT']],
            ctx=ctx
        )
    except Exception as e:
        click.echo(f"Error calling update_issue directly: {e}", err=True)
        ctx.exit(1)


@issue.command(name="delete")
@click.argument('issue_key')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompt')
@click.pass_context
def delete_issue(ctx, issue_key: str, force: bool):
    """Delete a JIRA issue."""
    script_module_path = SKILLS_ROOT_DIR / "jira-issue" / "scripts" / "delete_issue.py"

    script_args = [issue_key]
    if force: script_args.append("--force")

    try:
        spec = importlib.util.spec_from_file_location(
            "jira_issue_delete_script", str(script_module_path)
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        if hasattr(module, 'delete_issue') and callable(getattr(module, 'delete_issue')):
            module.main(script_args + ["--output", ctx.obj['OUTPUT']])
            ctx.exit(0)
        else:
            raise ImportError("Callable 'delete_issue' function not found in script.")

    except ImportError as e:
        click.echo(f"Warning: Falling back to subprocess for {script_module_path.name} ({e})", err=True)
        run_skill_script_subprocess(
            script_path=script_module_path,
            args=script_args + ["--output", ctx.obj['OUTPUT']],
            ctx=ctx
        )
    except Exception as e:
        click.echo(f"Error calling delete_issue directly: {e}", err=True)
        ctx.exit(1)
