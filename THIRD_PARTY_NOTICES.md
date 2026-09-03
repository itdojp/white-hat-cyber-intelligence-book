# Third-Party Notices

This file records third-party material copied into generated publication artifacts. Source links alone are managed separately in `references/`.

## itdojp/book-formatter shared publication components

| Field | Value |
|---|---|
| Name | `itdojp/book-formatter` shared layouts, includes, styles, and scripts |
| Source | <https://github.com/itdojp/book-formatter> |
| Commit | `198935ff8f60653c40e513343dc5f02573d9968e` |
| Upstream package version | `1.0.0` |
| Shared component version | `3.2.3` |
| Copyright holder / author | ITDO Inc.（株式会社アイティードゥ） |
| License | MIT License, as declared by the pinned repository's `package.json` and README |
| Retrieved / verified | 2026-09-04 |
| Verification | Each copied source file is verified against the Git blob SHA in `.book-formatter/revision.json` |
| Distribution scope | Generated `docs/` site source and `_site/` publication artifact; the files are not human-authored canonical manuscript source |

### Copied files and generated placement

| Upstream path | Generated path | Modification |
|---|---|---|
| `shared/layouts/book.html` | `_layouts/book.html` | Edit links target canonical `page.source_path`; unused Google Fonts preconnect hints and links to absent favicon files are removed |
| `shared/layouts/default.html` | `_layouts/default.html` | None |
| `shared/includes/sidebar-nav.html` | `_includes/sidebar-nav.html` | None |
| `shared/includes/page-navigation.html` | `_includes/page-navigation.html` | None |
| `shared/assets/css/main.css` | `assets/css/main.css` | None |
| `shared/assets/css/mobile-responsive.css` | `assets/css/mobile-responsive.css` | None |
| `shared/assets/css/syntax-highlighting.css` | `assets/css/syntax-highlighting.css` | None |
| `shared/assets/js/code-copy-lightweight.js` | `assets/js/code-copy-lightweight.js` | None |
| `shared/assets/js/search.js` | `assets/js/search.js` | None |
| `shared/assets/js/theme.js` | `assets/js/theme.js` | None |

The exact source paths, Git blob SHAs, generated targets, and declared local transforms are machine-readable in `.book-formatter/revision.json`. The generated `_data/build-manifest.json` records the transformed output SHA-256 values for each build.

### MIT License notice

```text
MIT License

Copyright (c) ITDO Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Future third-party additions

A pull request that adds another third-party work must record:

- name and canonical source
- copyright holder
- version, release, or commit SHA
- license and complete required notice
- whether the work is modified
- repository and publication placement
- retrieval date and integrity verification
- attribution, source-offer, or redistribution requirements

Material with unknown or incompatible redistribution terms must not be copied into the repository or publication artifact.
