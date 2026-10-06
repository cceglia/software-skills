#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const readline = require('readline/promises');
const process = require('process');

const ROOT = path.resolve(__dirname, '..');
const VERSION = require(path.join(ROOT, 'package.json')).version;
const PROFILE_SOURCE = path.join(ROOT, 'dist', '.opencode');
const REMOVED_SKILLS = ['my-git-commit', 'my-grill-to-spec', 'my-review-changes', 'my-spec-to-tickets'];

function usage() {
  return `software-skills ${VERSION}\n\n` +
`Install software-skills for OpenCode V2.\n\n` +
`Usage:\n` +
`  software-skills [options]\n\n` +
`Options:\n` +
`  --scope <scope>        Where to install: project | global\n` +
`  --target <path>        Project root for --scope project (default: current directory)\n` +
`  --force                Overwrite existing managed files\n` +
`  --dry-run              Print planned file operations without writing\n` +
`  --git-exclude <mode>   auto | yes | no (default: auto; project scope only)\n` +
`  --help                 Show this help\n` +
`  --version              Print installer version\n\n` +
`Scopes:\n` +
`  project  <target>/.opencode — skills and agents available only in that project.\n` +
`  global   ~/.config/opencode (or $OPENCODE_CONFIG_DIR, or $XDG_CONFIG_HOME/opencode) — available in every project.\n`;
}

function parseArgs(argv) {
  const out = { scope: null, target: null, force: false, dryRun: false, gitExclude: 'auto' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--') continue;
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--version' || a === '-v') out.version = true;
    else if (a === '--force') out.force = true;
    else if (a === '--dry-run') out.dryRun = true;
    else if (a === '--scope') out.scope = normalizeScope(argv[++i]);
    else if (a.startsWith('--scope=')) out.scope = normalizeScope(a.slice(8));
    else if (a === '--target') out.target = path.resolve(requireValue(a, argv[++i]));
    else if (a.startsWith('--target=')) out.target = path.resolve(a.slice(9));
    else if (a === '--git-exclude') out.gitExclude = normalizeGitExclude(argv[++i]);
    else if (a.startsWith('--git-exclude=')) out.gitExclude = normalizeGitExclude(a.slice(14));
    else throw new Error(`Unknown argument: ${a}`);
  }
  return out;
}

function requireValue(flag, value) {
  if (!value) throw new Error(`${flag} requires a value`);
  return value;
}

function normalizeScope(value) {
  const v = requireValue('--scope', value).toLowerCase();
  if (['project', 'local', 'repo'].includes(v)) return 'project';
  if (['global', 'user', 'personal'].includes(v)) return 'global';
  throw new Error(`Unknown scope: ${value}. Use project or global.`);
}

function normalizeGitExclude(value) {
  const v = requireValue('--git-exclude', value).toLowerCase();
  if (!['auto', 'yes', 'no'].includes(v)) throw new Error('--git-exclude must be auto, yes, or no');
  return v;
}

function opencodeHome() {
  if (process.env.OPENCODE_CONFIG_DIR) return path.resolve(process.env.OPENCODE_CONFIG_DIR);
  const base = process.env.XDG_CONFIG_HOME ? path.resolve(process.env.XDG_CONFIG_HOME) : path.join(os.homedir(), '.config');
  return path.join(base, 'opencode');
}

async function interactiveMissing(opts) {
  if (opts.scope) return opts;
  if (!process.stdin.isTTY) throw new Error('Interactive input is unavailable. Pass --scope project or --scope global.');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    console.log('\nWhere should the OpenCode V2 skills be installed?');
    console.log(`  1) Project (${path.join(opts.target || process.cwd(), '.opencode')})`);
    console.log(`  2) Global (${opencodeHome()})`);
    const answer = (await rl.question('Scope [1/2]: ')).trim();
    if (answer === '1') opts.scope = 'project';
    else if (answer === '2') opts.scope = 'global';
    else throw new Error('Invalid scope selection');
  } finally {
    rl.close();
  }
  return opts;
}

