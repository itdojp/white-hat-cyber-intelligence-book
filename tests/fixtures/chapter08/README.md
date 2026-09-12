# Chapter 8 Layer A contract

Owning Issue: #33. Model/schema version: 1.0.0. Shared Publication Projection:
1.1.0. Content Safety Policy: 1.2.0. No shared grammar is defined here.

`publication-contract.json` declares four complete canonical documents, finite
H1/H2 sections, required typed field/heading associations, exact provenance
false positives, Source identity, publication routes and retained parent hashes.
Case table parity is computed from all three canonical JSON documents, rather
than maintaining a second independent expected data copy. The JSON schemas are
closed and use the repository's existing finite schema evaluator, without
resolving external references.

The 72 control checks and 9 signal records are **authored synthetic assumptions**,
not runtime measurements. `generate_receipts()` regenerates this one finite
recipe; seed 208 labels the recipe and is not a user input. The evidence hash is
calculated from the actual UTF-8/LF bytes. Both byte equality to the recipe and
semantic ownership/derived state are required. A hash-only refresh cannot admit
a new scenario. Schema and model changes require a new review.

## Permanent bounded regression families

The runner is `scripts/chapter08_regressions.py`, invoked once by the Chapter 8
contract unless `--no-regressions` is selected for pre-publication validation.

- `CH08-SCHEMA`, `CH08-REQUIRED`, `CH08-CLOSED`, `CH08-STRICT`: required fields,
  unknown fields, exact types, strict JSON and unsupported schema keywords.
- `CH08-DATA`, `CH08-PARENT`, `CH08-TIME`: exact Authority/Scope/parent/Run IDs,
  no inherited-state promotion, ownership, producer and UTC time bounds.
- `CH08-STATE`, `CH08-PREFLIGHT`, `CH08-RUNTIME`, `CH08-STOP-ORDER`,
  `CH08-CLEANUP`: each control slot has Fail and Unknown counterexamples; no
  Running after failed preflight or failure, no implicit cleanup, failure is
  retained across cleanup, and unvisited stages are not observations.
- `CH08-BYTES`, `CH08-RECIPE`, `CH08-JSON`: actual hash and generator equality,
  every JSON key/value through Policy, exact filename-only host exception and
  no JSON action exception. Changed path/owner/value or nested/key spoof fails.
- `CH08-PATH`, `CH08-IO`, `CH08-REPLAY`: finite paths, leaf/ancestor/root symlinks,
  malformed/oversize/non-regular files, nonblocking FIFO rejection, explicit
  UTF-8 under ASCII locale, deterministic stdout, no canonical byte mutation.
- `CH08-SELECT`, `CH08-PUBLIC`, `CH08-EXEMPT`, `CH08-PARITY`, `CH08-SOURCE`:
  every typed field reaches shared Policy; preamble/tail/section drift fails;
  exact provenance text/heading/owner/cardinality cannot expand; every Case
  table row matches JSON. One unsupported-source integration test delegates the
  diagnostic to shared Projection. No chapter-specific syntax fixture grammar.
- `CH08-SRC-COMPAT`, `CH08-PREFLIGHT-COMPAT`, `CH08-NAV-COMPAT`: Chapter 25
  accepts a later scoped Berkeley audit without accepting old/malformed dates
  or guessing a publication day; all three publication safety gates precede
  generation; Chapter 7 precedes Chapter 8, which precedes Chapter 11.

Run with `PYTHONHASHSEED=0`, `1`, `7`, `42`. The full shared renderer parity corpus
runs separately through `npm test`. Real publication fail-closed tests use an
isolated clean worktree to prove generated output is unchanged on rejection.
No test starts a container, contacts an external exercise target, mounts a host
filesystem, obtains credentials, or deletes resources outside its ignored local
scratch directory. The IO guard assumes a stable authoring worktree; it is not
a sandbox against concurrent hostile filesystem replacement.

## Limits

The six analytic/prohibition and seventeen host/provenance exceptions record
exact complete fields, not new Policy grammar. The canonical values and their
reasons must be read during review; modifying the declaration does not replace
review. This is a finite educational contract, not a general lab configuration,
PII detector, full legal approval, runtime isolation audit or forensic custody
certification. Actual normal merge/main Pages verification remains an operator
merge followed by a separate publication gate.
