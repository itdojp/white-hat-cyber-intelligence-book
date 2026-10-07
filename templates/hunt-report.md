# Hunt Plan and Findings

`ART-06`はHypothesisからEvidence、許容結論、再評価へ接続する記録である。[第18章](../manuscript/18-threat-hunting.md)と[完全合成Case](../cases/ch18-hunt-plan-example.md)を参照する。既存の五見出しは保持し、Scopeと根拠を具体化する。空欄を都合のよい推測で埋めない。

- Hunt ID / Record revision / Case ID / relation:
- Threat ID / Detection ID / Telemetry Map ID:
- Decision question / 判断期限 / Intelligence or incident trigger:
- Hunt Hypothesis / Expected behavior / 反証条件:
- Subject / Revision / Population / Exclusions:
- Scope / Time window / Timezone / 判断時点:
- Baseline / 承認Snapshot / 想定する代替説明:
- Authority / Data ownership / Purpose / Safety / Stop / Cleanup:

本書の演習では完全合成の供給入力だけを読む。実Log、実User、実IP、PII、実Tokenは使わず、外部Targetや実SIEMへ接続しない。親CaseのIDは許可や証拠を付け替えない。Scope、取扱根拠、入力の出所が不明なら止める。

## Available and missing telemetry

- Stream / 必要Field / Consumer / Purpose:
- 対象版 / Population / Window / Producer / Collection / Retention / Queryability:
- Event time / Ingest time / Clock uncertainty / Identity namespace / Normalizer版:
- Coverage根拠 / Gap ID / Gap reason / 許されない結論:
- Input fixture ID / Supply Evidence ID / 入力Digest / 比較方法 / 取得と変換の制限:
- Data classification / Privacy / Owner / 期限:

供給合成Receiptは教育用仮定であり、実Collectorの受領証拠ではない。Hashは固定表現の一致に限定し、真正性、完全性、取扱権限を保証しない。実Coverageへ転用する場合の確認を本章の演習で代行しない。

## Queries and pivots

| Step | Query / method | Reason | Result | Next pivot |
|---|---|---|---|---|
| 記入欄 | Query ID・入力版・有限条件 | 仮説のどの部分を調べるか | 期待Evidenceと実際の比較結果 | Pivot ID・Trigger・同一Scopeか |

- Query ID / Input ID / Query contract version / Expected result:
- Pivot ID / Trigger / Next question / Time bound / Identity join:
- IOC-onlyかBehavior比較か / 未検証の問い:
- Impact / Stop / 未知の入力に対する拒否条件 / Cleanup:

結果を見てScopeを無制限に広げない。型・ID・版・未知Keyの入力エラーを、正規のStopped判断と混同しない。

## Findings

- Finding ID / Evidence ID / Query ID / 確認事実:
- Result: Supported / Weakened / Negative finding / Inconclusive / Stopped
- Positive findings / 支持する観測 / 反証条件:
- Negative findings / Scope・Population・Time・Query・Coverageに限った未観測:
- Observability limitations / Gap / 不足する証拠:

0件だけでNegative Findingへ昇格しない。必要条件が不足すればInconclusive、停止条件が成立すればStoppedと記す。Supportedは悪意・帰属・侵害の確定ではない。

## Judgments

- Assessment / 許容結論 / 言えないこと:
- Confidence / 根拠 / 合成記録内に限定する範囲:
- Alternative explanations / 支持と反証のEvidence:
- 確認事実 / 分析判断 / 仮定 / 未知:
- Gap ID / Next action / Owner / Due date / Reassessment ID:

「侵害なし」と一般化しない。低い確信度や未解決Gapを隠さず、同じ入力でも問いやCoverageが変われば判断を見直す。

## Follow-up

- Detection backlog / ID / 関連Detection / 受入条件:
- Collection backlog / ID / 不足Field・期間・品質 / 再確認条件:
- Incident escalation / ID / 評価依頼の条件 / 宣言権限を持つ担当:
- Handoff ID / Source Finding ID / Source Evidence ID / Purpose / Owner / Due date:
- Delivery status / Receipt ID / executionAuthorized:
- Re-run condition / Reassessment ID / Input・Query・Scope・Coverage変更時の扱い:

演習のHandoffはplanned-not-delivered、Receipt IDはnull、executionAuthorizedはfalseである。作成済みRecordを実通知や受領済みへ読み替えない。第17章のDetection改修、第19章のIR判断、第22章の改善に接続するのは限定した記録であり、実行指示ではない。