// Resolves the OpenCode root (.opencode directory) that receives skills and agents.
function resolveInstallRoot(opts) {
  if (opts.scope === 'global') {
    if (opts.target) throw new Error('--target applies only to --scope project');
    if (opts.gitExclude === 'yes') throw new Error('--git-exclude=yes applies only to --scope project');
    return opencodeHome();
  }
  opts.target = opts.target || process.cwd();
  if (!fs.existsSync(opts.target)) throw new Error(`Target does not exist: ${opts.target}`);
  if (!fs.statSync(opts.target).isDirectory()) throw new Error(`Target is not a directory: ${opts.target}`);
  return path.join(opts.target, '.opencode');
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

function planOperations(installRoot) {
  const files = walkFiles(PROFILE_SOURCE);
  if (!files.length) throw new Error(`No built profile found in ${PROFILE_SOURCE}. Run python3 scripts/build.py.`);
  return files
    .map(src => ({ src, dest: path.join(installRoot, path.relative(PROFILE_SOURCE, src)) }))
    .sort((a, b) => a.dest.localeCompare(b.dest));
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
  if (opts.scope !== 'project' || opts.gitExclude === 'no') return null;
  const gitDir = resolveGitDir(opts.target);
  if (!gitDir) {
    if (opts.gitExclude === 'yes') throw new Error(`--git-exclude=yes requires a Git repository or worktree at ${opts.target}`);
    return null;
  }
  const exclude = path.join(gitDir, 'info', 'exclude');
  const rule = '/.agents/tmp/';
  const current = fs.existsSync(exclude) ? fs.readFileSync(exclude, 'utf8') : '';
  if (current.split(/\r?\n/).some(line => line.trim() === rule)) return null;
  return { exclude, current, rule };
}

function display(base, p) {
  const r = path.relative(base, p);
  return r && !r.startsWith('..') ? r : p;
}

function execute(ops, opts, base, excludeOp) {
  const conflicts = ops.filter(op => fs.existsSync(op.dest) && !fs.readFileSync(op.dest).equals(fs.readFileSync(op.src)));
  if (conflicts.length && !opts.force && !opts.dryRun) {
    const preview = conflicts.slice(0, 10).map(op => `  - ${display(base, op.dest)}`).join('\n');
    throw new Error(`Existing managed files differ. Re-run with --force to overwrite:\n${preview}${conflicts.length > 10 ? `\n  ... and ${conflicts.length - 10} more` : ''}`);
  }
  if (opts.dryRun && conflicts.length) {
    console.log(`[dry-run] ${conflicts.length} existing managed file(s) differ and would require --force for a real install.`);
  }

  for (const op of ops) {
    console.log(`${opts.dryRun ? '[dry-run] ' : ''}write ${display(base, op.dest)}`);
    if (!opts.dryRun) {
      fs.mkdirSync(path.dirname(op.dest), { recursive: true });
      fs.copyFileSync(op.src, op.dest);
    }
  }

  if (excludeOp) {
    console.log(`${opts.dryRun ? '[dry-run] ' : ''}append ${excludeOp.rule} -> ${display(base, excludeOp.exclude)}`);
    if (!opts.dryRun) {
      fs.mkdirSync(path.dirname(excludeOp.exclude), { recursive: true });
      const needsNl = excludeOp.current.length && !excludeOp.current.endsWith('\n');
      fs.appendFileSync(excludeOp.exclude, `${needsNl ? '\n' : ''}${excludeOp.rule}\n`);
    }
  }
}

// Skills removed from the package are reported, never deleted.
function leftovers(installRoot) {
  return REMOVED_SKILLS
    .map(name => path.join(installRoot, 'skills', name))
    .filter(p => fs.existsSync(path.join(p, 'SKILL.md')));
}

function printSummary(opts, installRoot, ops) {
  console.log(`\n${opts.dryRun ? 'Dry run complete.' : 'Installation complete.'}`);
  console.log(`Scope: ${opts.scope}`);
  console.log(`OpenCode directory: ${installRoot}`);
  console.log(`Files managed: ${ops.length}`);
  if (opts.scope === 'global') {
    console.log('Note: workflow ledgers live in each project under ./.agents/tmp/; keep that path out of commits (for example via .git/info/exclude).');
  }
  const legacy = leftovers(installRoot);
  if (legacy.length) {
    console.log('Note: these skills from earlier software-skills releases are no longer shipped and can be removed:');
    for (const p of legacy) console.log(`  - ${p}`);
  }
}

(async () => {
  try {
    let opts = parseArgs(process.argv.slice(2));
    if (opts.help) { console.log(usage()); return; }
    if (opts.version) { console.log(VERSION); return; }
    opts = await interactiveMissing(opts);
    const installRoot = resolveInstallRoot(opts);
    const base = opts.scope === 'project' ? opts.target : installRoot;
    const ops = planOperations(installRoot);
    const excludeOp = ensureTmpExclude(opts);
    execute(ops, opts, base, excludeOp);
    printSummary(opts, installRoot, ops);
  } catch (err) {
    console.error(`\nsoftware-skills: ${err.message}`);
    process.exitCode = 1;
  }
})();
