# 第18章 Source Review — 2026-09-22

## 確認範囲

第18章の仮説語彙、Detection Strategyの役割、Incident評価への接続を、以下の一次資料に限定して確認した。Source Registry全件の再監査ではない。根の監査基準日2026-07-25は変更せず、三Sourceの確認日と第18章mappingを更新する。

## SRC-ATTACK-001

[Version History](https://attack.mitre.org/resources/versions/)のcurrentは19.2。[Updates](https://attack.mitre.org/resources/updates/)の更新説明も確認した。Version Historyの2026-04-28という系列開始表示と、19.2の更新日表示は区別する。過去Issue設計の19.1を現在版として引用しない。

採用するのは、行動の共通語彙を版付きで利用するという範囲だけである。全Technique、Platform、CTI objectの完全監査、Actor attribution、手元のCoverageや検証成功の証明は行っていない。親第17章の版付き記録を本章の新規入力で書き換えない。

## SRC-ATTACK-DET-001

[Detection Strategies](https://attack.mitre.org/detectionstrategies/)の冒頭説明を確認し、Strategyを複数のAnalyticsをまとめる上位方針として扱う。単一製品の実行可能Query、Data sourceの取得完了、すべてのPlatformでの同等な観測可能性を意味しない。

本章の五Result、30分のPivot、有限Query契約は教育用設計であり、MITREの標準算法ではない。実装済みのDetectionや攻撃再現手順として掲載しない。

## SRC-IR-001

[NIST SP 800-61 Rev.3 Final](https://csrc.nist.gov/pubs/sp/800/61/r3/final)は2025-04-03公開で、Rev.2を置き換える。参照した[Final PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf)の印刷ページ番号は次のとおりである。

| 採用箇所 | 本章で使うこと | 使わないこと |
|---|---|---|
| DE.AE-08 / p.26 | Incident宣言には定義した基準との比較が必要 | Supportedからの自動宣言 |
| RS.MA-02 / p.27 | 報告のTriageとValidationを分ける | 本教材が実Incidentを受領・処理したという主張 |
| RS.AN-06 / RS.AN-07 / p.29 | 調査記録の完全性・来歴、収集と保持を意識する | 合成Digestによる真正性や法的適格性の認定 |

五ResultやQuery算法の規範、法的助言、全IR工程の実装仕様としては利用しない。

## 取得証跡と制限

確認日2026-09-22。公式HTML四応答とPDFをHTTPSで取得し、最終応答はすべて200であった。初回の一部取得は403となり、監査用User-Agentを明示した通常HTTPS取得で再確認した。TLS検証の無効化や制限回避は行っていない。

PDFのSHA-256は`e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d`。これは取得したByteの識別であり、本文全節の監査や電子署名検証を意味しない。HTMLの応答HashとUTC取得時刻は制作時のローカル監査証跡に保持し、変動するWeb内容の永続性を保証しない。

## 再確認条件

ATT&CK版、Strategy構造、NIST文書Status・採用節、本章の対象範囲・判断契約が変わったときに再確認する。次回期限は各Source Registryを参照する。新しい一次資料を採用する場合は用途と非採用範囲を追加し、AI出力や未読の先行草稿を根拠にしない。
