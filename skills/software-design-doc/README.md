# software-design-doc

**Version:** 1.0.0

An interactive software design documentation skill for OpenCode.

It helps the agent gather project context, discover missing requirements, delegate broad codebase exploration to subagents, reason about consequential architectural decisions, and produce a reviewable software design document.

## Install from this repository

```bash
npx skills add OWNER/REPOSITORY --skill software-design-doc --agent opencode
```

Install globally for OpenCode:

```bash
npx skills add OWNER/REPOSITORY --skill software-design-doc --agent opencode --global
```

## Version

The canonical skill version is stored in `SKILL.md` as:

```yaml
metadata:
  version: "1.0.0"
```

`VERSION` mirrors the same value for humans and tooling.

See `CHANGELOG.md` for release history.
