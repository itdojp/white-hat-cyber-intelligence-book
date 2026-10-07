// Isolated children inject real late writes before rmdir, not synthetic errors.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const mode = process.argv[2];
const modes = ['ordinary', 'missing', 'old-race', 'late-write', 'persistent'];
if (!mode) {
  const tmp = path.resolve(__dirname, '../.tmp');
  fs.mkdirSync(tmp, { recursive: true });
  const root = fs.mkdtempSync(path.join(tmp, 'cleanup-contract-'));
  try {
    for (const mode of modes) {
      const result = spawnSync(process.execPath, [__filename, mode, root], {
        encoding: 'utf8', timeout: 30000,
      });
      assert.ifError(result.error);
      assert.equal(result.status, 0, `${mode}: ${result.stderr}`);
      assert.equal(result.stdout.trim(), `${mode}: passed`);
    }
    console.log('Browser profile cleanup contract passed: 5 cases, sibling preservation');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
} else {
  assert(modes.includes(mode), `Unknown test mode: ${mode}`);
  const root = process.argv[3];
  const profile = fs.mkdtempSync(path.join(root, 'profile-'));
  const sibling = path.join(root, 'keep.txt');
  fs.writeFileSync(sibling, 'must remain');
  const target = path.join(profile, 'Default');
  fs.mkdirSync(target);
  fs.writeFileSync(path.join(target, 'seed'), 'initial profile data');
  // Install before the first async rm: Node's recursive remover captures rmdir.
  const original = fs.rmdir;
  let calls = 0, writes = 0;
  fs.rmdir = function (file, ...args) {
    if (String(file) === target) {
      calls++;
      if ((mode === 'persistent' && calls >= 2) ||
          (['old-race', 'late-write'].includes(mode) && calls === 2)) {
        fs.writeFileSync(path.join(target, 'late'), 'late profile write');
        writes++;
      }
    }
    return original.call(this, file, ...args);
  };
  (async () => {
    try {
      if (mode === 'missing') fs.rmSync(profile, { recursive: true });
      const { removeBrowserProfile } = await import('./browser_profile_cleanup.mjs');
      const remove = mode === 'old-race'
        ? () => fs.promises.rm(profile, { recursive: true, force: true })
        : () => removeBrowserProfile(profile);
      if (['old-race', 'persistent'].includes(mode)) {
        await assert.rejects(remove, { code: 'ENOTEMPTY' });
        assert(fs.existsSync(profile), 'Failure must not claim cleanup succeeded');
      } else {
        await remove();
        assert(!fs.existsSync(profile));
      }
      if (['old-race', 'late-write'].includes(mode)) assert.equal(writes, 1);
      if (mode === 'persistent') assert(writes > 1, 'Persistent case must exhaust retries');
      assert.equal(fs.readFileSync(sibling, 'utf8'), 'must remain');
      console.log(`${mode}: passed`);
    } finally {
      fs.rmdir = original;
      // Sync teardown is outside the instrumented async rmdir path.
      fs.rmSync(profile, { recursive: true, force: true });
    }
  })().catch(error => { console.error(error); process.exitCode = 1; });
}
