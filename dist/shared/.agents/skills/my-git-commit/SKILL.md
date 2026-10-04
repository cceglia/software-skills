---
name: my-git-commit
description: Explicit-only workflow. Commit all project changes except ephemeral ./.agents/tmp state. Never amend.
license: MIT
compatibility: Shared Agent Skills profile for Codex, Claude Code, OpenCode V2, and Antigravity; native support files install separately.
metadata:
  version: "2.5.1"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-git-commit

## Invocation

Explicit-only workflow. Run it only when the user explicitly requests it by name; never invoke it implicitly.

Treat command/skill arguments plus immediately relevant conversation context as the invocation input.

Commit all project changes except `./.agents/tmp/`.

Before staging, ensure `./.agents/tmp/` remains excluded and untouched. Never amend an existing commit.
