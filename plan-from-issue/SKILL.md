---
name: plan-from-issue
description: This skill should be used when the user asks to "plan an issue", "create an implementation plan for an issue", "start working on issue #N", or mentions a specific GitHub issue number and wants to understand and plan the implementation.
---

# Plan from GitHub Issue

Fetch a GitHub Issue and create a detailed implementation plan.

## Steps

### 1. Fetch the Issue

```bash
gh issue view {issueNo}
```

Understand the following from the Issue:
- Title and summary
- Requirements and acceptance criteria
- Related existing features

### 2. Investigate the Codebase

Identify files related to the Issue and understand the current state.

- Identify affected Views, Models, and Services
- Review existing implementation patterns
- Map out dependencies

### 3. Create an Implementation Plan

Use the Plan agent to create a detailed implementation plan.

The plan must include:
- **New files to create** — file paths and their roles
- **Existing files to modify** — file paths and what changes are needed
- **Implementation steps** — numbered, ordered steps
- **Gotchas** — technical risks and considerations

### 4. Present the Plan to the User

After presenting the plan, confirm:
- Whether to proceed with implementation
- If any manual Xcode operations are required, state them upfront before coding begins

## Branch Naming Convention

Always create a branch with the following naming convention when starting implementation:

```
feature/{issueNo}-{description}
```

Example: `feature/10-widget-support`
