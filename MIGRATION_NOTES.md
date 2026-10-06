# Migration notes

## 3.0.0

- OpenCode V2 only. The Codex, Claude Code, Antigravity, and shared `.agents/skills` profiles are gone, and with them `--harness`/`--layout`. Use `--scope project|global` (or answer the interactive prompt). Skills and agents now install together under `.opencode/` or `~/.config/opencode`.
- `my-grill-to-spec`, `my-spec-to-tickets`, `my-review-changes`, and `my-git-commit` were removed: use `grill-with-docs` + `to-spec`, `to-tickets`, and `code-review` directly. The `./.agents/tmp/grill/` ledger no longer exists.
- `my-grill-to-implementation` now commits per slice and reviews the whole change once at the end (fix -> commit -> new fresh review). Ledgers from earlier versions record a single final commit; on resume, the workflow reconciles them with the current HEAD and continues with the new flow.
- `my-implement-orchestrator` commits per ticket, reviews a ticket individually only for a high and concrete risk (data migration, data-loss risk, new security boundary), then runs a final `code-review` before tracker finalization. Reinstall with `--force` to replace older copies.
