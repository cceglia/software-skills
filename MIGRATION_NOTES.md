# Migration notes

## 2.5.0

- `my-grill-to-spec` keeps only a resumable decision ledger in `./.agents/tmp/grill/`; Matt Pocock's `to-spec` remains the sole owner of canonical SPEC synthesis and tracker destination.
- `my-grill-to-spec` uses a fresh reviewer only after the canonical SPEC exists and stops after SPEC approval.
- `my-grill-to-implementation` keeps the light `explore -> develop -> fresh review` flow and requires Matt's `tdd` in develop/fix passes.
- `my-implement-orchestrator` now composes Matt's `tdd` and `code-review`, not user-only `implement` / `implement-spec`, and requires a new code review after every fix before commit.
- `my-spec-to-tickets` remains a thin wrapper around `to-tickets`; canonical tickets live in the configured tracker.

## Canonical artifacts

`setup-matt-pocock-skills` configures the issue tracker in `docs/agents/issue-tracker.md`. `to-spec` and `to-tickets` decide where canonical artifacts live. In local-markdown mode Matt uses `.scratch/<feature>/spec.md` and `.scratch/<feature>/issues/<NN>-<slug>.md`.

`./.agents/tmp/` is only ephemeral/resumable workflow state and should stay out of commits.
