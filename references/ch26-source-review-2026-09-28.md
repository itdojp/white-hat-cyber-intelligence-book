# 第26章 Source再監査（2026-09-28）

対象は[第26章](../manuscript/26-cti-distribution.md)、ART-08 / ART-09と、独立した有限STIX/TAXII構造例です。確認日は日本時間2026-09-28、取得記録のUTC日は2026-09-27です。Registry全体や、既存章の全主張の再監査ではありません。

## STIX 2.1の固定基準とErrataの段階

`SRC-STIX-001` は[OASISの固定OS](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html)の表題・citationが示す2.1 / OASIS Standard / 2021-06-10を保持します。[latest](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)は2025-04-02のDraft 01 of Errata 01を取り込んだ文書で、citationはCommittee Specification Draft 01です。[版固定のDraft](https://docs.oasis-open.org/cti/stix/v2.1/errata01/csd01/stix-v2.1-errata01-csd01-complete.md)も確認し、Approved Errataとして扱いません。

採用箇所はOSの識別子・共通Property・版管理、Actor / Campaign / Malware / Infrastructure / Observed Data / Indicator / Attack Pattern、Relationship、Domain Name、Bundleに限定します。有限profileは13Object、固定した関係と単一Domain等価Patternだけです。SCOのID算出は一つのASCII値の正規化に限定し、汎用JSON正規化やPattern言語を再実装しません。

SDO/SROの時刻、SCO、BundleのPropertyを混同しないこと、Objectの版とProduct訂正を分けることを確認しました。数値Confidenceを本書の確信度へ暗黙に変換しません。独立の構造例を親Caseの帰属やEvidenceへ昇格しないという制約、合成名・時刻・関係、Productの有限状態は本書の著者設計です。STIXに準拠すれば分析が正しい、という主張ではありません。

## TAXII 2.1とoffline fixture

`SRC-TAXII-001` の[固定OS](https://docs.oasis-open.org/cti/taxii/v2.1/os/taxii-v2.1-os.html)は2.1 / OASIS Standard / 2021-06-10です。[latest](https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html)は取得時に固定OSとbyte同一でした。

Discovery / API Root / Collection、Manifest / Objects / Status、版を含むMedia Typeとenvelopeを確認しました。2.1ではChannels用語が予約されてもサービスは定義されていません。fixtureはCollectionと一回のGETの静的request/responseだけを採用し、DiscoveryやStatus APIの完全実装・適合性を主張しません。

外部TAXIIへ接続せず、HTTP 200やcan_readは供給した架空値です。Objectsの内容とBundle内Object群の対応を検査しますが、信頼、品質、利用許可、実配送の証明ではありません。

## ATT&CKと親Caseの版

`SRC-ATTACK-001` の[公式Versions](https://attack.mitre.org/resources/versions/)はcurrent 19.2、[Updates](https://attack.mitre.org/resources/updates/)はAugust 2026の19.2を示しました。既存RegistryのCommit / Hash / 公開日精度を保持します。Versionsの表示期間とUpdatesの開始日を、そのlive Page自体の公開日に置き換えません。

本章は版付きの挙動語彙という用途だけで、全ObjectやRelationshipの再監査をしていません。古いIssue設計の19.1を現在値として優先せず、親第25章が歴史的な19.1を使った記述は変更しません。ATT&CK対応付けをCoverage、Control効果、Actor帰属の証明にはしません。

## ICD 203

`SRC-ICD203-001` は[公式PDF](https://www.dni.gov/files/documents/ICD/ICD-203.pdf)のweb readerと[Objectivity](https://www.intelligence.gov/mission/our-values/objectivity)を使い、D6.c/d/eの適時性、Source品質、不確実性、情報と仮定・判断、代替説明の分離を限定確認しました。

直接HTTP取得は双方403で、署名画像、正確な新署名日、取得PDF byte hashは未確認です。2015 / 2022 / 2023-06の既存履歴と精度、歴史的な確認基準を保持します。米ICの規範を民間の包括的義務、収集許可、分析の正しさの認証に使いません。

## TLP 2.0

`SRC-TLP-001` は[FIRST公式定義](https://www.first.org/tlp/)が示す現行2.0を採用します。2022年8月以降有効との説明を確認しましたが、同live Page自体の正確な公開日は特定せずpublishedAtはnullです。

採用は共有の境界、AMBER+STRICT、指定より広い共有に必要な明示許可、分類・ライセンス・暗号化との違いに限定します。ラベルや色表を転載した図は作りません。TLP 2.0を古いSTIXのTLP Propertyへ機械的に当てはめる実装、全組織の情報分類規則、保持義務、実操作の許可は対象外です。

## 記録の限界と再確認

公開一次資料のURL、取得応答、byte hashと読解範囲は制作時のlocal証拠へ保存しました。HTMLのbyte hashは規範の真正性や将来の不変性を保証しません。NIST SP800-150は候補としてlandingを探索しましたが、未読本文を採用したとは主張せず、本章のSource mappingに追加しません。

再確認Triggerは正式版・Errata段階の変更、利用Propertyの訂正、ATT&CK版の変更、ICD改訂、TLPラベルや定義の改訂です。個別Sourceだけを更新し、既存notesのprefix、他章の意味、Registry全体の確認日を保持します。合成Caseの7月のProduct時刻と、独立構造例の10月の未来時刻は教材設定で、Source確認日・実観測・実配送ではありません。
