# Telemetry Coverage Map

## このTemplateの目的と安全境界

`ART-24`は問いから必要Telemetry、品質、Consumer、Gap、再評価までを結ぶ。製品設定、実Logの収集、実施許可書ではない。完全合成の読み取り専用教材で記入し、実Target・実User・実Token・PIIは使用しない。

[第16章](../manuscript/16-telemetry-evidence-readiness.md)の説明を読み、[完全合成記入例](../cases/ch16-telemetry-coverage-example.md)と比較する。親Caseをrefinesする場合も対象・版・ScopeとEvidenceの用途を明記する。親の状態・権限・未配達記録は変更しない。

## 1. Document Controlと親参照

| Field | 記入内容 |
|---|---|
| Map ID / Artifact ID | 一意なRecordとART-24 |
| Case / Relation | 親Caseとrefines、別判断対象は区別 |
| Subject / Revision / Scope | 判断対象・教材版・利用範囲 |
| Threat / Observation / Signal Flow | 入力の直接参照と利用できない結論 |
| Finding / Handoff | 親のGap、未配達と受領記録の区別 |
| Owner / As of / Source IDs | 担当、判断時点、実際に使う出典 |

## 2. Evidence QuestionとRequired Field

| Field | 記入内容 |
|---|---|
| Question ID / Question | 何を確認したいか |
| Consumer / Decision deadline | 利用目的と期限 |
| Event / Field / Purpose | 必要な記録と欄ごとの理由 |
| Subject / Revision / Window | 対象・版・期間を限定 |
| Permitted conclusion | 未観測・不明を含む結論の上限 |

## 3. Collectionと品質

| Field | 記入内容 |
|---|---|
| Producer / Collector / Transport | 生成、受取、経路を別々に示す |
| Normalizer / Schema version | 正規化と形式の版 |
| Event / Observed / Ingest time | 発生、観測、到着を分離 |
| Clock / Timezone / Maximum uncertainty | 相関条件に対する誤差 |
| Identity namespace / Normalization | 表示名だけに依存しない同一性 |
| Retention / Integrity / Original reference | 必要期間、比較方法、元記録の用途 |
| Classification / Basis / Access role | 必要性と取扱条件。不明なら計画を止める |

## 4. CoverageとValidation

`T-16-05`は状態を記す際の最小欄である。Required / Produced / Collected / Retained / Queryable / Validated / Unknownだけを用いる。Correlatableを追加状態にしない。

| Field | 記入内容 |
|---|---|
| Coverage | 当該問いへ示せる状態。自動昇格しない |
| Stage receipt / Evidence ID | それぞれの段階の対象・版・問いを照合 |
| Test / Validation / Evidence ID | 限定した比較と根拠を直接接続 |
| Expected / Observed / Limitation | 期待を観測値に合わせて書き換えない |
| Gap / Owner / Due / Reassessment | 不足、担当、期限、判断を変える条件 |

Validatedは限定した合成入力検査であり、実際の収集・検知・調査・法的適格性を認定しない。HashやIDの存在だけで完全性・真正性・受領を主張しない。

## 5. ConsumerへのHandoff

| Field | 記入内容 |
|---|---|
| Consumer / Record / Row IDs | 渡す目的と対象行 |
| Acceptance / Limitation | 必須入力、残るGap、結論の上限 |
| Status / Receipt ID | 受領根拠がなければplanned-not-delivered |
| Owner / Due / Reassessment | 受け手の確認と再評価条件 |

## 6. 読解の完了・停止・Cleanup

問いから必要Field、段階の根拠、品質、Consumer、Gap、Owner、再評価まで説明できれば読解を完了とする。全行Validatedにすることは合格条件ではない。

未知の入力、実データらしい内容、外部接続要求、Scope不明を見つけたら停止し、追加取得せず不足を記録する。整理するのは自分のメモだけであり、供給Evidenceや正本は削除・改変しない。環境を起動しないためRuntimeの破棄は発生しない。
