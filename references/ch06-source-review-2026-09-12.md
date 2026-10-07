# 第6章 Source Review Note — 2026-09-12

## 対象と採否

Issue #31 / ART-16を対象とする。base mainは`c83bf8a8cc02aa206c67ba178de665acc8bf9237`、Policyは`1.2.0`、Publication Projectionは`1.1.0`である。2026-09-12に公式の出版記録、本文、MITREページを直接取得して確認した。

## 一次資料と適用範囲

| Source ID | 一次資料・版 | 採用範囲 |
|---|---|---|
| SRC-NIST-ZTA-001 | [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)、Final、2020-08-11 | §3と§3.4のDecision / Enforcement、Control / Data Planeの論理分離 |
| SRC-NIST-ZTAA-001 | [NIST SP 800-207A](https://csrc.nist.gov/pubs/sp/800/207/a/final)、Final、2023-09-13 | UserだけでなくApplication / Service identityを扱う必要性 |
| SRC-NIST-LOG-001 | [NIST SP 800-92](https://csrc.nist.gov/pubs/sp/800/92/final)、Final、2006-09-13 | §2〜3の生成・転送・保存・分析、時刻差、正規化、保持の区別 |
| SRC-NIST-LOG-DRAFT-001 | [NIST SP 800-92 Rev.1](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd)、Initial Public Draft、2023-10-11 | 改訂監視のみ。Final規範としては不採用 |
| SRC-IETF-OAUTH-CORE-001 | [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749.html)、2012-10、Proposed Standard | §1.1と§1.3.4のRole、Client自身のための行動。操作例は不採用 |
| SRC-ATTACK-001 | [MITRE Version History](https://attack.mitre.org/resources/versions/)、v19.2 | 第5章で採用した版を継承。新たなTechnique対応は作らない |
| SRC-ATTACK-DET-001 | [Detection Strategies](https://attack.mitre.org/detectionstrategies/)、v19.2 | Strategyの参照と実際のData保有・Validationの分離 |

NISTの公開日はCSRCのDocument Historyを用い、PDF表紙の月表示から日を推測しない。RFCの公表日は月までのためRegistryではpublishedAtをnullとし、notesへ2012-10と不明理由を残す。

SP 800-92 Rev.1の出版記録と[Log Management project](https://csrc.nist.gov/projects/log-management)を照合した。意見募集が終了していてもFinalとは扱わない。SP 800-92の2006年の製品例やMD5 / SHA-1に関する記述は採用しない。SourceがFinalであることは、全記述が現在の実装推奨であることを意味しない。

RFC 6749の更新元である[RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html)、BCP 240、2025-01も確認した。RFC 6749の古いGrantの選択やSecurity recommendationを本章へ転用せず、採用はRole説明に限定する。実装選択は専門書へ委譲する。

ATT&CKは公式HTTP取得とMITRE/CTIのreleaseでv19.2を確認した。検索経由のキャッシュに同版が表示されない場合があったため、キャッシュだけで現行版を決定していない。第5章の固定commit `8543c5b05bd9bbcace9fc37f30bba96b675b6f33`、既存の最小metadataと原典の意味を維持する。release時刻、Version Historyページ自体の日付不明、代表章の歴史的記述を混同しない。

## Source変更の影響と限界

SP 800-207系は論理的役割だけ、SP 800-92は観測経路だけ、OAuthは主体の区別だけを本文へ採用する。六つのCoverage status、完全合成受領票、Gap、Rubric、Build planeという補助分類は本書独自であり、標準の引用や適合認証ではない。

ATT&CK二項目の確認日と第6章mappingを更新する。第5章・第17章・第25章の既存の限定命題は変わらず、親のObservation、Control、Gap、Decisionを昇格させない。Registry全体の一括監査日は更新しない。

Next reviewは2026-12-12。改訂版・Status・使用箇所の意味・ATT&CK release・委譲先routeの変更時には期限前でも確認する。出典を読んだことは、実環境のAudit schemaや監視性能を検証したことではない。

## Editorial Input Record

- Package ID: EIP-0002
- Package SHA-256: `fffbd2af8a17cbbfa60c09c37c30a682a9c528b44194e0e9f0f3588e2a6a46ca`
- Target: Issue #31 / chapter-06
- Input path: `chapter06-observable-systems.predraft.md`
- Input SHA-256: `2c4e8b2b85086bde3d0f83bb4e2ed61cf0d7512252e27fbc805a272249e8973d`
- Input確認状況: `not-present-in-authorized-workspace`
- Adopted: raw predraftからの直接採用なし。登録metadataだけを照合。
- Rewritten: Issue #31、current contract、親Case、再確認した一次資料から本文とART-16を新規作成。
- Rejected: 未確認rawの読了・実体hash検証・直接採用、旧草稿の追加Status、親Caseの観測結果の無根拠な昇格。
- Deferred: 実製品Log schema、Protocol操作、実環境検知、Chapter7以降。
- Raw tracked files: 0。

登録候補の明示選択と専用PRは機械可読Manifestで追跡する。通常merge・main/publication前にはconsumedへ進めない。
