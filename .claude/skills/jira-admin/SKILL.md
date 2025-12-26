# JIRA Admin Skill

## When to Use This Skill

Use this skill when you need to:
- **Create, configure, or delete JIRA projects**
- **Manage project categories** (group projects by department, type, etc.)
- **Update project settings** (lead, default assignee, avatar, URL)
- **Archive or restore projects** for compliance or cleanup
- **List and search projects** across your JIRA instance
- **View detailed project configuration** (schemes, issue types, etc.)
- **Manage automation rules** (list, create, update, enable/disable)
- **Invoke manual automation rules** on issues
- **Create automation rules from templates**

This skill requires **Administer Jira** global permission for most operations, or **Administer Projects** permission for project-level changes.

## What This Skill Does

### Project Management
- Create new projects with various templates (Scrum, Kanban, Business)
- Get detailed project information and configuration
- Update project properties (name, description, lead, URL)
- Delete projects (moves to trash for 60 days)
- List and search projects with filtering

### Project Categories
- Create and manage project categories
- Assign projects to categories for organization
- List all categories in the instance

### Project Configuration
- Set project avatars (upload custom or select system)
- Change project lead
- Configure default assignee (PROJECT_LEAD, UNASSIGNED, COMPONENT_LEAD)
- View complete project configuration with schemes

### Archive/Restore Operations
- Archive inactive projects (read-only mode)
- Restore archived or deleted projects from trash
- List projects in trash with expiry dates

## Available Scripts

### Project CRUD Operations

| Script | Description |
|--------|-------------|
| `create_project.py` | Create a new JIRA project |
| `get_project.py` | Get detailed project information |
| `list_projects.py` | List and search projects |
| `update_project.py` | Update project properties |
| `delete_project.py` | Delete a project (moves to trash) |

### Project Categories

| Script | Description |
|--------|-------------|
| `create_category.py` | Create a project category |
| `list_categories.py` | List all project categories |
| `assign_category.py` | Assign a project to a category |

### Project Configuration

| Script | Description |
|--------|-------------|
| `set_avatar.py` | Set project avatar from file or system |
| `set_project_lead.py` | Change project lead |
| `set_default_assignee.py` | Configure default issue assignee |
| `get_config.py` | View full project configuration |

### Archive/Restore

| Script | Description |
|--------|-------------|
| `archive_project.py` | Archive a project (read-only) |
| `restore_project.py` | Restore archived/trashed project |
| `list_trash.py` | List deleted projects in trash |

## Examples

### Create a New Scrum Project

```bash
# Create with Scrum template
python create_project.py --key MOBILE --name "Mobile App" --type software --template scrum

# Create with lead and description
python create_project.py --key WEBAPP --name "Web Application" \
  --type software --template kanban \
  --lead alice@example.com \
  --description "Customer-facing web application"

# Create business project
python create_project.py --key MKTG --name "Marketing" --type business
```

### Get Project Information

```bash
# Get basic info
python get_project.py PROJ

# Get with components and versions
python get_project.py PROJ --show-components --show-versions

# JSON output
python get_project.py PROJ --output json
```

### List Projects

```bash
# List all projects
python list_projects.py

# Filter by type
python list_projects.py --type software

# Search by name
python list_projects.py --search "mobile"

# Include archived projects
python list_projects.py --include-archived

# Export to CSV
python list_projects.py --output csv > projects.csv
```

### Update Project

```bash
# Update name
python update_project.py PROJ --name "New Project Name"

# Update lead
python update_project.py PROJ --lead bob@example.com

# Update multiple fields
python update_project.py PROJ --name "Updated" --description "New desc" --url https://example.com
```

### Delete Project

```bash
# Delete with confirmation prompt
python delete_project.py PROJ

# Skip confirmation
python delete_project.py PROJ --yes

# Dry run to preview
python delete_project.py PROJ --dry-run
```

### Manage Categories

