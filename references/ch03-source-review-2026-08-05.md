# 第3章 Source Review Note — NICE Framework

## 監査範囲

| 項目 | 値 |
|---|---|
| Source Note ID | `SRC-NICE-001` |
| 対象章 | 第0章、第1章、第3章 |
| Checked at | 2026-08-05 |
| 次回確認日 | 2026-11-05 |
| 目的 | NICE Frameworkの構造文書と、別管理される現行Componentsの版・用途・識別子を分離して確認する |

## 確認した公式一次資料

1. NIST CSRC、`NIST SP 800-181 Rev.1`最終版
   - <https://csrc.nist.gov/pubs/sp/800/181/r1/final>
2. NIST、NICE Framework Components v2.2.0リリース告知
   - <https://www.nist.gov/news-events/news/2026/04/nice-releases-nice-framework-components-v220>
3. NIST NICE Framework Change Logs
   - <https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/current-version/change-logs>
4. NIST NICE Framework Current Versions
   - <https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/nice-framework-current-versions>
5. NIST CSRC Cybersecurity and Privacy Reference Tool（CPRT）Catalog
   - <https://csrc.nist.gov/projects/cprt/catalog>
6. Current Versionsから公開されているNICE Framework Components v2.2.0 JSON
   - <https://csrc.nist.gov/csrc/media/Projects/cprt/documents/nice/v2-2-0_nf_components.json>

すべてのURLは2026-08-05にHTTP 200を確認した。Certification vendorの資料は、標準や能力証明の根拠として採用していない。

## 確認結果

### 構造文書

- `NIST SP 800-181 Rev.1`は最終版である。
- 公開履歴は2020-11-16のFinalを示す。
- 本文はCybersecurity workをTaskで表し、Knowledge / Skillを学習者やWorkforceの共通語彙として扱う。
- CSRCのPlanning Noteは、Work Role、Competency Area、Task / Knowledge / Skill等のComponentsが別管理であり、Current Versionsを参照するよう明記している。

### 現行Components

- NICE Framework Componentsの現行確認版は`v2.2.0`である。
- リリース告知とChange Logsは、リリース日を2026-04-28としている。
- `v2.2.0`の変更には次が含まれる。
  - Cybersecurity Supply Chain Risk Management Work Role `OG-WRL-017`の追加
  - Cryptography Competency Area `NF-COM-006`の更新
  - DevSecOps Competency Area `NF-COM-008`の更新
  - Task / Knowledge / Skill（TKS）のadministrative changes
- 公式JSONは`version: 2.2.0`と`doc_identifier: SP_800_181_2_2_0`を持ち、上記3識別子を収録している。JSON自体にはリリース日を固定するFieldがないため、日付はリリース告知とChange Logsで判定した。

## 日付不整合のDisposition

Current Versionsページの表示は`CURRENT VERSION: 2.2.0 (April 28, 2025)`となっている。一方で、次の公式情報は2026-04-28で整合する。

- URLが`/2026/04/`であるリリース告知
- リリース告知本文と`Released April 28, 2026`表示
- Change Logsの`28 April 2026`表示
- `v2.1.0`が2025-12-03、その後継`v2.2.0`が2026-04-28という版順序
- Current Versionsから配布される`v2-2-0` JSON

したがって、Current Versionsページの`2025`は**見かけ上のページ誤記**として扱う。Source Registryへ誤った2025-04-28を転記せず、Componentsのリリース日は2026-04-28と記録する。NISTによる表示修正または公式訂正が確認された場合は、このDispositionを再監査する。

## 第3章での採用範囲

- NICE Frameworkは、Work Role、Task、Knowledge、Skill、Competency Areaを分解するための共通語彙として使う。
- Work Roleは仕事のGroupingであり、Job titleや個人そのものとして扱わない。
- Competency AreaはComponentsのGroupingであり、個人が有能であることの証明として扱わない。
- NICE identifierへの対応付けだけでは、個人の能力を証明しない。
- 個人のCapability Judgmentには、明示した条件下で作成した複数のArtifact Evidence、Rubric、Reviewer、限界、期限、再評価Triggerを必要とする。
- `observe / explain / assess / design / lead`は本書固有の学習進行表現であり、NISTの普遍的な標準Levelとして記載しない。

## Registry更新方針

- Source ID `SRC-NICE-001`は維持する。
- `version`で構造文書`SP 800-181 Rev.1`と現行Components `v2.2.0`を区別する。
- 個別Source Noteの`checkedAt`だけを2026-08-05へ更新し、Registry全体の一括監査日は変更しない。
- `nextReviewAt`は2026-11-05とする。
- Review triggerは次とする。
  - NIST SP 800-181 revision or errata
  - NICE Framework Components major or minor release
  - Chapter 3で使用するWork Role、Competency Area、TKS identifierの変更

## 制約

- 現行Components全件を安定本文へ複製しない。
- Chapter 3の合成例で使うComponents版は`v2.2.0`へ固定する。
- 本Noteは人事評価、採用判定、資格認定の基準を提供しない。
- 公開前にはCurrent Versions、Change Logs、公式JSON、リリース告知を再確認する。
