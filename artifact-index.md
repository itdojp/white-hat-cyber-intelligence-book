# Artifact Index

| ID | 成果物 | 主な章 | テンプレート |
|---|---|---:|---|
| ART-01 | Learning Route Plan | 0 | `templates/learning-route-plan.md` |
| ART-02 | Rules of Engagement | 9 | `templates/rules-of-engagement.md` |
| ART-03 | Threat Model | 4 | `templates/threat-model.md` |
| ART-04 | Finding Report | 15 | `templates/finding-report.md` |
| ART-05 | Detection Validation Record | 17 | `templates/detection-validation.md` |
| ART-06 | Hunt Plan and Findings | 18 | `templates/hunt-report.md` |
| ART-07 | Incident Timeline | 20 | `templates/incident-timeline.md` |
| ART-08 | CTI Report | 26 | `templates/cti-report.md` |
| ART-09 | Executive Brief | 26, 29 | `templates/executive-brief.md` |
| ART-10 | Integrated Security Case Map | 1, 29 | `templates/integrated-security-case-map.md` |
| ART-11 | Web/API Assessment Hypothesis Pack | 11 | `templates/web-api-assessment-hypothesis-pack.md` |

`ART-05`は、Threat Hypothesis、Telemetry contract、Detection logic、fixture replay、Evidence、Triage / Incident handoff、Control / Reassessmentを一つの判断記録へ接続する。

第17章の合成記入例は`cases/ch17-detection-validation-example.md`を参照する。オフラインfixtureは`cases/fixtures/ch17-detection-engineering-fixture.md`と`cases/fixtures/ch17-detection-engineering-fixture.json`、合成ruleとrunnerは`detections/cloud_identity/det_2026_017_001.json`と`scripts/replay_chapter17_detection.py`を参照する。

`ART-10`は、他の成果物を置き換えるものではない。Case ID、Hypothesis ID、Evidence ID、Finding ID、Detection ID、Analytic Judgment ID、Decision ID、Reassessment IDを接続する索引兼判断記録である。

第1章の合成記入例は`cases/ch01-integrated-security-case-example.md`を参照する。

`ART-11`は`ART-10`のCase IDとDecision Requirement IDを継承し、Web/API評価のAsset、Boundary、State、Validation、Evidence、Finding、Telemetry、Detection、Reassessmentを接続する。第11章の合成記入例は`cases/ch11-web-api-assessment-example.md`、読み取り専用の合成Datasetは`cases/fixtures/ch11-web-api-assessment-dataset.json`を参照する。

成果物IDは章間・演習・評価ルーブリックで共通利用する。
