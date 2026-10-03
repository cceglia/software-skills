# Custom installer reference

Canonical repository: <https://github.com/cceglia/software-skills>

The complete public CLI reference and copy-paste examples are maintained in the root `README.md` under:

- Quick install
- Non-interactive install
- Installer CLI reference
- Command examples with parameters
- Pinning a branch, tag, or commit
- Running from a cloned repository
- What gets installed
- Existing files and `--force`

Canonical interactive command:

```bash
npx --yes github:cceglia/software-skills
```

Canonical fully non-interactive command:

```bash
npx --yes github:cceglia/software-skills -- \
  --harness all \
  --layout native \
  --target . \
  --git-exclude auto
```

Use `--dry-run` before installation when evaluating changes, and `--force` only when replacing a known older managed installation.
