---
name: my-git-commit
description: Commit all project changes except ephemeral ./.agents/tmp state. Never amend.
license: MIT
compatibility: Claude Code with native skill controls and project subagents.
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional context]"
metadata:
  version: "2.5.1"
---

# my-git-commit

## Invocation

Explicit-only Claude Code workflow. Run `/my-git-commit`; never invoke it implicitly.

Treat `$ARGUMENTS` plus immediately relevant conversation context as the invocation input.

Commit all project changes except `./.agents/tmp/`.

Before staging, ensure `./.agents/tmp/` remains excluded and untouched. Never amend an existing commit.
