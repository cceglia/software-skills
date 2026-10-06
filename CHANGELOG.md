# Changelog

## 3.1.0 — 2026-10-06

- Per-ticket/per-slice review is now exceptional: only for a high and concrete risk (data migration, data-loss risk, new security boundary), announced to the user beforehand. Public contracts or dependent tickets no longer qualify.

## 3.0.0 — 2026-10-06

- OpenCode V2-only distribution: removed the Codex, Claude Code, Antigravity, and shared `.agents/skills` profiles; `dist/.opencode/` is the only generated profile.
- Installer now asks for install scope: project (`<target>/.opencode`) or global (`~/.config/opencode`, honoring `$OPENCODE_CONFIG_DIR` and `$XDG_CONFIG_HOME`). `--scope` replaces `--harness`/`--layout`.
- Removed `my-grill-to-spec`, `my-spec-to-tickets`, `my-review-changes`, and `my-git-commit`: use Matt Pocock's skills directly. Removed the `./.agents/tmp/grill/` ledger.
- `my-grill-to-implementation`: per-slice `develop(tdd) -> validation green -> commit`, then one fresh review of the whole change with `fix -> commit -> new fresh review` cycles (max 3).
- `my-implement-orchestrator`: per-ticket `develop(tdd) -> validation green -> commit`, an individual `code-review` only for important tickets, and a final `code-review` with `fix -> commit -> new code-review` cycles before tracker finalization.
- Both workflows work only in the current checkout (no worktrees, branches, pull requests, or pushes) and run roles sequentially.
- Installer lists removed skills still present in the destination, without deleting them.

## 2.5.1 — 2026-10-04

- Added root `AGENTS.md` as the concise maintenance contract for future agents.
- Documented canonical-source, no-duplication, runtime-ledger, Matt Pocock composition, harness-native, and validation invariants.
- Added `AGENTS.md` to the npm package payload.
- Validation now treats the repository guidance as a required architectural artifact.

## 2.5.0 — 2026-10-03

- Clarified canonical SPEC/ticket ownership: Matt Pocock's configured issue tracker owns them; `.agents/tmp` contains only resumable ledgers.
- `my-grill-to-spec` now explicitly stops after canonical SPEC publication plus fresh independent review.
- `my-grill-to-implementation` uses Matt's `tdd` inside develop/fix passes while preserving explicit explore/develop/review subagents.
- `my-implement-orchestrator` now runs `develop(tdd) -> code-review -> fix(tdd) -> new code-review` until clean or the configured review-cycle limit.
- Removed the invalid orchestrator dependency on Matt's user-only `implement`; `implement-spec` remains an optional user-invoked upstream alternative, not an orchestrator dependency.

## 2.4.0 — 2026-10-03

- Made both grill workflows explicitly resumable from `./.agents/tmp/` ledgers.
- `my-grill-to-spec` now composes `grill-with-docs` + `to-spec`.
- `my-grill-to-implementation` now uses `explore`, `develop`, and fresh `review` subagents for the development phase.
- `my-spec-to-tickets` now delegates decomposition and publishing to `to-tickets`.

## 2.3.0 — 2026-10-03

- Replaced `my-grill-to-plan` + `my-plan-to-spec` with `my-grill-to-spec`.
- `my-grill-to-spec` invokes Matt Pocock's `grill-with-docs` and preserves its `CONTEXT.md`/ADR conventions.
- The configured tracker SPEC is updated after every grill round and acts as the sole planning ledger.
- Removed duplicate `./.agents/tmp/grill/` state; only direct implementation keeps resumable runtime state.

## 2.2.0 — 2026-10-03

- Removed `my-update-skills-list` and the generated `skills.json` registry.
- Switched implementation workflows to native harness skill discovery with explicit worker load verification.
- Moved all ephemeral workflow state under `./.agents/tmp/`.
- Changed the installer Git-exclude rule to `/.agents/tmp/`.
- Reduced canonical skill size and removed duplicated workflow instructions.
- Kept harness-native invocation metadata, agents, workflows, rules, and Codex sidecars.

## 2.1.0 — 2026-10-03

- Added the custom zero-dependency Node.js installer with interactive harness/layout selection.
- Added non-interactive `--harness`, `--layout`, `--target`, `--force`, `--dry-run`, and `--git-exclude` options.
- Added the shared `.agents/skills` profile and Codex + Antigravity collision handling.

## 2.0.0 — 2026-10-03

- Introduced one canonical workflow source plus native OpenCode V2, Codex, Claude Code, and Antigravity adapters.
