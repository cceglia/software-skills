---
name: my-review-changes
description: Independently review specified modified files or the current working-tree changes without editing them.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "2.2.0"
  opencode/autoinvoke: false
  opencode/slash: true
---

# my-review-changes

## Invocation

Explicit-only OpenCode V2 workflow. Run `/my-review-changes`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use OpenCode V2 child sessions: built-in `explore` plus bundled `develop` and `review`.

Resolve scope from the invocation input. Explicit paths/globs/directories limit the review; empty input means staged, unstaged, and untracked working-tree changes.

Always exclude `./.agents/tmp/`. Exclude generated, vendored, third-party, and build-artifact files unless explicitly requested or materially relevant to a manually authored change.

If nothing relevant changed, report that and stop. A full review may be skipped only when all relevant changes are clearly mechanical and low-risk (for example whitespace-, comment-, documentation-, or formatter-only changes with no semantic effect). In that case return:

```text
VERDICT: REVIEW_NOT_NEEDED
REASON: ...
FILES: ...
```

Otherwise use one fresh independent read-only `review` role. Pass the resolved files, complete diff, repository instructions/standards, and available validation results. Review correctness/regressions, scope, compatibility, security/performance where relevant, repository standards, misleading comments/spacing, and missing tests.

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
