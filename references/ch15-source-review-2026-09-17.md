# 第15章 Source Review — 2026-09-17

確認日: 2026-09-17。対象はFindingの構造、Retestの参照、Severityと組織判断、情報取扱いの限定範囲である。全規範・法令・実製品の適合監査ではない。Registry-wide baselineは2026-07-25を維持し、三つの個別Sourceの採用scopeだけを再確認する。

## SRC-IPA-VDP-001：役割と調整

[IPA公式ページ](https://www.ipa.go.jp/security/guide/vuln/partnership_guide.html)は2024年版を案内し、ページ最終更新は2026-04-06である。[公式PDF](https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/partnership_guideline.pdf)の2024年版・全61ページを取得し、SHA256は`98ec2ed52e14a2065c4a4befd154be2627d47fb08d4ed290b93d20438183e458`で、前回の第9章監査と一致した。

今回読む範囲はⅠの枠組み・関係者の役割と、Ⅱの情報・対策・対応状況の定義である。Findingの状態とは別にAudienceと調整状況を記録する補助として使用する。届出手順の実行、実際の公表時期の判断、法的責任の認定、全付録の再監査には使用しない。

ページの更新日、2024年版の案内日、PDFの版を区別する。RegistryのpublishedAtは従来どおりnullとし、今回の限定確認で文書全体の公開日を上書きしない。次回確認2026-12-17、改訂または開示章の公開時に再確認する。第2章・第9章の既存利用記録は保持する。

## SRC-WSTG-001：固定4.2のReporting

[OWASP公式Project](https://owasp.org/www-project-web-security-testing-guide/)のStable 4.2と開発版を区別する。本章は[公式Repositoryの4.2固定commitにあるReporting](https://github.com/OWASP/wstg/blob/dd33419e10edb22b78d89325a6c2aad9f184e3a2/document/5-Reporting/README.md)を参照する。tag v4.2からcommit `dd33419e10edb22b78d89325a6c2aad9f184e3a2`へ対応し、取得本文のGit blobは`9e2131fb657f555acc48f55785da2b50a4a4feda`、SHA256は`ac4c37f76f1d4ef1aab5d67636cef856a8cfecb0c482cbb73238ef0269fdba12`である。署名検証済みのtagとは主張しない。

採用範囲はAbout this Section、1.4 Scope、1.5 Limitations、2 Executive Summary、3 Findingsの前回結果との参照と3.2の報告項目である。一つの報告形式の提案を、固定必須標準として扱わない。実機微情報の取得、個別悪用手順、免責文の転載、外部参考リンク群の採用は範囲外である。

公式Webの旧Reporting routeは前回404だったため、取得可能な固定Sourceを使う。Web routeの復旧を確認したという意味ではない。第9・10・14章の既存notesと採用範囲を全文保持し、今回のReporting scopeを追記する。次回確認2026-12-17、Stableまたは開発版のreleaseと参照先変更を契機に再確認する。

## SRC-CVSS-001：Severityと判断の分離

[FIRST Specification](https://www.first.org/cvss/v4.0/specification-document)と[User Guide](https://www.first.org/cvss/v4.0/user-guide)で、標準4.0と両文書版1.2を確認した。採用する意味はSpecificationの冒頭・Introductionの四Metric groups、ScoreとVector、組織のRisk判断にはCVSS範囲外の要因も必要という限定範囲である。User Guideは文書版を確認し、全Scoring rubricを再監査したとは主張しない。

第7章の既存Source契約と供給比較例を保持する。本章では新たなScore・Vectorを付けず、実CVEの評価をOAuth Appへ転用しない。Calculatorの更新、CWEの新規採用、実脆弱性のrating、全仕様適合の確認は行わない。publishedAtは文書改訂の正確な日付を推定せずnullを保持する。次回確認2026-12-17、版・採用意味の変更時に再確認する。

## 本書独自の契約と非採用範囲

六Finding Status、五Retest Result、二条件の比較優先順、供給Acceptanceの有効性判定は本書独自の有限教材であり、上記Sourceの規定をそのまま実装したものではない。NIST SP800-53A・800-39・CSF、CWEは登録済み先行草稿で名前が挙がっても、本章では新規採用しない。

実Target、実Credential、実Account、実変更、実Retest、実届出、実公表は行わない。権限・法的判断・Disclosureの個別判断が必要になったら、教材の外で責任者と専門家へ確認する。
