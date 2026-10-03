---
name: my-git-commit
description: Commit all project changes except ephemeral ./.agents/tmp state. Never amend.
license: MIT
compatibility: Codex with native Agent Skills sidecars and project agents.
metadata:
  version: "2.2.0"
---

# my-git-commit

## Invocation

Explicit-only Codex workflow. Invoke `$my-git-commit`; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

Commit all project changes except `./.agents/tmp/`.

Before staging, ensure `./.agents/tmp/` remains excluded and untouched. Never amend an existing commit.
