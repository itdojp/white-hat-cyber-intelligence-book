# ホワイトハッカーとサイバーインテリジェンス実践体系

## 攻撃者の行動を理解し、検証・検知・対応・経営判断につなげる

本書は、攻撃評価、Detection Engineering、Threat Hunting、Incident Response、DFIR、OSINT、Cyber Threat Intelligenceを、ひとつの意思決定ループとして学ぶ実践書です。

## 学習成果

本書を通じて、読者は次の成果物を一貫した証拠と判断の流れで作成できるようになります。

- Integrated Security Case Map
- Rules of Engagement
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
3. [Quick Start](quickstart.md)
4. [Concept Map](concept-map.md)
5. [詳細目次](TOC.md)

## 第1章の成果物

- [Integrated Security Case Mapテンプレート](templates/integrated-security-case-map.md)
- [合成記入例：請求書連携OAuthアプリの権限見直し](cases/ch01-integrated-security-case-example.md)

この成果物は、Assessment、Detection、Hunting、IR / DFIR、CTI、経営判断、再評価を、共通Case IDとEvidence IDで接続します。

## 第25章の成果物

- [第25章 本文](manuscript/25-structured-analysis-attribution.md)
- [Analytic Judgment Recordテンプレート](templates/analytic-judgment-record.md)
- [合成記入例：共同報告に埋もれた技術クラスタの判断](cases/ch25-structured-analysis-attribution-example.md)
- [Case索引](cases/index.md)
- [Fixture catalog](cases/fixtures/index.md)

この成果物は、Fact、Assumption、Judgment、Forecast、Recommendationを分離し、Lineage、circular reporting、deception candidate、Attribution Ladder、Decision、Reassessmentを同じCaseで接続します。

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
