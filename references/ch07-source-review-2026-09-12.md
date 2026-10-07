# 第7章 Source Review Note — 2026-09-12

## 対象と採否

Issue #32 / ART-17を対象とする。base mainは`665ca8e3c1846778f6657e38ca15facf638a028b`、Content Safety Policyは`1.2.0`、Publication Projectionは`1.1.0`。確認日は2026-09-12である。下表の採用範囲を超える運用・法的結論は導かない。

## 一次資料と適用範囲

| Source ID | 一次資料・版 | 採用範囲 |
|---|---|---|
| SRC-CVE-001 | [NIST CSRC CVE glossary](https://csrc.nist.gov/glossary/term/common_vulnerabilities_and_exposures)、版・公表日不明 | 脆弱性の共通識別の役割。CVE.orgのSPA shellを本文読了の証拠にはしない |
| SRC-CWE-001 | [MITRE CWE archive](https://cwe.mitre.org/data/archive.html)、4.20、XML Date 2026-04-30 | 弱点分類とCWE-639。日付はXMLのRoot属性による |
| SRC-CVSS-001 | [FIRST CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document) / [User Guide](https://www.first.org/cvss/v4.0/user-guide)、両Document Version 1.2 | Metric group、Vector、Nomenclature。標準4.0と説明文書1.2を区別 |
| SRC-EPSS-001 | [FIRST EPSS](https://www.first.org/epss/) / [Data](https://www.first.org/epss/data)、Model v5 | 30日間の悪用確率Signal、Percentile、日次値とModel境界 |
| SRC-KEV-001 | [CISA KEV official mirror](https://github.com/cisagov/kev-data)、Catalog 2026.09.11 | 固定Catalogの掲載有無。Mirrorの同期遅延と取得限界を維持 |
| SRC-CISA-VRM-001 | [CISA発行告知](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/41b445a)、2026-06-10 | BOD 26-04発行とリスクベースの優先付けという目的だけ。告知は命令本文の代替でない |
| SRC-OWASP-TOP10-001 | [OWASP Top 10:2025](https://top10.owasp.org/2025/)、2025 | Awarenessと対象漏れを考える補助。網羅的検査や個別優先順位の保証には使わない |

CVEの定義はNISTの一次資料本文をブラウザ経由で確認した。直接HTTP取得は403であり、本文を取得できなかったCVE.orgのSPAとは区別する。Live glossaryの版・公表日は分からないためnullとする。

## 固定Snapshotと再現範囲

最小抽出値と来歴は[Source snapshot](../cases/fixtures/ch07-source-snapshot.json)、利用値は[Case JSON](../cases/fixtures/ch07-vulnerability-prioritization.json)に記録する。全文Catalog、外部Calculator、raw predraftは同梱しない。公開Signal値は一次資料からの固定入力であり、導入・到達性・統制Evidence・意思決定だけが完全合成である。

EPSSは2026-09-11の公式CSV gzipと、同日の二つのCVEを取得したAPIをDecimalで照合した。CSVの`model_version`は`v2026.06.15`、`score_date`は`2026-09-11T12:00:21Z`である。gzip SHA-256は`36e793fea920d9f0af62516c9ceed759b77f2da4f43421d3a02375d3c31a8cba`。CVE-2021-44228は0.99999 / 1.0、CVE-2024-3094は0.85974 / 0.99716（Score / Percentile）。過去Snapshotであり利用時の現在値ではない。API v1はModel v5と別の版である。

FIRST Dataページによるv5運用開始は2026-06-15。[関連告知](https://www.first.org/newsroom/releases/202606-036)の公開日2026-07-15と同一視しない。Live EPSSページ自体の公表日は分からないためRegistryではnullとし、Model移行日はnotesに記録する。

KEVは公式Mirrorのcommit `acdcfd43102c098c377568b417a42c0e00cc63a5`、Catalog `2026.09.11`、dateReleased `2026-09-11T19:32:16.8993Z`、全1709件を確認した。Catalog SHA-256は`c27673ad6c346c50f573c566f14c11c373e4ae452880d2cdb8f01a364e1e630b`。CVE-2021-44228は掲載、CVE-2024-3094はこの全件Snapshotには未掲載。後者を過去・将来・全世界の悪用不存在とは解釈しない。

CVSSの二つの合成Vectorは[FIRST Calculator](https://github.com/FIRSTdotorg/cvss-v4-calculator)のcommit `c5b0d409ae9f57c44264c6ce5f27d89298e1d32a`を固定し、数学計算用のコードだけを検査してオフラインで評価した。結果はCVSS-Bの9.3と2.1。実CVEのベンダー評価ではない。Runtime依存を追加せず、章契約はこの二組の一致だけを検証し、任意Vectorの計算器を実装しない。

CWEの公式4.20 XML ZIPのSHA-256は`3976f599e5e5200219a3108bb896d06e2a88fbb293369e1883cb423a5e9d7d50`。Root Version / DateとCWE-639の名称を照合した。Web footerやcache用の数字から公開日を推測しない。

## Authorityと取得限界

CISAのCatalog正規WebページとBOD 26-04本文は403で取得できなかった。公式MirrorのREADMEと、CISA発行のGovDelivery告知は取得した。第三者の転載は法的根拠として採用しない。詳細な適用対象、例外、旧命令の置換関係、数値期限は未検証のため本章の命題へ採用していない。

`requiredActionApplicability`はCVEの有無にかかわらず全教材記録で`Unverified`のまま、担当を`SYNTH-GOVERNANCE-REVIEWER`に分離する。Catalog due dateは組織のDeadlineではない。教材の非実行分析が完了しても、現実の義務免除・猶予・Risk acceptanceや操作許可は成立しない。実作業へ移すには原文と適用範囲の確認を含む第2章のGateが必要である。

## Source変更の影響と再確認

EPSSの旧v4からv5への変更は第7章の説明とSnapshotに適用する。KEVは利用時確認を引き続き必要とし、OWASPは第11章のAwarenessという限定を変えない。Registry全体のcheckedAtや他章の歴史的な記述を一括更新しない。

Next reviewは2026-12-12。Model・標準・文書版・Catalog・Directive・利用命題の変更時、実作業への転用前には期限前でも再確認する。親Chapter4 / 5 / 6のAsset、Path、Coverage、Control、Gap、期限は変更しない。

## Editorial Input Record

- Package ID: EIP-0003
- Package SHA-256: `d986ee9a9c71cf210420bb921f078a395133e2e5e0b9050960ad63554c22582a`
- Target: Issue #32 / chapter-07
- Input path: `chapter07-vulnerability-prioritization.predraft.md`
- Input SHA-256: `6caf4e3d9174ae8b527df5b14301cd456550b1eca1ea7e88cf7c19e5031338cb`
- Input確認状況: `not-present-in-authorized-workspace`
- Adopted: raw predraftからの直接採用なし。登録metadataを照合。
- Rewritten: Issue #32、current contract、親Case、再確認した一次資料から新規作成。
- Rejected: 未確認rawの読了・実体hash検証・直接採用、公開Signalの組織侵害確率への置換、未検証の法的適用除外。
- Deferred: 任意CVSS計算器、実環境評価、具体的な修正作業、Chapter8以降。
- Raw tracked files: 0。

選択と専用PRをManifestで追跡し、通常mergeと実際のmain/publication前にはconsumedにしない。
