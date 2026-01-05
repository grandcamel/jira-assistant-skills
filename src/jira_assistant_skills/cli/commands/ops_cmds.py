import click

from jira_assistant_skills.utils import SKILLS_ROOT_DIR, run_skill_script_subprocess


@click.group()
def ops():
    """Commands for cache management and operational utilities."""
    pass


@ops.command(name="cache-status")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.pass_context
def ops_cache_status(ctx, output_json: bool, verbose: bool):
    """Show cache status and statistics."""
    script_path = SKILLS_ROOT_DIR / "jira-ops" / "scripts" / "cache_status.py"

    script_args = []
    if output_json:
        script_args.append("--json")
    if verbose:
        script_args.append("--verbose")

    run_skill_script_subprocess(script_path, script_args, ctx)


@ops.command(name="cache-clear")
@click.option(
    "--category",
    "-c",
    type=click.Choice(["issue", "project", "user", "field", "search", "default"]),
    help="Clear only entries in this category",
)
@click.option("--pattern", help="Clear keys matching glob pattern (e.g., 'PROJ-*')")
@click.option("--key", help="Clear specific cache key (requires --category)")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be cleared without clearing"
)
@click.option("--force", "-f", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def ops_cache_clear(
    ctx, category: str, pattern: str, key: str, dry_run: bool, force: bool
):
    """Clear cache entries."""
    script_path = SKILLS_ROOT_DIR / "jira-ops" / "scripts" / "cache_clear.py"

    script_args = []
    if category:
        script_args.extend(["--category", category])
    if pattern:
        script_args.extend(["--pattern", pattern])
    if key:
        script_args.extend(["--key", key])
    if dry_run:
        script_args.append("--dry-run")
    if force:
        script_args.append("--force")

    run_skill_script_subprocess(script_path, script_args, ctx)


@ops.command(name="cache-warm")
@click.option("--projects", is_flag=True, help="Cache project list")
@click.option("--fields", is_flag=True, help="Cache field definitions")
@click.option(
    "--users", is_flag=True, help="Cache assignable users (requires project context)"
)
@click.option("--all", "warm_all", is_flag=True, help="Cache all available metadata")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.pass_context
def ops_cache_warm(
    ctx, projects: bool, fields: bool, users: bool, warm_all: bool, verbose: bool
):
    """Pre-warm cache with commonly accessed data."""
    script_path = SKILLS_ROOT_DIR / "jira-ops" / "scripts" / "cache_warm.py"

    script_args = []
    if projects:
        script_args.append("--projects")
    if fields:
        script_args.append("--fields")
    if users:
        script_args.append("--users")
    if warm_all:
        script_args.append("--all")
    if verbose:
        script_args.append("--verbose")

    run_skill_script_subprocess(script_path, script_args, ctx)


@ops.command(name="discover-project")
@click.argument("project_key")
@click.option(
    "--personal",
    "-p",
    is_flag=True,
    help="Save to settings.local.json instead of skill directory",
)
@click.option(
    "--both", is_flag=True, help="Save to both skill directory and settings.local.json"
)
@click.option(
    "--no-save", is_flag=True, help="Do not save output (useful with --output json)"
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format",
)
@click.option(
    "--sample-size",
    "-s",
    type=int,
    default=100,
    help="Number of issues to sample for patterns",
)
@click.option("--days", "-d", type=int, default=30, help="Sample period in days")
@click.pass_context
def ops_discover_project(
    ctx,
    project_key: str,
    personal: bool,
    both: bool,
    no_save: bool,
    output: str,
    sample_size: int,
    days: int,
):
    """Discover project configuration and capabilities."""
    script_path = SKILLS_ROOT_DIR / "jira-ops" / "scripts" / "discover_project.py"

    script_args = [project_key]
    if personal:
        script_args.append("--personal")
    if both:
        script_args.append("--both")
    if no_save:
        script_args.append("--no-save")
    if output != "text":
        script_args.extend(["--output", output])
    if sample_size != 100:
        script_args.extend(["--sample-size", str(sample_size)])
    if days != 30:
        script_args.extend(["--days", str(days)])

    run_skill_script_subprocess(script_path, script_args, ctx)
