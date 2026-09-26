# 合成Case索引

このディレクトリは、本書の章で使用する完全合成Caseの索引である。

- すべての組織、担当者、Domain、ログ、判断は架空である。
- 実在Targetの調査や実在主体の帰属には使用しない。
- 機械可読fixtureは[fixtures catalog](./fixtures/index.md)で管理する。

## 公開中のCase

| 章 | Case | 主な成果物 | 備考 |
|---|---|---|---|
| 第1章 | [請求書連携OAuthアプリの権限見直し](./ch01-integrated-security-case-example.md) | Integrated Security Case Map | Assessment、Detection、Decisionの接続 |
| 第2章 | [OAuth連携評価前のAuthorization判断](./ch02-authorization-decision-example.md) | Authorization Checklist | Authority、Scope、Safety、Disclosure、RoE Handoffの接続 |
| 第3章 | [Capability Evidence Matrix](./ch03-capability-evidence-example.md) | Capability Evidence Matrix | Task、Evidence、Review、Gap、Reassessmentの接続 |
| 第4章 | [資産・信頼境界・脅威モデル](./ch04-threat-model-example.md) | Threat Model | Asset、Flow、Boundary、Threat、Control、Evidence、Reassessmentの接続 |
| 第5章 | [ATT&CK Behavior Map](./ch05-attack-behavior-example.md) | ATT&CK Behavior Map | 根拠、版、Data、Evidence threshold、Gapの接続 |
| 第11章 | [マルチテナント受注Export APIとWebhook登録の評価](./ch11-web-api-assessment-example.md) | Web/API Assessment Hypothesis Pack | 仮説、Evidence、Finding、Detectionの接続 |
| 第17章 | [未承認管理者同意変更のDetection Validation](./ch17-detection-validation-example.md) | Detection Validation Record | Telemetry、Replay、Triage、Handoffの接続 |
| 第25章 | [共同報告に埋もれた技術クラスタの判断](./ch25-structured-analysis-attribution-example.md) | Analytic Judgment Record | 競合仮説、不確実性、Attribution Ladder、circular reporting |

## 利用上の注意

- `.example`、`.test`、`.invalid`以外のDomainをCaseへ追加しない。
- 実Credential、個人情報、第三者Dataを持ち込まない。
- Negative Findingは不存在証明として扱わない。
- 合成Case内のReview表は記入例であり、実際の章Gate、法的承認、Repository merge承認ではない。

## 第6章の教育用補足

[Signal Flow合成記入例](ch06-signal-flow-example.md) / ART-16 / SFM-2026-001はCASE-2026-001をrefinesする。第4章Asset/Boundaryと第5章Behaviorを参照するが、親のObservation・Control・Gap・Decisionを更新しない。

## 第7章の教育用補足

[脆弱性優先順位の六件の合成記入例](ch07-vulnerability-prioritization-example.md) / ART-17 / VPR-2026-001はCASE-2026-001をrefinesする。導入・統制・判断は合成、EPSS / KEVは固定した公開Source入力である。親のCoverage・Control・Gap・期限を更新しない。

## 第8章の教育用補足

[Lab SafetyとEvidenceの完全合成記入例](ch08-lab-evidence-example.md) / ART-18 / LABPLAN-2026-001はCASE-2026-001をrefinesする。実Runtimeは実行せず、八状態と三判定、停止、六種Cleanup、実ByteのHashと保持を照合する。親のCoverage・Gap・Authorityは更新しない。

## 第9章の教育用補足

[RoEの完全合成記入例](ch09-engagement-roe-example.md) / ART-02 / ROE-2026-009はCASE-2026-001をrefinesする。三つの供給Objectだけを読む非実行計画で、親Authorizationの期限経過を保持しDraft / Do not proceedとする。第11章の独立Caseへ権限やEvidenceを転用しない。

## 第10章の教育用補足

[Attack Surface Registerの完全合成記入例](ch10-attack-surface-example.md) / ART-19 / ASR-2026-010はCASE-2026-001をrefinesする。九Source・六候補を限定して比較し、所有確認と実行許可を分ける。親RoEのDraft/失効/三Objectを保持し、全候補はrecord-only / 未承認である。

## 第12章の教育用補足

[Identity Attack Path Reviewの完全合成記入例](ch12-identity-path-review-example.md) / ART-20 / IAR-2026-012はCASE-2026-001をrefinesする。四Principal、十四Edge、六Pathを有限比較し、MFA・設定・合成Event・実施許可を分ける。親RoEのDraft/失効/三Object、Signal Flow Gap、独立CASE-2026-011を変更しない。

