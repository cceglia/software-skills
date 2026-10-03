#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const readline = require('readline/promises');
const process = require('process');

const ROOT = path.resolve(__dirname, '..');
const VERSION = require(path.join(ROOT, 'package.json')).version;
const HARNESSES = ['codex', 'claude-code', 'opencode', 'antigravity'];
const LABELS = {
  'codex': 'Codex',
  'claude-code': 'Claude Code',
  'opencode': 'OpenCode V2',
  'antigravity': 'Antigravity IDE',
};

function usage() {
  return `software-skills ${VERSION}\n\n` +
`Usage:\n` +
`  software-skills [options]\n\n` +
`Options:\n` +
`  --harness <list>       Comma-separated: codex,claude-code,opencode,antigravity,all\n` +
`  --layout <mode>        Skill location: agents | native\n` +
`  --target <path>        Project root to install into (default: current directory)\n` +
`  --force                Overwrite existing managed files\n` +
`  --dry-run              Print planned file operations without writing\n` +
`  --git-exclude <mode>   auto | yes | no (default: auto)\n` +
`  --help                 Show this help\n` +
`  --version              Print installer version\n\n` +
`Layouts:\n` +
`  agents   Install one shared Agent Skills copy under .agents/skills.\n` +
`           Harness-specific agents/workflows/rules are still installed natively.\n` +
`  native   Install skills in each harness' project-native skill directory.\n` +
`           Claude Code: .claude/skills; OpenCode: .opencode/skills;\n` +
`           Codex and Antigravity: .agents/skills (their documented project-native path).\n`;
}

function parseArgs(argv) {
  const out = { harnesses: null, layout: null, target: process.cwd(), force: false, dryRun: false, gitExclude: 'auto' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--') continue;
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--version' || a === '-v') out.version = true;
    else if (a === '--force') out.force = true;
    else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--harness') out.harnesses = parseHarnesses(argv[++i]);
    else if (a.startsWith('--harness=')) out.harnesses = parseHarnesses(a.slice(10));
    else if (a === '--layout') out.layout = normalizeLayout(argv[++i]);
    else if (a.startsWith('--layout=')) out.layout = normalizeLayout(a.slice(9));
    else if (a === '--target') out.target = path.resolve(argv[++i]);
    else if (a.startsWith('--target=')) out.target = path.resolve(a.slice(9));
    else if (a === '--git-exclude') out.gitExclude = normalizeGitExclude(argv[++i]);
    else if (a.startsWith('--git-exclude=')) out.gitExclude = normalizeGitExclude(a.slice(14));
    else throw new Error(`Unknown argument: ${a}`);
  }
  return out;
}

function parseHarnesses(value) {
  if (!value) throw new Error('--harness requires a value');
  const raw = value.split(',').map(v => v.trim().toLowerCase()).filter(Boolean);
  if (raw.includes('all')) return [...HARNESSES];
  const aliases = { claude: 'claude-code', 'claude_code': 'claude-code', open: 'opencode', ag: 'antigravity' };
  const resolved = [...new Set(raw.map(v => aliases[v] || v))];
  const invalid = resolved.filter(v => !HARNESSES.includes(v));
  if (invalid.length) throw new Error(`Unknown harness: ${invalid.join(', ')}`);
  if (!resolved.length) throw new Error('Select at least one harness');
  return resolved;
}

function normalizeLayout(value) {
  if (!value) throw new Error('--layout requires a value');
  const v = value.toLowerCase();
  if (['agents', '.agents', 'shared'].includes(v)) return 'agents';
  if (['native', 'custom', 'harness'].includes(v)) return 'native';
  throw new Error(`Unknown layout: ${value}. Use agents or native.`);
}

function normalizeGitExclude(value) {
  if (!value) throw new Error('--git-exclude requires a value');
  const v = value.toLowerCase();
  if (!['auto', 'yes', 'no'].includes(v)) throw new Error('--git-exclude must be auto, yes, or no');
  return v;
}

