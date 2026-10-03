---
description: Commit all project changes except ephemeral ./.agents/tmp state. Never amend.
---


# my-git-commit

## Invocation

Explicit-only Antigravity workflow. Run `/my-git-commit`; never trigger it through semantic skill matching.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

Commit all project changes except `./.agents/tmp/`.

Before staging, ensure `./.agents/tmp/` remains excluded and untouched. Never amend an existing commit.
