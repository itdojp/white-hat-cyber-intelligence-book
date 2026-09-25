# Mermaid publication owner — Issue #160

## Decision (2026-09-25)

Jekyll correctly emits fenced source, but the pinned formatter has no Mermaid initializer. GitHub's Markdown preview and this Pages build are different products. Keep canonical source and the pinned Kramdown/Projection/Policy contracts unchanged; enhance their emitted code blocks in the browser.

Use the official **Tiny 12.0.0 standalone browser distribution**, obtained through an exact npm dev dependency only as a byte-distribution channel. It is not imported as a Node API. `package-lock.json` pins package integrity; `scripts/publication_assets.py` independently verifies the browser file SHA-256 before replacing generated output. The 2,898,960-byte bundle has no runtime chunk fetches and is requested only when an article contains diagrams. Browser traffic stays on this Pages origin; there is no CDN, external font, online renderer or network call during generation after installation. Node >=22.12 matches the package metadata.

The [official Tiny README](https://www.npmjs.com/package/@mermaid-js/tiny) recommends the full package for general application development. This use is deliberately its narrow standalone-script case, self-hosting the same distribution instead of its CDN example. Tiny omits mindmap, architecture and KaTeX; this book currently uses only flowcharts. The [Mermaid API documentation](https://mermaid.js.org/config/usage.html) describes explicit initialization and strict security. The [configuration schema](https://mermaid.js.org/config/schema-docs/config.html) documents secure keys and deterministic IDs. Package release: [12.0.0](https://github.com/mermaid-js/mermaid/releases/tag/mermaid%4012.0.0).

## Rejected alternatives

- An unpinned CDN script is small to configure but creates a third-party runtime dependency and mutable supply-chain/privacy boundary.
- The full 12.0.0 standalone distribution is 5,575,485 bytes; its extra diagram families/math are unnecessary here. ESM lazy chunks add asset copying/import graph ownership that this finite book does not need.
- Build-time CLI/SVG generation would remove client JS but add a browser/rendering dependency to source generation, font/layout pinning and a second Markdown transformation stage. Do not introduce that larger migration for a missing initializer.
- Hand-writing flowchart layout or rewriting individual chapters would duplicate a renderer and miss other published diagrams.

## Security / limits

Only `article pre > code.language-mermaid` is selected. Source comes from textContent, not source HTML. The official parser owns the grammar. A small shared feature policy rejects diagram configuration, callbacks/links, diagram CSS, resource-bearing `@{...}` shapes and HTML other than `br`; it is not a second Mermaid parser. Other diagram families fail visibly and fail the publication browser gate. Strict mode, SVG text labels, bounded source/edges, secure configuration keys, no callback binding, and cleanup of the temporary rendering host are enforced. The site is not a general untrusted diagram editor. New syntax needs an explicit coverage/security review, not a chapter-specific parser exception.

The original pre/code is retained unchanged in details after success; no-script and failure cases retain source plus authored prose. Regions are keyboard-scrollable and offer a fit/restore control. The SVG has a white background for consistent contrast under both page themes. Fit mode trades label size for overview; default size preserves readable labels. Printed diagrams fit the page.

The checked-in fixture corpus tests positive LR/TD/graph, Japanese/br, multiple diagrams, and negative configuration/HTML/image/click/size/syntax/library cases. `check_mermaid_browser.mjs` reads the actual built manifest, exercises all published diagrams at desktop/mobile widths, tests keyboard scrolling and fit, and checks for duplicate IDs and external page requests. Syntax/resource failures stop Book QA/Pages before artifact upload. Node's built-in CDP transport avoids an additional browser-driver dependency. Chrome comes from the documented Ubuntu runner image; the test records its observed version and does not claim pixel equality across all browsers/OSs. [Runner inventory](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md).

`npm audit` inspects the installed package metadata, not every dependency bundled inside the upstream JS. Review the upstream security advisories and bundled notices when changing this pin. Do not claim the audit alone proves the renderer safe. Distribution attribution is recorded in `THIRD_PARTY_NOTICES.md` and copied into the site.

## Verification

```bash
npm ci --ignore-scripts
npm run check:mermaid
BOOK_FORMATTER_DIR=../book-formatter npm run check:book-qa
```

The full QA includes the browser gate; it requires an installed Chrome/Chromium (`BOOK_BROWSER_BIN` override). `BOOK_BROWSER_TMPDIR` and `BOOK_BROWSER_OUTPUT` must be kept inside the active workspace. Browser screenshots/results are ignored artifacts, not canonical book content. No real target operations or repository settings changes are involved.

### Linux browser temporary paths

Linux Chrome uses Unix sockets with short pathname limits. CI workspace names can exceed that limit even though ordinary files are valid. The browser gate holds an open handle to the workspace-owned temporary directory and uses `/proc/<parent-pid>/fd/<handle>` as Chrome's short `TMPDIR` alias. Actual temporary files stay inside that directory; nothing is written into `/proc` or an out-of-workspace temporary directory. The handle is closed after Chrome exits. Signal-terminated Chrome is treated as a failed launch and cleaned up without waiting for an already-emitted exit event. An absent/unusable browser fails the gate rather than skipping rendering.
