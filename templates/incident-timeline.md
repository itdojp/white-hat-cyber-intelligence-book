# Incident Timeline

`ART-07`は原記録、正規化した時刻幅、判断時点、RelationとGapを結ぶ。記入だけで実収集・真正性・権限・原因成立を認定しない。[第20章](../manuscript/20-dfir-timeline-causality.md)と[全欄の合成記入例](../cases/ch20-dfir-timeline-causality-example.md)を参照する。既存の見出しと公開URLは保持する。

## 基本識別情報と境界

- Timeline ID / version:
- Incident ID: 対応上の参照。実Incidentか完全合成かを明示する。
- Time standard: 原Timezone、UTCへの変換、Clock条件と有効Window。
- Scope status: 対象、版、Window、既知・除外・Unknownを別記する。
- Evidence cut-off: 利用可能時点による採否の締切。
- Analysis time / owner:
- Evidence Question IDs / Claim IDs:
- Source / Actor / Session / Asset registry:
- 親Case、方法参照、未配達Handoff、継承しないEvidenceと権限:

## Provenance and time basis

| Field | 記入内容 |
|---|---|
| Original record | Evidence ID、Source ID、Source内Event ID、元payloadの保持 |
| Integrity | 原本・作業Copyの区別、比較表現、Hashの意味と限界 |
| Handling | 供給主体、Custodian、保持参照、取扱い、変換履歴 |
| Event time | 原表現とTimezone。未知を推測で補わない |
| Clock | 基準、offsetの符号、総不確かさ、条件と有効期間、根拠の利用可能時点 |
| Receipt times | Collection、Ingest、Availableを分離 |
| Transform | Timezone変換、offset補正、不確かさ区間。原記録を上書きしない |
| Duplicates | 同一Source・Event・内容のReceiptを残す。衝突は停止 |

## Timeline entries

Normalized timeは一点とは限らず、区間とClock参照を記入する。表示順を発生順や因果順と同一視しない。

| Normalized time | Original time | Source | Identity / asset | Event | Evidence ID | Interpretation | Confidence |
|---|---|---|---|---|---|---|---|
| UTC区間 / Clock ID | 元Timezone付き表現 | Source / Event ID | Actor / Session / Asset | 供給された事実 | 原Record / 再送Receipt | Claim、支持・反証・未確定 | 不確かさと根拠不足 |

## Confirmed facts

- 当該対象・版・Cutoffで実際に供給されたRecordとEvidence ID:
- 未到着・採用不可のRecordとその理由:
- 同じ出来事の再送、別Sourceの記録、内容衝突の区別:

## Analytic judgments

- Before / After / Concurrent / Possibly related / Contradictedのどれか、左右のEventと根拠:
- 時刻幅の接触・重なり、同時性の独立根拠、誤った順序主張の反証:
- 相関に用いたActor / Session / Assetと、一致しても証明しないこと:
- 代替順序・説明、確信度、その制限と反証条件:

## Gaps and collection actions

- Gap ID、欠けるField / Window / Source、判断への影響:
- 追加Evidence Question、Owner、期限、再評価条件:
- 計画と実収集の区別、必要な承認と停止条件:
- 教材では実収集0。欠けたRecordを創作しない。

## Root cause and contributing factors

- [ART-26](root-cause-analysis.md)のRCA ID:
- Trigger、根底の条件の仮説、機構Evidence、代替説明:
- 分析を難しくするCollector遅延と、事案自体の因果的寄与の区別:
- 供給事実の範囲、Unknown scope、原因未確定の理由:

## Containment, eradication, recovery

- 第19章の対応判断への参照。Timelineだけで状態を更新しない。
- 実施案、実施記録、効果確認、復旧検証、残余リスクを区別する。
- Control ID、検証Question、担当、期限、再評価ID:
- Handoff先、受領状態、Receipt ID、実行権限:

## Review and cleanup

原時刻と原記録、Cutoff、変換履歴、後着Evidence、未確定の判断を保持してレビューする。解答Copyの取扱いと保持期限を記す。教材の記入・検査は実原本や実ログの変更、外部への追加操作を許可しない。
