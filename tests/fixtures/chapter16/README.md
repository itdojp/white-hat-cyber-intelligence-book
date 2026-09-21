# Chapter16 finite contract

Layer A owns only ART-24 questions, authored receipts, Consumer constraints,
parent non-inheritance, complete document selection and exact provenance.
Publication Projection 1.1.0 owns Markdown/Kramdown/HTML precedence; Content
Safety Policy 1.2.0 owns action and host grammar. No local syntax parser exists.

`publication-contract.json` is a reviewed editorial snapshot, not an observation
or a replacement for semantic tests. `scripts/chapter16_regressions.py` runs the
semantic kernel directly without schema or authored snapshot rejection first:
TCM-K tests stage receipts, separate targets/revisions/questions, clock, delay,
normalization, retention, original digest, fields and bounded absence. TCM-S
requires every field of every authored object. TCM-M rejects asserted promotions,
Safety/Handoff changes and missing Gap ownership. TCM-P covers all four documents,
preamble/body/tail, headings, every JSON leaf, order and exact provenance. TCM-J
and TCM-IO reject ambiguous JSON, unlisted paths, static symlinks, nonregular or
oversized inputs and unsupported descriptor platforms.

All ten scenarios are independent authored contrasts, not a live pipeline.
Twenty-four receipts are supplied assertions, not measured collection evidence.
Validated means a bounded input comparison; it never validates Chapter17's whole
detection, parent retention, permission, real Handoff or legal admissibility.
Original fixture digests compare the sorted-key, compact, UTF-8 JSON representation
(`ensure_ascii=False`, `allow_nan=False`), not source-file whitespace or authenticity.

Run `python3 scripts/check_chapter16_contract.py` with Linux/WSL2 Python3.12 and
repository-pinned renderer dependencies already installed. Repeat with
PYTHONHASHSEED 0, 1, 7 and 42. The command does not fetch dependencies or connect to
products. `--no-regressions` is the mandatory publication preflight; it still
checks all canonical documents, schema, semantics, parents, Source and routes.
Unknown fields/surfaces are fail closed until reviewed; arbitrary telemetry,
product parsers, collection engines and filesystem race confinement are non-goals.
