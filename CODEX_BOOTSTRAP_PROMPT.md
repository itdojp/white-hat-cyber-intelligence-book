# Codex CLI Bootstrap Prompt

以下をCodex CLIの新規セッションへ渡す。

```text
/goal Resume GitHub Issue #1 in itdojp/white-hat-cyber-intelligence-book and execute Phase 0 only: build the current Series UX and book-formatter foundation on branch bootstrap/book-foundation, update the existing Draft PR, and leave a verified handoff for Phase 1.

Authoritative issues:
- Repository Phase 0: https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/1
- Parent book proposal: https://github.com/itdojp/it-engineer-knowledge-architecture/issues/280

Known repository state:
- Repository already exists and is public.
- Root commit on main: 346e838ec619214249e674b9669cbebc9cbf7891
- Working branch already exists: bootstrap/book-foundation
- The root commit contains only the minimum README required to materialize main.
- Do not create another repository or another bootstrap branch.

Local starter packet, if available:
white-hat-cyber-intelligence-book-starter/

Scope for this run:
1. Read Issue #1 and parent Issue #280 in full.
2. Inspect the current, not historical, publishing contracts in itdojp/it-engineer-knowledge-architecture, including:
   - docs/publishing/new-book-quickstart.md
   - docs/publishing/book-structure.md
   - docs/publishing/ux-profiles.md
   - docs/publishing/ux-modules.md
   - docs/publishing/review-checklist.md
   - templates/book/
   - current catalog, schema, canonical-source, build, QA, and Pages rules
3. Inspect and pin the exact current main SHA of itdojp/book-formatter used for generation.
4. Work only on bootstrap/book-foundation. Confirm it descends from the documented root commit before changing files.
5. Generate the book skeleton from the current book-formatter and Series UX contracts. Do not invent a separate publishing stack.
6. Use Series UX Profile B and only these currently defined modules:
   quickStart, readingGuide, checklistPack, troubleshootingFlow,
   conceptMap, figureIndex, legalNotice, glossary.
7. Establish one canonical authoring source and a non-destructive build contract.
8. Add the minimum governance and publication files:
   README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, book-config,
   standard QA/workflows, and initial site/navigation files required by the current template.
9. Import the planning and bootstrap material needed for Phase 0. Do not bulk-write all chapters. Keep chapter content to the minimum needed to validate navigation and the editorial contract.
10. Run all applicable local validation, build, drift, link, metadata, Markdown, Unicode, and safety checks.
11. Push only to bootstrap/book-foundation and update the existing Draft PR. If no Draft PR exists, create one.
12. Record fixed SHAs, commands, results, review findings, and remaining admin/operator actions in Issue #1. Add a concise status update to parent Issue #280.

Hard constraints:
- Do not push directly to main. The documented root commit is the only exception and is already complete.
- Do not merge, enable auto-merge, alter branch protection, change repository settings, or use admin bypass.
- Do not modify existing book repositories or the portfolio catalog in this run.
- Do not perform network scanning, authentication attempts, or testing against any external or production target.
- Do not introduce real credentials, tokens, cookies, personal data, malware, C2, persistence, evasion, destructive operations, or third-party target strings.
- Keep sample domains and addresses in reserved documentation ranges.
- Pin versions or digests where the current series contract requires them; do not use latest implicitly.
- Do not mark Issue #1 or parent Issue #280 complete until the stated gates and handoff conditions are satisfied.

Safety-stop conditions:
- The current template, book-formatter, canonical-source, or build contract is ambiguous or conflicting.
- A same-purpose repository or duplicate implementation issue is discovered.
- The only path requires direct main changes, admin bypass, or changes to existing books.
- A build or example requires external target access or real credentials.
- The existing bootstrap branch does not descend from the documented root commit.

On safety stop, do not improvise. Post an operator packet containing:
- exact completed checks and fixed SHAs,
- exact missing permission or decision,
- the smallest required human action,
- exact resume command and next safe step.
```
