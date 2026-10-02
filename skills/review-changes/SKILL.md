---
name: review-changes
description: Review a specified set of modified files, or the current working-tree changes, using one independent read-only review subagent.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# review-changes

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/review-changes`. Do not select or invoke it implicitly.

Treat the user's explicit slash request, including any text supplied with it and the immediately relevant conversation context, as the **invocation input**. If the workflow cannot resolve a required input from that information, follow the skill's own missing-input behavior.

Review modified files without editing them.

Files/scope:

```text
invocation input
```

## Resolve review scope

If `invocation input` contains file paths, globs, or a directory, review only the corresponding modified files.

If `invocation input` is empty, resolve the modified files from the current working tree, including staged, unstaged, and untracked files where applicable.

Exclude generated, vendored, third-party, and build-artifact files unless they are explicitly requested or materially relevant to a manually authored change.

If there are no relevant modified files, report that there is nothing to review and stop.

## Decide whether a review is warranted

Inspect only enough metadata/diff summary to classify the changes.

A full review MAY be skipped when all relevant changes are clearly mechanical and low-risk, for example:

- whitespace-only changes;
- comment/documentation-only changes with no executable-code edits;
- formatter-only changes with no semantic diff.

If review is skipped, report:

```text
VERDICT: REVIEW_NOT_NEEDED
REASON: ...
FILES: ...
```

If there is any uncertainty about semantic impact, mixed change types, executable-code modification, API/config/migration/test behavior, or repository-standard compliance, perform the review.

## Review

Use exactly one active subagent.

Start one read-only `review` subagent and pass:

- the resolved changed-file list;
- the complete diff for those files;
- applicable repository instructions;
- `CODING_STANDARDS.md` when present;
- relevant tests/validation results if already available.

The reviewer should inspect the diff first and open surrounding source only when necessary.

Review for:

- unintended behavior changes;
- correctness and regressions;
- API/data/config/migration compatibility;
- security and performance concerns where relevant;
- repository and coding-standard violations;
- stale, misleading, or low-value comments;
- misleading logical spacing;
- unrelated changes or accidental scope expansion;
- missing tests or validation when executable behavior changed.

The reviewer MUST NOT edit, fix, stage, commit, push, reset, clean, stash, or delegate.

Return exactly:

```text
VERDICT: APPROVED | CHANGES_REQUIRED | BLOCKED
SUMMARY: ...
FINDINGS: ...
VALIDATION: ...
REVIEWED_FILES: ...
```

## Final boundary

This command is review-only.

Do not modify files and do not automatically fix findings. If fixes are needed, report them so the caller can choose the appropriate modification command or implementation workflow.
