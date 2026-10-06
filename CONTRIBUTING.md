# Contributing

## Source of truth

Edit `source/skills/<skill-name>/`; never hand-edit `dist/`. Regenerate with `python3 scripts/build.py`.

This branch targets OpenCode V2 only. OpenCode frontmatter (`slash`, `metadata.opencode/*`), role mapping, and the bundled `develop`/`review` agents belong in `scripts/build.py`; canonical bodies describe delegated responsibilities.

## Runtime invariants

Only resumable state belongs under:

```text
./.agents/tmp/implementation/
```

There is no skill registry. Use OpenCode V2's native skill discovery. Never stage, commit, or review `./.agents/tmp/`; do not ignore `.agents/` globally.

## Skill style

Keep `SKILL.md` concise and single-source-of-truth: state each invariant once, delegate upstream behavior instead of restating it, and preserve exact schemas only when callers depend on them.

## Validation

Run:

```bash
python3 scripts/build.py
python3 scripts/validate.py
npm test
npm pack --dry-run
```
