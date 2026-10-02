---
name: my-update-skills-list
description: Read all SKILL.md files from user and project skill directories and regenerate ./.opencode/skills.json.
license: MIT
compatibility: OpenCode V2; explicit slash invocation only.
slash: true
metadata:
  version: "1.0.0"
  opencode/autoinvoke: "false"
  opencode/slash: "true"
---

# my-update-skills-list

## Invocation

This is an explicit-only OpenCode V2 skill. Run it manually with `/my-update-skills-list`. Do not select or invoke it implicitly.

# Update skills.json

Regenerate the project-local skill registry consumed by commands such as `my-implement-orchestrator`.

## Inputs

Scan recursively:

1. `~/.agents/skills/`
2. `./.agents/skills/`

A skill is any directory containing `SKILL.md`.

## Output

Always overwrite:

```text
./.opencode/skills.json
```

Format:

```json
{
  "skill-name": "Short description extracted from SKILL.md"
}
```

For each skill:

* key = directory name containing `SKILL.md`;
* description = YAML `description` when present; otherwise the first meaningful paragraph after frontmatter/title;
* keep descriptions concise (about 200 characters maximum, preferably a complete sentence).

If the same skill name exists in both roots, the **project skill wins** over the user skill.

## Procedure

1. Scan both roots recursively.
2. Read each `SKILL.md` and extract name + description.
3. Merge by skill name, applying project-over-user precedence.
4. Create `./.opencode/` if needed.
5. Write formatted JSON with 2-space indentation and deterministic key ordering.
6. Validate the result as JSON, for example:

```bash
python3 -m json.tool ./.opencode/skills.json >/dev/null
```

## Constraints

* Do not modify any skill.
* Do not commit anything.
* Skip directories without `SKILL.md`.
* Fully regenerate the registry; never patch it incrementally.
* Preserve descriptions in English when the source description is in English.
