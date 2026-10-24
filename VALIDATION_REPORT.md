# Validation report — 4.0.0

Validated on 2026-10-24.

## Passed

- root `AGENTS.md` is present and contains the required maintenance invariants;
- 5 canonical commands and 1 canonical skill;
- the OpenCode V2 profile builds into `dist/.opencode/` (`commands/`, `skills/`, `agents/`) and is the only generated profile;
- user-invoked workflows are commands with `$ARGUMENTS`, never model-discoverable skills;
- `my-grill-to-implementation` maps `explore`, `develop`, and `review`, commits per slice, and gates the change with a final fresh review;
- `my-implement-orchestrator` maps `develop`, commits per ticket, reviews only important tickets individually, and gates tracker finalization with a final `code-review`;
- no generated `skills.json`; runtime state stays under `./.agents/tmp/implementation`;
- installer tests passed;
- `npm pack --dry-run` includes `AGENTS.md` and the hidden `dist/.opencode/` directory.
