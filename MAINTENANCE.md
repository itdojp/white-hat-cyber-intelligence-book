# Maintenance Guide

## Purpose

This guide defines recurring maintenance for the manuscript, source registry, shared publishing components, dependencies, workflows, and public site.

## Maintenance classes

| Class | Typical trigger | Required action |
|---|---|---|
| Source freshness | `nextReviewAt`, new standard, law amendment, framework release | Recheck canonical source, update affected chapters, regenerate baseline |
| Publishing components | new audited `book-formatter` revision | Review upstream diff, update blob manifest, rerun deterministic generation and visual checks |
| Dependencies | Dependabot alert, Ruby or Node update, action release | Update lock or immutable action SHA, run full QA and audit |
| Content defect | reader report, review finding, failed exercise | Reproduce safely, correct canonical source, add regression check |
| Security issue | private report or supply-chain alert | Follow `SECURITY.md`, avoid public exploit detail until coordinated |
| Public site | failed deployment, broken navigation, accessibility regression | Rebuild from canonical source, inspect artifact, repair generator or shared component pin |

## Source freshness

Run at least monthly and before every release:

```bash
python3 scripts/render_reference_baseline.py --check
python3 scripts/check_contract.py
```

For each source whose review date or trigger has been reached:

1. open the canonical official source
2. confirm title, status, version, publication or update date
3. compare with the recorded version
4. identify every affected chapter from `references/sources.json`
5. create a focused Issue for semantic changes
6. update the registry and manuscript together
7. regenerate `references/reference-baseline.md`
8. obtain source-quality and technical review

A reachable URL does not prove that the recorded claim remains correct.

## book-formatter update

Do not change only the commit field.

1. compare the currently pinned commit with the candidate commit
2. inspect changes to schema, layout, includes, assets, checks, and workflows
3. run the formatter test suite at the candidate commit
4. update every component path and Git blob SHA in `.book-formatter/revision.json`
5. update `scripts/check_shared_version.py`
6. run `npm test`
7. build the site twice and compare generated hashes
8. inspect the built preview on desktop and mobile widths
9. record the reason and evidence in the PR

The candidate must not be a mutable branch reference.

## Node and Ruby dependencies

```bash
npm ci
npm audit --audit-level=moderate
bundle check
bundle exec jekyll build --source docs --config docs/_config.yml --destination _site
```

- Commit lockfile changes with the manifest change that caused them.
- Separate content changes from dependency migrations when possible.
- Do not suppress an advisory without a documented reachability and risk analysis.
- Review generated transitive changes instead of accepting lockfile churn blindly.

## GitHub Actions

`python3 scripts/check_workflows.py` enforces full immutable action SHAs. When updating an action:

1. identify the release tag
2. resolve it to the exact commit SHA
3. inspect release notes and action metadata
4. update the SHA and version comment together
5. run the workflow on a PR
6. confirm no Node runtime or deprecation warning was introduced

## Release readiness

Before tagging a release:

```bash
npm ci
bundle install
BOOK_FORMATTER_DIR=../book-formatter npm test
BOOK_FORMATTER_DIR=../book-formatter npm run check:book-qa
npm audit --audit-level=moderate
```

Also confirm:

- all cited source mappings are complete
- no source review is overdue without an accepted exception
- all P0 and P1 review findings are closed
- all labs have stop, destroy, and cleanup evidence
- no real credential, personal data, or third-party target is present
- PDF and EPUB generation, when enabled, pass smoke tests
- Pages deployment and important public routes return successful responses
- release notes state known limitations and time-sensitive assumptions

## Incident recovery

If generated output, deployment, or automation is compromised:

1. stop deployment and revoke affected credentials
2. preserve workflow and artifact evidence
3. identify the last trusted source and formatter revisions
4. rebuild from a clean checkout
5. compare generated hashes and public output
6. publish a corrected release or advisory as appropriate
7. document root cause and add a regression gate

Never treat a clean rebuild as proof that no information was exposed; investigate access and audit records separately.
