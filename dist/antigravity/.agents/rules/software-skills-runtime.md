# Software Skills Runtime Rules

- `./.agents/tmp/` is ephemeral runtime state; never stage, commit, or review it.
- Full-path grill ledger: `./.agents/tmp/grill/`.
- Direct implementation ledger: `./.agents/tmp/implementation/`.
- Explicit workflows live in `.agents/workflows/`; `my-software-design-doc` remains a semantic skill.
- Use `.agents/agents.md` when a workflow requests `@explore`, `@develop`, or `@review`.
