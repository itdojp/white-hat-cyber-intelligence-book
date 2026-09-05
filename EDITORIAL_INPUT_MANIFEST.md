# Editorial Input Manifest

このファイルは`editorial-input-manifest.json`から決定的に生成します。機械可読Manifestを更新し、`npm run render:editorial-inputs`を実行してください。このファイルを手編集しないでください。

- Manifest version: `1.0.0`
- Audit date: `2026-09-05`
- Packages / targets / candidates: `14 / 29 / 30`
- Provenance: [Issue #63](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63) / [Issue #98](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/98)
- External audit artifact: `not-present-in-authorized-workspace`。内容やhash一致を推測しません。
- Raw ZIP / predraftはRepository正本ではなく、Gitへ追加しません。
- Candidate selectionは`selectedCandidateId`だけで表します。Filename、Wave、日時、File size、配列順は選択根拠になりません。

## Status summary

| Status | Count |
|---|---:|
| `blueprint-only` | 1 |
| `candidate-selection-required` | 1 |
| `consumed` | 1 |
| `generator-blueprint-only` | 2 |
| `registered-pending-prerequisites` | 23 |
| `selected-for-intake` | 1 |

## Acknowledged collisions

| ID | Kind | Value | Package IDs | Reason |
|---|---|---|---|---|
| `EICOLL-0001` | `filename` | `white-hat-book-parallel-drafts-2026-08-09-wave5.zip` | `EIP-0005`, `EIP-0006` | 同名だがSHA-256とTargetが異なる歴史的Package。filenameで選択しない。 |
| `EICOLL-0002` | `wave-label` | `wave-5` | `EIP-0005`, `EIP-0006` | 同一Wave labelが異なるPackageを表す。Wave番号で選択しない。 |

## Package index

| Package ID | Package filename | SHA-256 | Kind | Wave | Registered | Source |
|---|---|---|---|---|---|---|
| `EIP-0001` | `white-hat-book-parallel-drafts-2026-08-08.zip` | `caf8c73aa4e84c99f4062ac7cf85ac56794ad2cbb5d8ec5d9403138753eb6388` | `draft` | `initial` | `2026-08-08` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63) |
| `EIP-0002` | `white-hat-book-parallel-drafts-2026-08-08-wave2.zip` | `fffbd2af8a17cbbfa60c09c37c30a682a9c528b44194e0e9f0f3588e2a6a46ca` | `draft` | `wave-2` | `2026-08-08` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5223904155) |
| `EIP-0003` | `white-hat-book-parallel-drafts-2026-08-08-wave3.zip` | `d986ee9a9c71cf210420bb921f078a395133e2e5e0b9050960ad63554c22582a` | `draft` | `wave-3` | `2026-08-08` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5224086644) |
| `EIP-0004` | `white-hat-book-parallel-drafts-2026-08-08-wave4.zip` | `956a321088abed3058e59c58ceeda3d5fd57a9d12a6715240185d0d7c445d86f` | `draft` | `wave-4` | `2026-08-08` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5224564529) |
| `EIP-0005` | `white-hat-book-parallel-drafts-2026-08-09-wave5.zip` | `c4fd20d4c44d769c22bbab886535ca3105b3a3a5ed7bdb6cea71619e6b7279a0` | `draft` | `wave-5` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5228684652) |
| `EIP-0006` | `white-hat-book-parallel-drafts-2026-08-09-wave5.zip` | `1a2ccaa3dc3453dfc91c28a482bb8e319b5a2db6023d2d64f8cce2133619efb3` | `draft` | `wave-5` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5228688398) |
| `EIP-0007` | `white-hat-book-parallel-drafts-2026-08-09-wave6.zip` | `2ac28571912725ed838d4895779e3921b8138b52a66f2d5938c5776e46f3ff69` | `draft` | `wave-6` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5228712541) |
| `EIP-0008` | `white-hat-book-parallel-drafts-2026-08-09-wave8.zip` | `386e7148f504c9fa58a0b095bffcc6aeeaaf2be901e0d3b917e5e8db6c604b2c` | `draft` | `wave-8` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229170716) |
| `EIP-0009` | `white-hat-book-parallel-drafts-2026-08-09-wave9.zip` | `bef9879d4b230f63d5f1f8d037611bbab097328defc054cb2b801fbf8deeb1ad` | `draft` | `wave-9` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229191435) |
| `EIP-0010` | `white-hat-book-parallel-drafts-2026-08-09-wave10.zip` | `34a748e0d3373ad842aa512f6510c2ac17242d42588b82e19f377678d255c381` | `draft` | `wave-10` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229205526) |
| `EIP-0011` | `white-hat-book-parallel-drafts-2026-08-09-wave11.zip` | `cb9fee8ca0a1ff1b8e2ce6d45f5d0d1cc102303eacaddfec394deca098e83461` | `draft` | `wave-11` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229566622) |
| `EIP-0012` | `white-hat-book-parallel-drafts-2026-08-09-wave12.zip` | `6f5da12b33216dbc50473e9fd9d403213807d7f0219c50a71e5292386e82ea7b` | `mixed` | `wave-12` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229589913) |
| `EIP-0013` | `white-hat-book-parallel-drafts-2026-08-09-wave13.zip` | `16032793c917c17bd9478fb3f4e0a89e2afc89cf82b27400328dbfa74c9465d9` | `draft` | `wave-13` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5231023215) |
| `EIP-0014` | `white-hat-book-parallel-drafts-2026-08-09-wave14.zip` | `f6b11d439088d8e8571d7e8630b33a866b566a97815480ef7df074c45faa79a4` | `generator-blueprint` | `wave-14` | `2026-08-09` | [registration](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5231033156) |

