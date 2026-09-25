// Real-browser publication gate. No npm browser package or downloaded browser.
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir, mkdtemp, rm } from 'node:fs/promises';
import { resolve, join, sep, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const site = resolve(root, process.env.BOOK_BROWSER_SITE || '_site');
const output = resolve(root, process.env.BOOK_BROWSER_OUTPUT || '.tmp/mermaid-browser');
const tmp = resolve(root, process.env.BOOK_BROWSER_TMPDIR || '.tmp');
await mkdir(tmp, { recursive: true });
await mkdir(output, { recursive: true });
const profile = await mkdtemp(join(tmp, 'mermaid-'));
const sleep = ms => new Promise(ok => setTimeout(ok, ms));
const manifest = JSON.parse(await readFile(join(root, 'docs/_data/build-manifest.json'), 'utf8'));
const fixtures = JSON.parse(await readFile(join(root, 'tests/fixtures/mermaid/publication.json'), 'utf8'));
const prefix = '/white-hat-cyber-intelligence-book/';
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const fixtureHtml = (fixture, broken = false) => `<html lang="ja"><head><meta charset="utf-8">
<link rel="stylesheet" href="${prefix}assets/css/mermaid-diagrams.css"></head><body>
<article><h1>図の回帰テスト</h1><p>文章による説明を保持。</p>${fixture.sources.map(source =>
  `<pre><code class="language-mermaid">${escape(source)}</code></pre>`).join('')}</article>
<script defer src="${prefix}assets/js/mermaid-loader.js" data-mermaid-src="${prefix}assets/js/${broken ? 'missing' : 'mermaid-12.0.0.tiny'}.js"></script></body></html>`;
const server = createServer(async (request, response) => {
  try {
    const route = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (route.startsWith('/fixture/')) {
      const id = route.split('/').at(-1);
      const fixture = fixtures.find(item => item.id === id);
      assert(fixture);
      response.setHeader('Content-Type', 'text/html; charset=utf-8');
      response.end(fixtureHtml(fixture, id === 'library-unavailable'));
      return;
    }
    assert(route.startsWith(prefix));
    const path = resolve(site, route.slice(prefix.length) + (route.endsWith('/') ? 'index.html' : ''));
    assert(path.startsWith(site + sep));
    const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json' };
    response.setHeader('Content-Type', `${types[extname(path)] || 'application/octet-stream'}; charset=utf-8`);
    response.end(await readFile(path));
  } catch { response.writeHead(404); response.end('Not found'); }
});
await new Promise(ok => server.listen(0, '127.0.0.1', ok));
const origin = `http://127.0.0.1:${server.address().port}`;
const chrome = spawn(process.env.BOOK_BROWSER_BIN || 'google-chrome', [
  '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-background-networking',
  '--disable-breakpad', '--no-first-run', '--no-default-browser-check',
  `--user-data-dir=${profile}`, '--remote-debugging-port=0', 'about:blank',
], { env: { ...process.env, HOME: profile, TMPDIR: tmp, XDG_CONFIG_HOME: profile,
  XDG_CACHE_HOME: profile, XDG_DATA_HOME: profile }, stdio: ['ignore', 'ignore', 'pipe'] });
let stderr = '', socket, launchError;
chrome.stderr.on('data', data => { stderr += data; });
chrome.on('error', error => { launchError = error; });
const results = [], requests = [], external = [], exceptions = [];
try {
  let port;
  for (let attempt = 0; attempt < 150; attempt++) {
    if (launchError) throw launchError;
    try { port = (await readFile(join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]; break; } catch {}
    if (chrome.exitCode !== null) throw new Error('Chrome exited: ' + stderr);
    await sleep(200);
  }
  assert(port, 'Chrome unavailable; set BOOK_BROWSER_BIN to an installed Chrome/Chromium');
  const page = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(item => item.type === 'page');
  socket = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((ok, bad) => { socket.onopen = ok; socket.onerror = bad; });
  let id = 0;
  const pending = new Map();
  const call = (method, params = {}) => new Promise((ok, bad) => {
    const key = ++id;
    const timer = setTimeout(() => { pending.delete(key); bad(new Error(`CDP timeout: ${method}`)); }, 30000);
    pending.set(key, { ok, bad, timer });
    socket.send(JSON.stringify({ id: key, method, params }));
  });
  socket.onmessage = ({ data }) => {
    const message = JSON.parse(data);
    if (message.method === 'Runtime.exceptionThrown') exceptions.push(message.params);
    if (message.method === 'Network.requestWillBeSent') requests.push(message.params.request.url);
    if (message.method === 'Fetch.requestPaused') {
      const { requestId, request } = message.params;
      const local = request.url.startsWith(origin + '/') || request.url.startsWith('data:');
      if (!local) external.push(request.url);
      call(local ? 'Fetch.continueRequest' : 'Fetch.failRequest',
        local ? { requestId } : { requestId, errorReason: 'BlockedByClient' }).catch(error => exceptions.push(String(error)));
    }
    if (pending.has(message.id)) {
      const { ok, bad, timer } = pending.get(message.id);
      clearTimeout(timer); pending.delete(message.id);
      message.error ? bad(new Error(JSON.stringify(message.error))) : ok(message.result);
    }
  };
  const evaluate = async expression => {
    const value = await call('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    assert(!value.exceptionDetails, JSON.stringify(value.exceptionDetails));
    return value.result.value;
  };
  for (const domain of ['Page', 'Runtime', 'Network', 'Fetch']) await call(`${domain}.enable`);
  const navigate = async (route, expected, disabled = false) => {
    await call('Emulation.setScriptExecutionDisabled', { value: disabled });
    await call('Page.navigate', { url: origin + route });
    let state;
    for (let attempt = 0; attempt < 150; attempt++) {
      state = await evaluate(`(() => ({path:location.pathname, ready:document.readyState,
        states:[...document.querySelectorAll('code.language-mermaid')].map(x=>x.dataset.mermaidState || 'source'),
        figures:document.querySelectorAll('.mermaid-view svg').length,
        errors:document.querySelectorAll('.mermaid-error').length,
        sources:[...document.querySelectorAll('code.language-mermaid')].map(x=>x.textContent),
        overflow:document.documentElement.scrollWidth > innerWidth,
        title:document.querySelector('h1')?.textContent,
        views:[...document.querySelectorAll('.mermaid-view')].map(v=>({width:v.clientWidth,scroll:v.scrollWidth,
          nodes:v.querySelectorAll('g.node').length, edges:v.querySelectorAll('.flowchart-link').length,
          text:v.textContent, viewBox:v.querySelector('svg').getAttribute('viewBox'),
          ids:[...v.querySelectorAll('[id]')].map(x=>x.id)}))
      }))()`);
      if (state.path === route && state.ready === 'complete'
          && JSON.stringify(state.states) === JSON.stringify(expected)) break;
      await sleep(200);
    }
    assert.equal(state.path, route); assert.equal(state.ready, 'complete');
    assert.deepEqual(state.states, expected, JSON.stringify(state));
    return state;
  };
  const pages = [];
  for (const item of manifest.pages) {
    const path = item.destination.replace(/\.md$/, '.html');
    const html = await readFile(join(site, path), 'utf8');
    const count = (html.match(/class="language-mermaid"/g) || []).length;
    if (count) pages.push({ path, count, source: item.source });
  }
  assert(pages.length > 0, 'No canonical diagrams selected');
  for (const [device, width, height] of [['desktop', 1440, 1000], ['mobile', 390, 844]]) {
    await call('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: device === 'mobile' });
    for (const item of pages) {
      const state = await navigate(prefix + item.path, Array(item.count).fill('rendered'));
      assert.equal(state.figures, item.count); assert.equal(state.errors, 0);
      assert(!state.overflow, `${item.source}: viewport overflow`);
      for (const view of state.views) { assert(view.nodes > 1); assert(view.edges > 0); assert(view.width > 0); }
      const ids = state.views.flatMap(view => view.ids);
      assert.equal(ids.length, new Set(ids).size, `${item.source}: duplicate SVG IDs`);
      await evaluate("document.querySelector('.mermaid-figure').scrollIntoView({block:'start',behavior:'instant'});window.scrollBy({top:-90,behavior:'instant'})");
      await sleep(150);
      const shot = await call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
      await writeFile(join(output, `${item.path.replaceAll('/', '-')}-${device}.png`), Buffer.from(shot.data, 'base64'));
      // Actual keyboard scrolling and fit/restore, not just existence of overflow CSS.
      await evaluate("document.querySelector('.mermaid-view').focus()");
      await call('Input.dispatchKeyEvent', { type: 'keyDown', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39 });
      await call('Input.dispatchKeyEvent', { type: 'keyUp', key: 'ArrowRight', code: 'ArrowRight', windowsVirtualKeyCode: 39 });
      await sleep(300);
      state.keyboard = await evaluate("(()=>{const v=document.querySelector('.mermaid-view');return {left:v.scrollLeft,width:v.clientWidth,scroll:v.scrollWidth}})()");
      if (state.keyboard.scroll > state.keyboard.width + 2) assert(state.keyboard.left > 0);
      await evaluate("document.querySelector('.mermaid-figure button').click()");
      assert(await evaluate("document.querySelector('.mermaid-view').scrollWidth <= document.querySelector('.mermaid-view').clientWidth + 2"));
      await evaluate("document.querySelector('.mermaid-figure button').click()");
      results.push({ device, ...item, ...state });
    }
  }
  await call('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
  for (const fixture of fixtures) {
    const state = await navigate('/fixture/' + fixture.id, fixture.expected);
    assert.deepEqual(state.sources, fixture.sources, 'Fallback source modified');
    assert.equal(state.errors, fixture.expected.filter(x => x === 'error').length);
    assert.equal(state.figures, fixture.expected.filter(x => x === 'rendered').length);
    if (fixture.nodes) assert.deepEqual(state.views.map(x => x.nodes), fixture.nodes);
    if (fixture.edges) assert.deepEqual(state.views.map(x => x.edges), fixture.edges);
    if (fixture.direction) {
      const centers = await evaluate("[...document.querySelectorAll('.mermaid-view g.node')].map(x=>{const r=x.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})");
      assert(centers[1][fixture.direction === 'LR' ? 'x' : 'y'] > centers[0][fixture.direction === 'LR' ? 'x' : 'y']);
    }
    results.push({ fixture: fixture.id, ...state });
  }
  // Fresh navigation: JS disabled retains the original sources and body.
  const disabled = await navigate('/fixture/lr', ['source'], true);
  assert.equal(disabled.figures, 0); assert.equal(disabled.errors, 0);
  assert.equal(disabled.title, '図の回帰テスト'); results.push({ fixture: 'javascript-disabled', ...disabled });
  const before = requests.length;
  const noDiagram = await navigate(prefix + 'chapters/chapter-04/index.html', []);
  assert.equal(noDiagram.figures, 0);
  assert(!requests.slice(before).some(url => url.includes('mermaid-12.0.0.tiny.js')), 'Loaded library on diagram-free page');
  assert.deepEqual(external, [], 'External page request attempted');
  assert.deepEqual(exceptions, [], 'Uncaught page exception');
  await writeFile(join(output, 'results.json'), JSON.stringify({ version: await call('Browser.getVersion'),
    pages: pages.length, diagrams: pages.reduce((n, page) => n + page.count, 0), results, external, exceptions,
    scope: 'Local Chrome viewport emulation; network interception covers page requests, not OS traffic.' }, null, 2) + '\n');
  console.log(`Mermaid browser gate passed: ${pages.length} pages / ${pages.reduce((n, p) => n + p.count, 0)} diagrams, desktop/mobile, ${fixtures.length} fixtures, JS-disabled, diagram-free page`);
} finally {
  await writeFile(join(output, 'chrome.log'), stderr);
  socket?.close(); chrome.kill('SIGTERM');
  await new Promise(ok => { if (chrome.exitCode !== null || launchError) ok(); else chrome.once('exit', ok); });
  await new Promise(ok => server.close(ok));
  await rm(profile, { recursive: true, force: true }); // Only this process's mkdtemp.
}
