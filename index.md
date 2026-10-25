# ホワイトハッカーとサイバーインテリジェンス実践体系

## 攻撃者の行動を理解し、検証・検知・対応・経営判断につなげる

本書は、攻撃評価、Detection Engineering、Threat Hunting、Incident Response、DFIR、OSINT、Cyber Threat Intelligence、AI Securityを、Evidenceと意思決定で接続する専門実務書です。

第0章から第29章までの30章と、最終ポートフォリオ`ART-33`を公開しています。現在は、付録、Source freshness、Part V横断Review、人間の専門読者試行、配布物、`v1.0.0` Releaseを整備しています。30章の公開と、全書Release完了は同じ状態ではありません。

## 本書の対象

| 読者 | 主な目的 |
|---|---|
| SOC・CSIRT・Detection担当 | Telemetry、Detection、Hunting、IR、DFIRを一つのCaseとして接続する |
| CTI・分析担当 | Source、Evidence、不確実性、代替仮説、帰属限界を判断へ変換する |
| Security Architecture担当 | Asset、Identity、Cloud、Supply Chain、AI Agentの信頼境界を評価する |
| インフラ・SRE・DevOps・開発技術者 | 既存の技術経験をセキュリティ評価、観測、改善へ接続する |
| CISO室・Security Program責任者 | 技術的事実を優先順位、停止、投資、Risk acceptanceへ変換する |

前提知識は、Linux、TCP/IP、DNS、HTTP、Gitの基礎と、インフラ、クラウド、Web、開発、運用のいずれかの実務経験です。

本書は、コンピュータやネットワーク自体の入門書、CTF解法集、攻撃コマンド集、特定製品の操作手順書ではありません。詳細技術は既存の専門書へ委譲し、本書では分野間をつなぐ判断、証拠、成果物、責任、再評価を扱います。

## 三つの利用層

| 層 | 内容 | 主な入口 |
|---|---|---|
| 本文 | 概念、判断、根拠、反例、実務上の含意 | [第0章](manuscript/00-reading-guide.md)、[詳細目次](TOC.md) |
| 実務成果物 | Template、完全合成Case、Checklist、Rubric | [成果物索引](artifact-index.md)、[合成Case索引](cases/index.md) |
| 機械検証層 | JSON、Schema、fixture、contract、回帰検査 | [Fixture catalog](cases/fixtures/index.md)、Repositoryの`scripts/`・`schemas/` |

機械検査は、参照、版、状態、安全境界、公開面の漂流を検出します。実環境の安全性、人間の承認、Controlの有効性を認定するものではありません。

## 中心となるループ

```text
判断要求を定義する
  → 資産・信頼境界・脅威を把握する
  → 攻撃経路と観測仮説を立てる
  → 許可された隔離環境で最小限に検証する
  → ログ・証拠・痕跡を評価する
  → 検知・対応・コントロールを改善する
  → 確信度付きインテリジェンスに変換する
  → 技術・運用・経営判断を記録する
  → 再評価する
```

## 読み始める

### 初回の最短ルート

1. [第0章 本書の読み方](manuscript/00-reading-guide.md)
2. [Quick Start](quickstart.md)
3. [最初の成果物：判断と証拠不足の読解](cases/first-artifact-walkthrough.md)
4. [第1章 攻撃・防御・インテリジェンスを一つの業務として捉える](manuscript/01-integrated-discipline.md)
5. [成果物索引](artifact-index.md)

Quick Startは一般初心者向けの短縮版ではありません。本書の厳密な記録体系へ、判断要求、仮説、Evidence gap、停止条件から入るためのオンボーディングです。

### 代表的な専門ルート

- 評価・Threat Model: [第4章](manuscript/04-assets-boundaries-threat-model.md) → [第7章](manuscript/07-vulnerability-prioritization.md) → [第9〜15章](TOC.md)
- Detection・SOC: [第16章](manuscript/16-telemetry-evidence-readiness.md) → [第17章](manuscript/17-detection-engineering.md) → [第18〜22章](TOC.md)
- CTI・分析: [第23章](manuscript/23-intelligence-requirements.md) → [第24章](manuscript/24-osint-provenance-sources.md) → [第25章](manuscript/25-structured-analysis-attribution.md) → [第26章](manuscript/26-cti-distribution.md)
- AI Security: [第27章](manuscript/27-ai-agent-security.md) → [第28章](manuscript/28-ai-assisted-analysis-assurance.md) → [第29章](manuscript/29-capstone-case-study.md)
- 統合・経営判断: [第1章](manuscript/01-integrated-discipline.md) → [第19章](manuscript/19-incident-response.md) → [第22章](manuscript/22-measurement-improvement.md) → [第29章](manuscript/29-capstone-case-study.md)

## 学習成果

本書を通じて、読者は次の成果物を一貫した証拠と判断の流れで作成できるようになります。

- Integrated Security Case Map
- Authorization ChecklistとRules of Engagement
- Capability Evidence Matrix
- Threat ModelとAttack Path
- Finding ReportとRetest Record
- Telemetry Coverage MapとDetection Validation Record
- Hunt ReportとIncident Action Plan
- Incident TimelineとRoot Cause Analysis
- Evidence and Source TableとCTI Report
- Analytic Judgment Record
- AI / Agent Threat Model
- AI-Assisted Analysis Assurance Record
- Executive Decision Brief
- Final Security Decision Portfolio Index

