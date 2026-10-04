'use strict';

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CLI = path.join(ROOT, 'bin', 'software-skills.js');

function tempProject() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'software-skills-test-'));
}

function run(args, cwd = ROOT) {
  return execFileSync(process.execPath, [CLI, ...args], { cwd, encoding: 'utf8' });
}

function exists(root, rel) {
  return fs.existsSync(path.join(root, rel));
}

// Native OpenCode + Claude Code install.
{
  const target = tempProject();
  run(['--harness', 'opencode,claude-code', '--layout', 'native', '--target', target, '--git-exclude', 'no']);
  assert(exists(target, '.opencode/skills/my-git-commit/SKILL.md'));
  assert(exists(target, '.opencode/agents/review.md'));
  assert(exists(target, '.claude/skills/my-review-changes/SKILL.md'));
  assert(exists(target, '.claude/agents/review.md'));
  assert(!exists(target, '.agents/skills/my-git-commit/SKILL.md'));
  assert(!exists(target, '.opencode/skills/my-update-skills-list/SKILL.md'));
}

// Shared all-harness install.
{
  const target = tempProject();
  run(['--harness', 'all', '--layout', 'agents', '--target', target, '--git-exclude', 'no']);
  assert(exists(target, '.agents/skills/my-git-commit/SKILL.md'));
  assert(exists(target, '.agents/skills/my-git-commit/agents/openai.yaml'));
  assert(exists(target, '.codex/agents/review.toml'));
  assert(exists(target, '.claude/agents/review.md'));
  assert(exists(target, '.opencode/agents/review.md'));
  assert(exists(target, '.agents/workflows/my-git-commit.md'));
  assert(exists(target, '.agents/rules/software-skills-runtime.md'));
  assert(!exists(target, '.claude/skills/my-git-commit/SKILL.md'));
  assert(!exists(target, '.opencode/skills/my-git-commit/SKILL.md'));
  assert(!exists(target, '.agents/skills/my-update-skills-list/SKILL.md'));
}

// Codex + Antigravity native-path collision is resolved with shared .agents skills.
{
  const target = tempProject();
  const out = run(['--harness', 'codex,antigravity', '--layout', 'native', '--target', target, '--git-exclude', 'no']);
  assert(exists(target, '.agents/skills/my-git-commit/SKILL.md'));
  assert(exists(target, '.agents/skills/my-software-design-doc/agents/openai.yaml'));
  assert(exists(target, '.codex/agents/develop.toml'));
  assert(exists(target, '.agents/workflows/my-grill-to-spec.md'));
  assert(out.includes('Codex and Antigravity share .agents/skills'));
}

// Existing differing file blocks unless --force is used.
{
  const target = tempProject();
  const dest = path.join(target, '.opencode/skills/my-git-commit/SKILL.md');
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, 'local change\n');
  let failed = false;
  try {
    run(['--harness', 'opencode', '--layout', 'native', '--target', target, '--git-exclude', 'no']);
  } catch (err) {
    failed = true;
    assert(String(err.stderr || err.message).includes('--force'));
  }
  assert(failed);
  run(['--harness', 'opencode', '--layout', 'native', '--target', target, '--git-exclude', 'no', '--force']);
  assert(fs.readFileSync(dest, 'utf8').includes('name: my-git-commit'));
}


// Git exclude targets only ephemeral .agents/tmp state.
{
  const target = tempProject();
  fs.mkdirSync(path.join(target, '.git', 'info'), { recursive: true });
  fs.writeFileSync(path.join(target, '.git', 'info', 'exclude'), '');
  run(['--harness', 'codex', '--layout', 'native', '--target', target, '--git-exclude', 'yes']);
  const exclude = fs.readFileSync(path.join(target, '.git', 'info', 'exclude'), 'utf8');
  assert(exclude.includes('/.agents/tmp/'));
  assert(!exclude.includes('\n/.agents/\n'));
}

console.log('installer tests passed');
