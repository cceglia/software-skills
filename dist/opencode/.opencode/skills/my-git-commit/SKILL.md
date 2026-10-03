---
name: my-git-commit
description: Commit all project changes except ephemeral ./.agents/tmp state. Never amend.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "2.2.0"
  opencode/autoinvoke: false
  opencode/slash: true
---

# my-git-commit

## Invocation

Explicit-only OpenCode V2 workflow. Run `/my-git-commit`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

Commit all project changes except `./.agents/tmp/`.

Before staging, ensure `./.agents/tmp/` remains excluded and untouched. Never amend an existing commit.
