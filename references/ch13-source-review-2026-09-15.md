# 第13章 Source Review Note：PlatformとSupply Chain

## 確認範囲

確認日は2026-09-15です。[第13章](../manuscript/13-platform-supply-chain.md)とART-21の採用主張だけを一次資料へ照合しました。全規範、Provider、実Package、標準適合を監査したとは主張しません。AI生成物や非正本草稿を出典にしません。

## SSDF

`SRC-NIST-SSDF-001`は[NIST SP 800-218 / SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)です。Date PublishedはFebruary 2022、Document Historyは2022-02-03 Finalです。公開月と履歴上の日付を区別し、厳密な公開日は未確定としてRegistryのpublishedAtをnullにします。

[一次本文](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf)のPS.1.1、PS.2.1、PS.3.1/3.2、PW.4.4を限定確認しました。採用するのは最小権限、release完全性の情報、出所記録、第三者Componentの継続的評価を分ける考え方です。例示される操作を本章の実行手順にはしません。

[Rev.1 / SSDF 1.2](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd)は2025-12-17 Initial Public Draftで、コメント期間は終了しています。Finalとして採用しません。公式の[potential updates表](https://csrc.nist.gov/files/pubs/sp/800/218/final/docs/sp800-218-potential-updates.xlsx)はXML cellとして読み、p.iii謝辞の社名綴り訂正候補1件を確認しました。新しい技術要件や正式改訂として扱いません。

## SLSA

`SRC-SLSA-001`は[SLSA 1.2](https://slsa.dev/spec/v1.2/) Approvedです。[公式release発表](https://slsa.dev/blog/2025/11/announce-slsa-v1.2)の日付は2025-11-24です。これは公開発表日であり、承認決議日を独立確認したものではありません。1.1はRetiredで、過去設計コメントの「1.1 current」は再採用しません。

採用範囲は[Tracks](https://slsa.dev/spec/v1.2/tracks)、[Build Track Basics](https://slsa.dev/spec/v1.2/build-track-basics)、[Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)の手順1/2と前提です。SourceとBuildの保証対象、対象Digest、署名の検証と期待するBuilder、Source、buildType、externalParametersを分けます。Build platform自体の侵害はBuild L3の保証範囲外という限定を維持します。

教材のexpectationsは別の供給記録として固定した比較条件で、実際のroot of trustではありません。五状態や閉Schemaは本書独自で、実SLSA level判定、標準Attestation parser、署名検証器を実装しません。未知externalParametersの拒否と任意拡張Fieldの互換性を一律に扱いません。

## Container

`SRC-NIST-CONTAINER-001`は[NIST SP 800-190](https://csrc.nist.gov/pubs/sp/800/190/final)です。Date PublishedはSeptember 2017、Document Historyは2017-09-25 Finalです。既存の第8章Source identityと利用範囲を変更しません。

[一次本文](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-190.pdf)の§3.5.2、§4.1.4を限定確認しました。共有KernelとSecretの境界に関する歴史的原則だけを採用し、現行製品、具体的設定、隔離成功を保証しません。本Noteが第13章の追加利用範囲を記録します。

## SPDX

`SRC-SPDX-001`は[公式仕様一覧](https://spdx.dev/use/specifications/)のCurrent Version 3.0と、そこから参照できる[版別HTML 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/)です。一覧のminor表記と版別patch表記を区別します。厳密な公開日は分からないためpublishedAtはnullとします。

採用するのは仕様の所在と版の確認だけです。全SPDXモデル、Schema、JSON-LDを読了・実装したとは主張しません。供給するSBOM summaryは本書独自形式で、SPDX適合文書でも完全なComponent inventoryでもありません。

## 取得証跡と制限

公式HTMLは取得byte、HTTP status、SHA-256、response Dateをローカル証跡へ保存しました。HTTP取得時刻と資料公開日を区別します。公式PDFはweb readerで上記節を確認しました。ローカルPDF取得はHTTP403となったため、全PDFのローカルhash監査や完全保存を主張しません。

外部Source URLは資料の参照先であって演習Targetではありません。実Cloud、CI、Registry、Token、実Packageへ接続して評価したものではありません。署名、Trust、Compliance、Safety、許可は別の問いとして保持します。

## 再確認条件

SSDFのFinal化・改訂・更新候補、SLSAの版・status・検証前提、SPDXの版や所在、NIST Containerの改訂・廃止・利用範囲変更で再確認します。次回期限はSSDF/SLSA/SPDXが2026-12-15、Containerが2027-09-15です。Registry全体の基準日は進めず、今回確認した項目だけを更新します。読者影響をCHANGELOGへ記録します。
