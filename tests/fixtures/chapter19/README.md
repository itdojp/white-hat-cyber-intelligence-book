# Chapter 19 / ART-25 Layer A

- `decision-corpus.json`: 60 independently authored literal status/gap/error expectations. References reuse the supplied input of a canonical contrast, but expected values are not copied from the canonical `expected` field or calculated by the evaluator. Mutations are a finite list, not a fuzzing grammar.
- `publication-contract.json`: reviewed whole-document projected fields, schema/corpus hashes, supplied-input representation hashes, parent hashes, exact routes, Source identities and indices. These are editorial drift checkpoints, not cryptographic authenticity or proof of a correct interpretation.
- `cases/fixtures/ch19-incident-response.json`: 12 independent synthetic subject/revision snapshots. A previous decision, evidence, declaration criterion, approval, preservation and validation are supplied educational assumptions. Neither parent evidence nor a real incident receipt is imported.
- `scripts/chapter19_decisions.py`: pure finite decision guards, version 1.0.0. Schema validation is mandatory at the public checker/corpus boundary. It does not implement complete IR, real authorization, event ingestion, product commands, legal notification, evidence authenticity or arbitrary natural-language reasoning.
- `scripts/chapter19_judgments.py`: finite reviewed Japanese claims authored alongside the 12 contrasts, not an independently derived oracle. Refreshing drift hashes does not remove this separate semantic claim check. Published decision reasons also bind to the reviewed conclusion, and containment impact/rollback bind to the selected option profile. A prose change needs review, including an innocuous paraphrase.
- Schema uses the repository's supported finite JSON Schema 2020-12 keywords. Unknown properties, duplicate JSON keys, nonfinite numbers and bool-as-zero substitutions fail closed. Inputs are fixed regular files, bounded to 1 MiB, on Linux/WSL2; descriptor checks are not a sandbox against concurrent hostile writers.

The seven states are educational bookkeeping, not NIST's universal state machine. Valid incomplete records return deferred with unchanged previous status; malformed scope, references or time fail input validation. Approved options are not actual action. Monitoring is not containment. Validation must concern the declared scope and be available at the relevant decision time. Closure retains residual-risk responsibility; reopening keeps the supplied prior closure and requires later-available new evidence. All real operation/collection/notification counts are zero; all 36 handoffs remain planned-not-delivered with null receipt and no execution authority.

Four whole Markdown surfaces use the unchanged Publication Projection 1.1.0 and Content Safety Policy 1.2.0. Eleven individually reviewed exact typed/located fields exempt only false-positive host scanning (verified Source URLs, versions, registered delegation and the fixed local command). Action scanning is never exempt. Moved, duplicated, altered or synthetic JSON values are not covered. No chapter-specific syntax parser/regex was introduced. Generic Markdown/Kramdown/HTML/URL parity stays in the shared corpus.

Run `python3 scripts/check_chapter19_contract.py`; `--no-regressions` is the publication preflight, not an alternative to the full test suite. Use PYTHONHASHSEED 0/1/7/42 to compare deterministic results. Canonical prose, schema, input and snapshots must be reviewed together; there is no production auto-accept/update command.

## PR153独立Draftレビューの有限回帰

- `review-role-*`: 指摘4080321185。表示済み役割台帳と91 operational owner参照の整合。台帳だけ/参照だけの変更はhash再固定後も拒否し、双方の一貫した再割当は受理。record固有のresidual-risk ownerは六つの共通調整役割とは別の明示的割当である。
- `review-closure-*`: 指摘4080321202。現在のclosure欄はrequested Closedだけが所有する。非Closed十対比への混入を拒否し、Closed要求がdeferredになる教材例とReopenedのprevious.closureは保持する。
- `review-handoff-due-*`: 指摘4080321208。36 HandoffのdueAtが直接参照するdecision時刻より前なら拒否、同時刻は許可。asOf現在で期限超過かどうかとは別の条件である。
- この三群はmodel-levelでauthoredInputs全hashを更新した直接probe。日本語の再生成を行ったCLI全経路のbefore再現とは主張しない。既存60独立guard期待値、正本Data/Schema/表示snapshot/親章は不変。
