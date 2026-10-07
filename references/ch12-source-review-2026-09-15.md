# 第12章 Source Review Note：Identityとアクセス経路

## 確認範囲と日付

Checked at: **2026-09-15**。Issue #36 / ART-20の採用主張を、公式出版記録と以下の限定本文で再確認しました。開始mainは`f49455264dd6968fd3fd795ed645211d79950bc7`です。Sourceの全規範、実製品、適合性、法的許可の監査ではありません。

SP 800-63-4とA/B/Cの各CSRCページのDocument Historyは、いずれも **2025-07-31 Final** です。旧Draftの履歴やHTML生成時刻をFinalの公表日へ代用しません。四Principal、六Path state、三Method、必要Edgeの有限比較は、本書独自の教育契約です。

## SRC-NIST-DIGITAL-001 — SP 800-63-4

[公式出版記録](https://csrc.nist.gov/pubs/sp/800/63/4/final)と[公式本文](https://pages.nist.gov/800-63-4/sp800-63.html)を確認しました。採用はScope and Applicability、Assurance Levelsの限定説明です。

IAL / AAL / FALは別の過程に対するAssuranceです。自然人を中心とする範囲を確認し、機械間認証、IoT、主体に代わるAPI利用を包括的に規定する資料として扱いません。四分類の全PrincipalへAAL等を一律に割り当てる使い方は不採用です。

## SRC-NIST-PROOFING-001 — SP 800-63A-4

[公式出版記録](https://csrc.nist.gov/pubs/sp/800/63/a/4/final)と[公式本文](https://pages.nist.gov/800-63-4/sp800-63a.html)のIntroductionを確認しました。採用はIdentity proofingの目的と自然人の範囲だけです。

本Caseの合成名は本人確認Evidenceではなく、IAL適合を主張しません。本人確認書類の取得、実在人物の確認、Enrollmentの実装手順は採用しません。

## SRC-NIST-AUTHN-001 — SP 800-63B-4

[公式出版記録](https://csrc.nist.gov/pubs/sp/800/63/b/4/final)と[公式本文](https://pages.nist.gov/800-63-4/sp800-63b.html)の§2、§3.2.5を確認しました。AAL、MFA、phishing resistanceを区別する範囲に限定します。

AAL2における耐性を持つ選択肢の提供と、AAL3における耐性の要求を区別します。手入力OTP等をphishing-resistantと扱いません。MFAのフラグから認可の正しさや経路の不存在を導かないのは本章の分析上の制限です。Authenticator実装、鍵管理、全AAL要件への適合監査は行っていません。

## SRC-NIST-FEDERATION-001 — SP 800-63C-4

[公式出版記録](https://csrc.nist.gov/pubs/sp/800/63/c/4/final)と[公式本文](https://pages.nist.gov/800-63-4/sp800-63c.html)のIdP発行Assertion Contents、Audience Restrictionを確認しました。HTMLの対象anchorは`assertions`と`audience-restriction`です。別の`assertion-contents`はWallet側の節であり、混同しません。

Issuer、Audience、受入RP、有効期間、署名等の役割を分ける根拠として採用します。全FALでRPは自分がAudienceに含まれることを確認し、単一Audienceの要求はFAL2以上です。本教材の単一AudienceモデルをFAL1全般へ一般化しません。Issuer/Audienceの文字列一致は完全なAssertion検証ではなく、実Token処理や機械間認証への適合を実装したとは主張しません。

## SRC-IETF-OAUTH-BCP-001 — RFC9700 / BCP240

[公式本文](https://www.rfc-editor.org/rfc/rfc9700.html)と[Status / 更新関係](https://www.rfc-editor.org/info/rfc9700/)を確認しました。**January2025 / Best Current Practice / BCP240**、RFC6749 / 6750 / 6819をupdatesします。公表日は月までしか確認できないためRegistryのpublishedAtはnullとします。

採用は§2.3のPrivilege / Resource / Action / Audienceの制限だけです。[公式Errata検索](https://www.rfc-editor.org/errata/rfc9700)は確認時点で該当0でした。将来もErrataがないという意味ではありません。

RFC6749の全更新履歴やすべてのGrantの推奨状態を監査したとは主張しません。古い実装例を転記せず、Protocol実装は専門書へ委譲します。OAuth Access tokenと、SP 800-63Cの認証Assertionの用途を同一視しません。

## SRC-NIST-ZTAA-001 — SP 800-207A

[公式Final記録](https://csrc.nist.gov/pubs/sp/800/207/a/final)のDocument HistoryとAbstractを再確認しました。Final日は **2023-09-13** です。人に加えてApplication / Service identityを区別するという、第6章から継承する限定命題だけを使用します。

今回SP 800-207AのPDF全本文を再監査したとは主張しません。製品構成、具体的なWorkload identity実装、Zero Trust適合性は採用範囲外です。Registryの既存notesと第6章の意味は変更せず、第12章mappingと今回の確認日だけを追加します。

## 再確認と教材への制限

SP 800-63系列と207Aの次回確認は2026-12-15、RFC9700は2027-09-15とします。新版、Status、Errata、採用主張、委譲先routeの変化があれば期限前でも確認します。Registry全体のcheckedAtは2026-07-25のまま保持します。

[委譲先の公開入口](https://itdojp.github.io/practical-auth-book/)はHTTP200を確認しました。専門書全体の内容監査ではありません。第12章の読解と合成比較は、その専門書の実装を実行せずに完結します。

Raw Editorial Inputの登録名は認可workspace全域で見つかりませんでした。EIP-0008 / EIC-0036-bf2b7e4fe16eは設計来歴として選択しましたが、raw読了、実体Hash照合、直接採用は主張しません。本文、ART-20、合成JSON、Schema、有限検査は現行Issue、親契約、上記の一次Sourceから新規構成しています。同梱Chapter13のDispositionは変更しません。
