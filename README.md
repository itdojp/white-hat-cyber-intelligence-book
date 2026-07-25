# ホワイトハッカーとサイバーインテリジェンス実践体系

**攻撃者の行動を理解し、検証・検知・対応・経営判断につなげる**

本リポジトリは、IT Engineer Knowledge Architectureシリーズの書籍制作リポジトリです。攻撃技術の習得自体を目的にせず、脅威を理解し、許可された範囲で安全に検証し、観測・検知・対応・サイバー脅威インテリジェンス・経営判断へ変換する方法を体系化します。

- Repository: <https://github.com/itdojp/white-hat-cyber-intelligence-book>
- Phase 0 Runbook: <https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/1>
- Bootstrap Draft PR: <https://github.com/itdojp/white-hat-cyber-intelligence-book/pull/2>
- Parent proposal: <https://github.com/itdojp/it-engineer-knowledge-architecture/issues/280>
- Status: `0.1.0` editorial foundation / Phase 0 in progress

## 中心となるループ

```text
判断要求を定義する
  → 資産・信頼境界・脅威を把握する
  → 攻撃経路と観測仮説を立てる
  → 許可された隔離環境で最小限に検証する
  → ログ・証拠・痕跡を評価する
  → 検知・対応・コントロールを改善する
  → 確信度付きインテリジェンスに変換する
  → 技術・運用・経営判断を記録する
  → 再評価する
```

## 現在の正本

| 対象 | 正本 |
|---|---|
| 書籍企画 | `BOOK_PROPOSAL.md` |
| 詳細目次 | `TOC.md` |
| 既存書籍との境界 | `CROSS_BOOK_MAP.md` |
| 執筆規約 | `WRITING_GUIDE.md` |
| 出典・鮮度 | `SOURCE_POLICY.md`, `references/` |
| 安全な公開範囲 | `SAFETY_SCOPE.md` |
| 演習環境 | `LAB_ARCHITECTURE.md` |
| 章本文 | `manuscript/` |
| 実務成果物 | `templates/` |
| 出版設定 | `book-config.json` |

`docs/`は将来、固定した`book-formatter`と同期スクリプトから生成する公開成果物とします。編集元と生成物を混在させない契約は`CANONICAL_SOURCE.md`を参照してください。

## 安全上の原則

掲載する評価・演習は、明示的に許可された自己所有環境、隔離ラボ、合成データだけを対象とします。実在する第三者システムへのスキャン、認証試行、アクセス、資格情報の取得・再利用、永続化、検知回避、破壊を目的としません。

詳細は`SAFETY_SCOPE.md`と`SECURITY.md`を参照してください。

## ローカル検証

現在のPhase 0で実行できる契約検査はPython標準ライブラリだけで完結します。

```bash
python3 scripts/check_contract.py
```

Jekyllサイト、Book QA、Pagesは、`book-formatter`固定revisionから共通コンポーネントを同期した後に有効化します。未生成の公開サイトを完成扱いにしません。

## ライセンス

- 本文、図表、教材、テンプレート: CC BY-NC-SA 4.0
- `scripts/`および将来の`lab/`に置く自作コード: Apache License 2.0
- 第三者成果物: 原ライセンスに従い`THIRD_PARTY_NOTICES.md`へ記録

商用利用には別途契約が必要です。詳細は`LICENSE.md`を参照してください。
