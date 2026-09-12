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
