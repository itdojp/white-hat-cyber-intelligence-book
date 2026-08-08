# ホワイトハッカーとサイバーインテリジェンス実践体系

## 攻撃者の行動を理解し、検証・検知・対応・経営判断につなげる

本書は、攻撃評価、Detection Engineering、Threat Hunting、Incident Response、DFIR、OSINT、Cyber Threat Intelligenceを、ひとつの意思決定ループとして学ぶ実践書です。

## 学習成果

本書を通じて、読者は次の成果物を一貫した証拠と判断の流れで作成できるようになります。

- Integrated Security Case Map
- Authorization ChecklistとRules of Engagement
- Capability Evidence Matrix
- Threat ModelとAttack Path
- Finding ReportとRetest Record
- Telemetry Coverage MapとDetection Validation Record
- Incident TimelineとRoot Cause Analysis
- Evidence and Source TableとCTI Report
- Analytic Judgment Record
- Executive Decision Brief

## 想定読者

| 読者 | 主な目的 |
|---|---|
| インフラ・クラウド技術者 | 攻撃者視点、Identity、Cloud、Telemetryを防御設計へ接続する |
| 開発・DevOps技術者 | Web/API、CI/CD、Supply Chain、AI Securityを評価する |
| SOC・CSIRT・分析担当 | Detection、Hunting、IR、DFIR、CTIを統合する |
| CTO・CISO・技術経営者 | 技術的事実を投資、優先順位、停止、リスク受容へ変換する |

前提知識はLinux、TCP/IP、HTTP、Gitの基礎です。詳細技術は既存の専門書へ委譲し、本書では分野間をつなぐ判断、証拠、成果物を中心に扱います。

## 読み始める

1. [第0章 本書の読み方](manuscript/00-reading-guide.md)
2. [第1章 攻撃・防御・インテリジェンスを一つの業務として捉える](manuscript/01-integrated-discipline.md)
3. [第2章 法、倫理、許可、責任ある開示](manuscript/02-law-ethics-authorization.md)
4. [第3章 能力を分解し、証拠で学習する](manuscript/03-capability-evidence.md)
5. [第4章 資産、信頼境界、攻撃面、脅威モデル](manuscript/04-assets-boundaries-threat-model.md)
6. [第11章 Web・APIを仮説駆動で評価する](manuscript/11-web-api-hypothesis.md)
7. [第17章 Detection Engineering](manuscript/17-detection-engineering.md)
8. [第25章 構造化分析、不確実性、アトリビューション](manuscript/25-structured-analysis-attribution.md)
9. [Quick Start](quickstart.md)
10. [Concept Map](concept-map.md)
11. [詳細目次](TOC.md)

## 公開中の成果物

- [Integrated Security Case Mapテンプレート](templates/integrated-security-case-map.md)
- [第1章 合成記入例：請求書連携OAuthアプリの権限見直し](cases/ch01-integrated-security-case-example.md)
- [Authorization Checklistテンプレート](templates/authorization-checklist.md)
- [第2章 合成記入例：OAuth連携評価前のAuthorization判断](cases/ch02-authorization-decision-example.md)
- [Capability Evidence Matrixテンプレート](templates/capability-evidence-matrix.md)
- [第3章 合成記入例：Capability Evidence Matrix](cases/ch03-capability-evidence-example.md)
- [Threat Modelテンプレート](templates/threat-model.md)
- [第4章 合成記入例：資産・信頼境界・脅威モデル](cases/ch04-threat-model-example.md)
- [Web/API Assessment Hypothesis Packテンプレート](templates/web-api-assessment-hypothesis-pack.md)
- [第11章 合成記入例：マルチテナント受注Export APIとWebhook登録の評価](cases/ch11-web-api-assessment-example.md)
- [第11章 読み取り専用の合成Request / Response Dataset](cases/fixtures/ch11-web-api-assessment-dataset.json)
- [Detection Validation Recordテンプレート](templates/detection-validation.md)
- [第17章 合成記入例：未承認管理者同意変更のDetection Validation](cases/ch17-detection-validation-example.md)
- [第17章 オフラインfixture説明](cases/fixtures/ch17-detection-engineering-fixture.md)
- [Analytic Judgment Recordテンプレート](templates/analytic-judgment-record.md)
- [第25章 合成記入例：共同報告に埋もれた技術クラスタの判断](cases/ch25-structured-analysis-attribution-example.md)
- [合成Case索引](cases/index.md)
- [Fixture catalog](cases/fixtures/index.md)

これらの成果物は、Authorization、Capability Evidence、Threat Model、Assessment、Detection、Hunting、IR / DFIR、CTI、構造化分析、経営判断、再評価を、共通Case IDとEvidence IDで接続します。第2章では、Tool実行前にAuthority、Scope、Safety、Disclosureを評価し、条件付き許可・停止・EscalationをRules of Engagementへ引き渡します。第3章では、学習GoalをTask、Knowledge / Skill、許可されたPractice、Artifact Evidence、Review、Gap、Reassessmentへ分解し、限定されたCapability Judgmentを作ります。第4章では、Decision RequirementをAsset、Flow、Trust Boundary、Threat Hypothesis、非OperationalなAttack Path、Control assurance、Evidence Requirement、Reassessmentへ分解します。

## 実務参照

- [成果物索引](artifact-index.md)
- [実務テンプレート](templates/)
- [困ったときの停止・切り分けフロー](troubleshooting.md)
- [用語集](glossary.md)
- [図表索引](figure-index.md)
- [Source Baseline](references/reference-baseline.md)

## 安全と法的注意

本書の演習は、明示的に許可された自己所有環境、隔離ラボ、合成データだけを対象とします。公開されている第三者システムは演習対象ではありません。詳細は[安全な公開範囲](SAFETY_SCOPE.md)と[法的・安全上の注意](legal-notice.md)を確認してください。

## ライセンス

本文、図表、演習課題、テンプレートは、特記がない限りCC BY-NC-SA 4.0です。商用利用には別途契約が必要です。自作コードの扱いは[LICENSE.md](LICENSE.md)を参照してください。
