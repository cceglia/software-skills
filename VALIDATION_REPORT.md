# Validation report — 2.2.0

Validated on 2026-10-03.

Commands:

```bash
python3 scripts/build.py
python3 scripts/validate.py
npm test
npm pack --dry-run
```

Expected result: 11 canonical skills, 10 explicit workflows, four native harness profiles, and one shared `.agents/skills` profile.

Validated invariants:

- `my-update-skills-list` is absent from source and generated distributions;
- no generated `skills.json` registry exists;
- skill routing uses native harness discovery and workers report loaded/missing skills;
- runtime state is limited to `./.agents/tmp/grill/` and `./.agents/tmp/implementation/`;
- commits/reviews exclude `./.agents/tmp/`;
- OpenCode, Codex, Claude Code, and Antigravity native integration files are generated;
- shared `.agents/skills` remains standards-compliant;
- canonical/generated skill files remain under 250 lines;
- installer collision/overwrite behavior and `/.agents/tmp/` Git exclude are tested.
