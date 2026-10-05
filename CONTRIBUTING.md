# Contributing

## Source of truth

Edit `source/skills/<skill-name>/`; never hand-edit `dist/`. Regenerate with `python3 scripts/build.py`.

This branch targets Claude Code only. Claude Code frontmatter (`disable-model-invocation`, `argument-hint`, …) and shared generated blocks belong in `scripts/build.py`; canonical bodies describe delegated responsibilities and never name a subagent type.

## Runtime invariants

Only resumable state belongs under:

```text
./.agents/tmp/grill/
./.agents/tmp/implementation/
```

Canonical SPECs and tickets are owned by Matt Pocock's configured issue tracker through `to-spec` / `to-tickets`; never duplicate them under `.agents/tmp`.

There is no skill registry. Use Claude Code's native skill discovery. Never stage, commit, or review `./.agents/tmp/`; do not ignore `.agents/` globally.

## Skill style

Keep `SKILL.md` concise and single-source-of-truth: state each invariant once, delegate upstream behavior instead of restating it, never prescribe subagent types, and preserve exact schemas only when callers depend on them.

## Validation

Run:

```bash
python3 scripts/build.py
python3 scripts/validate.py
npm test
npm pack --dry-run
```