## Target index

| Target | Issue | Status | Selected candidate | Canonical PR | Evidence |
|---|---:|---|---|---:|---|
| `chapter-04` | #29 | `consumed` | `EIC-0029-c49f0a11ef9e` | #64 | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5245374024) |
| `chapter-05` | #30 | `selected-for-intake` | `EIC-0030-11e256480c15` | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/98) |
| `chapter-06` | #31 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5223904155) |
| `chapter-07` | #32 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5224086644) |
| `chapter-08` | #33 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5224564529) |
| `chapter-09` | #34 | `candidate-selection-required` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/98) |
| `chapter-10` | #35 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5228684652) |
| `chapter-12` | #36 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229170716) |
| `chapter-13` | #37 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229170716) |
| `chapter-14` | #38 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229191435) |
| `chapter-15` | #39 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229191435) |
| `chapter-16` | #40 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5228688398) |
| `chapter-18` | #41 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229205526) |
| `chapter-19` | #42 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229205526) |
| `chapter-20` | #43 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229566622) |
| `chapter-21` | #44 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229566622) |
| `chapter-22` | #45 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229589913) |
| `chapter-23` | #46 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5223904155) |
| `chapter-24` | #47 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5224086644) |
| `chapter-26` | #48 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5224564529) |
| `chapter-27` | #49 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5228712541) |
| `chapter-28` | #50 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5228712541) |
| `chapter-29` | #51 | `blueprint-only` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5229589913) |
| `appendix-a` | #52 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5231023215) |
| `appendix-d` | #52 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5231023215) |
| `appendix-h` | #52 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5231023215) |
| `appendices-b-c-i` | #53 | `generator-blueprint-only` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5231033156) |
| `appendices-e-f-g` | #54 | `generator-blueprint-only` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5231033156) |
| `appendix-j` | #55 | `registered-pending-prerequisites` | — | — | [status](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/63#issuecomment-5231023215) |

## Candidate disposition

### `chapter-04` / Issue #29

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0029-c49f0a11ef9e` | `EIP-0001` | `chapter04-assets-boundaries-threat-model.predraft.md` | `c49f0a11ef9e37f1952199d263125aae9df273032e0a996642cfe9899750c358` | `rewritten` | Raw package不在のため直接採用せず、Issue契約・current Repository・再検証済み一次資料からcanonical内容を再構成した。 |

### `chapter-05` / Issue #30

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0030-11e256480c15` | `EIP-0001` | `chapter05-attack-behavior.predraft.md` | `11e256480c15771334cc3c9e8eb0933635c305604ba9302482ce627205e1ef12` | `selected` | 登録候補は1件。Packageが利用可能ならhash検証し、利用不能なら直接採用を主張せずIssue #30と現行一次資料から再構成する。 |