async function interactiveMissing(opts) {
  if (opts.harnesses && opts.layout) return opts;
  if (!process.stdin.isTTY) throw new Error('Interactive input is unavailable. Pass --harness and --layout.');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    if (!opts.harnesses) {
      console.log('\nSelect the harnesses to install:');
      HARNESSES.forEach((h, i) => console.log(`  ${i + 1}) ${LABELS[h]}`));
      console.log('  a) All');
      const answer = (await rl.question('Harnesses [comma-separated numbers, e.g. 1,2,4]: ')).trim().toLowerCase();
      if (answer === 'a' || answer === 'all') opts.harnesses = [...HARNESSES];
      else {
        const nums = answer.split(',').map(x => Number(x.trim())).filter(Number.isInteger);
        if (!nums.length || nums.some(n => n < 1 || n > HARNESSES.length)) throw new Error('Invalid harness selection');
        opts.harnesses = [...new Set(nums.map(n => HARNESSES[n - 1]))];
      }
    }
    if (!opts.layout) {
      console.log('\nWhere should SKILL.md packages be installed?');
      console.log('  1) .agents/skills (shared Agent Skills location)');
      console.log('  2) Harness-native skill directories');
      const answer = (await rl.question('Skill layout [1/2]: ')).trim();
      if (answer === '1') opts.layout = 'agents';
      else if (answer === '2') opts.layout = 'native';
      else throw new Error('Invalid skill layout selection');
    }
  } finally {
    rl.close();
  }
  return opts;
}

function walkFiles(root) {
  if (!fs.existsSync(root)) return [];
  const out = [];
  const visit = (dir) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) visit(full);
      else if (entry.isFile()) out.push(full);
    }
  };
  visit(root);
  return out;
}

function addTree(ops, srcRoot, destRoot) {
  for (const src of walkFiles(srcRoot)) {
    ops.push({ src, dest: path.join(destRoot, path.relative(srcRoot, src)) });
  }
}

function addFile(ops, src, dest) {
  if (fs.existsSync(src)) ops.push({ src, dest });
}

function sharedSkillSource() {
  return path.join(ROOT, 'dist', 'shared', '.agents', 'skills');
}

function planOperations(opts) {
  const target = opts.target;
  const ops = [];

  const codexAntigravityCollision = opts.layout === 'native' && opts.harnesses.includes('codex') && opts.harnesses.includes('antigravity');

  if (opts.layout === 'agents' || codexAntigravityCollision) {
    addTree(ops, sharedSkillSource(), path.join(target, '.agents', 'skills'));
  }

  for (const h of opts.harnesses) {
    if (opts.layout === 'native') {
      if (h === 'opencode') addTree(ops, path.join(ROOT, 'dist', 'opencode', '.opencode', 'skills'), path.join(target, '.opencode', 'skills'));
      else if (h === 'claude-code') addTree(ops, path.join(ROOT, 'dist', 'claude-code', '.claude', 'skills'), path.join(target, '.claude', 'skills'));
      else if (h === 'codex' && !codexAntigravityCollision) addTree(ops, path.join(ROOT, 'dist', 'codex', '.agents', 'skills'), path.join(target, '.agents', 'skills'));
      else if (h === 'antigravity' && !codexAntigravityCollision) addTree(ops, path.join(ROOT, 'dist', 'antigravity', '.agents', 'skills'), path.join(target, '.agents', 'skills'));
    }

    // Harness-specific support files are always installed in native locations.
    if (h === 'opencode') {
      addTree(ops, path.join(ROOT, 'dist', 'opencode', '.opencode', 'agents'), path.join(target, '.opencode', 'agents'));
    } else if (h === 'claude-code') {
      addTree(ops, path.join(ROOT, 'dist', 'claude-code', '.claude', 'agents'), path.join(target, '.claude', 'agents'));
    } else if (h === 'codex') {
      addTree(ops, path.join(ROOT, 'dist', 'codex', '.codex', 'agents'), path.join(target, '.codex', 'agents'));
      if (opts.layout === 'agents') {
        // Shared profile already includes Codex agents/openai.yaml sidecars.
      }
    } else if (h === 'antigravity') {
      addTree(ops, path.join(ROOT, 'dist', 'antigravity', '.agents', 'workflows'), path.join(target, '.agents', 'workflows'));
      addTree(ops, path.join(ROOT, 'dist', 'antigravity', '.agents', 'rules'), path.join(target, '.agents', 'rules'));
      addFile(ops, path.join(ROOT, 'dist', 'antigravity', '.agents', 'agents.md'), path.join(target, '.agents', 'agents.md'));
    }
  }

  // Deduplicate identical destinations; last identical-content source is harmless, conflicting ones are blocked.
  const byDest = new Map();
  for (const op of ops) {
    const existing = byDest.get(op.dest);
    if (!existing) byDest.set(op.dest, op);
    else {
      const a = fs.readFileSync(existing.src);
      const b = fs.readFileSync(op.src);
      if (!a.equals(b)) throw new Error(`Installation profiles conflict at ${path.relative(target, op.dest)}. Use --layout agents for a shared copy or select fewer harnesses.`);
    }
  }
  return [...byDest.values()].sort((a, b) => a.dest.localeCompare(b.dest));
}

