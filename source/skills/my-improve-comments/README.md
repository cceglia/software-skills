# my-improve-comments

Improve code comments and documentation with batched develop subagents.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-improve-comments/SKILL.md` | `/my-improve-comments` |
| Codex | `.agents/skills/my-improve-comments/SKILL.md` + `agents/openai.yaml` | `$my-improve-comments` |
| Claude Code | `.claude/skills/my-improve-comments/SKILL.md` | `/my-improve-comments` |
| Antigravity | `.agents/workflows/my-improve-comments.md` | `/my-improve-comments` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