### `chapter-06` / Issue #31

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0031-2c4e8b2b8508` | `EIP-0002` | `chapter06-observable-systems.predraft.md` | `2c4e8b2b85086bde3d0f83bb4e2ed61cf0d7512252e27fbc805a272249e8973d` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-07` / Issue #32

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0032-6caf4e3d9174` | `EIP-0003` | `chapter07-vulnerability-prioritization.predraft.md` | `6caf4e3d9174ae8b527df5b14301cd456550b1eca1ea7e88cf7c19e5031338cb` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-08` / Issue #33

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0033-eee4bacd1c7b` | `EIP-0004` | `chapter08-safe-lab-evidence.predraft.md` | `eee4bacd1c7be3366e6343a10f5f69a184dffe8a16c662fcabe90f24f543373b` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-09` / Issue #34

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0034-00de5e803e04` | `EIP-0005` | `chapter09-engagement-roe.predraft.md` | `00de5e803e04d13ae80b9960489a2d7d90d6564c88324d7f32aed8c28c96ea91` | `pending-comparison` | Issue #34、Chapter 2/4/8契約、current Policyと一次資料に対する比較が未実施。 |
| `EIC-0034-dd0c5e0b83f3` | `EIP-0006` | `chapter09-engagement-roe.predraft.md` | `dd0c5e0b83f3cb75e099e7ca5bee572a6b51c1745bc985fc91f6b370b90f8579` | `pending-comparison` | Issue #34、Chapter 2/4/8契約、current Policyと一次資料に対する比較が未実施。 |

### `chapter-10` / Issue #35

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0035-23f9af567b80` | `EIP-0005` | `chapter10-recon-osint-boundary.predraft.md` | `23f9af567b80d64c0d191b0f7905ddd8350ce81606d24c72626949fa30739002` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-12` / Issue #36

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0036-bf2b7e4fe16e` | `EIP-0008` | `chapter12-enterprise-identity.predraft.md` | `bf2b7e4fe16e083924af23ecee183f3536e97b588770d56efd80e6b5e17b85cd` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-13` / Issue #37

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0037-16d33d9ab258` | `EIP-0008` | `chapter13-platform-supply-chain.predraft.md` | `16d33d9ab2589c661fd88739ec20f8d6b74221b60eece7efa0ca0293dc1be0ec` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-14` / Issue #38

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0038-3e687b3de61f` | `EIP-0009` | `chapter14-minimal-impact-validation.predraft.md` | `3e687b3de61f4c6a0b20365b04f483064edf5ac07c2ff4cc6ffbe0cbd89bf58f` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-15` / Issue #39

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0039-c168fc29af42` | `EIP-0009` | `chapter15-findings-retest-risk.predraft.md` | `c168fc29af42cc50a38d23c581172bc4953125775f71867d60c36d5a726b7b3c` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-16` / Issue #40

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0040-38fbe94b39aa` | `EIP-0006` | `chapter16-telemetry-evidence-readiness.predraft.md` | `38fbe94b39aac0ad6e59fcaa0c2cd9bfffc23b4eb01ca4dbbfd1cfb470a00c32` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-18` / Issue #41

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0041-5a08af6d1ae3` | `EIP-0010` | `chapter18-threat-hunting.predraft.md` | `5a08af6d1ae3f94b622ddec1f36f133b763d5b6eaac03f1ef08b415d0b540bbd` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-19` / Issue #42

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0042-3630c01fb55d` | `EIP-0010` | `chapter19-incident-response.predraft.md` | `3630c01fb55dab74344e89467e0a72881f8134995f84e0eb250a9c9648446f68` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-20` / Issue #43

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0043-58dc95fff364` | `EIP-0011` | `chapter20-dfir-timeline-causality.predraft.md` | `58dc95fff36417b259bab6c965d2bfe2289b3d59fa5d4e4f57a2b49806c81078` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-21` / Issue #44

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0044-a729d22fb189` | `EIP-0011` | `chapter21-purple-team-control-validation.predraft.md` | `a729d22fb1898e62d5ddf0d7bc2ebd1e4794ed82a49d77ff65ddaaf1aff0dbff` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-22` / Issue #45

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0045-78813e20d84e` | `EIP-0012` | `chapter22-measurement-improvement.predraft.md` | `78813e20d84e495b2aada2173b50b80a3efe947d9689dd90718e2a617a3bf15c` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-23` / Issue #46

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0046-29d20db7f44a` | `EIP-0002` | `chapter23-intelligence-requirements.predraft.md` | `29d20db7f44a073d8aa3b8d1c18db109f479297da79cec787edc5e8b4e5b9493` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-24` / Issue #47

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0047-b1b83a6735ac` | `EIP-0003` | `chapter24-osint-provenance-sources.predraft.md` | `b1b83a6735ac33f66afa27d1ac2ce1f260d70fc904eca9b6b5c2fefb36ed59bd` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-26` / Issue #48

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0048-38a432a5daf5` | `EIP-0004` | `chapter26-cti-distribution.predraft.md` | `38a432a5daf5477a3b986f8c19307d89a9565edf2f0d3a25ea9815126bb5bf32` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-27` / Issue #49

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0049-32e8846cf56d` | `EIP-0007` | `chapter27-ai-agent-security.predraft.md` | `32e8846cf56d741ba7fc28ca36df288132192e48d8f142dc8c32d433da375fed` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-28` / Issue #50

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0050-313c092a3659` | `EIP-0007` | `chapter28-ai-assisted-analysis-assurance.predraft.md` | `313c092a3659c566f85061efeb23a103fa2a7d3fd68845b76de72a7e6f29016a` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `chapter-29` / Issue #51

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0051-a90f9092493f` | `EIP-0012` | `chapter29-final-portfolio-blueprint.md` | `a90f9092493f64bcfbb3a36f269e83e686177203f276234b29cfd365e4444e04` | `blueprint-only` | 完成本文ではなく、live manifest/reportを基に統合するBlueprint。 |

### `appendix-a` / Issue #52

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0052-d6932c1a4774` | `EIP-0013` | `appendix-a-safety-legal-disclosure.predraft.md` | `d6932c1a47741992071cd05d866afd26980ec64e6e35c3ebda09d53c2eede854` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `appendix-d` / Issue #52

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0052-a1d1ce13dd48` | `EIP-0013` | `appendix-d-troubleshooting-stop-flow.predraft.md` | `a1d1ce13dd4827d438182ed1ad94b20f01c25c4d243b42e847d1ed9e2a2147da` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `appendix-h` / Issue #52

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0052-390579c705e1` | `EIP-0013` | `appendix-h-lab-operations.predraft.md` | `390579c705e1187c9765b6544f9628a7bd4b0542b7cc3da70ff5dc3172b8ecca` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

