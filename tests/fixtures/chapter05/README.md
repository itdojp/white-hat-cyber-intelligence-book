# Chapter 5 Layer A contract fixtures

`publication-contract.json` fixes the four Chapter 5 publication surfaces, their
H1/H2 inventory, selected semantic fields, reviewed exceptions, parent bindings,
parent Control states and routes. It is not a Markdown syntax corpus or a generated
manuscript snapshot. Changes require editorial review alongside the owning text.

- `scripts/check_chapter05_contract.py` consumes Publication Projection **1.1.0**
  and Content Safety Policy **1.2.0**. It scans complete documents, not selected
  excerpts. Generic syntax/renderer parity stays in the shared projection corpus.
- `scripts/chapter05_semantics.py` checks the finite ART-15 teaching set, typed ID
  joins and same-row Evidence/Test thresholds. Its classifier has no I/O and is
  not a production detector or an implementation of MITRE DET0539.
- `scripts/chapter05_regressions.py` owns Chapter-specific mutations: unsafe
  preamble/body/tail and projected attribute/destination forwarding, section
  drift, exact exception ownership/cardinality, parent identity and status,
  normal/missing-data replay, malformed JSON values and Source audit dates.
- Each text exception has a reason and is bound to exact document, heading path,
  field type/element/attribute/text and cardinality one. Provenance destinations
  additionally bind the nearest preceding same-line reader-visible owner. Action
  and host exceptions are separate; no hostname-wide exemption is granted.
- The machine-readable Case is `cases/fixtures/ch05-attack-behavior.json`.
  Displayed Case table rows must match typed values after shared projection.
- Source metadata is `tests/fixtures/attack/ch05-v19.2.json`, a hash-fixed eight-
  object subset. The full bundle is deliberately not tracked or fetched in CI.
  See the Chapter 5 Source Review Note for extraction and MITRE attribution.

Run `python3 scripts/check_chapter05_contract.py` with the repository's locked
Ruby/Jekyll environment. Run with `PYTHONHASHSEED=0`, `1`, `7` and `42` for the same
ordered report. A missing renderer or unsupported interpreted source fails closed.
