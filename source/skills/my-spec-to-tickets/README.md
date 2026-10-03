# my-spec-to-tickets

Decompose an approved SPEC into concise implementation tickets, review only the tickets, and publish them through the configured tracker.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-spec-to-tickets/SKILL.md` | `/my-spec-to-tickets` |
| Codex | `.agents/skills/my-spec-to-tickets/SKILL.md` + `agents/openai.yaml` | `$my-spec-to-tickets` |
| Claude Code | `.claude/skills/my-spec-to-tickets/SKILL.md` | `/my-spec-to-tickets` |
| Antigravity | `.agents/workflows/my-spec-to-tickets.md` | `/my-spec-to-tickets` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