### `appendices-b-c-i` / Issue #53

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0053-6a52b22b0613` | `EIP-0014` | `appendices-b-c-i-generation-blueprint.md` | `6a52b22b061342c8f0c4fc58ec36822ea8c8958d76c691bcff5cd452c7b5268a` | `generator-blueprint-only` | live Repositoryから付録を生成・監査するBlueprint。完成本文として扱わない。 |

### `appendices-e-f-g` / Issue #54

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0054-2a34e9e8d137` | `EIP-0014` | `appendices-e-f-g-generation-blueprint.md` | `2a34e9e8d137b59aac91692d5d824b0c4f65b1d77ef1bd8119032c37af5c63e1` | `generator-blueprint-only` | live Repositoryから付録を生成・監査するBlueprint。完成本文として扱わない。 |

### `appendix-j` / Issue #55

| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |
|---|---|---|---|---|---|
| `EIC-0055-50177ad8c7a7` | `EIP-0013` | `appendix-j-cross-book-learning-routes.predraft.md` | `50177ad8c7a7737203883384f38a60b5e209d6e920132f4056ba47139c7bd302` | `registered` | 前提完了後にcurrent contractと一次資料へ再構成する登録候補。 |

## Intake gate

1. `packageId`、Package SHA-256、Target IDをManifestと照合する。
2. ZIP展開前に`python3 scripts/check_editorial_input_manifest.py --verify-package <path> --package-id <EIP-...> --target <target-id>`を実行する。
3. 複数候補は`candidate-selection-required`のまま比較し、全代替候補のDispositionを記録する。
4. `canonical-pr-open`ではmachine-readable Intake RecordとPR本文のIntake Recordを同時に追加する。
5. Canonical実装はraw inputをコピーせず、current contractと再検証済み一次資料へ再構成する。
6. merge・main CI・Pages確認後にのみ`consumed`へ遷移する。
