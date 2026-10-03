# my-git-commit

Git commit all project changes except ephemeral ./.agents/tmp state. Never amends.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-git-commit/SKILL.md` | `/my-git-commit` |
| Codex | `.agents/skills/my-git-commit/SKILL.md` + `agents/openai.yaml` | `$my-git-commit` |
| Claude Code | `.claude/skills/my-git-commit/SKILL.md` | `/my-git-commit` |
| Antigravity | `.agents/workflows/my-git-commit.md` | `/my-git-commit` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
