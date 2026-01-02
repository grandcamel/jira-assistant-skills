# Deprecated: Local Library Copy

> **Status**: DEPRECATED
> **Replacement**: `jira-assistant-skills-lib` PyPI package
> **Removal Target**: v3.0.0

## Overview

This directory (`shared/scripts/lib/`) contains a legacy copy of the JIRA Assistant Skills library. It has been superseded by the `jira-assistant-skills-lib` PyPI package.

## Migration

All skill scripts have been migrated to use the PyPI package:

```python
# Old (deprecated):
from lib.jira_client import JiraClient

# New (current):
from jira_assistant_skills_lib import JiraClient, get_jira_client
```

## Why This Exists

This directory was the original location of the shared library before it was extracted into a separate PyPI package for:
- Better versioning and dependency management
- Easier installation and updates
- Cleaner separation of concerns
- Reusability in other projects

## Installation

Install the replacement package:

```bash
pip install jira-assistant-skills-lib>=0.2.1
```

Or for the plugin with all dependencies:

```bash
pip install -r plugins/jira-assistant-skills/skills/shared/scripts/lib/requirements.txt
```

## Removal Plan

This directory will be removed in v3.0.0. Until then:

1. Do not add new code to this directory
2. Do not import from this directory directly
3. Use `from jira_assistant_skills_lib import ...` instead

## Files to Remove in v3.0.0

```
shared/scripts/lib/
├── __init__.py
├── adf_helper.py
├── autocomplete_cache.py
├── automation_client.py
├── batch_processor.py
├── cache.py
├── config_manager.py
├── credential_manager.py
├── error_handler.py
├── formatters.py
├── jira_client.py
├── jira_client_new.py (unused)
├── jsm_utils.py
├── permission_helpers.py
├── project_context.py
├── request_batcher.py
├── time_utils.py
├── transition_helpers.py
├── user_helpers.py
└── validators.py
```

The only file that should remain is `requirements.txt` (with updated content pointing to the PyPI package).
