# Custom installer reference

Canonical repository: <https://github.com/cceglia/software-skills> (branch `main`, OpenCode V2 only)

The complete CLI reference and examples are maintained in the root `README.md` under "Install" and "Installer CLI reference".

Interactive command (asks project vs global):

```bash
npx --yes github:cceglia/software-skills
```

Fully non-interactive commands:

```bash
npx --yes github:cceglia/software-skills --scope project --target . --git-exclude auto
```

```bash
npx --yes github:cceglia/software-skills --scope global
```
