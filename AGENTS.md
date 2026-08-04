# AGENTS.md

## Repository purpose

This repository develops the Japanese book **ホワイトハッカーとサイバーインテリジェンス実践体系**.

The book connects authorized security assessment, telemetry, detection engineering, threat hunting, incident response, DFIR, OSINT, cyber threat intelligence, and technical or executive decision-making. It is not a collection of offensive tool recipes.

## Authoritative files

Read these before changing content or automation:

1. the owning GitHub Issue and its acceptance criteria
2. `BOOK_PROPOSAL.md`
3. `book-config.json`
4. `CANONICAL_SOURCE.md`
5. `WRITING_GUIDE.md`
6. `SOURCE_POLICY.md`
7. `SAFETY_SCOPE.md`
8. `CROSS_BOOK_MAP.md`
9. `.book-formatter/revision.json`

When they conflict, stop and report the conflict instead of silently choosing one.

## Canonical source

- Human-authored chapter source: `manuscript/`
- Human-authored appendices: `appendices/`
- Reader modules: selected root Markdown files
- Source registry: `references/sources.json`
- Artifact templates: `templates/`
- Book structure: `book-config.json`
- Generated site source: `docs/`
- Built site: `_site/`

Do not edit or commit `docs/` or `_site/`. Regenerate them with the documented commands.

## Required workflow

```text
Issue → branch → Draft PR → automated checks → independent review → merge
```

- Do not push directly to `main`.
- Keep one primary objective per PR.
- Do not mix changes to other book repositories or the portfolio catalog into a manuscript PR.
- Do not merge, enable auto-merge, bypass protection, or change repository settings unless the operator explicitly requests it.

## Safety boundary

All executable examples and labs must use one of the following:

- an isolated environment owned by the learner
- an environment covered by explicit written authorization
- synthetic data and simulated events supplied by this project
- a third-party training environment strictly within its published rules

Standard public content must not provide or require:

- scanning, authentication attempts, or access against real third-party systems
- credential, token, cookie, or session theft or reuse
- lateral movement, persistence, defense evasion, log deletion, or destructive actions
- denial of service, encryption, or unauthorized data modification
- deployable malware, C2, phishing infrastructure, or stealth tooling
- doxxing, tracking of real people, or aggregation of sensitive personal data
- confident attribution of an individual, organization, or state from weak evidence

Stop when authorization, scope, data ownership, recovery, or legal status becomes unclear.

## Lab defaults

- rootless and non-privileged execution
- no host networking
- no `--privileged`
- capabilities dropped by default
- outbound network access denied by default
- `.test`, `.example`, and documentation address ranges only
- invalid synthetic credentials only
- explicit preflight, stop conditions, evidence export, destroy, and cleanup checks

## Source and analysis rules

- Prefer laws, standards, specifications, official guidance, original research, and official advisories.
- Record source version, status, checked date, next review date, review triggers, and affected chapters in `references/sources.json`.
- Add each cited `SRC-*` ID to the source registry chapter mapping.
- Regenerate `references/reference-baseline.md`; do not hand-edit it.
- Separate confirmed facts, analytic judgments, assumptions, forecasts, and recommendations.
- State confidence, alternatives, and information gaps when the conclusion is uncertain.
- Do not use an AI model output as a source.

## Cross-book boundary

Classify material as:

- `OWN`: this book carries the primary explanation
- `BRIDGE`: explain only what is required to connect disciplines
- `DELEGATE`: refer detailed implementation to an existing specialist book

Do not duplicate detailed pentest recipes, infrastructure hardening procedures, authentication implementation guides, general incident operations, or AI-agent governance already owned by the linked books unless the integration argument requires a short bridge.

## Chapter contract

Every manuscript chapter must include:

- `この章の位置付け`
- `学習目標`
- `前提知識`
- a safe exercise or analysis task when appropriate
- an explicit artifact
- `章のまとめ`
- `次に学ぶこと`
- `参考文献・Source Note ID`

Commands must follow purpose, prerequisites, expected evidence, impact, stop conditions, and cleanup. Do not place commands before the reader understands those conditions.

## Validation

With the pinned formatter checkout:

```bash
npm ci
npm ci --prefix ../book-formatter --ignore-scripts
bundle install
BOOK_FORMATTER_DIR=../book-formatter npm test
BOOK_FORMATTER_DIR=../book-formatter npm run check:book-qa
```

The following must remain true:

- `npm test` passes
- site-source generation is deterministic
- canonical source hashes do not change during generation
- GitHub Actions use immutable full SHAs
- Jekyll build and built-site smoke checks pass
- no unresolved P0 or P1 review comment remains

## Stop and handoff

Stop instead of improvising when:

- the requested work requires a real external target or credential
- the canonical-source or publishing contract is ambiguous
- the only path requires a direct `main` change or administrative bypass
- a source version cannot be verified
- publication could expose an uncoordinated vulnerability
- generated output would overwrite canonical source

A handoff must state:

- completed checks and fixed commit SHAs
- exact blocker or missing decision
- smallest required operator action
- exact branch, Issue, PR, and resume point
