# 第24章 Source再監査（2026-09-27）

対象は[第24章](../manuscript/24-osint-provenance-sources.md)とART-30だけです。既存第10・20・23・25章の確認日を、新章の確認へ自動転用しません。以下は日本時間2026-09-27の用途限定再確認で、Registry全体の再監査ではありません。

## Berkeley Protocol

`SRC-BERKELEY-001`について、[共同発行者の公式project](https://humanrights.berkeley.edu/projects/developing-the-berkeley-protocol-on-digital-open-source-investigations/)から[publication](https://humanrights.berkeley.edu/publications/berkeley-protocol-on-digital-open-source-investigations/)と、そのDownload Reportが指す[2022 PDF](https://humanrights.berkeley.edu/wp-content/uploads/archive/2024/02/Berkeley-Protocol.pdf)を確認しました。102頁の表題・版権頁は2022です。publication頁の2020-12-02を2022 editionの正確な刊行日に置換せず、RegistryのpublishedAt nullを保持します。

採用はVI.B147〜152の関連性と事前検討、VI.C154〜155の原形式・変換・取得文脈、VI.D167〜169の来歴・作業Copy、VI.E176〜178・187・192〜194のSource/Item/Contentと文脈・循環・検証、VI.F196〜197の処理記録に限定します。印刷頁では57〜65です。本書の五用途、三軸の有限区分、Hash算法、合成Claimの関係は著者設計で、Protocolの正式採点規則ではありません。

資料は人権・国際刑事・人道法違反調査を背景とします。民間企業の包括的収集権限、普遍的義務、法的証拠能力、実世界の真正性を認定する規範として引用しません。個人の特定、地理特定、捜査、第三者への収集操作は本章に採用せず、表や手順の全文も転載しません。

OHCHRの登録landingはHTTP403でした。アクセス制限を回避せず、共同発行者の公式PDFをHTTP200で取得した範囲だけを採用します。取得はUTC 2026-09-27、byte hashと応答記録は制作時のlocal証拠へ保存しました。初回のPDF抽出はpdftotext未設置で失敗し、既設pypdfで再抽出しました。Repositoryの依存やformatter pinは変更していません。

## ICD 203

`SRC-ICD203-001`は[公式PDF](https://www.dni.gov/files/documents/ICD/ICD-203.pdf)のweb reader抽出本文で、D6e(1)〜(3)のSource品質、不確実性、情報と仮定・判断の分離を再確認しました。[公式Objectivity](https://www.intelligence.gov/mission/our-values/objectivity)の2023年6月の改訂・再承認も確認しました。

直接取得はHTTP403で、取得PDF byte hash、署名画像、正確な新署名日は未確認です。Registryの2015/2022/2023-06の履歴と精度を保持します。米国ICの分析規範を民間の収集許可へ転用せず、ICD206の引用実装や語彙規定の全体監査は行いません。

## 採用しない内容と再評価

CIAのStructured Analytic Techniquesは既存第25章へのBRIDGEだけで、新規Source mappingや再監査済み主張を追加しません。OSINT Strategy、CAI Policy、Archive製品固有仕様も、この章に用途がないため新規採用しません。Issue登録時の候補IDを現Registryへ重複追加しません。

二Sourceの第24章用途notesと必要な個別確認日だけを追記し、既存版、過去notes、次回期限、他章mapping、Registry全体の確認日は保持します。一次資料の改訂、採用箇所の訂正、利用範囲の変更時に再評価します。合成資料の未来時刻は教材設定であり、実収集日・実観測・本Sourceの確認日ではありません。
