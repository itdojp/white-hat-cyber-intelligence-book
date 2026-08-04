# 第2章 Source Review — 2026-08-05

## 位置付け

この文書は、第2章「法、倫理、許可、責任ある開示」の執筆時に確認した公式一次資料、現行状態、採用範囲、留保を記録するEditorial review noteである。

機械可読のSource正本は`references/sources.json`である。本Noteは正本を置き換えず、Registry更新と独立Reviewの根拠として使用する。

## 採用Source

### SRC-JP-LAW-001

| Field | Value |
|---|---|
| Publisher | e-Gov法令検索 |
| Title | 不正アクセス行為の禁止等に関する法律 |
| Canonical URL | https://laws.e-gov.go.jp/law/411AC0000000128 |
| Status checked | Current law display |
| Effective state observed | 2025-06-01施行表示 |
| Checked at | 2026-08-05 |
| Chapter use | 許可を欠く操作を、研究・教育・善意という目的だけで当然に許容されるものとして扱わない一般的な安全境界 |
| Not used for | 個別操作への法的適用判断、違法性の断定、免責判断 |
| Recheck trigger | 法令改正、施行日変更、e-Gov現行表示変更、Release前監査 |

執筆上の制約:

- 条文名を挙げるだけで結論を補強しない。
- System、Account、識別符号、Access control等の具体的適用は個別確認へ差し戻す。
- Authorization、Contract、Scope、Third-party rightを独立して確認する。

### SRC-IPA-VDP-001

| Field | Value |
|---|---|
| Publisher | IPA / JPCERT/CC |
| Title | 情報セキュリティ早期警戒パートナーシップガイドライン |
| Canonical URL | https://www.ipa.go.jp/security/guide/vuln/partnership_guide.html |
| Version observed | 2024年版 |
| Official page update observed | 2026-04-06 |
| Checked at | 2026-08-05 |
| Chapter use | 発見者、IPA / JPCERT/CC、製品開発者、ウェブサイト運営者等の役割、連絡・調整・情報管理を確認するための一次Guidance |
| Not used for | 届出対象・公開時期・法的義務を個別事案で自動判定すること |
| Recheck trigger | Guideline改訂、届出手順変更、窓口変更、Release前監査 |

執筆上の制約:

- 発見、追加検証、届出、調整、修正、公開を同一判断にしない。
- 製品とウェブサイトの取扱いを混同しない。
- 未調整の詳細、Secret、個人情報、第三者Dataを公開Issueへ持ち込まない。

## 追加候補Source

### 個人情報の保護に関する法律

| Field | Value |
|---|---|
| Publisher | e-Gov法令検索 |
| Canonical URL | https://laws.e-gov.go.jp/law/415AC0000000057 |
| Current display observed | 2026-07-17施行表示 |
| Checked at | 2026-08-05 |
| Status | Candidate; Chapter 2本文では未引用 |
| Reason | Personal Dataを含むEvidenceの利用目的、Access、保持、共有、廃棄を一般原則から具体化する際に必要となる可能性がある |

留保:

- 未施行改正が存在するため、現行義務、公布済み改正、将来施行予定を分離する。
- 個別の漏えい報告・本人通知義務は、事業者区分、Data、事案等を確認せず断定しない。

### 2026年改正個人情報保護法の公布資料

| Field | Value |
|---|---|
| Publisher | 個人情報保護委員会 |
| Canonical URL | https://www.ppc.go.jp/news/press/2026/260717_houdou/ |
| Status observed | 2026-07-17公布。一部を除き公布から2年以内の政令日施行 |
| Checked at | 2026-08-05 |
| Status | Candidate; current obligationのSourceとして未採用 |
| Reason | Release時に現行法と将来施行予定を混同しないためのFreshness trigger |

### 漏えい等事案への対応Guidance

| Field | Value |
|---|---|
| Publisher | 個人情報保護委員会 |
| Canonical URL | https://www.ppc.go.jp/personalinfo/legal/leakAction/ |
| Checked at | 2026-08-05 |
| Status | Candidate; Incident Response章との責任境界を確認して採否を決める |
| Reason | Personal Dataを含むIncident / Evidenceで、初動、報告、本人通知等の判断主体を明確にするため |

## 採用判断

第2章初稿では`SRC-JP-LAW-001`と`SRC-IPA-VDP-001`だけを本文の重要主張へ使用する。

個人情報保護法関連Sourceは、次の理由で初稿本文へ直接追加しない。

1. 本章の中心はAuthorization GateとRoE Handoffである。
2. 漏えい等対応の詳細は第19章Incident Responseと責任境界を調整する必要がある。
3. 2026年改正には未施行部分があり、現行義務と将来変更を混同するRiskがある。

ただし、Personal Dataを実Dataとして扱う場合は、Data owner、Privacy、法務による個別確認へEscalateする本文を維持する。

## Registry更新要求

本PRで完了させる項目:

- `SRC-JP-LAW-001.checkedAt`を`2026-08-05`へ更新
- `SRC-JP-LAW-001`の現行施行表示をNoteへ記録
- `SRC-IPA-VDP-001.checkedAt`を`2026-08-05`へ更新
- `SRC-IPA-VDP-001.version`を`2024年版`として確認
- Official page更新日`2026-04-06`をNoteへ記録
- `reference-baseline.md`をRegistryから再生成

追加候補SourceのRegistry登録は、第19章との責任境界とRelease時Freshness方針を確認して別判断する。

## 独立Review Checklist

- [ ] 現行と未施行を混同していない
- [ ] 公式一次資料へ遡及できる
- [ ] 法的結論を断定していない
- [ ] 法務・Privacy・契約責任者へのEscalation条件がある
- [ ] 発見、検証、届出、調整、公開を分離している
- [ ] Source Registryと生成Baselineへ反映した
