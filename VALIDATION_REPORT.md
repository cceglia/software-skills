# Validation report — 4.2.0

Validated on 2026-10-31.

## Passed

- root `AGENTS.md` is present and contains the required maintenance invariants;
- 6 canonical commands and 1 canonical skill;
- the OpenCode V2 profile builds into `dist/.opencode/` (`commands/`, `skills/`, `agents/`) and is the only generated profile;
- user-invoked workflows are commands with `$ARGUMENTS`, never model-discoverable skills;
- `source/shared/response-style.md` is the only canonical response-style source; every generated command and skill carries it at default level 80;
- `/asd-ste100` asks level and scope with the native `question` tool only without arguments, supports `help`, `status`, `off`, `replies`, and `docs`, and keeps the style active for the session;
- every command and skill writes the active directive into subagent prompts, and report/verdict contracts keep precedence over style;
- `my-grill-to-implementation` maps `explore`, `develop`, and `review`, commits per slice, loads `tdd` and `codebase-design` in every develop/fix pass, and gates the change with a final fresh review;
- `my-implement-orchestrator` maps `develop`, commits per ticket, loads `tdd` and `codebase-design` in every develop/fix pass including review fixes, reviews only important tickets individually, and gates tracker finalization with a final `code-review`;
- no generated `skills.json`; runtime state stays under `./.agents/tmp/implementation`;
- installer tests passed;
- `npm pack --dry-run` includes `AGENTS.md` and the hidden `dist/.opencode/` directory.
