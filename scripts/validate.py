#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source" / "skills"
DIST = ROOT / "dist"
VERSION = "2.2.0"
EXPECTED = {
    "my-git-commit",
    "my-grill-to-implementation",
    "my-grill-to-plan",
    "my-implement-orchestrator",
    "my-improve-code",
    "my-improve-comments",
    "my-improve-spacing",
    "my-plan-to-spec",
    "my-review-changes",
    "my-software-design-doc",
    "my-spec-to-tickets",
}
MANUAL = EXPECTED - {"my-software-design-doc"}

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def frontmatter(path: Path) -> tuple[dict, str]:
    text = read(path)
    if not text.startswith("---\n"):
        fail(f"missing frontmatter: {path.relative_to(ROOT)}")
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"unterminated frontmatter: {path.relative_to(ROOT)}")
        return {}, text
    raw, body = text[4:end], text[end + 5 :]
    if yaml is not None:
        try:
            value = yaml.safe_load(raw) or {}
            if not isinstance(value, dict):
                raise TypeError("frontmatter is not a mapping")
            return value, body
        except Exception as exc:
            fail(f"invalid YAML in {path.relative_to(ROOT)}: {exc}")
            return {}, body
    parsed: dict[str, object] = {}
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z0-9_./-]+):\s*(.*)$", line)
        if m:
            raw_value = m.group(2).strip().strip('"')
            parsed[m.group(1)] = {"true": True, "false": False}.get(raw_value, raw_value)
    return parsed, body


def nested(mapping: dict, *keys):
    cur: object = mapping
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def check_skill_dir(root: Path, expected: set[str] = EXPECTED) -> None:
    got = {p.parent.name for p in root.glob("*/SKILL.md")}
    if got != expected:
        fail(f"{root.relative_to(ROOT)} skills mismatch: expected {sorted(expected)}, got {sorted(got)}")
    for path in root.glob("*/SKILL.md"):
        fm, _ = frontmatter(path)
        if fm.get("name") != path.parent.name:
            fail(f"name/directory mismatch: {path.relative_to(ROOT)}")
        if nested(fm, "metadata", "version") not in (VERSION, None):
            fail(f"wrong version in {path.relative_to(ROOT)}")
        if len(path.read_text(encoding="utf-8").splitlines()) > 250:
            fail(f"skill should remain concise (<250 lines): {path.relative_to(ROOT)}")


def parse_yaml(path: Path) -> dict:
    text = read(path)
    if yaml is None:
        return {"_raw": text}
    try:
        value = yaml.safe_load(text) or {}
        if not isinstance(value, dict):
            raise TypeError("root is not a mapping")
        return value
    except Exception as exc:
        fail(f"invalid YAML in {path.relative_to(ROOT)}: {exc}")
        return {}


def validate_source() -> None:
    check_skill_dir(SRC)
    for name in EXPECTED:
        if read(SRC / name / "VERSION").strip() != VERSION:
            fail(f"source VERSION mismatch for {name}")
    text = "\n".join(p.read_text(encoding="utf-8") for p in SRC.rglob("*.md"))
    for forbidden in ("my-update-skills-list", "skills.json", "./.tmp/", ".opencode/grill", ".opencode/implementation", "subagent_type"):
        if forbidden in text:
            fail(f"obsolete token remains in canonical source: {forbidden}")
    for token in ("./.agents/tmp/grill/", "./.agents/tmp/implementation/"):
        if token not in text:
            fail(f"canonical source missing runtime path {token}")
    orchestrator = read(SRC / "my-implement-orchestrator" / "SKILL.md")
    for token in ("native skill discovery", "SKILLS_LOADED", "SKILLS_NOT_LOADED"):
        if token not in orchestrator:
            fail(f"orchestrator missing native skill-loading invariant: {token}")


def validate_opencode() -> None:
    root = DIST / "opencode" / ".opencode"
    check_skill_dir(root / "skills")
    for name in MANUAL:
        fm, body = frontmatter(root / "skills" / name / "SKILL.md")
        if fm.get("slash") is not True:
            fail(f"OpenCode {name} missing slash: true")
        if nested(fm, "metadata", "opencode/autoinvoke") is not False:
            fail(f"OpenCode {name} missing autoinvoke=false")
        if f"/{name}" not in body:
            fail(f"OpenCode {name} missing explicit slash invocation")
    for agent in ("develop", "review"):
        fm, _ = frontmatter(root / "agents" / f"{agent}.md")
        if fm.get("mode") != "subagent":
            fail(f"OpenCode {agent} missing mode: subagent")


