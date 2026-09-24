"""Chapter20 artifact ownership, supplied evidence and exact educational claims."""

import json
import os
from pathlib import PurePosixPath
import stat

from scripts.chapter20_timeline import digest, evaluate, instant, prepare, require
from scripts.check_editorial_input_manifest import (
    _reject_constant,
    _reject_duplicate_keys,
    validate_schema_instance,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

DATA = "cases/fixtures/ch20-dfir-timeline-causality.json"
SCHEMA = "schemas/ch20-dfir-timeline-causality.schema.json"
CONTRACT = "tests/fixtures/chapter20/publication-contract.json"
CORPUS = "tests/fixtures/chapter20/timeline-corpus.json"
DOCUMENTS = (
    "manuscript/20-dfir-timeline-causality.md",
    "templates/incident-timeline.md",
    "templates/root-cause-analysis.md",
    "cases/ch20-dfir-timeline-causality-example.md",
    "references/ch20-source-review-2026-09-25.md",
)
SOURCES = ("SRC-NIST-DFIR-001", "SRC-IR-001", "SRC-BERKELEY-001")
PARENTS = (
    "WRITING_GUIDE.md",
    "SOURCE_POLICY.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "manuscript/16-telemetry-evidence-readiness.md",
    "cases/fixtures/ch16-telemetry-coverage.json",
    "manuscript/19-incident-response.md",
    "templates/incident-action-plan.md",
    "cases/ch19-incident-action-plan-example.md",
    "cases/fixtures/ch19-incident-response.json",
    "scripts/content_safety_policy.py",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
    "Gemfile.lock",
    "package-lock.json",
    ".book-formatter/revision.json",
)
INDEX_PATHS = (
    "artifact-index.md",
    "figure-index.md",
    "glossary.md",
    "cases/index.md",
    "cases/fixtures/index.md",
    "README.md",
    "CHANGELOG.md",
    "CANONICAL_SOURCE.md",
)
INPUTS = (
    DATA,
    SCHEMA,
    CONTRACT,
    CORPUS,
    *DOCUMENTS,
    *PARENTS,
    *INDEX_PATHS,
    "package.json",
    "site-pages.json",
    "references/sources.json",
)
# These six authored reading outcomes are independent of the evaluator's output.
# They protect the prose's finite examples even if an expected/digest is refreshed.
CLAIM_OUTCOMES = {
    "TL-DFIR20-A": (
        "undetermined",
        "supported",
        "undetermined",
        "undetermined",
        "contradicted",
        "undetermined",
    ),
    "TL-DFIR20-B": (
        "undetermined",
        "supported",
        "contradicted",
        "undetermined",
        "contradicted",
        "undetermined",
    ),
}


def strict(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def read_regular(root, relative):
    """Fixed bounded input on Linux/WSL2, not a hostile-filesystem sandbox.

    The descriptor prevents final-component symlink/FIFO reads. Ancestor checks
    assume no concurrent hostile rename; no race-proof containment is claimed.
    """
    require(relative in INPUTS and not root.is_symlink(), "fixed input inventory/root")
    root = root.resolve(strict=True)
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        require(not path.is_symlink(), "symlink input/ancestor")
    require(path.resolve(strict=True).is_relative_to(root), "input containment")
    require(
        all(hasattr(os, f) for f in ("O_NOFOLLOW", "O_NONBLOCK")), "Linux/WSL2 flags"
    )
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        require(
            stat.S_ISREG(info.st_mode) and 0 < info.st_size <= 1024 * 1024,
            "bounded regular input",
        )
        raw = stream.read(1024 * 1024 + 1)
    require(len(raw) <= 1024 * 1024, "input size")
    return raw


def leaves(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaves(child, (*path, key))
    elif isinstance(value, list) and value:
        for i, child in enumerate(value):
            yield from leaves(child, (*path, str(i)))
    else:
        yield path, value


def case_groups(data):
    """Every leaf, including original evidence, has a public Artifact row."""
    for key, value in data.items():
        groups = [(key, value)]
        if key in ("sources", "clocks", "evidence", "claims", "snapshots", "handoffs"):
            groups = [(row["id"], row) for row in value]
        for title, group in groups:
            yield (
                title,
                [
                    (
                        "/".join(p) or title,
                        v if isinstance(v, str) else json.dumps(v, ensure_ascii=False),
                    )
                    for p, v in leaves(group)
                ],
            )


def validate_semantics(data):
    """Semantic failures cannot be waived by regenerating the digest snapshot."""
    require(data["record"]["artifactIds"] == ["ART-07", "ART-26"], "artifact ownership")
    require(data["record"]["sourceIds"] == list(SOURCES), "Source IDs")
    owner, lead = data["roles"]["analysisOwner"], data["roles"]["evidenceLead"]
    require(owner.strip() and lead.strip() and owner != lead, "distinct role registry")
    require(data["provenance"]["custodian"] == lead, "custodian role")
    require(
        data["provenance"]["transformations"]
        == [
            "timezone-to-UTC",
            "subtract-declared-offset",
            "closed-uncertainty-interval",
        ],
        "declared transform inventory",
    )
    for key in ("assets", "actors", "sessions"):
        values = data["context"][key]
        require(len(values) == len(set(values)) == 3, "context inventory " + key)
    sources = {s["id"] for s in data["sources"]}
    require(len(sources) == len(data["sources"]) == 4, "source inventory")
    require(
        len(data["clocks"]) == 4 and {c["sourceId"] for c in data["clocks"]} == sources,
        "source/clock inventory",
    )
    for c in data["clocks"]:
        require(
            instant(c["availableAt"])
            <= instant(c["validFrom"])
            < instant(c["validUntil"]),
            "supplied clock premise chronology",
        )
    for source in data["sources"]:
        require(source["custodyRef"] == data["provenance"]["id"], "source preservation")
    clocks, rows, _ = prepare(data)
    require(
        set(rows) == {f"EV20-{i:03}" for i in range(1, 6)}, "five evidence receipts"
    )
    for row in rows.values():
        require(row["sourceId"] in sources, "evidence source registry")
        require(
            row["preservationRef"] == data["provenance"]["id"], "receipt preservation"
        )
    # Literal record-role bindings support the Case's named examples.
    expected_operations = (
        "consent-change",
        "api-read",
        "admin-maintenance",
        "api-read",
        "change-scope",
    )
    for i, operation in enumerate(expected_operations, 1):
        require(
            rows[f"EV20-{i:03}"]["payload"]["operation"] == operation,
            "authored event role",
        )
    require(
        rows["EV20-002"]["sourceId"] == rows["EV20-004"]["sourceId"]
        and rows["EV20-002"]["eventId"] == rows["EV20-004"]["eventId"],
        "authored retransmission",
    )
    claim_ids = [f"CLM20-{i:03}" for i in range(1, 7)]
    require([c["id"] for c in data["claims"]] == claim_ids, "six finite claims/order")
    require(
        len({c["questionId"] for c in data["claims"]}) == 6, "claim question uniqueness"
    )
    require(
        [s["id"] for s in data["snapshots"]] == list(CLAIM_OUTCOMES),
        "two cutoff snapshots",
    )
    previous = None
    for snapshot in data["snapshots"]:
        cutoff = instant(snapshot["cutoff"])
        require(previous is None or previous < cutoff, "snapshot cutoff order")
        previous = cutoff
        result = evaluate(data, snapshot)
        require(result == snapshot["expected"], "literal snapshot expectation")
        require(
            tuple(result["claims"][c]["status"] for c in claim_ids)
            == CLAIM_OUTCOMES[snapshot["id"]],
            "authored reading outcomes",
        )
        rca = snapshot["rca"]
        require(snapshot["owner"] == rca["owner"] == owner, "analysis owner")
        require(rca["timelineId"] == snapshot["id"], "RCA timeline binding")
        require(rca["id"] == snapshot["id"].replace("TL-", "RCA-"), "RCA identity")
        require(
            instant(data["record"]["asOf"]) <= instant(rca["dueAt"]), "RCA due date"
        )
        require(
            rca["triggerEvidenceId"] == "EV20-001"
            and rca["causalClaimId"] == "CLM20-004",
            "RCA trigger/causal role",
        )
        require(
            rca["contributingEvidenceIds"] == ["EV20-001", "EV20-002"]
            and rca["impactEvidenceIds"] == ["EV20-002"],
            "RCA evidence roles",
        )
        require(
            all(
                e in result["included"]
                for e in [
                    rca["triggerEvidenceId"],
                    *rca["contributingEvidenceIds"],
                    *rca["impactEvidenceIds"],
                ]
            ),
            "RCA cutoff evidence",
        )
        require(
            rca["observedScope"] == [rows["EV20-002"]["payload"]["assetId"]]
            and rca["unknownScope"] == ["SYN-DFIR-DATA-D"]
            and not set(rca["observedScope"]) & set(rca["unknownScope"]),
            "RCA scoped impact/unknown",
        )
        require(
            rca["unknownScope"][0] in data["context"]["assets"],
            "unknown scope registry",
        )
        require(
            rca["evidenceGaps"]
            == [
                "GAP20-MECHANISM",
                "GAP20-OTHER-AUTHORITY",
                "GAP20-UNKNOWN-SCOPE",
                "GAP20-CLOCK-ORDER",
            ],
            "RCA retained gaps",
        )
        alt = rca["alternatives"]
        require(
            [(a["id"], a["claimId"]) for a in alt]
            == [
                ("HYP20-MAINT", "CLM20-003"),
                ("HYP20-MISUSE", "CLM20-004"),
                ("HYP20-ORDER", "CLM20-001"),
            ],
            "alternative claim ownership",
        )
        maintenance = result["claims"]["CLM20-003"]["status"]
        require(
            alt[0]["disposition"]
            == {
                "undetermined": "not-yet-testable",
                "contradicted": "contradicted-for-this-change",
            }[maintenance]
            and alt[1]["disposition"] == "not-established"
            and alt[2]["disposition"] == "order-uncertain",
            "alternative result binding",
        )
    last = data["snapshots"][-1]
    require(
        [h["targetChapter"] for h in data["handoffs"]] == [21, 22, 25],
        "handoff inventory",
    )
    require(
        len({h["id"] for h in data["handoffs"]}) == 3
        and len({h["questionId"] for h in data["handoffs"]}) == 3,
        "handoff unique IDs",
    )
    for h in data["handoffs"]:
        require(
            h["owner"] == owner
            and h["sourceTimelineId"] == last["id"]
            and h["sourceRcaId"] == last["rca"]["id"]
            and h["controlId"] == last["rca"]["controlId"],
            "handoff direct binding",
        )
        require(
            instant(data["record"]["asOf"]) <= instant(h["dueAt"]), "handoff due date"
        )
    return []


def validate_model(data, schema, contract):
    validate_schema_instance(data, schema)
    errors = validate_semantics(data)
    for path, value in leaves(data):
        if isinstance(value, str):
            location = DATA + ":" + "/".join(path)
            errors += [
                f"{location}: {f.category}"
                for f in (
                    *scan_action_text(value, location=location),
                    *scan_host_policy(value, location=location),
                )
            ]
    require(list(contract["authoredInputs"]) == list(data), "authored input inventory")
    for key, value in data.items():
        if digest(value) != contract["authoredInputs"][key]:
            errors.append("DFIR20 reviewed input representation: " + key)
    return errors
