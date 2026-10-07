# 第16章 Source Review（2026-09-21）

## 確認範囲と前提

本文、ART-24、完全合成Caseの外部規範に関する用途を確認した。全規範、全ATT&CK Object、製品実装、法的適格性の監査ではない。既存章のSource notesを保持し、本章の限定した用途だけを追記する。

## ATT&CK

- `SRC-ATTACK-001`: [公式Version History](https://attack.mitre.org/resources/versions/)はcurrent 19.2。ページのApril28表示をminor releaseの公開時刻と推定しない。第5章の既存固定snapshotと版契約は変更しない。
- `SRC-ATTACK-DET-001`: [Detection Strategies](https://attack.mitre.org/detectionstrategies/)の導入説明を確認。上位方針とplatform別Analyticsの整理に限定し、一覧の存在をCoverageやValidationの証明にしない。独立したページ版・公開日は不明のためnullを保持する。

本章では新しいTechniqueやStrategyを割り当てず、親の行動と必要な観測を区別するために用いる。

## Log Management

- `SRC-NIST-LOG-001`: [NIST SP800-92 Final](https://csrc.nist.gov/pubs/sp/800/92/final)、2006-09-13。§3.2 のライフサイクル・正規化・時刻、§4.2 の目的・保持・アクセス・機微情報の取扱い、§5.6 の検査と再評価を限定採用する。
- `SRC-NIST-LOG-DRAFT-001`: [SP800-92 Rev.1 IPD](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd)、2023-10-11、Initial Public Draft。metadataの状態だけを確認し、意見募集終了をFinal化と扱わない。Draft本文は規範として採用しない。

2006年Finalの製品例、古い法令への具体的適用、MD5/SHA-1の推奨、digestを署名と呼ぶ表現は採用しない。本章の七状態、期限、数値、合成receiptは本書の設計であり、NISTの共通Schemaではない。実Event生成や能動試験は必修化しない。

## Incident Responseの利用条件

`SRC-IR-001`: [NIST SP800-61 Rev.3 Final](https://csrc.nist.gov/pubs/sp/800/61/r3/final)、2025-04-03。PR.PS-04 のログ準備、RS.AN-06/07の記録・完全性・来歴・アクセス・保持に限定する。Telemetry Schema、製品構成、通知や実Incident操作、証拠の法的適格性へ一般化しない。

## 取得証跡と再確認条件

当日7公式endpointのHTML/PDFで版・状態を確認し、2つのPDFを取得して上記採用箇所を読解した。

| 資料 | PDF SHA-256 |
|---|---|
| SP800-92 / 72ページ | 466c3ab1580bc3b2e25d11bbd4b2ac92fd1762b3c5b10596924981bc1b9e61e1 |
| SP800-61r3 / 48ページ | e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d |

これは取得したファイルの識別であり、本文全体の採用・適合性証明ではない。ATT&CK release、NIST改版・状態・Errata、採用節の意味、Consumer要件が変わった場合に本文・Template・Case・fixtureを再確認する。旧章の判断時点やSource確認範囲は遡及変更しない。

OpenTelemetryは探索したが今回は採用しない。製品・形式への依存なしに、完全合成の読解課題を完了できるようにする。
