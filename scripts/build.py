#!/usr/bin/env python3
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source" / "skills"
DIST = ROOT / "dist"
VERSION = "3.1.1"

MANUAL = {
    "my-grill-to-implementation",
    "my-implement-orchestrator",
    "my-improve-code",
    "my-improve-comments",
    "my-improve-spacing",
}

ROLES = {
    "my-grill-to-implementation": ("explore", "develop", "review"),
    "my-implement-orchestrator": ("develop",),
    "my-improve-code": ("explore", "develop"),
    "my-improve-comments": ("explore", "develop"),
    "my-improve-spacing": ("explore", "develop"),
}


def parse_skill(path: Path):
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---\n", 4)
    if not text.startswith("---\n") or end < 0:
        raise ValueError(f"Invalid skill frontmatter: {path}")
    fm = text[4:end]
    body = text[end + 5 :]
    name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
    desc = re.search(r"^description:\s*(.+)$", fm, re.M).group(1).strip()
    return name, desc, body, path.parent


def copy_assets(src_dir: Path, dst_dir: Path):
    if (src_dir / "references").exists():
        shutil.copytree(src_dir / "references", dst_dir / "references", dirs_exist_ok=True)
    (dst_dir / "VERSION").write_text(VERSION + "\n", encoding="utf-8")


def insert_after_h1(body: str, block: str) -> str:
    m = re.search(r"^# .+$", body, re.M)
    if not m:
        return block.rstrip() + "\n\n" + body
    pos = m.end()
    return body[:pos] + "\n\n" + block.rstrip() + body[pos:]


def invocation_block(name: str) -> str:
    return (
        f"## Invocation\n\nExplicit-only OpenCode V2 workflow. Run `/{name}`; never invoke it implicitly.\n\n"
        "Treat command/skill arguments plus immediately relevant conversation context as the invocation input."
    )


def mapping_block(name: str) -> str:
    roles = ROLES.get(name)
    if not roles:
        return ""
    joined = ", ".join(f"`{r}`" for r in roles)
    return f"## Harness roles\n\nUse OpenCode V2 child-session roles: {joined}."


def adapt_body(name: str, body: str) -> str:
    if name in MANUAL:
        block = invocation_block(name)
        roles = mapping_block(name)
        if roles:
            block += "\n\n" + roles
        body = insert_after_h1(body, block)
    if name == "my-software-design-doc":
        body = body.replace(
            "Use the harness-mapped read-only `explore` role for broad codebase discovery.",
            "Use the built-in OpenCode V2 `explore` subagent for broad codebase discovery.",
        )
    return body


def load_skills():
    result = {}
    for p in sorted(SRC.glob("*/SKILL.md")):
        n, d, b, sd = parse_skill(p)
        result[n] = (d, b, sd)
    return result


def build_opencode(skills):
    root = DIST / ".opencode"
    sroot, aroot = root / "skills", root / "agents"
    sroot.mkdir(parents=True, exist_ok=True)
    aroot.mkdir(parents=True, exist_ok=True)

    for name, (desc, body, srcd) in skills.items():
        d = sroot / name
        d.mkdir(parents=True, exist_ok=True)
        fm = ["---", f"name: {name}", f"description: {desc}", "license: MIT"]
        if name in MANUAL:
            fm += ["compatibility: OpenCode V2; explicit slash invocation only.", "slash: true", "metadata:", f'  version: "{VERSION}"', "  opencode/autoinvoke: false", "  opencode/slash: true"]
        else:
            fm += ["compatibility: OpenCode V2 with native subagents.", "metadata:", f'  version: "{VERSION}"']
        fm += ["---", ""]
        (d / "SKILL.md").write_text("\n".join(fm) + adapt_body(name, body), encoding="utf-8")
        copy_assets(srcd, d)

    (aroot / "develop.md").write_text('''---
description: Scoped implementation and authoring worker for software-skills workflows.
mode: subagent
permissions:
  - action: subagent
    resource: "*"
    effect: deny
  - action: shell
    resource: "git commit*"
    effect: deny
  - action: shell
    resource: "git push*"
    effect: deny
  - action: shell
    resource: "git reset*"
    effect: deny
  - action: shell
    resource: "git clean*"
    effect: deny
  - action: shell
    resource: "git stash*"
    effect: deny
---

Follow the delegated scope exactly. Read repository instructions, load every skill requested by the parent, preserve unrelated changes, validate the work, never commit/push, and report loaded/missing skills, changed files, validation, and blockers.
''', encoding="utf-8")
    (aroot / "review.md").write_text('''---
description: Independent read-only reviewer for software-skills workflows.
mode: subagent
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: subagent
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: ask
  - action: shell
    resource: "git status*"
    effect: allow
  - action: shell
    resource: "git diff*"
    effect: allow
  - action: shell
    resource: "git log*"
    effect: allow
---

Review independently. Read repository instructions and every skill requested by the parent, inspect supplied evidence/diffs first, never edit or mutate repository state, never delegate, and report loaded/missing skills plus the exact verdict schema requested.
''', encoding="utf-8")


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    skills = load_skills()
    missing = (MANUAL | {"my-software-design-doc"}) - set(skills)
    if missing:
        raise SystemExit(f"Missing canonical skills: {sorted(missing)}")
    build_opencode(skills)
    print(f"Built {len(skills)} canonical skills for the OpenCode V2 profile")


if __name__ == "__main__":
    main()
