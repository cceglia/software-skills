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

// Every run gets an isolated home so global installs never touch the real ~/.claude.
function run(args, { home = tempDir(), env = {} } = {}) {
  const baseEnv = { ...process.env, HOME: home, USERPROFILE: home, ...env };
  if (!('CLAUDE_CONFIG_DIR' in env)) delete baseEnv.CLAUDE_CONFIG_DIR;
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

// Project install writes only Claude Code skills, without typed subagents.
{
  const target = tempDir();
  const home = tempDir();
  run(['--scope', 'project', '--target', target, '--git-exclude', 'no'], { home });
  assert(exists(target, '.claude/skills/my-git-commit/SKILL.md'));
  assert(exists(target, '.claude/skills/my-software-design-doc/references/design-doc-template.md'));
  assert(!exists(target, '.claude/agents'));
  assert(!exists(target, '.agents/skills'));
  assert(!exists(target, '.opencode'));
  assert(!exists(target, '.codex'));
  assert(!exists(home, '.claude'));
}

// Global install writes to ~/.claude/skills and leaves the project untouched.
{
  const home = tempDir();
  const out = run(['--scope', 'global', '--git-exclude', 'no'], { home });
  assert(exists(home, '.claude/skills/my-review-changes/SKILL.md'));
  assert(!exists(home, '.claude/agents'));
  assert(!exists(ROOT, '.claude/skills'));
  assert(out.includes('Scope: global'));
}

// Global install honors CLAUDE_CONFIG_DIR.
{
  const home = tempDir();
  const config = tempDir();
  run(['--scope=user'], { home, env: { CLAUDE_CONFIG_DIR: config } });
  assert(exists(config, 'skills/my-grill-to-spec/SKILL.md'));
  assert(!exists(home, '.claude'));
}

// Generated skills never prescribe a subagent type.
{
  const target = tempDir();
  run(['--scope', 'project', '--target', target, '--git-exclude', 'no']);
  const review = fs.readFileSync(path.join(target, '.claude/skills/my-review-changes/SKILL.md'), 'utf8');
  assert(!/^agent:/m.test(review));
  assert(!/^context:/m.test(review));
  assert(review.includes('Never prescribe a subagent type'));
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
  const dest = path.join(target, '.claude/skills/my-git-commit/SKILL.md');
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, 'local change\n');
  expectFailure(['--scope', 'project', '--target', target, '--git-exclude', 'no'], '--force');
  run(['--scope', 'project', '--target', target, '--git-exclude', 'no', '--force']);
  assert(fs.readFileSync(dest, 'utf8').includes('name: my-git-commit'));
}

// Dry run writes nothing.
{
  const home = tempDir();
  const out = run(['--scope', 'global', '--dry-run'], { home });
  assert(out.includes('[dry-run] write'));
  assert(!exists(home, '.claude'));
}

// Legacy typed subagents from older releases are reported, not deleted.
{
  const target = tempDir();
  const legacy = path.join(target, '.claude/agents/review.md');
  fs.mkdirSync(path.dirname(legacy), { recursive: true });
  fs.writeFileSync(legacy, '---\nname: review\ndescription: Independent read-only reviewer for software-skills workflows.\n---\n');
  const out = run(['--scope', 'project', '--target', target, '--git-exclude', 'no']);
  assert(out.includes('legacy software-skills subagents'));
  assert(fs.existsSync(legacy));
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