## 第13章の教育用補足

[Platform and Supply Chain Assessmentの完全合成記入例](ch13-platform-supply-chain-example.md) / ART-21 / PSA-2026-013はCASE-2026-001をrefinesする。三Planeと八Chainを五状態で評価し、mutable source、unversioned action、過大権限、出所不足、Runtime差異を記録する。実Cloud/CI/Registry/Tokenは使用せず、親RoE Draft/失効/三Objectと独立CASE-2026-011を変更しない。

## 第14章の教育用補足

[Minimal-Impact Validation Recordの完全合成記入例](ch14-minimal-impact-validation-example.md) / ART-22 / MIV-2026-014はCASE-2026-001をrefinesする。八記録を六Result・四Methodで比較し、全実操作0、未実施・停止・Cleanup・残存Unknownを分ける。親RoE Draft/失効/元Window/三Objectと独立CASE-2026-011の境界を変更しない。

## 第15章の教育用補足

[Finding ReportとRetest Recordの完全合成記入例](ch15-findings-retest-risk-example.md) / ART-04 / ART-23 / FRT-2026-015はCASE-2026-001をrefinesする。七つの独立した判断例、五Retest、五つの未配達Handoffを持つ。親14は方法参照だけで、新OAuth教材のEvidenceへ付け替えない。親RoEのDraft/失効/元Window/三Objectfalseと独立CASE-2026-011を保持する。

## 第II部の横断読解

[AssessmentからRisk判断への対応表](part-ii-assessment-risk-map.md)で、第9〜15章の参照ID、独立Case、対象・版・Scope、未配達Handoffを区別して読む。新しい許可やEvidenceの継承を意味しない。

## 第16章 Telemetry Coverage

[完全合成記入例](ch16-telemetry-coverage-example.md)はART-24の全欄と十の独立した対比を示す。[JSON](fixtures/ch16-telemetry-coverage.json)と[Schema](../schemas/ch16-telemetry-coverage.schema.json)を読解に用い、親のEvidence、権限、未配達を変更しない。

## 第18章 Threat Hunting

[Hunt Plan and Findings記入例](ch18-hunt-plan-example.md)はART-06の十二の独立対比である。[合成JSON](fixtures/ch18-threat-hunting.json)と[Schema](../schemas/ch18-threat-hunting.schema.json)へ対応し、0件と観測不足を区別する。原DVR/DET/TEL/fixtureと未配達は不変である。

## 第19章 Incident Response

[Incident Action Plan記入例](ch19-incident-action-plan-example.md)はART-25の十二の独立した条件付きSnapshotである。[合成JSON](fixtures/ch19-incident-response.json)と[Schema](../schemas/ch19-incident-response.schema.json)で、七状態、宣言・Scope・保存・復旧検証・残余リスクを分ける。親のEvidence・権限・未配達を継承せず、実操作と通知は0件である。

## 第20章 DFIR

[TimelineとRCAの全欄Case](ch20-dfir-timeline-causality-example.md)はART-07/26を五Receipt・二Cutoff・六Claimで比較する。[供給JSON](fixtures/ch20-dfir-timeline-causality.json)と[Schema](../schemas/ch20-dfir-timeline-causality.schema.json)に対応し、時刻幅、再送、後着Evidence、代替説明と原因未確定を分ける。親19の未配達・Evidence・実権限を更新しない。

## 第21章 Control Validation

[全欄Case](ch21-control-validation-example.md)はART-27の十Scenarioを五層のExpected/Actual、六Failure、Gap、Owner、Retestへ結ぶ。[供給JSON](fixtures/ch21-control-validation.json)と[Schema](../schemas/ch21-control-validation.schema.json)は完全合成・非実行であり、親のEvidence・実権限・未配達・原因未確定を更新しない。

## 第22章 Measurement and Improvement

[Security Improvement Backlog全欄Case](ch22-improvement-backlog-example.md)はART-28の十Metric、八Item、七Status、五対比を持つ。[供給JSON](fixtures/ch22-measurement-improvement.json)と[Schema](../schemas/ch22-measurement-improvement.schema.json)で分母・時刻・品質・Validation/Evidence・期限付き受容を照合する。実効果、実権限、親Evidenceの受領は認定しない。

## 第III部の横断読解

[観測から改善判断への対応表](part-iii-detection-improvement-map.md)で、第16〜22章の直接ID参照、方法参照、非継承、未配達とGapを確認する。新しい実施Caseではなく、七教材を読み直す補助教材である。
