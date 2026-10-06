# software-skills — OpenCode V2 edition

Software-engineering workflows packaged as native **OpenCode V2** skills and agents.

Repository: <https://github.com/cceglia/software-skills>

> This is the `main` branch: it installs the skills **only for OpenCode V2**. The Claude Code edition lives on the `claude` branch.

## Install

```bash
npx --yes github:cceglia/software-skills
```

The interactive installer asks where to install:

```text
Where should the OpenCode V2 skills be installed?
  1) Project (/path/to/project/.opencode)
  2) Global (/home/you/.config/opencode)
Scope [1/2]:
```

| Scope | Destination | Available in |
| --- | --- | --- |
| `project` | `<target>/.opencode/{skills,agents}/` | that project only (can be committed and shared with the team) |
| `global` | `~/.config/opencode/{skills,agents}/` (`$OPENCODE_CONFIG_DIR`, else `$XDG_CONFIG_HOME/opencode`) | every project on your machine |

Node.js 18+ is required. The installer has no npm runtime dependencies.

### Non-interactive install

Install into the current project:

```bash
npx --yes github:cceglia/software-skills --scope project
```

Install globally for your user:

```bash
npx --yes github:cceglia/software-skills --scope global
```

Install into another project:

```bash
npx --yes github:cceglia/software-skills --scope project --target ../my-project
```

Preview without writing:

```bash
npx --yes github:cceglia/software-skills --scope global --dry-run
```

Overwrite an older installation:

```bash
npx --yes github:cceglia/software-skills --scope global --force
```

Pin a branch, tag, or commit:

```bash
npx --yes github:cceglia/software-skills#<commit-sha> --scope project
```

Equivalent explicit `npm exec` form:

```bash
npm exec --yes --package=github:cceglia/software-skills -- software-skills --scope project
```

### From a cloned repository

```bash
git clone https://github.com/cceglia/software-skills.git
```

```bash
node ./software-skills/bin/software-skills.js --scope global
```

## Installer CLI reference

```text
software-skills [options]

--scope <scope>
    Where the skills and agents are installed.
    Values: project, global (aliases: local/repo, user/personal)
    Asked interactively when omitted.

    project   <target>/.opencode
    global    ~/.config/opencode, or $OPENCODE_CONFIG_DIR, or $XDG_CONFIG_HOME/opencode

--target <path>
    Project root for --scope project.
    Default: current working directory. Rejected with --scope global.

--force
    Overwrite existing managed files when their contents differ.
    Without --force, the installer stops rather than replacing them.

--dry-run
    Print every planned write without modifying anything.

--git-exclude <mode>
    Controls whether /.agents/tmp/ is added to .git/info/exclude (project scope only).
    Values: auto (default), yes, no

--help, -h
--version, -v
```

The installer only writes files. It never deletes anything; if it finds skills removed in 3.0.0 still installed, it lists them so you can remove them.

## Skills

| Skill | Invocation | Purpose |
| --- | --- | --- |
| `my-grill-to-implementation` | `/my-grill-to-implementation` | Light path: grill, explore, implement and commit every slice with `tdd`, then a final review with fix/review cycles |
| `my-implement-orchestrator` | `/my-implement-orchestrator` | Implement tracker tickets with `tdd` and per-ticket commits; review only important tickets individually, then a final `code-review` with fix/review cycles |
| `my-improve-code` | `/my-improve-code` | Improve comments and spacing without behavior changes |
| `my-improve-comments` | `/my-improve-comments` | Improve comments/documentation only |
| `my-improve-spacing` | `/my-improve-spacing` | Improve logical blank-line spacing only |
| `my-software-design-doc` | automatic or `/my-software-design-doc` | Create or review software design documents |

Every workflow except `my-software-design-doc` is explicit-only (`slash: true`, `metadata.opencode/autoinvoke: false`).

### OpenCode roles

Delegating skills use the built-in `explore` subagent plus the bundled `develop` and `review` subagents installed under `agents/`. `develop` never commits or pushes; `review` is read-only.

## Matt Pocock dependency

These workflows compose Matt Pocock's skills instead of duplicating them. Install them:

```bash
npx skills add mattpocock/skills
```

Run `setup-matt-pocock-skills` once per repository so Matt's skills know the configured issue tracker.

### Removed workflows

`my-grill-to-spec`, `my-spec-to-tickets`, `my-review-changes`, and `my-git-commit` were removed in 3.0.0: use Matt Pocock's skills directly (`grill-with-docs`, `to-spec`, `to-tickets`, `code-review`) or commit by hand. The installer never deletes files, but it lists removed skills still present in the destination so you can delete them.

### Ticket path

```text
my-implement-orchestrator
  per ticket:
    -> develop + tdd
    -> tests/typecheck green
    -> one commit (ticket reference in the message)
    -> important ticket only: code-review of that ticket -> (fix -> commit -> new code-review)*
  at the end:
    -> code-review since the starting revision
    -> (develop fix + tdd -> commit -> new code-review)*
    -> tracker finalization
```

Only important tickets (migrations, persistence, public contracts, security/auth, concurrency, or foundational for dependent tickets) are reviewed individually; every other ticket is covered by the final review.

### Light path

```text
my-grill-to-implementation
  -> grill-with-docs
  -> .agents/tmp/implementation/<slug>.md
  -> explore
  per slice:
    -> develop + tdd
    -> tests/typecheck green
    -> one commit
  at the end:
    -> fresh review (diff since the starting revision)
    -> (develop fix + tdd -> commit -> new fresh review)*
    -> completed
```

Both paths work only in the current checkout (no worktrees, branches, pull requests, or pushes) and run roles sequentially, in parallel only across different repositories. An intermediate review after a high-risk slice is optional.

## Runtime state and resume

All workflow state lives in the project under:

```text
./.agents/tmp/
└── implementation/<slug>.md
```

The ledger survives context exhaustion. Reinvoke the workflow with the ledger path:

```text
/my-grill-to-implementation ./.agents/tmp/implementation/<slug>.md
```

Workflows never include `./.agents/tmp/` in commits or code reviews. For project installs, the installer adds `/.agents/tmp/` to `.git/info/exclude` when the target is a Git repository. For global installs, add that rule yourself in each project where you use the workflows.

## Source architecture

```text
source/skills/            canonical skill source
scripts/build.py          generates dist/.opencode/ (OpenCode V2 profile)
scripts/validate.py       validates source and generated profile
scripts/test-installer.js installer tests
bin/software-skills.js    installer
dist/.opencode/           generated, installable skills and agents
```

```bash
python3 scripts/build.py
```

```bash
python3 scripts/validate.py
```

```bash
npm test
```

## License

MIT. See `LICENSE`.
