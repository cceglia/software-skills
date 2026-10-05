#!/usr/bin/env python3
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source" / "skills"
DIST = ROOT / "dist"
VERSION = "3.0.0"

MANUAL = {
    "my-git-commit",
    "my-grill-to-implementation",
    "my-grill-to-spec",
    "my-implement-orchestrator",
    "my-improve-code",
    "my-improve-comments",
    "my-improve-spacing",
    "my-review-changes",
    "my-spec-to-tickets",
}

# Skills that delegate work to subagents. They describe responsibilities, never subagent types.
DELEGATING = {
    "my-grill-to-implementation",
    "my-grill-to-spec",
    "my-implement-orchestrator",
    "my-improve-code",
    "my-improve-comments",
    "my-improve-spacing",
    "my-review-changes",
    "my-software-design-doc",
}

ARG_HINT = {
    "my-git-commit": "[optional context]",
    "my-grill-to-implementation": "[change request | .agents/tmp/implementation state]",
    "my-grill-to-spec": "[change request | .agents/tmp/grill ledger]",
    "my-implement-orchestrator": "[work item source]",
    "my-improve-code": "[scope]",
    "my-improve-comments": "[scope]",
    "my-improve-spacing": "[scope]",
    "my-review-changes": "[files | directory | glob]",
    "my-spec-to-tickets": "[approved SPEC]",
}

SUBAGENTS_BLOCK = (
    "## Subagents\n\n"
    "Never prescribe a subagent type: Claude Code chooses the most suitable available subagent for each delegation. "
    "State the delegated scope and constraints (read-only, no commits, skills to load, expected report) in the subagent prompt."
)


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


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


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
        f"## Invocation\n\nExplicit-only Claude Code workflow. Run `/{name}`; never invoke it implicitly.\n\n"
        "Treat `$ARGUMENTS` plus immediately relevant conversation context as the invocation input."
    )


def adapt_body(name: str, body: str) -> str:
    if name in MANUAL:
        body = insert_after_h1(body, invocation_block(name))
    if name in DELEGATING:
        body = body.rstrip() + "\n\n" + SUBAGENTS_BLOCK + "\n"
    return body


def load_skills():
    result = {}
    for p in sorted(SRC.glob("*/SKILL.md")):
        n, d, b, sd = parse_skill(p)
        result[n] = (d, b, sd)
    return result


def build_claude(skills):
    sroot = DIST / "skills"
    sroot.mkdir(parents=True, exist_ok=True)

    for name, (desc, body, srcd) in skills.items():
        d = sroot / name
        d.mkdir(parents=True, exist_ok=True)
        lines = ["---", f"name: {name}", f"description: {desc}", "license: MIT", "compatibility: Claude Code with native skill controls."]
        if name in MANUAL:
            lines += ["disable-model-invocation: true", "user-invocable: true"]
            if ARG_HINT.get(name):
                lines.append(f"argument-hint: {q(ARG_HINT[name])}")
        lines += ["metadata:", f'  version: "{VERSION}"', "---", ""]
        (d / "SKILL.md").write_text("\n".join(lines) + adapt_body(name, body), encoding="utf-8")
        copy_assets(srcd, d)


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    skills = load_skills()
    missing = (MANUAL | DELEGATING | {"my-software-design-doc"}) - set(skills)
    if missing:
        raise SystemExit(f"Missing canonical skills: {sorted(missing)}")
    build_claude(skills)
    print(f"Built {len(skills)} canonical skills for the Claude Code profile")


if __name__ == "__main__":
    main()
