---
name: my-git-commit
description: Commit all project changes except ephemeral ./.agents/tmp state. Never amend.
license: MIT
compatibility: Canonical Claude Code source; use scripts/build.py to generate the installable profile.
metadata:
  version: "3.0.0"
---

# my-git-commit

Commit all project changes except `./.agents/tmp/`.

Before staging, ensure `./.agents/tmp/` remains excluded and untouched. Never amend an existing commit.
