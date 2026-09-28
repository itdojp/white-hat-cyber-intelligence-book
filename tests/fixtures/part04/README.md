# Part IV finite boundary corpus

Owner: Issue #22 / `scripts/check_part04_contract.py` 1.0.0.

The four supplied chapter records and two independent exchange files are fixed inputs. The contract declares boundary literals and producer/consumer links independently of the input JSON. It does not recompute chapter judgments, Source quality, collection status, or general STIX/TAXII validity. Same ID is not delivery, permission, or evidence adoption.

`counterexamples.json` owns 30 explicit semantic mutations (including coordinated renaming and boolean/integer separation). Twelve frozen shared-Projection examples prove that this consumer scans visible text, titles and absolute destinations over the whole document and respects shared fail-closed diagnostics. They add no syntax grammar. Every declared boundary also has a deletion and wrong-value regression, and every reader field has a deletion probe. Strict bounded UTF-8/JSON and missing/symlink/FIFO/unowned input probes run locally under `.tmp/`.

`publication-contract.json` records all typed fields, not selected matching sentences. A deliberate reader revision requires review of this snapshot together with the source; it is not an automatic approval of meaning. Policy scanning is tested independently from snapshot mismatch. Parent canonical records, Source dates/versions and Editorial Intake are unchanged.

Run `npm run check:part04`; `--no-regressions` still enforces the canonical boundary, whole-reader safety/inventory and publication wiring before `sync:docs` can delete generated output. Full root QA remains responsible for every chapter's internal contract.
