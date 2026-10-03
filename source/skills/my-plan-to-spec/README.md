# my-plan-to-spec

Turn a completed grilling state and resolved plan into a reviewed, implementation-ready SPEC and publish it through the configured tracker.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-plan-to-spec/SKILL.md` | `/my-plan-to-spec` |
| Codex | `.agents/skills/my-plan-to-spec/SKILL.md` + `agents/openai.yaml` | `$my-plan-to-spec` |
| Claude Code | `.claude/skills/my-plan-to-spec/SKILL.md` | `/my-plan-to-spec` |
| Antigravity | `.agents/workflows/my-plan-to-spec.md` | `/my-plan-to-spec` |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
