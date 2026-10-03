# my-improve-code

Improve comments/documentation and logical spacing with batched develop subagents, without changing behavior.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-improve-code/SKILL.md` | `/my-improve-code` |
| Codex | `.agents/skills/my-improve-code/SKILL.md` + `agents/openai.yaml` | `$my-improve-code` |
| Claude Code | `.claude/skills/my-improve-code/SKILL.md` | `/my-improve-code` |
| Antigravity | `.agents/workflows/my-improve-code.md` | `/my-improve-code` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
