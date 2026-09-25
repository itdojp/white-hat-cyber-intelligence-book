/* Progressive enhancement of the locked Jekyll renderer's code blocks. */
(() => {
  'use strict';
  const libraryUrl = document.currentScript?.dataset.mermaidSrc;
  const blocks = [...document.querySelectorAll('article pre > code.language-mermaid')];
  if (!blocks.length) return;

  function fail(code) {
    code.dataset.mermaidState = 'error';
    const notice = document.createElement('p');
    notice.className = 'mermaid-error';
    notice.textContent = '図を描画できませんでした。図のソースと本文の文章による説明を参照してください。';
    code.parentElement.before(notice);
  }

  async function load() {
    if (!libraryUrl) throw new Error('Missing local Mermaid asset');
    await new Promise((resolve, reject) => {
      const script = document.createElement('script');
      const timer = setTimeout(() => { script.remove(); reject(new Error('Mermaid load timeout')); }, 15000);
      script.src = libraryUrl;
      script.onload = () => { clearTimeout(timer); resolve(); };
      script.onerror = () => { clearTimeout(timer); script.remove(); reject(new Error('Mermaid load failed')); };
      document.head.append(script);
    });
    if (!globalThis.mermaid) throw new Error('Missing Mermaid API');
    // Do not auto-render unrelated .mermaid elements or bind click callbacks.
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      suppressErrorRendering: true,
      deterministicIds: true,
      deterministicIDSeed: 'book-mermaid-v1',
      maxTextSize: 20000,
      maxEdges: 200,
      theme: 'default',
      htmlLabels: false,
      fontFamily: 'sans-serif',
      flowchart: { htmlLabels: false, useMaxWidth: false },
      secure: ['secure', 'securityLevel', 'startOnLoad', 'suppressErrorRendering',
        'maxTextSize', 'maxEdges', 'htmlLabels', 'flowchart', 'theme', 'fontFamily',
        'deterministicIds', 'deterministicIDSeed'],
    });
  }

  async function render(code, index) {
    const source = code.textContent;
    // Publication feature policy, not a Mermaid parser. The official parser
    // owns flowchart syntax. Configuration and resource-bearing extensions
    // are not part of this book's diagrams and must not override site policy.
    if (source.length > 20000 || !/^\s*(?:flowchart|graph)\s+(?:LR|RL|TD|TB|BT)\b/.test(source)
        || /%%\s*\{|@\s*\{|\b(?:click|style|classDef|linkStyle)\s|<(?!br\s*\/?\s*>)/i.test(source)) {
      throw new Error('Unsupported publication diagram feature');
    }
    const host = document.createElement('div');
    host.className = 'mermaid-render-host';
    document.body.append(host);
    try {
      const { svg } = await mermaid.render(`book-mermaid-${index + 1}`, source, host);
      const view = document.createElement('div');
      view.className = 'mermaid-view';
      view.tabIndex = 0;
      view.setAttribute('role', 'region');
      view.setAttribute('aria-label', `図 ${index + 1}（横にスクロールできます）`);
      // Mermaid strict sanitizes the generated SVG; source HTML is never used.
      view.innerHTML = svg;
      const graphic = view.querySelector('svg');
      if (!graphic || graphic.querySelector('.error-icon')) throw new Error('No diagram');
      const figure = document.createElement('figure');
      figure.className = 'mermaid-figure';
      const caption = document.createElement('figcaption');
      caption.textContent = '図は横にスクロールできます。文章による説明は本文を参照してください。';
      const fit = document.createElement('button');
      fit.type = 'button';
      fit.textContent = '全体表示';
      fit.setAttribute('aria-pressed', 'false');
      fit.addEventListener('click', () => {
        const fitted = view.classList.toggle('mermaid-fit');
        fit.setAttribute('aria-pressed', String(fitted));
        fit.textContent = fitted ? '読みやすい大きさに戻す' : '全体表示';
      });
      const details = document.createElement('details');
      const summary = document.createElement('summary');
      summary.textContent = '図のソースを表示';
      details.append(summary);
      code.parentElement.before(figure);
      details.append(code.parentElement);
      figure.append(caption, fit, view, details);
      code.dataset.mermaidState = 'rendered';
    } finally {
      host.remove();
    }
  }

  (async () => {
    try { await load(); } catch { blocks.forEach(fail); return; }
    await document.fonts.ready;
    for (const [index, code] of blocks.entries()) {
      try { await render(code, index); } catch { fail(code); }
    }
  })();
})();