## 公開中の成果物

- [Integrated Security Case Mapテンプレート](templates/integrated-security-case-map.md)
- [第1章 合成記入例：請求書連携OAuthアプリの権限見直し](cases/ch01-integrated-security-case-example.md)
- [Authorization Checklistテンプレート](templates/authorization-checklist.md)
- [第2章 合成記入例：OAuth連携評価前のAuthorization判断](cases/ch02-authorization-decision-example.md)
- [Capability Evidence Matrixテンプレート](templates/capability-evidence-matrix.md)
- [第3章 合成記入例：Capability Evidence Matrix](cases/ch03-capability-evidence-example.md)
- [Threat Modelテンプレート](templates/threat-model.md)
- [第4章 合成記入例：資産・信頼境界・脅威モデル](cases/ch04-threat-model-example.md)
- [ATT&CK Behavior Mapテンプレート](templates/attack-behavior-map.md)
- [第5章 合成記入例：ATT&CK Behavior Map](cases/ch05-attack-behavior-example.md)
- [Web/API Assessment Hypothesis Packテンプレート](templates/web-api-assessment-hypothesis-pack.md)
- [第11章 合成記入例：マルチテナント受注Export APIとWebhook登録の評価](cases/ch11-web-api-assessment-example.md)
- [第11章 読み取り専用の合成Request / Response Dataset](cases/fixtures/ch11-web-api-assessment-dataset.json)
- [Detection Validation Recordテンプレート](templates/detection-validation.md)
- [第17章 合成記入例：未承認管理者同意変更のDetection Validation](cases/ch17-detection-validation-example.md)
- [第17章 オフラインfixture説明](cases/fixtures/ch17-detection-engineering-fixture.md)
- [Analytic Judgment Recordテンプレート](templates/analytic-judgment-record.md)
- [第25章 合成記入例：共同報告に埋もれた技術クラスタの判断](cases/ch25-structured-analysis-attribution-example.md)
- [Rules of Engagementテンプレート](templates/rules-of-engagement.md)
- [Incident Action Planテンプレート](templates/incident-action-plan.md)
- [CTI Reportテンプレート](templates/cti-report.md)
- [Executive Briefテンプレート](templates/executive-brief.md)
- [AI / Agent Threat Modelテンプレート](templates/ai-agent-threat-model.md)
- [AI-Assisted Analysis Assurance Recordテンプレート](templates/ai-assisted-analysis-assurance-record.md)
- [Final Security Decision Portfolio Indexテンプレート](templates/final-security-decision-portfolio-index.md)
- [第29章 統合ケーススタディ](manuscript/29-capstone-case-study.md)
- [第29章 完全合成Case](cases/ch29-capstone-portfolio-example.md)
- [全成果物索引](artifact-index.md)
- [合成Case索引](cases/index.md)
- [Fixture catalog](cases/fixtures/index.md)

これらの成果物は、Authorization、Capability Evidence、Threat Model、Assessment、Detection、Hunting、IR / DFIR、CTI、AI Security、経営判断、再評価を、Case IDとEvidence IDで接続します。成果物の記入完了は、全Controlの合格、実作業の許可、実環境の安全確認を意味しません。

## 実務参照

- [成果物索引](artifact-index.md)
- [実務テンプレート](templates/)
- [困ったときの停止・切り分けフロー](troubleshooting.md)
- [用語集](glossary.md)
- [図表索引](figure-index.md)
- [Source Baseline](references/reference-baseline.md)
- [詳細目次](TOC.md)

## 安全と法的注意

本書の演習は、明示的に許可された自己所有環境、隔離ラボ、合成データだけを対象とします。公開されている第三者システムは演習対象ではありません。詳細は[安全な公開範囲](SAFETY_SCOPE.md)と[法的・安全上の注意](legal-notice.md)を確認してください。

## ライセンス

本文、図表、演習課題、テンプレートは、特記がない限りCC BY-NC-SA 4.0です。商用利用には別途契約が必要です。自作コードの扱いは[LICENSE.md](LICENSE.md)を参照してください。

## 第9章の成果物

[第9章 Engagement DesignとRules of Engagement](manuscript/09-engagement-roe.md) / [ART-02](templates/rules-of-engagement.md) / [完全合成Case](cases/ch09-engagement-roe-example.md) / [計画JSON](cases/fixtures/ch09-engagement-roe.json)。親の許可期限を保持したDraftで、作業を始めない判断と再承認を学ぶ。

## Intelligence Requirementから収集計画へ

[第23章](manuscript/23-intelligence-requirements.md)、[ART-29](templates/intelligence-requirement-collection-plan.md)、[完全合成例](cases/ch23-intelligence-requirements-example.md)で、判断期限と未解決Gapを辿る。

## 第24章の制作成果

[OSINT、Provenance、情報源評価](manuscript/24-osint-provenance-sources.md)は、ART-30と完全合成資料で原典、版、変換、三つの評価軸とEvidence用途を学ぶ。

## 第26章の制作成果

[CTIを構造化し、技術・経営へ配布する](manuscript/26-cti-distribution.md)では、同じ根拠からART-08 / ART-09を作り、未配達・Gap・再評価を保持する。
