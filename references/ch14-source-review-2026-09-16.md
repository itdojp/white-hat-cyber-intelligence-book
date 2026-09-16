# 第14章 Source Review Note：最小影響の判断と停止

## 確認範囲

確認日は2026-09-16です。第14章のMethod選択、事前計画、Evidence分析、停止・データ取扱い、Findingへの接続を説明するため、以下の範囲だけを再確認しました。Sourceは個別環境の実施許可ではなく、本書の六Result・四Method・数値上限・合成記録を規定していません。

## NIST SP 800-115

`SRC-NIST-TEST-001`。[公式Finalページ](https://csrc.nist.gov/pubs/sp/800/115/final)と[80ページPDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf)を確認しました。採用は§6.5の計画と承認、§7.2の実施中調整と停止、§7.3の分析、§7.4導入のデータ取扱い、§8.1〜8.2の緩和策と報告への接続です。既存第9章の§6.5〜6.6/Appendix Bの採用記録は保持します。

Date PublishedはSeptember 2008、Document Historyの2008-09-30 Finalは別の属性です。厳密な公開日は確認できないためRegistryのpublishedAtはnullを維持します。取得PDFのSHA-256は`58e5ed41e5c8ca34ce14fd80b70f118f2c6d613d1647bc307edca30bcc45f063`で、第9章の取得記録と一致しました。hash一致は資料の内容や主張全体を再監査した意味ではありません。

古い攻撃・秘匿例、製品手順、§7.4.4の当時の媒体消去分類を現在の運用手順として採用しません。実Dataの保存・廃棄を本章の合成Cleanup値で保証せず、組織の計画と現行規範へ戻します。ローカルPDF変換ツールは未導入のため、限定採用節の本文は公式PDFのweb readerで確認しました。

## OWASP WSTG

`SRC-WSTG-001`。[公式Project](https://owasp.org/www-project-web-security-testing-guide/)は4.2の版別提供、5.0開発中、4.3 Unreleasedを区別しています。既存の4.2公開日2020-12-03と採用版を保持します。

採用箇所は[versioned 4.2 Introduction](https://owasp.org/www-project-web-security-testing-guide/v42/2-Introduction/)のWhat is Testing、How To Reference WSTG Scenarios / Linking、The Need for a Balanced Approachです。基準との比較、版を含む参照、単一手法へ依存しない考え方を補助とし、個別脆弱性の手順や全Scenarioは採用しません。今回の供給応答比較は実HTTP試験ではありません。

既存第9〜11章のSource記録を保持し、第14章の利用箇所だけをRegistry notesへ追記しました。以前からある第15章mappingを今回の再監査済みという意味にしません。

## 本教材の判断と非採用範囲

六Result、四Method、二つの比較条件、八記録、Not performedの独立欄、供給記録上の停止優先とCleanup/Residualによる完了条件は、Issue #38と本書契約に基づく教育用の有限設計です。NIST/OWASPへの準拠判定や実システムの状態保証ではありません。

非正本の登録コメントにあったNIST SP 800-53Aは本章では採用しません。新しいSource IDや未確認の主張を追加せず、必要な二Sourceへ範囲を限定します。実Target、実Credential、外部通信、実Build/Deploy/署名検証は行っていません。

Registry-wide baselineは2026-07-25のままです。個別のcheckedAtは2026-09-16、nextReviewAtはNISTが2027-09-16、WSTGが2026-12-16です。版・Status・採用節・停止や許可境界が変わった場合は、本文・Template・Case・fixture・contractを一緒に再監査します。
