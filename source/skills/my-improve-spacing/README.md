# my-improve-spacing

Improve logical blank-line spacing with batched develop subagents.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-improve-spacing/SKILL.md` | `/my-improve-spacing` |
| Codex | `.agents/skills/my-improve-spacing/SKILL.md` + `agents/openai.yaml` | `$my-improve-spacing` |
| Claude Code | `.claude/skills/my-improve-spacing/SKILL.md` | `/my-improve-spacing` |
| Antigravity | `.agents/workflows/my-improve-spacing.md` | `/my-improve-spacing` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
