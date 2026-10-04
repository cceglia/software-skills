---
name: my-review-changes
description: Independently review specified modified files or the current working-tree changes without editing them.
license: MIT
compatibility: Claude Code with native skill controls and project subagents.
disable-model-invocation: true
user-invocable: true
argument-hint: "[files | directory | glob]"
context: fork
agent: review
background: false
metadata:
  version: "2.5.1"
---

# my-review-changes

## Invocation

Explicit-only Claude Code workflow. Run `/my-review-changes`; never invoke it implicitly.

Treat `$ARGUMENTS` plus immediately relevant conversation context as the invocation input.

## Harness role

Claude Code frontmatter already runs this workflow in the bundled `review` subagent; do not delegate again.

Resolve scope from the invocation input. Explicit paths/globs/directories limit the review; empty input means staged, unstaged, and untracked working-tree changes.

Always exclude `./.agents/tmp/`. Exclude generated, vendored, third-party, and build-artifact files unless explicitly requested or materially relevant to a manually authored change.

If nothing relevant changed, report that and stop. A full review may be skipped only when all relevant changes are clearly mechanical and low-risk (for example whitespace-, comment-, documentation-, or formatter-only changes with no semantic effect). In that case return:

```text
VERDICT: REVIEW_NOT_NEEDED
REASON: ...
FILES: ...
```

This skill already runs in a fresh bundled `review` subagent via its Claude Code frontmatter. Review the resolved files, complete diff, repository instructions/standards, and available validation results directly; do not delegate again. Review correctness/regressions, scope, compatibility, security/performance where relevant, repository standards, misleading comments/spacing, and missing tests.

The reviewer must not edit, fix, stage, commit, push, reset, clean, stash, or delegate.

Return:

```text
VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED
SUMMARY: ...
FINDINGS: ...
VALIDATION: ...
REVIEWED_FILES: ...
```

This workflow never fixes findings or commits changes.
