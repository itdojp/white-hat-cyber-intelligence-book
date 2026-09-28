# Chapter27 finite AI boundary contract

Owner: Issue49 / ART-31. Layer A `1.0.0`; Policy `1.2.0`; Publication Projection `1.1.0`.

`python3 scripts/check_chapter27_contract.py` validates the four complete published documents, their projected order/locations and exact source-provenance exceptions, all 958 authored JSON leaves, closed distribution schema, parent/pin hashes, routes, Source mappings, indices and preflight entrypoints. The Case tables contain all supplied leaves, including deliberately empty lists. Host exceptions are 25 individually reviewed reference/version fields; they do not exempt action scanning or additional occurrences. There is no chapter-specific Markdown parser.

`comparison-corpus.json` contains 61 named, bounded contrasts. Component state and request disposition are compared directly without the literal inventory: observation/validation binding and timestamps; six-state precedence; instruction origin; source/memory Case, Audience, version, quarantine and expiry; approval owner, request, action, target and window; tool capability; stop priority and a fixed step budget. These are authored-record comparisons, not a general prompt classifier or a runtime authorization service. A passing comparison never invokes a model or tool.

Other regressions cover required/closed shape, schema constants and array bounds independently of the record snapshot, duplicate/non-finite JSON, each literal/visible field selection, semantic binding with the authored snapshot refreshed, document preamble/tail/heading drift, and a small shared-owner reachability set. Generic syntax coverage remains in the shared Publication Projection corpus. Schema shape and fixed safety constraints do not replace cross-record semantic checks.

The frozen record is intentionally not a freely editable AI configuration. Corrections require review of the relevant literal/semantic expectation; do not regenerate all snapshots merely to accept a failure. `Allowed-in-model` means only that the synthetic fixed-response request meets the documented comparison conditions. All requests remain `executed=false`, the model descriptor remains Unknown, the parent RoE remains Draft / Do not proceed, and real deployment, cryptographic verification, runtime stop success and AISVS conformance are not claimed.

Repeat with `PYTHONHASHSEED=0`, `1`, `7`, `42`. The checker must produce the same ordered output. IO probes, actual `sync:docs` negative checks, pinned renderer/build parity and desktop/mobile publication checks are release evidence, not an unbounded fuzzing grammar.
