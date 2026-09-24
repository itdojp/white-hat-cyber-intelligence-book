# 第20章 Source Review — 2026-09-25

## 確認範囲

第20章の来歴、時刻・分析、代替説明、原因の問いと記録に限定して一次資料を確認した。Registry全件、全DFIR手順、個別法域の再監査ではない。根の基準日2026-07-25と過去のnotesを保持し、三Sourceへ用途を追記する。

## SRC-NIST-DFIR-001

[NIST SP 800-86 Final](https://csrc.nist.gov/pubs/sp/800/86/final)の公表ページはAugust 2006を示す。正確な公開日は未確定としてRegistryのpublishedAt nullを保持し、Publication Historyの日付を推測で代入しない。[公式PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf)の採用範囲は印刷pp.3-1、3-4、3-6〜3-8である。

収集・検査・分析・報告の区別、完全性と作業Copy、複数Sourceの対応付け、結論不能と代替説明、報告・手順改善の原則に限定する。2006年の製品、OS、記憶媒体、取得コマンドを現在の標準手順として採用しない。全PDFの技術監査や現行法への適合確認を行ったという意味ではない。

## SRC-IR-001

[SP 800-61 Rev.3 Final](https://csrc.nist.gov/pubs/sp/800/61/r3/final)は2025-04-03公開である。[公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf)の印刷pp.28〜29、RS.AN-03/06/07を参照した。

順序と関連資産、根底の原因を調べる問い、調査活動の記録とDataの来歴・保持に限定する。組織手順に依存する保持や取扱いを、一律の法的ルールへ変換しない。Chapter20の有限時刻モデル、Cutoff、重複排除、Claim評価はこの文書の標準算法ではない。

## SRC-BERKELEY-001

[OHCHRの公表ページ](https://www.ohchr.org/en/publications/policy-and-methodological-publications/berkeley-protocol-digital-open-source)は今回403を返した。この経路で本文やStatusを再確認できたとはしない。共同発行者の[UC Berkeley公式Project](https://humanrights.berkeley.edu/projects/developing-the-berkeley-protocol-on-digital-open-source-investigations/)と、その[公式PDF](https://humanrights.berkeley.edu/wp-content/uploads/archive/2024/02/Berkeley-Protocol.pdf)は200で取得した。PDF表題・版権頁で2022 editionを確認し、正確な刊行日が不明なpublishedAt nullは保持する。

採用箇所はVI.C154/155(g,h)の印刷p.59、VI.D167〜169のp.61である。原形式と変換記録、取得文脈、保存・来歴、作業Copyの区別を参考にする。Digital Open Source調査の資料を一般DFIRの法的適格性の証明や実在人物の調査許可には使わない。

## 取得証跡と非目標

2026-09-25 JSTにTLS検証有効のHTTPSで確認した。NISTの二HTML・二PDFとUC Berkeleyの一HTML・一PDFは200、OHCHR HTMLは403である。版・採用節は一次PDFの表示とローカルPDF抽出で読解した。取得した三PDFの識別子を示す。

| PDF | SHA-256 |
|---|---|
| NIST SP 800-86 | `ea7eb645bcd3feaf3ab9ea7dfc3c8987a08bf260c40682df1e5e8292bf9fe9b4` |
| NIST SP 800-61r3 | `e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d` |
| Berkeley Protocol | `caa5ea4806545658e0cfd21ed5d21c0250922903eece89bf58d26756dac3a0ae` |

Hashは取得Byteの識別であり、署名検証でも全節の監査でもない。ART-07/26の有限Field、五Relation、二Snapshot、六Claim、UTC offsetの符号、総不確かさ、Cutoff、同一性と衝突の扱い、評価基準は本書独自である。原典や未読の登録草稿に書かれた内容と偽って引用しない。AI出力をSourceとして使わない。

## 再確認条件

版・Status・採用節、時刻や保持の用途、対象Scope、因果に関する主張が変わったら再確認する。実Data、実操作、個別法的判断を必要とする場合は本章の範囲外として停止する。Sourceごとの期限と過去の採用範囲はRegistryを参照する。
