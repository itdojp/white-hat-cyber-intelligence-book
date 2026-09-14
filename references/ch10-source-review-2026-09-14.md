# 第10章 Source Review Note：ReconとOSINTの境界

## 確認範囲と日付

Checked at: **2026-09-14**。第10章、ART-19、合成Caseで実際に用いた主張だけを確認しました。資料全体への適合、法的判断、実対象の収集、Sourceの真正性を保証しません。既存章の歴史的な引用やRegistry全体の監査日を置き換えません。

一次資料を公式Publisherから取得し、本文の該当箇所、版、Status、関係するErrataを読みました。Raw Editorial Inputは認可workspaceに不在です。登録概要は設計来歴として用いますが、原文読了・実体Hash検証・直接採用は主張しません。原稿はIssue #35、現行契約、以下の一次資料から構成しています。

## SRC-BERKELEY-001 — Berkeley Protocol

- 版: **2022 edition**。共同発行者の[公式Project](https://humanrights.berkeley.edu/projects/developing-the-berkeley-protocol-on-digital-open-source-investigations/)と[公式PDF](https://humanrights.berkeley.edu/wp-content/uploads/archive/2024/02/Berkeley-Protocol.pdf)を確認。
- 実取得PDF: 102頁、SHA-256 `caa5ea4806545658e0cfd21ed5d21c0250922903eece89bf58d26756dac3a0ae`。
- 限定採用: III39–41の法的枠組みの文脈依存、VI.C155(g/h)の取得時点・Hash、VI.D167–169の取扱いと原本/作業コピー、VI.E176のSource・item・contentの評価。
- 採用しない内容: 実在人物を調査する手順、機微情報の集約、実際の収集環境や法的証拠能力の認定。本章では合成要約の最小Fieldと限界に置き換えます。
- 日付: PDFは2022年版で奥付はMarch2022。公開日は日まで特定できないためRegistryのpublishedAtはnull。Projectの2020年発表日を2022版の公開日へ流用しません。

人権・国際刑事調査のための文脈を、企業CTIの普遍的な法的義務へ拡張しません。Hash対象を明示するという本章の設計は、Hashから真正性や実施許可が導かれるという意味ではありません。

## SRC-WSTG-001 — WSTG Information Gathering

[公式Project](https://owasp.org/www-project-web-security-testing-guide/)はstable **4.2**、5.0をdevelopmentとしています。4.2のReleaseは2020-12-03です。[Versioned Information Gathering](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/README)の分類目次を確認しました。

本章は情報収集を評価の問いへ結ぶ分類の参考に限定します。掲載Techniqueの実行許可、網羅性、ツール操作手順は採用しません。Registryの既存版・過去章のnotesを保持し、第10章の用途と今回のcheckedAtを追加します。

## SRC-CT-001 — RFC9162

[公式本文](https://www.rfc-editor.org/rfc/rfc9162.html)と[Status / 更新関係](https://www.rfc-editor.org/info/rfc9162/)を確認。**December2021 / Experimental**、RFC6962をobsoletesします。日まで分からない発行日はnullとします。

採用範囲は§3.2/§3.2.1のCertificate / Precertificateと発行意図の区別だけです。最終Certificateが発行されない場合もあることから、CT metadataだけで現在の所有・稼働・実行許可を確定しないのは本章の分析上の制限です。ブラウザの実採用版、CT API、Logの網羅性、Merkle proofの実装を監査したわけではありません。

[Errata](https://www.rfc-editor.org/errata/rfc9162)は8670 **Held for Document Update**、Editorial、§2.1.3.2/§2.1.4.2のループ記述に関するものです。採用する発行意図の主張とは別で、Verifiedと記載しません。

## SRC-SECURITYTXT-001 — RFC9116

[公式本文](https://www.rfc-editor.org/rfc/rfc9116.html)と[Status](https://www.rfc-editor.org/info/rfc9116/)を確認。**April2022 / Informational**。§5.2のRedirect、§5.3のStale情報も確認し、本文への直接採用は§5.5のTesting permissionとの分離に限定します。

[Errata](https://www.rfc-editor.org/errata/rfc9116)の現在の記録は、6946 **Verified**（Editorial、§4の参照節訂正）、7264 **Reported**（Technical、時刻のZ/z）、7743 **Reported**（Technical、改行文法）です。Reportedを確定済みの仕様変更として扱いません。これらは本章が採用する§5.5の意味を変更する内容ではありません。security.txt Parserや署名の検証は実装しません。

## SRC-DNS-TERM-001 — RFC9499

[公式本文](https://www.rfc-editor.org/rfc/rfc9499.html)と[Status / 更新関係](https://www.rfc-editor.org/info/rfc9499/)を確認。**March2024 / Best Current Practice / BCP219**、RFC8499をobsoletesしRFC2308をupdatesします。

採用は§5のRR **OwnerがRRのあるDomain名を指す**という用語だけです。これを法人の所有者やAssetのOwner confirmedと同一視しません。数値上限を含むTTL実装の説明は本Sourceから採用しません。TTLの本章の主張は次のRFC8767で限定します。

[Errata](https://www.rfc-editor.org/errata/rfc9499)は8189 **Rejected**（Editorial、用語の配列に関する報告）で、Ownerの意味を変更する根拠として扱いません。

## SRC-DNS-STALE-001 — RFC8767

[公式本文](https://www.rfc-editor.org/rfc/rfc8767.html)と[Status / 更新関係](https://www.rfc-editor.org/info/rfc8767/)を確認。**March2020 / Standards Track**、RFC1034/1035/2181をupdatesします。

採用は§4のserve-staleとTTLに関する限定説明です。期限の経過や正のTTLだけで現在性を確定しないという分析上の制限へ用います。Resolver設定、全DNS仕様、実際のCache挙動の測定や推奨値は扱いません。[Errata検索](https://www.rfc-editor.org/errata/rfc8767)は確認日時点で該当記録0でした。将来も存在しないという意味ではありません。

## 再確認と採用しなかった資料

新規四RFCは月までの発行情報しか確認できないためpublishedAtをnullとし、notesに理由を記録します。今回確認したinfoページに後続のUpdated by / Obsoleted byは見当たりませんでしたが、2026-09-14時点の観測であり将来の状態を保証しません。

Berkeleyと固定RFCは次回確認を2027-09-14、継続更新されるWSTGは2026-12-14とします。それ以前でも新版・Status・Errata・採用主張の変更があれば再確認します。Registry全体のcheckedAtは2026-07-25のままです。

RFC1034の全更新史を監査したとは主張しません。採用するOwner語彙はRFC9499、TTL/serve-staleの限定主張はRFC8767から確認できるため、RFC1034の未使用の広い引用は追加しません。ODNIの旧Strategyは後継状態が分からないため任意のContextual Sourceとして保留し、「後継なし」やcurrentと推定しません。

## 成果物への対応

[第10章](../manuscript/10-recon-osint-boundary.md)、[ART-19](../templates/attack-surface-register.md)、[完全合成Case](../cases/ch10-attack-surface-example.md)は、Sourceの意味を教材の限定した判断に用います。実Targetの照会、Credential、実人物の情報集約、法的認定、実測を教材へ導入しません。
