'use strict';

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const CLI = path.join(ROOT, 'bin', 'software-skills.js');

function tempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'software-skills-test-'));
}

// Every run gets an isolated home so global installs never touch the real ~/.config/opencode.
function run(args, { home = tempDir(), env = {} } = {}) {
  const baseEnv = { ...process.env, HOME: home, USERPROFILE: home, ...env };
  for (const key of ['OPENCODE_CONFIG_DIR', 'XDG_CONFIG_HOME']) if (!(key in env)) delete baseEnv[key];
  return execFileSync(process.execPath, [CLI, ...args], { cwd: ROOT, encoding: 'utf8', env: baseEnv, stdio: ['ignore', 'pipe', 'pipe'] });
}

function exists(root, rel) {
  return fs.existsSync(path.join(root, rel));
}

function expectFailure(args, message, options) {
  let failed = false;
  try {
    run(args, options);
  } catch (err) {
    failed = true;
    assert(String(err.stderr || err.message).includes(message), `expected "${message}" in: ${err.stderr}`);
  }
  assert(failed, `expected failure for ${args.join(' ')}`);
}

// Project install writes OpenCode skills and agents only.
{
  const target = tempDir();
  const home = tempDir();
  run(['--scope', 'project', '--target', target, '--git-exclude', 'no'], { home });
  assert(exists(target, '.opencode/skills/my-improve-code/SKILL.md'));
  assert(exists(target, '.opencode/skills/my-implement-orchestrator/SKILL.md'));
  assert(exists(target, '.opencode/skills/my-software-design-doc/references/design-doc-template.md'));
  assert(exists(target, '.opencode/agents/develop.md'));
  assert(exists(target, '.opencode/agents/review.md'));
  assert(!exists(target, '.agents'));
  assert(!exists(target, '.claude'));
  assert(!exists(target, '.codex'));
  assert(!exists(home, '.config/opencode'));
  for (const removed of ['my-git-commit', 'my-grill-to-spec', 'my-review-changes', 'my-spec-to-tickets']) {
    assert(!exists(target, `.opencode/skills/${removed}`));
  }
}

// Global install writes to ~/.config/opencode and leaves the project untouched.
{
  const home = tempDir();
  const out = run(['--scope', 'global', '--git-exclude', 'no'], { home });
  assert(exists(home, '.config/opencode/skills/my-improve-comments/SKILL.md'));
  assert(exists(home, '.config/opencode/agents/review.md'));
  assert(!exists(ROOT, '.opencode/skills'));
  assert(out.includes('Scope: global'));
}

// Global install honors XDG_CONFIG_HOME and OPENCODE_CONFIG_DIR (the latter wins).
{
  const home = tempDir();
  const xdg = tempDir();
  const config = tempDir();
  run(['--scope=user'], { home, env: { XDG_CONFIG_HOME: xdg } });
  assert(exists(xdg, 'opencode/skills/my-improve-spacing/SKILL.md'));
  run(['--scope=user'], { home, env: { XDG_CONFIG_HOME: xdg, OPENCODE_CONFIG_DIR: config } });
  assert(exists(config, 'skills/my-improve-spacing/SKILL.md'));
  assert(!exists(home, '.config'));
}

// Generated workflows use OpenCode roles and carry no other harness's controls.
{
  const target = tempDir();
  run(['--scope', 'project', '--target', target, '--git-exclude', 'no']);
  const text = fs.readFileSync(path.join(target, '.opencode/skills/my-implement-orchestrator/SKILL.md'), 'utf8');
  assert(text.includes('Use OpenCode V2 child-session roles: `develop`.'));
  assert(text.includes('opencode/autoinvoke: false'));
  assert(!text.includes('disable-model-invocation'));
}

// Scope is required without a TTY, and project-only flags are rejected for global installs.
{
  expectFailure([], '--scope');
  expectFailure(['--scope', 'everywhere'], 'Unknown scope');
  expectFailure(['--scope', 'global', '--target', tempDir()], '--target applies only to --scope project');
  expectFailure(['--scope', 'global', '--git-exclude', 'yes'], '--git-exclude=yes applies only to --scope project');
}

// Existing differing file blocks unless --force is used.
{
  const target = tempDir();
  const dest = path.join(target, '.opencode/skills/my-improve-code/SKILL.md');
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, 'local change\n');
  expectFailure(['--scope', 'project', '--target', target, '--git-exclude', 'no'], '--force');
  run(['--scope', 'project', '--target', target, '--git-exclude', 'no', '--force']);
  assert(fs.readFileSync(dest, 'utf8').includes('name: my-improve-code'));
}

// Existing agents are never overwritten, even with --force; missing agents are still installed.
{
  const target = tempDir();
  const agent = path.join(target, '.opencode/agents/develop.md');
  fs.mkdirSync(path.dirname(agent), { recursive: true });
  fs.writeFileSync(agent, 'my custom agent\n');
  run(['--scope', 'project', '--target', target, '--git-exclude', 'no']);
  run(['--scope', 'project', '--target', target, '--git-exclude', 'no', '--force']);
  assert.strictEqual(fs.readFileSync(agent, 'utf8'), 'my custom agent\n');
  assert(exists(target, '.opencode/agents/review.md'));
  assert(exists(target, '.opencode/skills/my-improve-code/SKILL.md'));
}

// Dry run writes nothing.
{
  const home = tempDir();
  const out = run(['--scope', 'global', '--dry-run'], { home });
  assert(out.includes('[dry-run] write'));
  assert(!exists(home, '.config/opencode'));
}

// Leftover skills from older releases are reported, not deleted.
{
  const target = tempDir();
  const oldSkill = path.join(target, '.opencode/skills/my-review-changes/SKILL.md');
  fs.mkdirSync(path.dirname(oldSkill), { recursive: true });
  fs.writeFileSync(oldSkill, '---\nname: my-review-changes\n---\n');
  const out = run(['--scope', 'project', '--target', target, '--git-exclude', 'no']);
  assert(out.includes('no longer shipped and can be removed'));
  assert(out.includes(path.dirname(oldSkill)));
  assert(fs.existsSync(oldSkill));
}

// Git exclude targets only ephemeral .agents/tmp state, and only for project installs.
{
  const target = tempDir();
  fs.mkdirSync(path.join(target, '.git', 'info'), { recursive: true });
  fs.writeFileSync(path.join(target, '.git', 'info', 'exclude'), '');
  run(['--scope', 'project', '--target', target, '--git-exclude', 'yes']);
  const exclude = fs.readFileSync(path.join(target, '.git', 'info', 'exclude'), 'utf8');
  assert(exclude.includes('/.agents/tmp/'));
  assert(!exclude.includes('\n/.agents/\n'));
}

console.log('installer tests passed');
