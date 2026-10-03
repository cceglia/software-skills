# Native harness references

These adapters were checked against the following current product documentation on 2026-10-03.

## OpenCode V2

- Skills: https://opencode.ai/v2/docs/skills
- Agents: https://opencode.ai/v2/docs/agents
- Permissions: https://opencode.ai/v2/docs/permissions

Adapter assumptions: `.opencode/skills`, `slash`, `metadata.opencode/autoinvoke`, `metadata.opencode/slash`, V2 `subagent`, ordered `permissions`, built-in `explore`, project custom subagents.

## OpenAI Codex

- Skills: https://developers.openai.com/codex/skills
- Subagents: https://developers.openai.com/codex/subagents

Adapter assumptions: repo/user skills under `.agents/skills`, optional `agents/openai.yaml`, `policy.allow_implicit_invocation`, explicit `$skill` invocation, project custom agents under `.codex/agents/*.toml`, and `sandbox_mode`.

## Claude Code

- Skills: https://code.claude.com/docs/en/skills
- Subagents: https://code.claude.com/docs/en/sub-agents

Adapter assumptions: `.claude/skills`, `disable-model-invocation`, `user-invocable`, `argument-hint`, `context: fork`, `agent`, `background`, project `.claude/agents`, and `permissionMode`.

## Google Antigravity / Antigravity IDE

- Getting started / skills: https://codelabs.developers.google.com/getting-started-google-antigravity
- Skills authoring: https://codelabs.developers.google.com/getting-started-with-antigravity-skills
- Workflows and rules example: https://codelabs.developers.google.com/sdd-adk-antigravity
- `agents.md` personas + slash workflow example: https://codelabs.developers.google.com/autonomous-ai-developer-pipelines-antigravity

Adapter assumptions: project `.agents/skills`, slash-triggered `.agents/workflows`, persistent `.agents/rules`, and team personas in `.agents/agents.md`.

## Maintenance rule

Harness-specific adapters are intentionally generated. Re-check these references before changing native frontmatter, project directories, agent configuration, invocation controls, or permission semantics.