```bash
# Create a category
python create_category.py --name "Development" --description "All dev projects"

# List categories
python list_categories.py

# Assign project to category
python assign_category.py PROJ --category "Development"

# Remove category from project
python assign_category.py PROJ --remove
```

### Project Configuration

```bash
# Set avatar from file
python set_avatar.py PROJ --file /path/to/logo.png

# List available system avatars
python set_avatar.py PROJ --list

# Change project lead
python set_project_lead.py PROJ --lead alice@example.com

# Set default assignee
python set_default_assignee.py PROJ --type PROJECT_LEAD

# View full configuration
python get_config.py PROJ --show-schemes
```

### Archive and Restore

```bash
# Archive inactive project
python archive_project.py OLDPROJ --yes

# List trashed projects
python list_trash.py

# Restore from trash/archive
python restore_project.py OLDPROJ
```

## Project Types and Templates

### Project Types
- **software**: Jira Software projects (requires Jira Software license)
- **business**: Jira Core/Work Management projects
- **service_desk**: Jira Service Management projects (requires JSM license)

### Template Shortcuts
| Shortcut | Full Template Key | Description |
|----------|-------------------|-------------|
| `scrum` | `com.pyxis.greenhopper.jira:gh-scrum-template` | Scrum board |
| `kanban` | `com.pyxis.greenhopper.jira:gh-kanban-template` | Kanban board |
| `basic` | `com.pyxis.greenhopper.jira:gh-simplified-basic` | Basic software |

## Permission Requirements

| Operation | Required Permission |
|-----------|---------------------|
| Create project | Administer Jira (global) |
| Update project (general) | Administer Projects |
| Update project key/schemes | Administer Jira (global) |
| Delete project | Administer Jira (global) |
| Archive/restore project | Administer Jira (global) |
| Create category | Administer Jira (global) |
| Browse projects | Browse Projects |

## Important Notes

1. **Deleted projects remain in trash for 60 days** before permanent deletion
2. **Project keys cannot be changed** after creation without Administer Jira permission
3. **Project type cannot be changed** after creation (API limitation)
4. **Templates are only used during creation** and don't persist
5. **Archived projects are read-only** but can be browsed and restored

## Error Handling

Common errors and solutions:

- **403 Permission Denied**: Contact your JIRA administrator for Administer Jira permission
- **409 Conflict**: Project key already exists - choose a different key
- **400 Invalid Key**: Keys must be uppercase, 2-10 characters, start with a letter
- **404 Not Found**: Project doesn't exist - check the key spelling

---

## Automation Rules Management

### What Automation Management Does

1. **Rule Discovery & Inspection**
   - List all automation rules with filtering by project, state
   - Get detailed rule configuration including triggers and actions
   - Search rules by trigger type, enabled/disabled state, or project scope

2. **Rule State Management**
   - Enable disabled automation rules
   - Disable active automation rules
   - Toggle rule state (enabled <-> disabled)
   - Dry-run mode for previewing changes

3. **Manual Rule Invocation**
   - List manually-triggered automation rules
   - Invoke manual rules on specific issues
   - Pass custom properties to rule execution

4. **Rule Creation & Updates**
   - List available automation templates
   - Get template details and required parameters
   - Create rules from templates with custom configuration
   - Update existing rule name, description, and configuration

### Automation Scripts

#### Rule Discovery
| Script | Description |
|--------|-------------|
| `list_automation_rules.py` | List all automation rules with filtering |
| `get_automation_rule.py` | Get detailed rule configuration |
| `search_automation_rules.py` | Search rules by trigger, state, scope |

#### Rule State Management
| Script | Description |
|--------|-------------|
| `enable_automation_rule.py` | Enable a disabled rule |
| `disable_automation_rule.py` | Disable an active rule |
| `toggle_automation_rule.py` | Toggle rule state |

#### Manual Rules
| Script | Description |
|--------|-------------|
| `list_manual_rules.py` | List manually-triggered rules |
| `invoke_manual_rule.py` | Trigger a manual rule on an issue |

