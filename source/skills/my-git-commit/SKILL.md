---
name: my-git-commit
description: Commit all project changes except ephemeral ./.agents/tmp state. Never amend.
license: MIT
compatibility: Canonical multi-harness source; use scripts/build.py to generate native profiles.
metadata:
  version: "2.5.1"
---

# my-git-commit

Commit all project changes except `./.agents/tmp/`.

Before staging, ensure `./.agents/tmp/` remains excluded and untouched. Never amend an existing commit.
