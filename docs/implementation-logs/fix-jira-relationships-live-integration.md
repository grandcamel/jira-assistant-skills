# jira-relationships Live Integration Test Fixes

## Summary
- Tests run: 47
- Passed: 47
- Fixed: 7

## Failures Found

All 7 failures were in `test_blocker_chain.py` related to incorrect JIRA link direction semantics:

1. `TestDirectBlockers::test_get_direct_blockers_inward` - Expected issue A, found issue C
2. `TestDirectBlockers::test_get_direct_blockers_outward` - Expected 1+ blocker, found 0
3. `TestRecursiveBlockers::test_recursive_blocker_chain` - Expected 2+ blockers, found 0
4. `TestRecursiveBlockers::test_recursive_with_depth_limit` - Expected 1+ blocker, found 0
5. `TestRecursiveBlockers::test_recursive_outward_direction` - Expected 2+ blockers, found 0
6. `TestBlockerChainOutput::test_all_blockers_flattened` - Expected 2+ all_blockers, found 0
7. `TestBlockerChainOutput::test_tree_structure_preserved` - Expected 1+ blockers, found 0

## Root Cause

The `extract_blockers()` function in `get_blockers.py` had inverted logic for JIRA link direction semantics.

When fetching links for issue B where "A blocks B":
- The link returned has `outwardIssue=A` (A is on the "blocks" side)
- The link has NO `inwardIssue` because B itself is the inward issue

The original code incorrectly looked for:
- `direction='inward'` -> `inwardIssue` field
- `direction='outward'` -> `outwardIssue` field

The correct logic is:
- `direction='inward'` (find issues blocking us) -> look for `outwardIssue`
- `direction='outward'` (find issues we block) -> look for `inwardIssue`

## Fixes Applied

**File:** `.claude/skills/jira-relationships/scripts/get_blockers.py`

Updated `extract_blockers()` function to swap the direction logic:

```python
# Before (incorrect):
if direction == 'inward' and 'inwardIssue' in link:
    issue = link['inwardIssue']
elif direction == 'outward' and 'outwardIssue' in link:
    issue = link['outwardIssue']

# After (correct):
if direction == 'inward' and 'outwardIssue' in link:
    # Issues that block this issue - they appear as outwardIssue
    # because this issue is on the "is blocked by" (inward) side
    issue = link['outwardIssue']
elif direction == 'outward' and 'inwardIssue' in link:
    # Issues that this issue blocks - they appear as inwardIssue
    # because this issue is on the "blocks" (outward) side
    issue = link['inwardIssue']
```

Also added detailed docstring explaining JIRA link semantics to prevent future confusion.

## Final Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.0.2, pluggy-1.6.0
collected 47 items

test_blocker_chain.py::TestDirectBlockers::test_get_direct_blockers_inward PASSED
test_blocker_chain.py::TestDirectBlockers::test_get_direct_blockers_outward PASSED
test_blocker_chain.py::TestDirectBlockers::test_get_blockers_no_blockers PASSED
test_blocker_chain.py::TestDirectBlockers::test_extract_blockers_function PASSED
test_blocker_chain.py::TestRecursiveBlockers::test_recursive_blocker_chain PASSED
test_blocker_chain.py::TestRecursiveBlockers::test_recursive_with_depth_limit PASSED
test_blocker_chain.py::TestRecursiveBlockers::test_recursive_outward_direction PASSED
test_blocker_chain.py::TestCircularDetection::test_circular_blocker_detection PASSED
test_blocker_chain.py::TestCircularDetection::test_visited_set_prevents_infinite_loop PASSED
test_blocker_chain.py::TestBlockerMetadata::test_blocker_includes_status PASSED
test_blocker_chain.py::TestBlockerMetadata::test_blocker_includes_summary PASSED
test_blocker_chain.py::TestBlockerMetadata::test_resolved_blocker_status PASSED
test_blocker_chain.py::TestBlockerChainOutput::test_all_blockers_flattened PASSED
test_blocker_chain.py::TestBlockerChainOutput::test_tree_structure_preserved PASSED
test_clone_issue.py::TestBasicCloning::test_clone_simple_issue PASSED
test_clone_issue.py::TestBasicCloning::test_clone_with_custom_summary PASSED
test_clone_issue.py::TestBasicCloning::test_clone_preserves_priority PASSED
test_clone_issue.py::TestBasicCloning::test_clone_preserves_labels PASSED
test_clone_issue.py::TestCloneLink::test_clone_creates_cloners_link PASSED
test_clone_issue.py::TestCloneLink::test_clone_without_link PASSED
test_clone_issue.py::TestCloneWithSubtasks::test_clone_with_subtasks PASSED
test_clone_issue.py::TestCloneWithSubtasks::test_clone_without_subtasks PASSED
test_clone_issue.py::TestCloneWithLinks::test_clone_with_links PASSED
test_clone_issue.py::TestCloneWithLinks::test_clone_without_links PASSED
test_clone_issue.py::TestCloneFieldExtraction::test_extract_fields_basic PASSED
test_clone_issue.py::TestCloneFieldExtraction::test_extract_fields_to_different_project PASSED
test_clone_issue.py::TestCloneFieldExtraction::test_extract_fields_summary_prefixed PASSED
test_clone_issue.py::TestCloneEdgeCases::test_clone_issue_with_description PASSED
test_clone_issue.py::TestCloneEdgeCases::test_clone_bug_issue_type PASSED
test_clone_issue.py::TestCloneEdgeCases::test_clone_story_issue_type PASSED
test_clone_issue.py::TestCloneEdgeCases::test_clone_result_structure PASSED
test_link_lifecycle.py::TestLinkTypeDiscovery::test_get_all_link_types PASSED
test_link_lifecycle.py::TestLinkTypeDiscovery::test_link_type_structure PASSED
test_link_lifecycle.py::TestLinkTypeDiscovery::test_common_link_types_available PASSED
test_link_lifecycle.py::TestLinkCreation::test_create_relates_link PASSED
test_link_lifecycle.py::TestLinkCreation::test_create_blocks_link PASSED
test_link_lifecycle.py::TestLinkCreation::test_create_duplicate_link PASSED
test_link_lifecycle.py::TestLinkCreation::test_create_multiple_links PASSED
test_link_lifecycle.py::TestLinkRetrieval::test_get_issue_links PASSED
test_link_lifecycle.py::TestLinkRetrieval::test_get_link_by_id PASSED
test_link_lifecycle.py::TestLinkRetrieval::test_link_contains_issue_info PASSED
test_link_lifecycle.py::TestLinkRetrieval::test_get_links_empty_issue PASSED
test_link_lifecycle.py::TestLinkDeletion::test_delete_link PASSED
test_link_lifecycle.py::TestLinkDeletion::test_delete_all_links_from_issue PASSED
test_link_lifecycle.py::TestLinkDeletion::test_delete_link_affects_both_issues PASSED
test_link_lifecycle.py::TestLinkDirectionality::test_blocks_link_direction PASSED
test_link_lifecycle.py::TestLinkDirectionality::test_relates_link_is_symmetric PASSED

======================== 47 passed in 181.42s (0:03:01) ========================
```