#### Templates & Creation
| Script | Description |
|--------|-------------|
| `list_automation_templates.py` | List available templates |
| `get_automation_template.py` | Get template details |
| `create_rule_from_template.py` | Create rule from template |
| `update_automation_rule.py` | Update rule configuration |

### Automation Examples

```bash
# List all automation rules
python list_automation_rules.py
python list_automation_rules.py --project PROJ
python list_automation_rules.py --state enabled
python list_automation_rules.py --state disabled --output json

# Get rule details
python get_automation_rule.py "ari:cloud:jira::site/12345..."
python get_automation_rule.py --name "Auto-assign to lead"
python get_automation_rule.py RULE_ID --output json

# Search rules
python search_automation_rules.py --trigger "jira.issue.event.trigger:created"
python search_automation_rules.py --state enabled --project PROJ
python search_automation_rules.py --trigger issue_created --state disabled

# Enable/Disable rules
python enable_automation_rule.py RULE_ID
python enable_automation_rule.py --name "Auto-assign to lead"
python disable_automation_rule.py RULE_ID --confirm
python toggle_automation_rule.py RULE_ID

# Dry run mode
python enable_automation_rule.py RULE_ID --dry-run
python disable_automation_rule.py RULE_ID --dry-run

# Manual rules
python list_manual_rules.py --context issue
python invoke_manual_rule.py RULE_ID --issue PROJ-123
python invoke_manual_rule.py RULE_ID --issue PROJ-123 --property '{"priority": "High"}'

# Templates
python list_automation_templates.py
python list_automation_templates.py --category "Issue Management"
python get_automation_template.py TEMPLATE_ID

# Create from template
python create_rule_from_template.py TEMPLATE_ID --project PROJ
python create_rule_from_template.py TEMPLATE_ID --project PROJ --name "My Rule"
python create_rule_from_template.py TEMPLATE_ID --project PROJ --dry-run

# Update rule
python update_automation_rule.py RULE_ID --name "New Rule Name"
python update_automation_rule.py RULE_ID --description "Updated description"
python update_automation_rule.py RULE_ID --config rule_config.json
```

### Automation API Requirements

#### Authentication
- JIRA API token with appropriate scopes
- Jira Administrator permissions (for full rule management)
- Project Administrator permissions (for project-scoped rules only)

#### Required API Token Scopes
- `manage:jira-automation` - For create/update/delete operations
- `read:jira-work` - For list/get operations

#### Cloud ID Requirement
All Automation API calls require the Atlassian Cloud ID, which is automatically retrieved from the JIRA instance using the tenant info endpoint (`/_edge/tenant_info`).

### Automation Limitations

1. **Complex Rule Creation**: Very complex rules with nested conditions may require the UI
2. **Execution History**: No API for viewing rule execution logs (UI only)
3. **Bulk Operations**: No dedicated bulk enable/disable endpoint (must process sequentially)
4. **Analytics**: No API for rule performance metrics
5. **Audit Trail**: Limited audit information in API responses

---

## Permission Schemes

### When to Use Permission Scheme Scripts

Use these scripts when you need to:
- View, create, update, or delete permission schemes
- Manage permission grants within schemes
- Assign permission schemes to projects
- List all available JIRA permissions
- Clone existing permission schemes with modifications

### Permission Scheme Scripts

| Script | Description |
|--------|-------------|
| `list_permission_schemes.py` | List all permission schemes with optional filtering |
| `get_permission_scheme.py` | Get detailed information about a specific scheme |
| `create_permission_scheme.py` | Create a new permission scheme |
| `update_permission_scheme.py` | Update an existing scheme's metadata or grants |
| `delete_permission_scheme.py` | Delete a permission scheme (must not be in use) |
| `assign_permission_scheme.py` | Assign a scheme to one or more projects |
| `list_permissions.py` | List all available JIRA permissions |

### Permission Scheme Examples

