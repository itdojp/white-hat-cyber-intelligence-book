# Repository Governance

## 正本

- 作業の優先順位と完了条件: GitHub Issue
- 変更のレビュー単位: Pull Request
- 書籍構造: `book-config.json`と`TOC.md`
- 編集・安全・出典契約: 各ポリシーファイル

## 標準フロー

1. Issueで目的、非目標、受入条件、停止条件を定義する
2. Issue専用branchを作る
3. Draft PRを早期に作る
4. 対象ファイルだけを変更する
5. ローカル検査とCIを記録する
6. 独立レビューを行う
7. unresolved threadを0にする
8. merge後に公開成果物と親ポータルを確認する

## Merge

- 原則Squash merge
- mainへの直接pushは禁止。空リポジトリを実体化したroot commitだけを例外とする
- admin bypass、force push、branch deletionを通常手順にしない
- 自動mergeは、運用ルールとrequired checksが確定するまで使用しない

## AIエージェント

AIエージェントは、調査、草稿、レビュー、検証、Issue/PR作成を担当できる。次は人間の判断を必要とする。

- 法的許可と実対象の承認
- 高リスクな公開範囲
- 実環境への操作
- リスク受容
- 最終的なアトリビューション表現
- Repository Rules、Pages、Security settings等の管理者操作

AIによる執筆と最終レビューは、可能な限り別セッション・別モデル・別観点で行う。
