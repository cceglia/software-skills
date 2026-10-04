---
name: my-review-changes
description: Explicit-only workflow. Independently review specified modified files or the current working-tree changes without editing them.
license: MIT
compatibility: Shared Agent Skills profile for Codex, Claude Code, OpenCode V2, and Antigravity; native support files install separately.
metadata:
  version: "2.5.1"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-review-changes

## Invocation

Explicit-only workflow. Run it only when the user explicitly requests it by name; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

## Harness roles

Use the active harness's installed support roles: `review`.

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
