# my-software-design-doc

Create or review software design documents for greenfield or existing software projects. Interactively discover requirements, ask for missing information, delegate broad codebase exploration to isolated exploration subagents, and focus the document on consequential decisions, trade-offs, interfaces, operability, security, and unresolved questions.

This directory is the **canonical multi-harness source**. Do not install it directly when native harness behavior matters; run `python3 scripts/build.py` from the repository root and install the corresponding generated profile.

## Native mapping

| Harness | Native surface | Invocation |
| --- | --- | --- |
| OpenCode V2 | `.opencode/skills/my-software-design-doc/SKILL.md` | semantic/on-demand |
| Codex | `.agents/skills/my-software-design-doc/SKILL.md` + `agents/openai.yaml` | semantic or `$my-software-design-doc` |
| Claude Code | `.claude/skills/my-software-design-doc/SKILL.md` | semantic or `/my-software-design-doc` |
| Antigravity | `.agents/skills/my-software-design-doc/SKILL.md` | semantic/on-demand |

Harness-specific invocation controls, permissions, subagents/personas, and metadata are added by the build adapter. Ephemeral workflow state is stored under `./.agents/tmp/`. Skill routing uses the active harness's native discovery.
