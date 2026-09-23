# 第19章 Source Review — 2026-09-23

## 確認範囲

第19章のCSFへの接続、宣言、分類・優先度、Evidence記録、通知照会、復旧検証に限定して一次資料を確認した。Registry全件、個別法域、全製品の再監査ではない。根の監査基準日2026-07-25と過去のnotesを保持し、二Sourceへ用途を追記する。

## SRC-CSF-001

[NIST CSF 2.0の公表ページ](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20)で2024-02-26の文書を確認した。[Final PDF](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)の印刷p.5では六Functionを同時並行で扱う考え方が示される。本章では上位Outcomeへの対応付けとして用い、七状態や特定製品の実装、有効性、認証の根拠にはしない。

## SRC-IR-001

[SP 800-61 Rev.3 Final](https://csrc.nist.gov/pubs/sp/800/61/r3/final)は2025-04-03公開、Rev.2を置き換える。[Final PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf)の採用箇所は以下のとおり。ページはPDFビューアの番号ではなく印刷番号である。

| 箇所 | 採用する概念 | 採用しない主張 |
|---|---|---|
| pp.1–2 | リスク管理全体へのIR接続、EventとIncidentの区別 | 全組織に同じ状態機械を強制 |
| DE.AE-08 / p.26 | 定義した基準に対する宣言 | Huntの支持だけで宣言 |
| RS.MA-02〜05 / pp.27–28 | 報告の確認、分類・優先度、復旧開始基準 | 教材による実対応や実受領 |
| RS.AN-06 / 07 / p.29 | 記録とDataの来歴・保持 | Hashによる真正性や法的適格性 |
| RS.CO-02 / 03 / pp.30–31 | 関係者との調整と情報共有 | 個別通知の要否・期限の自動判断 |
| RS.MI-01 / 02 / pp.32–33 | 封じ込めと根絶の区別 | 実操作や製品コマンドの許可 |
| RC.RP-01〜06 / p.34 | 復旧、検証、終結の基準 | 復旧と全改善完了の同一視 |

ART-25、七状態、十二対比、有限検査の遷移・Gap・時刻表現は本書独自である。Sourceに掲載された標準算法と偽って引用しない。法的通知は第2章の責任境界へ戻し、個別法令の解釈を本章で追加していない。

## 取得証跡と制限

2026-09-23に公式HTML二応答とPDF二応答をTLS検証有効のHTTPSで取得し、最終応答はすべて200であった。取得時刻・応答Hashは制作時のローカル証跡に保持する。

- IR PDF SHA-256: `e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d`
- CSF PDF SHA-256: `3c31f46fee98cac0c4323453e5109291a213b4de7fef8c058af9bf67f717433c`

Hashは取得Byteの識別であり、署名検証でも全節監査でもない。ローカルPDF抽出器は未導入のため抽出に失敗し、一次PDFのWeb表示で該当箇所を読解した。未読の先行草稿やAI出力をSourceとして扱っていない。

## 再確認条件

NISTの版・Status・採用節、章のScope・状態契約・通知や復旧の用途が変わったら再確認する。個別法域・実Data・実操作が必要になった場合は本教材の範囲外として停止する。各Sourceの次回期限はRegistryを参照する。