```bash
# List all permission schemes
python list_permission_schemes.py
python list_permission_schemes.py --show-grants
python list_permission_schemes.py --filter "Development"
python list_permission_schemes.py --show-projects

# Get detailed scheme information
python get_permission_scheme.py 10000
python get_permission_scheme.py "Default Software Scheme"
python get_permission_scheme.py 10000 --show-projects
python get_permission_scheme.py 10000 --export-template grants.json

# Create permission schemes
python create_permission_scheme.py --name "New Scheme" --description "Description"
python create_permission_scheme.py --name "New Scheme" --template grants.json
python create_permission_scheme.py --name "New Scheme" --clone 10000
python create_permission_scheme.py --name "New Scheme" \
  --grant "BROWSE_PROJECTS:anyone" \
  --grant "CREATE_ISSUES:group:jira-developers"

# Update permission schemes
python update_permission_scheme.py 10000 --name "Updated Name"
python update_permission_scheme.py 10000 --add-grant "EDIT_ISSUES:group:developers"
python update_permission_scheme.py 10000 --remove-grant 10103
python update_permission_scheme.py 10000 --remove-grant "EDIT_ISSUES:group:testers"

# Delete permission schemes
python delete_permission_scheme.py 10050 --confirm
python delete_permission_scheme.py 10050 --check-only
python delete_permission_scheme.py 10050 --force --confirm

# Assign to projects
python assign_permission_scheme.py --project PROJ --scheme 10050
python assign_permission_scheme.py --projects PROJ1,PROJ2 --scheme "Custom Scheme"
python assign_permission_scheme.py --project PROJ --show-current

# List permissions
python list_permissions.py
python list_permissions.py --type PROJECT
python list_permissions.py --search "issue"
```

### Permission Grant Format

When specifying grants, use the format:
```
PERMISSION:HOLDER_TYPE[:HOLDER_PARAMETER]

Examples:
  BROWSE_PROJECTS:anyone
  CREATE_ISSUES:group:jira-developers
  EDIT_ISSUES:projectRole:Developers
  ADMINISTER_PROJECTS:projectLead
  RESOLVE_ISSUES:user:5b10a2844c20165700ede21g
```

### Holder Types

| Type | Description | Parameter Required |
|------|-------------|-------------------|
| `anyone` | All users (logged in or anonymous) | No |
| `group` | JIRA group | Group name |
| `projectRole` | Project role | Role name |
| `user` | Specific user | Account ID |
| `projectLead` | Project lead | No |
| `reporter` | Issue reporter | No |
| `currentAssignee` | Current issue assignee | No |
| `applicationRole` | Application role | Role key |

### Common Permission Keys

**Project Permissions:**
- `BROWSE_PROJECTS` - View projects and issues
- `CREATE_ISSUES` - Create issues
- `EDIT_ISSUES` - Edit issues
- `DELETE_ISSUES` - Delete issues
- `ASSIGN_ISSUES` - Assign issues
- `ASSIGNABLE_USER` - Be assigned to issues
- `RESOLVE_ISSUES` - Resolve/reopen issues
- `CLOSE_ISSUES` - Close issues
- `TRANSITION_ISSUES` - Transition issues
- `MOVE_ISSUES` - Move issues between projects
- `LINK_ISSUES` - Link issues
- `ADD_COMMENTS` - Add comments
- `EDIT_ALL_COMMENTS` - Edit all comments
- `DELETE_ALL_COMMENTS` - Delete all comments
- `CREATE_ATTACHMENTS` - Create attachments
- `WORK_ON_ISSUES` - Log work on issues
- `ADMINISTER_PROJECTS` - Administer projects
- `MANAGE_SPRINTS` - Manage sprints
- `MANAGE_WATCHERS` - Manage watchers

### Permission Scheme Permission Requirements

| Operation | Required Permission |
|-----------|---------------------|
| List/view schemes | Permission to access Jira |
| Create scheme | Administer Jira (global) |
| Update scheme | Administer Jira (global) |
| Delete scheme | Administer Jira (global) |
| Assign to project | Administer Jira (global) |
| List permissions | None (public endpoint) |
