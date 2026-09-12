# 第8章 Source Review Note：Lab SafetyとEvidence

## 確認範囲と採用方針

確認日2026-09-13。対象は[第8章](../manuscript/08-safe-lab-evidence.md)、[ART-18](../templates/lab-safety-evidence-plan.md)、[合成記入例](../cases/ch08-lab-evidence-example.md)の原則と限界である。原典の該当箇所を読み、著者の有限モデルと外部の規範を分離した。全文監査、実Runtimeの動作確認、法的証拠能力の確認は行っていない。

本章は実環境のWSL2・Podman構築を実行しない。版固定された製品操作を提供する章ではなく、それらに相当する抽象モデルの合成receiptをオフライン照合する。八状態、三判定、72チェック、seed 208、SHA-256の選択は本書独自の教材契約である。

## SRC-NIST-DFIR-001

- 発行主体: NIST。
- 文書: Guide to Integrating Forensic Techniques into Incident Response、SP 800-86、Final。
- 版・公開時点: August 2006。CSRCの履歴には09/01/06を別に表示する。月単位のDate Publishedと履歴日を同一視せず、公開日の「日」は不明としてRegistryのpublishedAtをnullにする。
- 一次資料: [公式出版ページ](https://csrc.nist.gov/pubs/sp/800/86/final)、[公式PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf)。
- 採用箇所: §3（本文3-1）と§3.1.2（本文3-4）。収集・検査・分析・報告の区別、取得計画、データ完全性、取扱いと時刻の記録を参照した。
- 読者影響: EvidenceのID、生成元、Hash、Time zone、取扱い、変換履歴を別欄にする。Hash単独で内容の真実性を証明しない。
- 限界: IT-orientedな技術ガイドであり、法執行や法的助言の代替ではない。2006年時点の旧Hash方式や製品操作を現在の推奨として採用しない。SHA-256は本書の教材仕様である。

直接のPDFダウンロード要求はHTTP 403だったが、ブラウザの一次PDFテキスト取得から該当箇所を確認した。ローカルへ完全取得してPDFのHashを検証したとは主張しない。

## SRC-NIST-CONTAINER-001

- 発行主体: NIST。
- 文書: Application Container Security Guide、SP 800-190、Final。
- 版・公開時点: September 2017。CSRCの履歴09/25/17は別属性として保持し、公開日の「日」を推測しない。publishedAtはnull。
- 一次資料: [公式出版ページ](https://csrc.nist.gov/pubs/sp/800/190/final)、[公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)。
- 採用箇所: §3.5.2の共有Kernel、§4.4.2のNetwork、§4.4.3のRuntime設定、§4.5.5の限定Mount。境界と残余リスクを複数層で扱う原則に限定した。
- 読者影響: rootlessという名前だけで安全を断定せず、権限、Network、Host、Dataを別チェックにする。
- 限界: 現行WSL2・Podmanの仕様、完全なコンテナ認証基準、実装済みの隔離の証明ではない。Resource上限や分離の実測は未実施である。

一次PDFの該当テキストを確認した。非公式翻訳の文言や表を正本として転載していない。

## SRC-BERKELEY-001

- 発行主体: OHCHR / Human Rights Center, UC Berkeley School of Law。
- 文書: Berkeley Protocol on Digital Open Source Investigations、2022 edition。HR/PUB/20/2、ISBN 978-92-1-154233-2を版の補助情報とする。
- 一次資料: [OHCHR出版ページ](https://www.ohchr.org/en/publications/policy-and-methodological-publications/berkeley-protocol-digital-open-source)、[公式共同発行者のPDF](https://humanrights.berkeley.edu/wp-content/uploads/2024/02/Berkeley-Protocol.pdf)。
- 確認箇所: 表紙・Copyrightと、§VI.Cの155(g/h)（本文59）、§VI.Dの167–169（本文61）。取得時刻、Hash、文脈、取扱いの時系列、原本と作業コピーの区別を限定的に参照した。
- 日付: 2022 editionの公開日の日まで確認できず、publishedAtはnullを維持する。別の2020年告知日やPDFの配信Pathを2022年版の公開日に流用しない。
- 取得制約: OHCHR出版ページの直接取得はHTTP 403。公式共同発行者PDFの一次テキストで該当箇所を確認した。
- 読者影響: 本章にCustodian、Retention、Transform historyと限界を追加する。既存第25章の2022 editionと出典評価の意味は変更しない。
- 限界: 人権・国際犯罪調査という原文の目的を留保する。独自ART-18は法的手続の代替や証拠能力の認定ではない。原文の図表やTemplateは転載しない。

原典と、それを参照した資料を独立した証拠の本数として加算しない。合成receiptのProducerも、現実の観測主体の信頼性を裏付けるものではない。

## 非採用と再確認

NISTIR 8176の出版情報とLinux Application ContainerのAssuranceを扱う位置付けは確認したが、詳細な要件を本章の判定基準として採用しない。本章のSource集合へ追加せず、実Runtime実装の別レビューへ委譲する。

次回確認は2027-09-13まで、または原典の改訂・撤回・公式URL移動・利用範囲の変更時とする。実Runtime操作、法的手続、取得対象Dataを追加する場合は、この限定監査を再利用せず、許可と新しい一次資料のGateへ戻る。

Registry直下の一括監査日は2026-07-25のまま保持する。今回更新するのは二つの新規NIST Sourceと、Berkeleyの第8章向け限定確認だけである。過去の章や未執筆章を一括再監査したとは扱わない。