function resolveGitDir(target) {
  const dotGit = path.join(target, '.git');
  if (!fs.existsSync(dotGit)) return null;
  const stat = fs.statSync(dotGit);
  if (stat.isDirectory()) return dotGit;
  if (stat.isFile()) {
    const firstLine = fs.readFileSync(dotGit, 'utf8').split(/\r?\n/, 1)[0].trim();
    const match = /^gitdir:\s*(.+)$/i.exec(firstLine);
    if (match) return path.resolve(target, match[1]);
  }
  return null;
}

function ensureTmpExclude(opts) {
  if (opts.gitExclude === 'no') return null;
  const gitDir = resolveGitDir(opts.target);
  if (!gitDir) {
    if (opts.gitExclude === 'yes') throw new Error(`--git-exclude=yes requires a Git repository or worktree at ${opts.target}`);
    return null;
  }
  const exclude = path.join(gitDir, 'info', 'exclude');
  const rule = '/.agents/tmp/';
  let current = fs.existsSync(exclude) ? fs.readFileSync(exclude, 'utf8') : '';
  if (current.split(/\r?\n/).some(line => line.trim() === rule)) return null;
  return { exclude, current, rule };
}

function relativeDisplay(target, p) {
  const r = path.relative(target, p);
  return r && !r.startsWith('..') ? r : p;
}

function execute(ops, opts, excludeOp) {
  const conflicts = ops.filter(op => fs.existsSync(op.dest) && !fs.readFileSync(op.dest).equals(fs.readFileSync(op.src)));
  if (conflicts.length && !opts.force && !opts.dryRun) {
    const preview = conflicts.slice(0, 10).map(op => `  - ${relativeDisplay(opts.target, op.dest)}`).join('\n');
    throw new Error(`Existing managed files differ. Re-run with --force to overwrite:\n${preview}${conflicts.length > 10 ? `\n  ... and ${conflicts.length - 10} more` : ''}`);
  }
  if (opts.dryRun && conflicts.length) {
    console.log(`[dry-run] ${conflicts.length} existing managed file(s) differ and would require --force for a real install.`);
  }

  for (const op of ops) {
    console.log(`${opts.dryRun ? '[dry-run] ' : ''}write ${relativeDisplay(opts.target, op.dest)}`);
    if (!opts.dryRun) {
      fs.mkdirSync(path.dirname(op.dest), { recursive: true });
      fs.copyFileSync(op.src, op.dest);
    }
  }

  if (excludeOp) {
    console.log(`${opts.dryRun ? '[dry-run] ' : ''}append ${excludeOp.rule} -> ${relativeDisplay(opts.target, excludeOp.exclude)}`);
    if (!opts.dryRun) {
      fs.mkdirSync(path.dirname(excludeOp.exclude), { recursive: true });
      const needsNl = excludeOp.current.length && !excludeOp.current.endsWith('\n');
      fs.appendFileSync(excludeOp.exclude, `${needsNl ? '\n' : ''}${excludeOp.rule}\n`);
    }
  }
}

function printSummary(opts, ops) {
  console.log('\nInstallation complete.');
  console.log(`Target: ${opts.target}`);
  console.log(`Harnesses: ${opts.harnesses.map(h => LABELS[h]).join(', ')}`);
  console.log(`Skill layout: ${opts.layout === 'agents' ? '.agents/skills' : 'harness-native'}`);
  console.log(`Files managed: ${ops.length}`);
  if (opts.layout === 'agents' && opts.harnesses.includes('claude-code')) {
    console.log('Note: shared .agents mode uses standard Agent Skills frontmatter. Claude Code-specific SKILL.md invocation fields are only available with --layout native.');
  }
  if (opts.harnesses.includes('codex') && opts.harnesses.includes('antigravity')) {
    console.log('Note: Codex and Antigravity share .agents/skills at project scope, so a standards-compliant shared skill copy is used to avoid conflicting SKILL.md variants.');
  }
  if (opts.layout === 'agents' && opts.harnesses.includes('antigravity')) {
    console.log('Note: Antigravity will also see shared explicit-only skill packages while its slash workflows are installed under .agents/workflows.');
  }
}

(async () => {
  try {
    let opts = parseArgs(process.argv.slice(2));
    if (opts.help) { console.log(usage()); return; }
    if (opts.version) { console.log(VERSION); return; }
    opts = await interactiveMissing(opts);
    if (!fs.existsSync(opts.target)) throw new Error(`Target does not exist: ${opts.target}`);
    if (!fs.statSync(opts.target).isDirectory()) throw new Error(`Target is not a directory: ${opts.target}`);
    const ops = planOperations(opts);
    const excludeOp = ensureTmpExclude(opts);
    execute(ops, opts, excludeOp);
    printSummary(opts, ops);
  } catch (err) {
    console.error(`\nsoftware-skills: ${err.message}`);
    process.exitCode = 1;
  }
})();