def validate_codex() -> None:
    root = DIST / "codex"
    sroot = root / ".agents" / "skills"
    check_skill_dir(sroot)
    for name in EXPECTED:
        data = parse_yaml(sroot / name / "agents" / "openai.yaml")
        if yaml is not None:
            if nested(data, "policy", "allow_implicit_invocation") is not (name not in MANUAL):
                fail(f"Codex {name} implicit invocation policy mismatch")
            if nested(data, "policy", "products") != ["CODEX"]:
                fail(f"Codex {name} products policy mismatch")
    expected_sandbox = {"explore": "read-only", "develop": "workspace-write", "review": "read-only"}
    for name, sandbox in expected_sandbox.items():
        path = root / ".codex" / "agents" / f"{name}.toml"
        try:
            data = tomllib.loads(read(path))
        except Exception as exc:
            fail(f"invalid TOML in {path.relative_to(ROOT)}: {exc}")
            continue
        if data.get("sandbox_mode") != sandbox:
            fail(f"Codex {name} sandbox mismatch")


def validate_claude() -> None:
    root = DIST / "claude-code" / ".claude"
    check_skill_dir(root / "skills")
    for name in MANUAL:
        fm, body = frontmatter(root / "skills" / name / "SKILL.md")
        if fm.get("disable-model-invocation") is not True or fm.get("user-invocable") is not True:
            fail(f"Claude {name} missing explicit-only invocation fields")
        if f"/{name}" not in body:
            fail(f"Claude {name} missing slash invocation text")
    review_fm, _ = frontmatter(root / "skills" / "my-review-changes" / "SKILL.md")
    if review_fm.get("context") != "fork" or review_fm.get("agent") != "review" or review_fm.get("background") is not False:
        fail("Claude my-review-changes must use context: fork + agent: review + background: false")


def validate_antigravity() -> None:
    root = DIST / "antigravity" / ".agents"
    check_skill_dir(root / "skills", {"my-software-design-doc"})
    workflows = {p.stem for p in (root / "workflows").glob("*.md")}
    if workflows != MANUAL:
        fail(f"Antigravity workflows mismatch: {sorted(workflows)}")
    for path in (root / "workflows").glob("*.md"):
        _, body = frontmatter(path)
        if f"/{path.stem}" not in body:
            fail(f"Antigravity workflow missing slash invocation: {path.name}")
    rules = read(root / "rules" / "software-skills-runtime.md")
    for token in ("./.agents/tmp/", "./.agents/tmp/grill/", "./.agents/tmp/implementation/"):
        if token not in rules:
            fail(f"Antigravity runtime rules missing {token}")


def validate_shared() -> None:
    root = DIST / "shared" / ".agents" / "skills"
    check_skill_dir(root)
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    for name in EXPECTED:
        fm, body = frontmatter(root / name / "SKILL.md")
        if set(fm) - allowed:
            fail(f"shared {name} has unsupported top-level fields: {sorted(set(fm)-allowed)}")
        if name in MANUAL:
            metadata = fm.get("metadata") or {}
            if metadata.get("opencode/autoinvoke") != "false" or metadata.get("opencode/slash") != "true":
                fail(f"shared {name} missing OpenCode namespaced metadata")
            if not str(fm.get("description", "")).startswith("Explicit-only workflow."):
                fail(f"shared {name} description must state explicit-only")
            if "never invoke it implicitly" not in body:
                fail(f"shared {name} body missing explicit-only instruction")
        data = parse_yaml(root / name / "agents" / "openai.yaml")
        if yaml is not None and nested(data, "policy", "allow_implicit_invocation") is not (name not in MANUAL):
            fail(f"shared Codex sidecar policy mismatch for {name}")


def validate_global() -> None:
    files = [p for p in DIST.rglob("*") if p.is_file() and p.suffix in {".md", ".yaml", ".toml"}]
    text = "\n".join(p.read_text(encoding="utf-8") for p in files)
    for forbidden in ("my-update-skills-list", "skills.json", "./.tmp/", ".opencode/grill", ".opencode/implementation", "subagent_type"):
        if forbidden in text:
            fail(f"obsolete token remains in generated profiles: {forbidden}")
    if "./.agents/tmp/" not in text:
        fail("generated profiles missing ./.agents/tmp runtime invariant")


def main() -> int:
    validate_source()
    validate_opencode()
    validate_codex()
    validate_claude()
    validate_antigravity()
    validate_shared()
    validate_global()
    if errors:
        print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("OK: canonical source, four native profiles, and shared .agents profile validated")
    print(f"- canonical skills: {len(EXPECTED)}")
    print(f"- explicit workflows: {len(MANUAL)}")
    print("- runtime state: ./.agents/tmp/grill and ./.agents/tmp/implementation")
    print("- skill routing: native harness discovery; no skills.json registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
