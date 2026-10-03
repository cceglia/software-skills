# Migration notes — 2.2

## Runtime state

Ephemeral workflow state now lives only under:

```text
./.agents/tmp/grill/<plan-slug>.md
./.agents/tmp/implementation/<work-slug>.md
```

`my-update-skills-list` and `skills.json` were removed. Skill selection now uses the active harness's native discovery, and delegated workers must actually load every selected skill or return `BLOCKED`.

The installer can add this local Git exclude rule:

```text
/.agents/tmp/
```

It does not ignore `.agents/` as a whole because skills, Antigravity workflows/rules, and other project configuration may be intentionally versioned there.

## Native harness adapters

- **OpenCode V2:** `.opencode/skills`, native invocation metadata, built-in `explore`, bundled `develop`/`review` subagents.
- **Codex:** `.agents/skills`, `agents/openai.yaml`, and `.codex/agents/*.toml`.
- **Claude Code:** `.claude/skills`, native invocation fields, and `.claude/agents/*`; `my-review-changes` uses a forked `review` agent.
- **Antigravity:** explicit workflows in `.agents/workflows/`, semantic design-doc skill in `.agents/skills/`, plus `.agents/agents.md` and `.agents/rules/`.

The canonical source remains harness-neutral; `scripts/build.py` generates native projections.

## Installer

Interactive:

```bash
npx --yes github:cceglia/software-skills
```

Non-interactive example:

```bash
npx --yes github:cceglia/software-skills \
  --harness all \
  --layout native
```

See `README.md` for all parameters and examples.
