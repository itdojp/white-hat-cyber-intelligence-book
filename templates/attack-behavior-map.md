# ATT&CK Behavior Map

## 目的

`ART-15`はThreat Hypothesisを条件付きのBehaviorへ変換し、Object、版、Data、Evidence、Gap、Decisionへ接続する。Templateを埋めただけでは、侵害、検知有効性、Control effectiveness、主体の存在を証明しない。

## 使用条件

読解課題は完全合成Dataだけで行う。実Target、実Log、実Credentialを使用しない。外部通信、Token取得、設定変更、侵害再現は行わない。Authority / Scopeが不明な場合は停止する。

空欄を推測で埋めない。情報が足りなければUnknownとし、Gap、Owner、再評価条件を記録する。実務への転用時は、組織のAuthorizationと公開範囲を別に審査する。

## Document Control

| Field | Value |
|---|---|
| Artifact ID | ART-15 |
| Map ID | BMAP-YYYY-NNN |
| Parent Case ID / Relation | Case IDとrefines / supersedes / independentを記録 |
| Parent Threat Model / Decision Requirement | 親の命題と判断期限を変更せず参照 |
| Authorization Record / Scope | 許可されたDataとMethodの範囲 |
| Owner / Reviewer / Review date | 担当する役割と再評価期限 |
| Catalog / Object / fixture version | 三つの版を区別して記録 |
| Source / hash / checkedAt | 原典、固定commit、取得確認日、hash |
| Non-goals | 主体帰属、実行許可、完全Coverageの証明ではない |

## 行動とMapping

一行は一つの観測可能な命題とする。複数Hypothesisを同じ意味としてjoinしない。

| Field | 記入内容 |
|---|---|
| rowId / threatId | 行と親命題を一意に指定 |
| assetIds / boundaryIds / flowIds | 前提、対象、観測点へ追跡 |
| catalogVersion | Enterprise / Mobile / ICSとcatalog版を明示 |
| techniqueId / tacticId / subtechniqueId | 有効なObject、Type、name、Object version、modified、permalinkを別途確認 |
| mappingBasis | Hypothesized / Source-reported / Observed / Reproduced |
| preconditions | 確認済みと未確認の成立条件 |
| observableBehavior | 誰の、何に対する、どの変化を読むか。操作手順にしない |
| analyticIds / dataComponentIds | 原典の関係と、自組織の採否・理由 |
| alternativeMapping | 正常な代替説明、別候補、保留理由 |
| limitation | この行から主張できないこと |

Object名の一致だけで決めない。採用しないSub-techniqueは「なし」とし、架空のIDを作らない。無効・旧版のObjectはMigration記録なしに新規利用しない。

## Dataと既存Control

| Field | 記入内容 |
|---|---|
| telemetryId | Event class、Field、取得点、時刻、期間、欠落、Owner |
| availability | Available / Partial / Not collected / Synthetic only |
| detectionId | 本書側のRule識別子と版。MITREのDET番号と区別 |
| Existing prevention / detection / response | Control ID、assurance state、根拠、未検証条件 |
| gapId / Owner / Review date | 情報不足を誰がいつ再評価するか |
| Evidence ID | 命題、取得条件、参照先、時刻、完全性、限界 |

Telemetryの不在は侵害不存在ではない。Historical Evidenceからcurrent stateを補完しない。Data Componentと製品Fieldの対応は、対象環境で確認する。

## StatusとEvidence threshold

| Status | 必須条件 |
|---|---|
| Proposed | 行動候補と調査理由 |
| Mapped | Object、版、前提、Mapping basis、代替説明 |
| Observed | 同じ行のObservable behaviorに対応するEvidence IDと観測範囲 |
| Validated | 同じ行のTest ID、条件・版、Expected / Actual、Result、EvidenceがそろいPass |
| Not applicable | 情報不足ではない適用対象外の理由 |
| Unknown | 不足情報、Gap、Owner、再評価条件 |

Test ResultはPass / Fail / Inconclusive / Not collectedから選ぶ。Pass以外や未収集ではValidatedへ進めない。合成Dataを用いたTestのPassを実製品や別のControlへ拡張しない。

## Validation Record

| Field | 記入内容 |
|---|---|
| Test ID / rowId | Testと検証対象命題を結合 |
| Scope / Preconditions | 許可、入力、環境、対象外 |
| Rule version / fixture version | 再現対象の版 |
| Expected / Actual | 正常系、異常候補、情報不足の各結果 |
| Result / Evidence ID | Resultと結果を示す参照先 |
| Reviewer / Limitations | 判定責任と適用できない範囲 |

本章の空Templateは実行指示ではない。実環境のRule testやData取得には別の承認が必要である。

## DecisionとReassessment

| Field | 記入内容 |
|---|---|
| decisionContribution | 支持できる結論、留保する結論 |
| Coverage denominator | 対象、期間、版、除外理由、Unknown数 |
| Handoff ID / consumer | 次章と受け取る成果物 |
| Acceptance / Reject | 必須入力と差戻し条件 |
| reassessmentTrigger | Source、Field、Scope、承認、版、期限の変更 |
| Migration record | 旧新Object、差分、影響行、採否、Owner |

Mapping数を安全性や帰属確信度へ変換しない。親CaseのControl / Gapを変更する場合は、その親のEvidence thresholdを別途満たす。

## ReviewとCleanup

- 技術: Object / Type / version / relationの整合
- 分析: Mapping basis、Evidence、代替説明、許容結論
- 安全: Authority / Scope / Stopが維持されること
- 引渡し: Owner、期限、Data不足、再評価条件
- Cleanup: 自分の作業コピーだけを整理し、正本と親Evidenceを保持

OWNはBehavior Map、BRIDGEはThreat Model / Detection Validation、DELEGATEは製品実装である。[第5章](../manuscript/05-attack-behavior.md)と[合成記入例](../cases/ch05-attack-behavior-example.md)を参照する。
