# 第5章 Source Review Note — 2026-09-06

## 対象と採否

Issue #30、Editorial Input契約 #63 / #98を対象とする。Canonical baseは`518ea8579439a2c29cfc0e4fbea4086995ada1c0`、Content Safety Policyは`1.2.0`、Publication Projectionは`1.1.0`である。

2026-09-06にMITREの公式Version History、Updates、FAQ、Detection Strategies、Data Sources、T1671、DET0539と固定Enterprise STIX bundleを確認した。本文へ採用するのは行動分類、版、関係、限界だけであり、Procedure exampleや実行手順を転載しない。

## Releaseと取得証跡

- [Version History](https://attack.mitre.org/resources/versions/): currentはv19.2。開始日の表示はApril 28, 2026のまま。
- [Updates](https://attack.mitre.org/resources/updates/): August 2026 update、開始日2026-08-06。
- [MITRE/CTI release](https://github.com/mitre/cti/releases/tag/ATT%26CK-v19.2): `published_at=2026-08-05T22:57:35Z`。
- Annotated tag object: `8378689cbd8cf6ad7d566d3924c3c9755417cf43`。
- Tagの参照先commit: `8543c5b05bd9bbcace9fc37f30bba96b675b6f33`。
- [固定Enterprise bundle](https://raw.githubusercontent.com/mitre/cti/8543c5b05bd9bbcace9fc37f30bba96b675b6f33/enterprise-attack/enterprise-attack.json)。
- Bundle SHA-256: `f7eaf37fe53b50404084fe1fe67237278f7317e61c11ad550295722d13ede259`。
- Next review: 2026-12-06。Catalog release、対象Object・関係・有効性、Data model変更で期限前でも再確認する。

Version Historyの日付をminor releaseの公開日とみなさない。Updatesの表示日とGitHubのUTC時刻は別フィールドで保持し、表示日のタイムゾーンを推測しない。WebsiteのVersion Permalinkはv19単位であり、minor releaseは固定commitとbundle digestを正とする。

## 採用Object

| ID | Type | Object version | modified (UTC) | 状態 |
|---|---|---|---|---|
| T1671 | attack-pattern | 1.0 | 2025-04-15T19:59:05.283Z | active、Sub-techniqueなし |
| TA0003 | x-mitre-tactic | 1.0 | 2025-04-25T14:45:33.492Z | active、Persistence |
| DET0539 | x-mitre-detection-strategy | 1.0 | 2026-05-12T16:34:50.684Z | active |
| AN1487 | x-mitre-analytic | 1.0 | 2025-10-21T15:10:28.402Z | active、Office Suite |
| AN1488 | x-mitre-analytic | 1.0 | 2025-10-21T15:10:28.402Z | active、SaaS |
| DC0066 | x-mitre-data-component | 2.0 | 2025-11-12T22:03:39.105Z | active |
| DC0069 | x-mitre-data-component | 2.0 | 2025-11-12T22:03:39.105Z | active |
| DC0038 | x-mitre-data-component | 3.0 | 2026-05-12T15:12:00.776Z | active |

`active`は固定bundle内でrevoked / x_mitre_deprecatedがtrueではないことを意味する。任意のrevokedプロパティがないObjectはfalseとして扱い、抽出fixtureに元のプロパティ有無を別途残す。全ObjectのSTIX ID、正規化したObject hash、domains、必要な参照関係もfixtureへ保存する。

- [T1671 Version Permalink](https://attack.mitre.org/versions/v19/techniques/T1671/)
- [DET0539 Version Permalink](https://attack.mitre.org/versions/v19/detectionstrategies/DET0539/)
- [AN1487](https://attack.mitre.org/versions/v19/detectionstrategies/DET0539/#AN1487)
- [AN1488](https://attack.mitre.org/versions/v19/detectionstrategies/DET0539/#AN1488)

AnalyticはDET0539ページ内のanchorを使う。推測した独立Analytic routeは使用しない。DET0539からT1671への`detects`関係、DET0539のanalytic refs、AN1487のDC0066 / DC0069、AN1488のDC0069 / DC0038を固定bundleで確認した。T1671のplatformはOffice Suite / SaaS、TacticはPersistenceである。

## 原典の用途と限界

- `SRC-ATTACK-001`: v19.2の版とrelease経緯。分類の網羅と防御有効性を同一視しない。
- `SRC-ATTACK-FAQ-001`: [公式FAQ](https://attack.mitre.org/resources/faq/)のTactic、Technique、Sub-technique、Procedureの区別。FAQの更新頻度説明は今回のAgile releaseの根拠に使わない。
- `SRC-ATTACK-T1671-001`: 固定bundleの最小metadata。T1671とDetection関連の分類・参照を扱い、攻撃実施や自組織観測を裏付けない。
- `SRC-ATTACK-DET-001`: [Detection Strategies](https://attack.mitre.org/detectionstrategies/)の高位検知方針とAnalyticの関係。自組織のData保有や検知率を保証しない。
- `SRC-ATTACK-DS-001`: [Data Sources](https://attack.mitre.org/datasources/)のv18 deprecation。歴史的な移行説明だけに使用し、現在のDCオブジェクトと混同しない。

第17章のSource参照はDetectionとDataの区別、第25章のv19.1に関する歴史的な文章はBehavior mappingを帰属証拠としない限定命題である。今回の再確認でもこの意味は変わらない。Catalogのcurrent metadataを更新しても、代表章の当時の分析記録や本文をv19.2で再執筆したと主張しない。Registry-wideの一括監査日は更新しない。

SRC-ATTACK-001のurlは随時更新されるVersion Historyであり、このページそのものの公表日時は確定できない。RegistryのpublishedAtはnullとし、関連するrelease公開時刻とUpdates開始日は別の情報として保存する。

## 最小fixtureと再現方法

`tests/fixtures/attack/ch05-v19.2.json`は8 Objectと1つのdetects relationの有限metadataであり、完全なSTIX bundleではない。Procedure descriptions、全Group / Software / Campaign、関連しないLog source一覧は含めない。Raw bundleはGitやPagesへ含めない。

取得済みbundleをWorkspace内の非追跡作業領域へ置いたうえで、次の読み取り専用コマンドで抽出を比較する。ネットワーク取得や外部プラグイン実行は行わない。

```bash
python3 scripts/extract_chapter05_attack_snapshot.py \
  .work/source-input/enterprise-attack.json --check
```

前提は上記SHA-256に一致する公式bundleである。hash不一致、Object欠落、抽出結果不一致では停止する。期待結果は8 Objectの一致であり、ATT&CK全体の完全性ではない。検証後は自分で取得した作業用bundleだけを整理し、追跡済みfixtureを手修正しない。CIではlive bundleを取得せず、fixtureの固定digestと章固有の関係・Status契約を検証する。

## Editorial Input Record

- Package ID: `EIP-0001`
- Package: `white-hat-book-parallel-drafts-2026-08-08.zip`
- Package SHA-256: `caf8c73aa4e84c99f4062ac7cf85ac56794ad2cbb5d8ec5d9403138753eb6388`
- Target: Issue #30 / chapter-05
- Input: `chapter05-attack-behavior.predraft.md`
- Input SHA-256: `11e256480c15771334cc3c9e8eb0933635c305604ba9302482ce627205e1ef12`
- Input確認状況: `not-present-in-authorized-workspace`
- Adopted: raw predraftからの直接採用なし。
- Rewritten: Issue #30の構成・学習目的をcurrent contractとv19.2一次資料から新規に作成。
- Rejected: 草稿の未確認内容を読んだ、hash確認した、採用したという主張。
- Deferred: 実環境のDetection Rule、Control Validation、Chapter 6以降の実装。
- Raw tracked files: `0`

Package不在を推測再構成で埋めない。`canonical-pr-open`のPR IDとIntake Recordは機械可読Manifestと専用Draft PRに記録し、通常merge・main/publication後の別更新まで`consumed`にしない。

## 利用条件

MITRE由来のmetadataの出所、固定commit、変更範囲とライセンスは[Third-Party Notices](../THIRD_PARTY_NOTICES.md)へ記録する。MITREによる本教材の推奨・承認を意味しない。合成Event、Map、判定条件は本書独自の教材であり、MITREの検証結果ではない。
