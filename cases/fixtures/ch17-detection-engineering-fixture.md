# 第17章 オフラインfixture：未承認管理者同意変更の検知検証

このページは、`cases/fixtures/ch17-detection-engineering-fixture.json`の利用前提と意味契約を説明する。

- machine-readable fixture本体: [`ch17-detection-engineering-fixture.json`](./ch17-detection-engineering-fixture.json)
- 関連Case ID: `CASE-DET-2026-001`
- 関連Case Map Case / Decision ID: `CASE-2026-001` / `DEC-2026-001`
- 関連Detection ID: `DET-2026-017-001`
- 関連Triage ID / Handoff ID: `TRI-DET-2026-001` / `HO-DET-2026-001`

## Fixtureの構成

| Fixture ID | 種類 | 期待結果 | 意味 |
|---|---|---|---|
| `FIX-2026-017-POS` | Positive | Alert | 未承認scope差分あり |
| `FIX-2026-017-NEG` | Negative | No alert | 必要Telemetryは利用可能だが、検知対象のconsent変更recordがない |
| `FIX-2026-017-BNM` | Benign near miss | No alert / Allowed | Eventはあるが承認済みChangeに一致 |
| `GAP-DET-2026-001` | Coverage gap example | 判定不能 | Telemetry absenceはEvent absenceではない |

## 安全条件

- 合成データのみ
- オフライン専用
- Malware、外部制御基盤、認証情報窃取、回避、永続化、実Tenant操作を含まない
- 実Credential、実PII、実Tenant IDを含まない

## 利用方法

1. JSON内の`fixtures`配列で期待結果を確認する。
2. `python3 scripts/replay_chapter17_detection.py`で、合成ruleを3種類のfixtureとcore telemetry gapへオフラインReplayする。
3. `coverageGapExample`はPositive fixtureから`TEL-DET-2026-002`を除く決定的な派生入力であり、Negative fixtureとTelemetry gapを区別する。
4. `scripts/check_chapter17_contract.py`でID、fixture semantics、安全条件を検証する。

合成rule本体は[`detections/cloud_identity/det_2026_017_001.json`](https://github.com/itdojp/white-hat-cyber-intelligence-book/blob/f546a03a5f0534e7603dbb86ff2bdaa98542e01f/detections/cloud_identity/det_2026_017_001.json)である。このリンクは監査済みcommit `f546a03a5f0534e7603dbb86ff2bdaa98542e01f`に固定している。Replay時は同一checkout内のrule、runner、fixtureを使用し、異なる版を混在させない。これは教材用の決定的な評価契約であり、実SIEM / EDRへ投入しない。
