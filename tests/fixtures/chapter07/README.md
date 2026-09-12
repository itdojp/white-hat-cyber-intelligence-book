# Chapter 7 contract corpus

Ownership: Layer A only. `publication_projection.py` 1.1.0 is the sole Layer B owner; Content Safety Policy 1.2.0 is Layer C. This corpus does not add a Markdown/HTML/URL parser, arbitrary CVSS calculator or risk/compliance engine.

## Inputs and invariants

- Four complete publication documents are selected by `check_chapter07_contract.py`: manuscript, ART-17 template, six-record case and dated Source Note. Preamble/body/tail all reach the shared projection and policy; H1/H2 drift fails closed.
- `publication-contract.json` fixes finite section/semantic relations, exact source/version/delegation/rubric provenance exceptions, source identities, parent document hashes and routes. Exceptions depend on exact field text/type, heading ancestry, destination owner and cardinality one. Changing, moving or duplicating one invalidates it. No automatic regeneration occurs in CI.
- `cases/fixtures/ch07-vulnerability-prioritization.json` is the closed teaching corpus. Its deployment/control/decision context and seven evidence receipts are synthetic assumptions, not real validation. Its EPSS/KEV values are public-source inputs, not synthetic observations.
- `cases/fixtures/ch07-source-snapshot.json` is the minimal audited source extraction, with immutable source bytes/commits and two author-synthetic CVSS-B pairs. It is not a live feed. CVE-linked synthetic ratings are explicitly not vendor/CVE published ratings.
- Six scenarios, all record fields, evidence claims, direct parent bindings, optional values, strict types (including booleans vs numbers), finite dates, unknown-confidence decisions, deadlines, control expiry, source pairings and JSON-to-reader table parity are checked. The checker deliberately does not infer business priority from a score.
- Detailed BOD 26-04 legal scope, exceptions, supersession and numeric deadlines were not verified. The official issuance bulletin does not substitute for directive text. Applicability remains Unverified for all six records regardless of CVE presence; no operational authorization or legal waiver is claimed.

Run the finite suite with `python3 scripts/check_chapter07_contract.py`. Run deterministic repetitions with `PYTHONHASHSEED=0`, `1`, `7`, `42`. Generic renderer syntax/parity remains in `npm run check:publication-projection`; this chapter tests selection and typed-field forwarding only.

## Optional offline source re-extraction

Purpose: an editor can independently recheck the exact published subset and author-vector scores. This is source verification, not scanning a target. It requires the repository Python environment and Node 20 or later, plus locally supplied copies of the following public-source files. The script performs no download, dependency installation, extraction onto disk, source modification or network operation. Keep inputs in ignored `.work/ch07-source-inputs/`, not `/tmp` or a tracked folder.

| Local file | Official source |
|---|---|
| `epss.csv.gz` | `https://epss.empiricalsecurity.com/epss_scores-2026-09-11.csv.gz` |
| `kev.json` | `https://raw.githubusercontent.com/cisagov/kev-data/acdcfd43102c098c377568b417a42c0e00cc63a5/known_exploited_vulnerabilities.json` |
| `cwe.zip` | `https://cwe.mitre.org/data/xml/cwec_v4.20.xml.zip` |
| `metrics.js`, `cvss_lookup.js`, `max_composed.js`, `max_severity.js`, `cvss_score.js` | Files from `https://github.com/FIRSTdotorg/cvss-v4-calculator/tree/c5b0d409ae9f57c44264c6ce5f27d89298e1d32a` |

Every input must match the SHA-256 recorded in the frozen snapshot before parsing or mathematical evaluation. FIRST's inspected code owns scoring; the wrapper only supplies the two fixed vectors. Node `vm` is not a security sandbox: safety depends on the mandatory exact-byte gate for these previously inspected mathematical sources. No arbitrary code or vectors are accepted by the CLI. The upstream code is not vendored or installed as a runtime dependency.

After the files are supplied, execute from the repository root:

```bash
python3 scripts/verify_chapter07_sources.py --directory .work/ch07-source-inputs
```

Expected evidence: EPSS two exact values, KEV two membership/metadata results against the complete 1709-entry catalog, CWE one taxonomy item and FIRST two exact CVSS scores. The script reads only its local inputs and reports one summary. Stop on any missing input, digest/version mismatch, timeout or failed comparison; do not relax the hash gate or silently substitute current source bytes. An upstream republication may make the historical bytes unavailable and requires an explicit new source audit, not a fixture refresh to make tests pass. Clean up only the editor-owned input copies after exporting the result. Root CI runs the frozen offline contract without fetching these upstream files; an external re-extraction run must be reported separately, not inferred from green CI.

## Bounded regressions and change review

`chapter07_regressions.py` records deterministic test labels on failure, including root/record/evidence required fields, malformed values, source drift, synthetic identity, parent/claim misbinding, deadline order, canonical positives, coherent explanation/deadline changes, direct unsafe JSON, source hash rejection, strict JSON and UTF-8, selection drift, exact provenance non-expansion and data/reader mismatch. Required semantic edits need human-readable source review and a corresponding explicit contract change; fixture auto-learning is prohibited.

Before Ready: review pedagogy/acceptance, primary-source meaning and versions, authority/legal boundary, data/parent semantics, architecture/ownership, security and host handling, regression/determinism, and publication/layout. A green contract is not independent review or a merge decision. Issue #32 remains open until the operator's normal merge and actual main/publication verification. Chapter 8 and unrelated maintenance are out of scope.

## PR #120 independent-review regressions

- `CH07-LEGAL-001/002` (discussion 3996091116): CVE absence only makes keyed EPSS/KEV lookups inapplicable. It never establishes that unverified legal requirements are inapplicable. All six records retain Unverified and the governance owner.
- `CH07-SNAPSHOT-001` through `014` (discussion 3996091119): source snapshot strings, including JSON member names, reach shared action and host policy independently of the snapshot digest. Only two exact source URL values and five exact pinned mathematical filename keys have provenance exceptions. They are tuple-path, Source ID, exact text, cardinality and (for filenames) commit/hash bound. There are no action exemptions. A new snapshot must pass both integrity and safety, not simply refresh its hash.
- The old head accepted an added unsafe snapshot string when its digest and case/document references were refreshed together. The corrected head rejects that same refresh. Positive source metadata and explicit prohibitions still pass. Duplicate/relocated provenance, slash-key path spoofing, changed Source ID/commit/hash, expanded URL and unapproved keys are permanent negatives.

Source-to-case associations read the actual snapshot Model/identifier/date/catalog metadata and snapshot ID. Refreshing those metadata alone cannot leave stale model/date labels in the case. This is a relational consistency check, not evidence that a new source version has been independently audited.
