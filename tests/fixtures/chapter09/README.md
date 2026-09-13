# Chapter 9 finite ART-02 contract

## Ownership and limits

- Layer A: `chapter09_semantics.py` owns the closed teaching-plan structure, direct parent IDs, finite scope/operation/data/stop/budget/time/approval conditions, and Case rows. `check_chapter09_contract.py` selects all four canonical documents and binds typed fields to their chapter heading/label owners. `chapter09_regressions.py` owns the finite counterexamples.
- Layer B remains `publication_projection.py` 1.1.0 and the exact pinned renderer. No new chapter-specific Markdown/HTML/Kramdown/URL parser or syntax grammar.
- Layer C remains Content Safety Policy 1.2.0. The JSON string scan and projected fields use the shared action/host scanners. This is not a general PII recognizer or a proof of real authorization, signature authenticity, communication, isolation or destruction.
- The complete canonical record is Draft / Do not proceed, as of 2026-09-13T09:00:00Z. The parent expires on 2026-08-19T09:00:00Z. CI must not renew the parent, backdate the canonical record, or promote parent Evidence/Coverage/Gap.
- A manufactured positive model at 2026-08-06 tests declared conditions inside the retained historical authorization period and original test window. It is not a claim that an actual approval occurred then. `executionAuthorized=false` in both positive and canonical cases. No runtime or authorization service is implemented.
- The input reader accepts only the fixed two data/schema inputs, four selected documents and listed provenance parents. It rejects static symlinks, special/oversized files and unsupported primitives, under Linux/WSL2. This is a stable authoring-worktree guard, not a sandbox against hostile concurrent filesystem replacement.

## Corpus and commands

```bash
python3 scripts/check_chapter09_contract.py
python3 scripts/check_chapter09_contract.py --no-regressions
PYTHONHASHSEED=0 python3 scripts/check_chapter09_contract.py
PYTHONHASHSEED=1 python3 scripts/check_chapter09_contract.py
PYTHONHASHSEED=7 python3 scripts/check_chapter09_contract.py
PYTHONHASHSEED=42 python3 scripts/check_chapter09_contract.py
```

Install the repository's locked Ruby/Bundler renderer dependencies before these commands. No live target, credential, container or mutable dependency is required for the checks themselves. Scratch test files are created only under the ignored repository `.work/` directory and removed by the fixture runner.

| ID family | Invariant / positive control |
|---|---|
| CH09-POS | Canonical complete-but-blocked plan; manufactured condition-positive declaration cannot replace canonical |
| CH09-STATE | Eight exact record states, only Approved/Active may meet declared operation conditions; still no real permission |
| CH09-AUTH | Direct Authority ID, retained period, current status, written proof, same version, all roles, bounded Window |
| CH09-REAUTH | Restart requires cause-clearance plus same-version proof; Retest requires new same-version proof |
| CH09-SCHEMA | Every object key is required and every object shape closed; JSON schema supports only the existing finite evaluator |
| CH09-SEM | Parent non-promotion, exact object/scope/owner inventory, overlap/default deny, Method, Data, budgets, Stop, Recovery, completion and Handoff |
| CH09-POLICY | Unsafe direct JSON text rejected; supplied-synthetic-only near miss accepted by shared Policy |
| CH09-JSON / TIME | Duplicate keys, nonfinite numbers, malformed UTF-8/JSON and noncanonical UTC timestamps rejected |
| CH09-DOC | Every required semantic field belongs to its reviewed chapter section and occurs once |
| CH09-EX | Changing or duplicating each provenance exemption loses it; ordinary unsafe text is scanned |
| CH09-SURFACE | Actual preamble/body/tail mutations in all four documents reach shared projection/scanning; unexpected sections fail |
| CH09-PARITY | Every Case table row corresponds to a JSON leaf, including null and empty arrays |
| CH09-IO | Finite path inventory, bounded regular files, no-follow/nonblocking prerequisites |
| CH09-SOURCE-DATE | Retained audit baseline accepts scoped newer canonical dates, rejects stale/noncanonical/type-confused dates |

Generic renderer precedence and syntax families remain tested by the shared Publication Projection corpus, not copied into Chapter 9. No unbounded fuzz grammar is introduced.

## Reviewed narrow provenance

`publication-contract.json` freezes each full typed field, heading path, destination's visible owner and cardinality. Exemptions are not host-wide, document-wide, or permission waivers. They exist only for the following demonstrably nonoperative reader fields:

1. Nine analytic/prohibition fields: the manuscript's non-execution introduction, table column explicitly stating what authorization evidence does not prove, explicit prohibited operations, Credential-reference/minimization explanation, unexpected-Data stopping paragraph; the Template's prohibition paragraph and Data classification/prohibition fields; the Case's explicitly unmeasured real-environment confidence limitation.
2. Eleven primary/delegation/build-document destinations: specialist book (manuscript and Case), canonical build guide, NIST landing/PDF, WSTG project/versioned Introduction, e-Gov landing/official law-data API, IPA landing/PDF. These are citation/navigation destinations, not test targets.
3. One local read-only checker command, whose `.py` path the host scanner conservatively flags.
4. Four bounded version/section-number fields in the manuscript/Source Note, which the shared host scanner conservatively flags as address-like text.

The exact fields must occur once at the reviewed section and label. Changed unsafe text, changed URL, moved ownership or duplication must not inherit an exemption. Human-independent review is still required to confirm the meaning and source scope.

## Bounded compatibility changes

- Chapter 2's Source date comparison reuses `source_audit.meets_audit_baseline`. Source version and historical note markers are unchanged; only the actually used Source audit dates advance.
- Existing Manifest negative fixtures depended on live Chapter 9 still being in comparison. Test-only `prepare_comparison_regression` restores a valid comparison fixture and matching checkpoint before injecting the original negative. Production validation is unchanged. The Chapter 8 whole-file provenance hash advances only after an AST comparison proves every non-test node unchanged.
- Chapter 7/8 publication command inventories add the Chapter 9 preflight. Chapter 6's own prefix check already accepts the extension and is unchanged.
- Navigation puts Chapter 9 between Chapters 8 and 11; Chapter 11's exact order constant moves from 52 to 54, leaving 53 for the later Chapter 10. No Chapter 11 prose, semantic contract, fixture or authority changes.
- Shared Policy/Projection, formatter pin, dependency locks, parent canonical content and CROSS_BOOK_MAP are unchanged. Broad law/ethics/RoE remains BRIDGE; Chapter 9 owns only the book-specific artifact/decision/handoff layer under the existing §4/5/7 boundary. The theme-granularity follow-up remains Issue #55.
