# Changelog

## 4.6.0 — 2026-11-13

- Removed `/my-golang-codebase-design`. The installer reports an already installed copy as a leftover and does not delete it.

## 4.5.0 — 2026-11-13

- `/my-spec-review`: asks for `FIX_SCOPE` before the first cycle: `BLOCKING_ONLY` (previous behavior), `ALL` (fix blocking and non-blocking problems until a fresh review finds none), or `BLOCKING_THEN_ALL` (clear blocking problems first, then fix the accumulated non-blocking notes and loop until none remain).

## 4.4.1 — 2026-11-08

- `/my-spec-review`: the verifier classifies problems as `BLOCKING` or `NON_BLOCKING`; only blocking problems are fixed and drive the loop. Non-blocking problems are kept as notes, passed to later verifiers so they are not re-verified, and listed in the final report.

## 4.4.0 — 2026-11-08

- Added `/my-spec-review`: loops a fresh read-only verification of a spec and its issues (traceability, contradictions, testability, terminology), fixes every problem through the configured tracker, and stops only when a new fresh verification is clean, bounded by `MAX_REVIEW_CYCLES`. Product/domain decisions go to the user; nothing is committed or pushed.

## 4.3.0 — 2026-11-01

- Added `/my-golang-codebase-design`: reshapes Go packages into deep modules with Matt Pocock's `codebase-design` skill (mandatory; `BLOCKED` when missing) plus the available Go skills. Every package gets a narrow facade and an `internal/<domain>`; the command migrates one package at a time in dependency order, preserves behavior and public contracts, validates with `go build`, `go vet`, tests and the Makefile allowlist gate, and records the decision with a new ADR plus a `Package layout` section in `CODING_STANDARDS.md`. `cmd/*` is excluded.
- The command is explicit-only, like the other improvement workflows, and does not review or commit.

## 4.2.0 — 2026-10-31

- `my-grill-to-implementation`: `codebase-design` is now mandatory, like `tdd`, in every slice and fix pass; a missing mandatory skill blocks the slice, while a missing language/tool skill does not. The workflow diagrams and the `AGENTS.md` contract now read `develop(tdd+codebase-design)`.
- `my-implement-orchestrator`: the workflow diagram names `codebase-design`, and the review loop requires the fix pass to load the mandatory `tdd` and `codebase-design` skills, so the requirement no longer lives only in the Develop section.
- `scripts/validate.py` and `AGENTS.md` treat the new diagram token and the mandatory skill as invariants for both workflows.

## 4.1.0 — 2026-10-31

- Added `/asd-ste100`: sets the ASD-STE100 response style for the session, with level 80 as default, an optional scope for in-chat documents, and `help`, `status`, and `off`. Without arguments it asks level and scope with the native `question` tool; explicit arguments skip the question.
- Added `source/shared/response-style.md` as the single canonical response-style source. `scripts/build.py` injects it into every generated command and skill at default level 80.
- Every command and skill now asks the parent to write the active directive into each subagent prompt; subagents reply with the same style and keep their report schema.
- Reporter/verdict contracts take precedence over style: required fields, evidence, file paths, and schema stay complete.

## 4.0.0 — 2026-10-24

- The five user-invoked workflows now ship as native OpenCode V2 commands under `commands/` instead of autoinvoke-disabled skills: `my-grill-to-implementation`, `my-implement-orchestrator`, `my-improve-code`, `my-improve-comments`, `my-improve-spacing`. Slash invocation (`/name`) is unchanged; OpenCode no longer exposes them to model skill discovery.
- `source/commands/` is the canonical source for those workflows; `source/skills/` keeps only `my-software-design-doc`, the one model-invokable skill.
- `scripts/build.py` generates `dist/.opencode/commands/*.md` with `$ARGUMENTS` invocation blocks and OpenCode role mappings; the installer installs them at project or global scope.
- Installer now reports the 3.x skill copies of the converted workflows as removable leftovers; it still never deletes files.

## 3.4.0 — 2026-10-22

- `my-implement-orchestrator`: `codebase-design` is now required; every develop/fix pass loads `tdd` and `codebase-design` plus the available language/framework/tool skills.

## 3.3.0 — 2026-10-10

- Installer never overwrites existing agents (`agents/*.md`), not even with `--force`; only skills are overwritten.

## 3.2.0 — 2026-10-10

- `my-grill-to-implementation`: the plan is now a `spec.md` (slices, no per-slice tickets) in the spec folder defined by `docs/agents/issue-tracker.md` (set up by `/setup-matt-pocock-skills`; `BLOCKED` if missing) and is committed as the last commit; the ledger stays temporary in `./.agents/tmp/` and is never committed.
- `my-grill-to-implementation` and `my-implement-orchestrator`: development/fix subagents must stop at and return edge cases; the orchestrator decides when the spec/SPEC defines the behavior, otherwise asks the user.

## 3.1.1 — 2026-10-06

- `my-grill-to-implementation`: every slice must be implemented by a subagent, never directly by the orchestrator; the final fresh review is unchanged.

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
