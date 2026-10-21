# 第29章の限定Source Review（2026-10-21）

Issue #51の判断・共有・再評価に必要な二つの公式資料だけを確認した。原典を全頁監査した、全59Sourceの最新版を確認した、法務承認した、という記録ではない。公式landingとPDFを取得し、既存pypdfで対象節を読解した。図表転載や長文引用は行わず、本書のCase・六状態・Rubricは独自教材と区別する。

## SRC-CSF-001

NIST CSWP 29 / CSF 2.0、Final、2024-02-26。[公式刊行頁](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20)と[公式PDF](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)を確認。PDF SHA-256: `3c31f46fee98cac0c4323453e5109291a213b4de7fef8c058af9bf67f717433c`。

Abstract、§1（印刷pp.1〜2）、§5.1（印刷pp.10〜11）の高位Outcome、技術担当・管理者・判断担当の情報の往復に限定採用する。実装手順、固定直列の十二段階、Control有効性や完全性の証明へは使わない。

## SRC-NIST-RISK-001

NIST SP 800-30 Rev.1、Final。公式頁の本文はSeptember 2012、Document HistoryのFinal日付は2012-09-17。[公式刊行頁](https://csrc.nist.gov/pubs/sp/800/30/r1/final)と[公式PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf)を確認。PDF SHA-256: `f214087f0bdb35932a28c16eb93932a33c67a6edfb5e6f1638866bd201c98e04`。

§3.3（印刷p.37）の結果と根拠の共有、§3.4（印刷pp.38〜39）の変化を踏まえた評価維持に限定採用する。連邦向けProcessを普遍的な法的義務、本書の状態算法、実操作許可へ変換しない。

## 時点・License・変更の扱い

今回の確認日と出版用hashは、合成Caseの過去cutoff、判断、許可期間を変更しない。EPSS/KEV等の継続更新Dataは新規取得せず、元章の固定Snapshot・取得日・hashをそのまま参照する。参照先が存在することは、その内容が今回の事案を支持することとは別である。

二Sourceの章mappingに29を追加し、個別checkedAtだけを進める。Registry-wide baseline、他Source、親章の採用節、次回確認日を保持する。訂正・改訂・撤回・対象節の変更時は本文、二Brief、再評価条件を再確認する。PDF表紙画像の直接目視、全仕様適合、全Source/Licenseの最終監査は未実施。公式資料へのリンクと独自要約だけで、図表・PDFを本書へ再配布しない。既存第三者通知を削除しない。

[第29章](../manuscript/29-capstone-case-study.md)へ戻る。
