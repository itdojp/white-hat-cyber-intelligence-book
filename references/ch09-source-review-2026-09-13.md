# 第9章 Source Review Note：EngagementとRoE

## 監査範囲

2026-09-13に第9章で実使用する4件の一次Sourceを再確認しました。Sourceは計画上の検討材料であり、個別の実施許可、法的助言、現行製品の安全な操作手順を代替しません。Registry全体の監査日や、既存章の歴史的監査記録は更新しません。

本章の8状態、直接ID、数値上限、完全合成Object、非実行の計画検査は本書の教育設計です。NIST・OWASP・法令・IPAがこのモデルを定めた、承認した、または実証したとは主張しません。

## SRC-NIST-TEST-001

[NIST SP 800-115公式ページ](https://csrc.nist.gov/pubs/sp/800/115/final)と[公式PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf)を取得しました。Final / September 2008、Document Historyは09/30/08です。発行月の表示と履歴日の属性は異なるため、日まで特定したpublishedAtは設定しません。

- 確認箇所: §6.5 Assessment Plan、§6.6 Legal Considerations、Appendix B Rules of Engagement Template（本文の6-10〜6-12、B-1〜B-3等）。
- 採用範囲: 目的、範囲、制約、関係者、連絡、Data取扱い、停止/再開、報告、承認を事前に記録する計画観点。
- 非採用: 古い攻撃Techniqueや監視抑止の例を標準許可へ取り込みません。現在のCloud/Identity製品レシピ、包括的なModern testing standard、法的承認として扱いません。
- 取得Evidence: PDF80頁、544,047 bytes、SHA256 `58e5ed41e5c8ca34ce14fd80b70f118f2c6d613d1647bc307edca30bcc45f063`。全文の引用ではなく該当箇所の限定的な要約です。
- 次回: 2027-09-13、または改訂・撤回・置換・Source用途変更を検知した時点。

## SRC-WSTG-001

[OWASP WSTG project](https://owasp.org/www-project-web-security-testing-guide/)と[version 4.2 Introduction](https://owasp.org/www-project-web-security-testing-guide/v42/2-Introduction/)を確認しました。公式公開先へのredirect後も内容を取得しています。stableは4.2、5.0は開発中です。4.2のRelease表示は2020-12-03です。

要求、評価、Evidence、報告の語彙を第11章へ接続する補助に限定します。全項目を実施することやTool使用をRoEの許可と同一視しません。version指定を維持し、mutableなstable/latestだけに根拠を置きません。古い一般的な推奨を新しい安全基準として移植しません。

Registryの既存version `4.2; 5.0 under development`を保持します。次回確認は2026-12-13、または新しい安定版・参照先変更・適用範囲変更時です。

## SRC-JP-LAW-001

[e-Gov不正アクセス行為の禁止等に関する法律](https://laws.e-gov.go.jp/law/411AC0000000128)を確認しました。ページ本体はJavaScript shellのため、それだけで法文を確認したとは扱いません。公式の[law-data v2](https://laws.e-gov.go.jp/api/2/law_data/411AC0000000128)と公開画面の改正表示APIも取得し、現行表示と第2条の定義・第3条の禁止規定を読みました。

- 現行表示: revision `411AC0000000128_20250601_504AC0000000068`、CurrentEnforced、2025-06-01施行。公開画面の改正表示も同じ施行日を現行として返しました。
- law-data JSONのSHA256: `ace9e9b644770d4aac03f690765614ab3cca90ea8e2ca85a759adb585027189b`。
- 既存version `current display effective 2025-06-01`は変更しません。原制定の公布日を現行条文の発行日と混同しません。
- 確認対象は一般的な用語・禁止の境界であり、Caseに対する法的適用や、書面があれば必ず適法という判断ではありません。個別の権限・契約・第三者条件は未確認のまま扱います。

旧APIの取得失敗は法文の確認証拠に含めません。次回は2026-12-13、または改正・施行・管轄・契約/利用条件・適用範囲の変更時です。

## SRC-IPA-VDP-001

[IPA公式ページ](https://www.ipa.go.jp/security/guide/vuln/partnership_guide.html)と[2024年版PDF](https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/partnership_guideline.pdf)を取得しました。版は2024年版、ページ更新日は2026-04-06です。版の更新案内2024-06-18と現在のページ更新日を混同しません。

- 確認箇所: 役割と情報取扱い、製品の発見者向けIIIの1(2)〜(4)等（本文8頁付近）。
- 採用範囲: 予期しない情報を得た場合の取扱い、届出・調整・公表の役割を分けるための補助。製品とWebサイトの手続きを無条件に同一視しません。
- 非採用: このGuidelineを個別の検査許可、公表の許可、特定の法的免責と見なしません。
- 取得Evidence: PDF61頁、1,221,433 bytes、SHA256 `98ec2ed52e14a2065c4a4befd154be2627d47fb08d4ed290b93d20438183e458`。
- 次回: 2026-12-13、または版・届出/調整・法令・適用範囲変更時。

## 編集判断と残る限界

第2章の期限経過した`AUTH-CASE-2026-001`を新しいSource確認日で更新しません。第4章のNeeds Evidence、第8章の非実行Lab、第11章の独立Caseを維持します。Sourceの確認、計画の完全性、実施承認、実測Evidence、法的判断は別の主張です。

登録済みEditorial Inputは2候補を比較してBを設計来歴として選択しましたが、両raw Packageはworkspaceにありません。本文読了・実体hash照合・rawからの直接採用は主張せず、Issueと現行契約、上記の実取得した一次資料から新規作成しました。未選択候補は品質不良と断定せず、原文比較を保留しています。

[第9章](../manuscript/09-engagement-roe.md) / [Source Registry](reference-baseline.md)
