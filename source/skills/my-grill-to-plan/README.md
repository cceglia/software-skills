# my-grill-to-plan

Interview the user and inspect the repository to produce a complete implementation plan in chat while continuously persisting grilling state.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-grill-to-plan/SKILL.md` | `/my-grill-to-plan` |
| Codex | `.agents/skills/my-grill-to-plan/SKILL.md` + `agents/openai.yaml` | `$my-grill-to-plan` |
| Claude Code | `.claude/skills/my-grill-to-plan/SKILL.md` | `/my-grill-to-plan` |
| Antigravity | `.agents/workflows/my-grill-to-plan.md` | `/my-grill-to-plan` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
