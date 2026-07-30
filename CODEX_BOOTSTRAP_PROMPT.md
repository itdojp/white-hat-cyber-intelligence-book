# Codex CLI Phase 0 Resume Prompt

Phase 0の実装は完了し、PR #2はReady for reviewである。この指示は、最終レビュー対応とmerge前の検証を別のCodex CLIセッションへ引き継ぐ場合にだけ使用する。

```text
/goal Resume GitHub Issue #1 and PR #2 in itdojp/white-hat-cyber-intelligence-book. Preserve the completed Phase 0 architecture, address only new actionable findings against the current PR head, rerun all required checks, and leave an exact operator handoff. Do not merge or change repository settings.

Authoritative state to verify before acting:
- repository: itdojp/white-hat-cyber-intelligence-book
- base root commit: 346e838ec619214249e674b9669cbebc9cbf7891
- branch: bootstrap/book-foundation
- pull request: #2
- Phase 0 Issue: #1
- operator/admin Issue: #9
- Phase 1-2 Roadmap: #3; representative chapter Issues #4 through #8
- pinned book-formatter: 69eb5c12f5a750b65614bc9bbbc3d7abd5aa6f6c
- canonical-source contract: CANONICAL_SOURCE.md
- agent contract: AGENTS.md
- expected Series UX: Profile B and exactly the eight defined modules

Known completed capabilities:
- editorial, safety, source, lab, governance, license, maintenance, and contribution contracts
- book-config with all 30 chapters (Chapter 0 through Chapter 29) and 10 appendices
- Chapter 0 and Chapter 1 drafts and nine artifact templates
- 20-source registry with chapter-mapping validation and generated reference baseline
- deterministic, non-destructive docs generation using pinned formatter components verified by Git blob SHA
- output restricted to docs/ with symlink and path-traversal rejection
- Book Contract, Book QA, Jekyll build, built-site smoke check, and Pages workflow
- immutable action SHAs, non-persistent checkout credentials, ignored npm lifecycle scripts, deploy-job-only OIDC
- complete formatter MIT attribution in THIRD_PARTY_NOTICES.md and the published License page

Before changing files:
1. Read Issue #1, Issue #9, PR #2, AGENTS.md, CANONICAL_SOURCE.md, SAFETY_SCOPE.md, SOURCE_POLICY.md, and .book-formatter/revision.json.
2. Fetch the live PR head, checks, reviews, and unresolved threads. Do not trust the head SHA recorded in this prompt after the repository moves.
3. Inspect the current diff and confirm no generated docs/, _site/, build/, node_modules/, or .work/ content is tracked.
4. Treat resolved review comments as historical evidence; do not reintroduce their old fixes.

Permitted work:
- address new actionable review comments on PR #2
- add a narrowly scoped regression test for each correctness or security fix
- rerun npm ci --ignore-scripts, npm test, Book QA-equivalent checks, Jekyll build, npm audit, and artifact inspection
- reply to each review thread with commit and run evidence, then resolve it
- update PR #2 and Issue #1 with the exact current head and workflow run IDs
- produce an operator packet for Issue #9

Required validation:
- npm test
- BOOK_FORMATTER_DIR=<pinned checkout> npm run build
- python3 scripts/check_built_site.py --source docs --site _site
- npm audit --audit-level=moderate
- Git status shows no canonical-source modification from generation and no tracked generated output
- Book Contract and Book QA succeed on the exact final head
- unresolved review threads are zero
- public artifact contains required license notices and canonical edit links

Hard constraints:
- no direct push to main
- no merge, auto-merge, administrator bypass, branch-rule change, Pages setting change, or Security setting change
- no changes to existing book repositories or the parent portfolio catalog
- no real external target, credential, token, cookie, personal data, malware, C2, persistence, evasion, destructive action, or uncoordinated vulnerability detail
- do not begin representative chapter implementation in PR #2
- do not mark Issue #1 complete before explicit merge and first Pages deployment verification

If no actionable review finding remains:
- do not create churn
- record the final head, successful run IDs, unresolved-thread count, and artifact audit
- hand off Issue #9 as the only remaining Phase 0 operator work
- state that Roadmap #3 can begin only after PR #2 is merged and Pages is verified
```
