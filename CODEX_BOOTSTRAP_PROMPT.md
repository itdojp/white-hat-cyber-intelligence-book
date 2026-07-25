# Codex CLI Bootstrap Prompt

このチャットでEditorial Foundationまで実装済みである。Codex CLIを使う場合は、既存Draft PR #2を継続し、未完了のSeries UX同期とbuild検証だけを実施する。

```text
/goal Resume GitHub Issue #1 in itdojp/white-hat-cyber-intelligence-book. Continue the existing Draft PR #2 on bootstrap/book-foundation. Do not recreate the repository, branch, editorial contract, or planning files. Complete only the remaining Phase 0 Series UX synchronization, generated docs, Book QA, Jekyll build, drift checks, and verified handoff.

Known fixed state:
- main root commit: 346e838ec619214249e674b9669cbebc9cbf7891
- working branch: bootstrap/book-foundation
- Draft PR: #2
- book-formatter pinned revision: 69eb5c12f5a750b65614bc9bbbc3d7abd5aa6f6c
- canonical authoring contract: CANONICAL_SOURCE.md
- Series UX: Profile B; exactly 8 defined modules in book-config.json

Before changing files:
1. Read Issue #1, parent Issue #280, PR #2, CANONICAL_SOURCE.md, book-config.json, and .book-formatter/revision.json.
2. Confirm the branch head descends from main root commit and inspect the entire current diff.
3. Re-check that the pinned book-formatter revision is still the intended audited revision; do not silently change it.

Remaining scope:
- Synchronize current shared layouts/includes/assets from the pinned revision and record provenance.
- Generate docs/ from canonical sources without modifying canonical files.
- Add deterministic sync --check / drift checks.
- Add minimal package/Gem/Python dependencies and lockfiles required by the current series contract.
- Add Book QA and, if repository settings permit, Pages workflow using the current series pattern.
- Run config, metadata, links, Markdown structure, Unicode, source registry, safety, docs-sync, Jekyll build, and non-destructive build checks.
- Update PR #2 and Issue #1 with exact commands, SHAs, results, and remaining admin actions.

Hard constraints:
- no direct push to main, merge, auto-merge, admin bypass, or repository settings changes
- no changes to existing books or parent catalog
- no external target testing, credentials, personal data, malware, persistence, evasion, or destructive operations
- do not mark Issue #1 complete until sync, build, QA, and independent review gates pass
```
