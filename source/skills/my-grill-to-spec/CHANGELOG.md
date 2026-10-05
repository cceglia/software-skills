# Changelog — my-grill-to-spec

## 3.0.0 — 2026-10-05

- Claude Code-only profile: installs into project `.claude/skills` or global `~/.claude/skills`.
- Subagent delegation no longer names a subagent type; Claude Code chooses the most suitable subagent.

## 2.5.0 — 2026-10-03

- Canonical SPEC writing remains owned by `to-spec`; only a resumable decision ledger lives under `.agents/tmp`.
- Added an explicit stop after independent SPEC approval; tickets are a separate workflow.
- Clarified that no subagent authors the SPEC; only the post-publish review uses a fresh reviewer.

## 2.4.0 — 2026-10-03

- Added a resumable working SPEC ledger under `./.agents/tmp/grill/`.
- Compose `grill-with-docs` for decisions and `to-spec` for the canonical SPEC.

## 2.3.0 — 2026-10-03

- Replaced `my-grill-to-plan` + `my-plan-to-spec` with one incremental SPEC workflow.
- Delegates interviewing/domain documentation to Matt Pocock's `grill-with-docs`.
- Uses the configured tracker SPEC itself as the ledger and independently reviews it before finalization.
