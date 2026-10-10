# Repository guidance

This file is the maintenance contract for future agents working on `software-skills` (`claude` branch: Claude Code only). Keep it concise. Do not duplicate the README, individual skills, or upstream Matt Pocock skill instructions.

## Architecture

- `source/skills/` is the canonical source of truth. Never edit generated files under `dist/` directly.
- `scripts/build.py` generates the single Claude Code profile in `dist/skills/`.
- `bin/software-skills.js` installs that profile into project `.claude/skills` or global `~/.claude/skills` (`$CLAUDE_CONFIG_DIR/skills` when set), asking interactively when `--scope` is missing.
- Prefer composition over reimplementation. Matt Pocock skills own their domain behavior; our skills add orchestration, resumability, and stronger acceptance loops.
- Keep skills short. Put a rule in the narrowest single place that owns it; do not repeat shared concepts across multiple skills.
- Use Claude Code's native skill discovery. Do not recreate `skills.json` or another persistent skill registry.

## Subagents

Skills delegate responsibilities (exploration, development, review) but never name a subagent type: Claude Code chooses the subagent autonomously. Do not ship custom agents, `agent:`/`context: fork` frontmatter, or `subagent_type` instructions. The shared "never prescribe a subagent type" rule is appended once by `scripts/build.py` to every delegating skill.

## Runtime state

- All ephemeral/resumable state owned by this project lives under `./.agents/tmp/`.
- Light implementation ledgers: `./.agents/tmp/implementation/<slug>.md`. The light path's plan is `spec.md` in the spec folder of `docs/agents/issue-tracker.md`, committed as the last commit (never the ledger).
- `./.agents/tmp/` is never a canonical deliverable and must not be staged, committed, or treated as review scope.

## Workflow contracts

### `my-grill-to-implementation`

This is the light path for changes that do not justify SPEC + tickets. Use `grill-with-docs`, keep one resumable implementation ledger, delegate exploration, then:

```text
per slice:  develop(tdd) -> validation green -> commit
at the end: fresh review -> (develop fix(tdd) -> commit -> new fresh review)* -> completed
```

Every fix requires a subsequent clean fresh review before `completed`; fixes are committed first because the review diffs committed history from the recorded starting revision. No per-slice review by default; an intermediate review only for a high and concrete risk (data migration, data-loss risk, new security boundary), announced to the user beforehand. Work only in the current checkout: no worktrees, branches, pull requests, or pushes. Subagents run sequentially; parallelism is allowed only across different repositories. Never approve by self-review.

### `my-implement-orchestrator`

This is the full ticket implementation path:

```text
per ticket:        develop(tdd) -> validation green -> commit
exceptional ticket: + code-review of that ticket -> (develop fix(tdd) -> commit -> new code-review)*
at the end:        code-review -> (develop fix(tdd) -> commit -> new code-review)* -> tracker finalization
```

Do not review tickets individually by default: only a high and concrete risk (data migration, data-loss risk, new security boundary; a contract or dependents are not enough) gets its own `code-review`, announced to the user beforehand. Every fix requires a subsequent clean `code-review`; fixes are committed first because `code-review` diffs committed history. Tickets are finalized only after the final review is clean. Same working-copy and subagent rules as `my-grill-to-implementation`. Keep `MAX_REVIEW_CYCLES` explicit and do not replace Matt Pocock's `tdd` or `code-review` with duplicated local rules.

## Deliberately removed workflows

Do not reintroduce these unless the architecture is intentionally changed:

- `my-update-skills-list` and `skills.json`: native skill discovery is the source of truth.
- `my-grill-to-plan` and `my-plan-to-spec`: superseded, then removed.
- Removed in 4.0.0 because Matt Pocock's skills are used directly: `my-grill-to-spec` (`grill-with-docs` + `to-spec`), `my-spec-to-tickets` (`to-tickets`), `my-review-changes` (`code-review`), and `my-git-commit`.
- Codex, OpenCode V2, Antigravity, and shared `.agents/skills` profiles: they live on `main`; this branch is Claude Code only.

## Upstream Matt Pocock constraints

Respect upstream invocation policy. Some Matt Pocock workflows such as `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, and `implement-spec` are user-invoked only (`disable-model-invocation: true`). Do not silently patch or pretend those policies do not exist; prefer the model-invokable primitives (`tdd`, `code-review`) when a skill must compose them.

## Change procedure

1. Change canonical files under `source/` and supporting build/installer code as needed.
2. Update the version/changelog when behavior or packaging changes.
3. Run `python3 scripts/build.py`.
4. Run `python3 scripts/validate.py`.
5. Run `node scripts/test-installer.js`.
6. Verify `npm pack --dry-run` still includes `dist/skills/` and `AGENTS.md`.
7. Never hand-edit `dist/` to fix a generated profile; fix the source/build logic instead.
