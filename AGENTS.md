# Repository guidance

This file is the maintenance contract for future agents working on `software-skills`. Keep it concise. Do not duplicate the README, individual skills, or upstream Matt Pocock skill instructions.

## Architecture

- `source/skills/` is the canonical source of truth. Never edit generated files under `dist/` directly.
- `scripts/build.py` generates harness-specific profiles for Codex, Claude Code, OpenCode V2, Antigravity, and the shared `.agents` layout.
- Prefer composition over reimplementation. Matt Pocock skills own their domain behavior; our skills add orchestration, resumability, stronger acceptance loops, and harness adaptation.
- Keep skills short. Put a rule in the narrowest single place that owns it; do not repeat shared concepts across multiple skills.
- Use the active harness's native skill discovery. Do not recreate `skills.json` or another persistent skill registry.
- Harness-specific behavior belongs in generated adapters/support files, not in duplicated canonical workflow bodies.

## Runtime state

- All ephemeral/resumable state owned by this project lives under `./.agents/tmp/`.
- Grill ledgers: `./.agents/tmp/grill/<slug>.md`.
- Light implementation ledgers: `./.agents/tmp/implementation/<slug>.md`.
- `./.agents/tmp/` is never a canonical deliverable and must not be staged, committed, or treated as review scope.
- Canonical SPECs and tickets belong to the issue tracker configured by Matt Pocock's tooling. For the local tracker, that means `.scratch/<feature>/spec.md` and `.scratch/<feature>/issues/<NN>-<slug>.md`.

## Workflow contracts

### `my-grill-to-spec`

Compose Matt Pocock's `grill-with-docs` and `to-spec`. Maintain a resumable decision ledger while grilling, let `to-spec` own canonical SPEC synthesis/publishing, run a fresh independent post-SPEC review, then stop. Do not create tickets or start implementation.

### `my-spec-to-tickets`

Remain a thin wrapper around Matt Pocock's `to-tickets`. Let upstream own decomposition, dependencies, approval quiz, and publishing. Stop after ticket creation.

### `my-grill-to-implementation`

This is the light path for changes that do not justify SPEC + tickets. Use `grill-with-docs`, keep one resumable implementation ledger, then run explicit harness-native `explore -> develop -> fresh review`. Develop/fix passes use Matt Pocock's `tdd`. On findings, run a new develop fix pass followed by a new fresh review. Commit only after approval.

### `my-implement-orchestrator`

This is the full ticket implementation path. Per ticket, enforce:

```text
develop(tdd) -> code-review -> (develop fix(tdd) -> new code-review)* -> commit -> tracker finalization
```

Every fix requires a subsequent clean `code-review`; never commit immediately after fixes. Keep review-cycle limits explicit. Do not replace Matt Pocock's `tdd` or `code-review` with duplicated local rules.

## Deliberately removed workflows

Do not reintroduce these unless the architecture is intentionally changed:

- `my-update-skills-list` and `skills.json`: native harness discovery is the source of truth.
- `my-grill-to-plan`: replaced by `my-grill-to-spec`.
- `my-plan-to-spec`: the grill-to-SPEC workflow already composes `to-spec`.

## Upstream Matt Pocock constraints

Respect upstream invocation policy. Some Matt Pocock workflows such as `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, and `implement-spec` may be marked user-invoked only on strict harnesses. Do not silently patch or pretend those policies do not exist. `my-implement-orchestrator` intentionally composes the model-invokable `tdd` and `code-review` primitives instead of depending on user-only `implement`/`implement-spec`.

## Harness invariants

- Preserve native properties for Codex, Claude Code, OpenCode V2, and Antigravity instead of reducing all targets to a lowest-common-denominator `SKILL.md`.
- Codex-specific skill metadata belongs in `agents/openai.yaml`; project agents belong in `.codex/agents/`.
- Claude Code-specific invocation/context fields and project agents belong in its native `.claude/` structures.
- OpenCode V2-specific slash/autoinvoke metadata and agents belong in `.opencode/` structures.
- Antigravity manual commands belong in `.agents/workflows/`; its roles/rules use the native `.agents/` structures.
- When the installer uses shared `.agents/skills`, install one standards-compatible skill copy and keep harness-specific support artifacts in their native locations.

## Change procedure

1. Change canonical files under `source/` and supporting build/installer code as needed.
2. Update the version/changelog when behavior or packaging changes.
3. Run `python3 scripts/build.py`.
4. Run `python3 scripts/validate.py`.
5. Run `node scripts/test-installer.js`.
6. Verify `npm pack --dry-run` still includes required hidden harness directories and `AGENTS.md`.
7. Never hand-edit `dist/` to fix a generated profile; fix the source/build logic instead.
