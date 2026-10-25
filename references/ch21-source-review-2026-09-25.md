# 第21章 Source Review — 2026-09-25（ATT&CK v20再確認 2026-10-26）

## 確認範囲

Control Validationの問い、対象・方法・結果、役割・権限と改善へ用途を限定して確認した。Registry全件、全Control catalogue、全ATT&CK、全法域の再監査ではない。Registry根の基準日2026-07-25、既存notes、CTI pinを保持する。

## SRC-ATTACK-001

2026-10-26に[MITRE/CTI v20.0 release](https://github.com/mitre/cti/releases/tag/ATT%26CK-v20.0)と固定bundleを用途限定再確認した。release公開日、commit、bundle digestを固定し、可変Pageの表示だけで版を決めない。

本章の供給記録はATT&CK 20.0を版付き語彙として使う。第17章のT1098対応は親の方法参照であり、新しいCoverage判定ではない。v19.1 / v19.2の歴史的記録は保持し、今回の確認を全Object・全変更点の監査やControl有効性の証明にしない。移行詳細は[第5章v20 Source Review](ch05-source-review-2026-10-26.md)を参照する。

## SRC-ATTACK-DET-001

[Detection Strategies](https://attack.mitre.org/detectionstrategies/)の導入定義を確認した。上位の検知方針と、それを具体化するPlatform別Analyticsという区別だけに使う。独立したPage版・公表日を特定できないversion / publishedAt nullは保持する。

Strategy掲載、Technique mapping、Control存在、入力取得、検知成功、実有効性を同一視しない。全Strategyや全Analyticsの内容・件数を本章の固定事実にしない。

## SRC-NIST-ASSESS-001

[NIST SP 800-53A Rev.5公表ページ](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final)はJanuary 2022 Final、Document Historyは2022-01-25を示す。[公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53Ar5.pdf)の採用範囲は、印刷pp.11〜12の§2.4、p.25の§3.2.3.1、pp.31〜33の§3.3〜3.4である。

対象・方法・目的と判定条件の接続、必要な根拠に応じた手法選択、期待と実際の差、情報不足、変更後の再評価、評価と組織のリスク判断の分離を参考にした。examine / interview / testは方法であり、Atomic / End-to-Endという本書のScenario typeとは別の軸である。

公表ページのPlanning Noteと[公式Release告知](https://csrc.nist.gov/News/2025/nist-releases-revision-to-sp-800-53-controls)はRelease 5.2.0を2025-08-27としている。これをJanuary 2022 PDFの刊行日や全文改訂日へ置き換えない。追加された個別Control assessment procedureやRelease 5.2.0全catalogueを今回採用・監査したとはしない。

原典のsatisfied / other than satisfiedという結果語彙と、本書の五Resultを区別する。情報不足の扱いを参考にしたのであり、本書の有限比較がNIST適合を認定するものではない。すべての評価対象・組織で同じ判定算法を使うという主張もしない。

## SRC-IR-001

[SP 800-61 Rev.3 Final](https://csrc.nist.gov/pubs/sp/800/61/r3/final)は2025-04-03公開である。[公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf)の印刷p.13のGV.RR-02、pp.19〜20のID.IM-01/02/03を参照した。

役割・責任・権限を明確にすることと、評価・演習・運用から改善を見いだす背景に限定する。本章の供給仮定が実権限を付与したり、実Incidentで得た教訓になったりする根拠にはしない。個別の通知義務や実対応の承認手順を一律に定めない。

## 取得証跡と非目標

2026-09-25 JSTにTLS検証有効のHTTPSで六HTML・二PDFを取得し、すべてHTTP200を確認した。版・Status・採用範囲を公表ページと一次PDFの該当節で確認した。PDFはローカル抽出も併用したが、全733頁のSP800-53Aを精読したとはしない。

| PDF | SHA-256 |
|---|---|
| NIST SP 800-53A Rev.5 | `75665570048b969ad465a4f4f1db425ce505c374951c2c64e462949c6b21be47` |
| NIST SP 800-61 Rev.3 | `e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d` |

Hashは取得Byteの識別であり、署名検証や全節監査ではない。D3FEND、製品固有のEmulation、全Controlの標準適合、実法的判断は今回採用しない。五Result、六Failure、部分充足の二種類、集約優先順、十Scenarioと評価ルーブリックは本書独自である。AI出力や未読の登録草稿を一次資料として扱わない。

## 再確認条件

版・Status・採用節、Control objective、Expected、対象・版・Scope、Authority、入力契約、Retest比較条件が変われば再確認する。実Target・実Data・実操作や個別の法的判断が必要なら本章の範囲外として停止する。Sourceごとの確認日・期限・過去用途はRegistryに残す。
