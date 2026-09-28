#!/usr/bin/env python3
"""Part IV finite cross-record/reader boundary, not a chapter or STIX evaluator."""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.check_editorial_input_manifest import (  # noqa: E402
    ManifestError,
    _reject_constant,
    _reject_duplicate_keys,
)
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION,
    scan_action_text,
    scan_host_policy,
)
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION,
    ProjectionRuntimeError,
    project_documents,
    is_policy_scan_field,
    is_absolute_destination,
)

VERSION = "1.0.0"
DOCUMENT = "cases/part-iv-intelligence-decision-map.md"
CONTRACT = "tests/fixtures/part04/publication-contract.json"
CORPUS = "tests/fixtures/part04/counterexamples.json"
SOURCES = {
    23: "cases/fixtures/ch23-intelligence-requirements.json",
    24: "cases/fixtures/ch24-source-evaluation.json",
    25: "cases/fixtures/ch25-structured-analysis-attribution-dataset.json",
    26: "cases/fixtures/ch26-cti-distribution.json",
    "stix": "cases/fixtures/ch26-stix-bundle.json",
    "taxii": "cases/fixtures/ch26-taxii-exchange.json",
}
INPUTS = (
    *SOURCES.values(),
    DOCUMENT,
    CONTRACT,
    CORPUS,
    "package.json",
    "site-pages.json",
    "cases/index.md",
)
ROUTE = {
    "source": DOCUMENT,
    "destination": "cases/part-iv-intelligence-decision-map/index.md",
    "section": "additional",
    "order": 330,
    "title": "第IV部 横断読解：要求から配布と判断へ",
}
PREFLIGHT = "python3 scripts/check_part04_contract.py --no-regressions"


def read_regular(root, relative):
    """Read only declared UTF-8 files; not a hostile concurrent-FS sandbox."""
    if relative not in INPUTS or root.is_symlink():
        raise ValueError("P4-fixed-input")
    path = root / relative
    if any(p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root)):
        raise ValueError("P4-symlink-input")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("P4-regular-input")
        raw = stream.read(1048577)
    if len(raw) > 1048576:
        raise ValueError("P4-input-size")
    return raw.decode("utf-8")


def load(root, path):
    return json.loads(
        read_regular(root, path),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def same(a, b):
    return json.dumps(
        a, sort_keys=True, ensure_ascii=False, allow_nan=False
    ) == json.dumps(b, sort_keys=True, ensure_ascii=False, allow_nan=False)


def at(value, path):
    for key in path:
        value = value[key]
    return value


def boundaries(data):
    """Authored boundary literals, followed by producer/consumer bindings.

    These observations describe supplied records, not a new evaluation of their
    evidence. Chapter validators continue to own internal schema and semantics.
    """
    checks = []

    def fixed(source, prefix, **values):
        for key, value in values.items():
            path = (source, *prefix, key)
            checks.append(("P4-" + "/".join(map(str, path)), path, value))

    def link(source, path, parent, parent_path):
        checks.append(
            (
                "P4-link-" + "/".join(map(str, (source, *path))),
                (source, *path),
                at(data[parent], parent_path),
            )
        )

    for n in (23, 24, 26):
        fixed(
            n,
            (),
            synthetic=True,
            readOnly=True,
            networkRequired=False,
            executionAuthorized=False,
        )
    fixed(
        25,
        (),
        synthetic=True,
        caseId="CASE-2026-025",
        artifactId="ART-12",
        intelligenceRequirementId="IR-2026-025",
        decisionRequirementId="DR-2026-025",
        analyticJudgmentId="AJ-2026-025",
        decisionId="DEC-2026-025",
        reassessmentId="REA-2026-025",
    )
    fixed(
        23,
        ("record",),
        id="IRCP-2026-023-001",
        artifactId="ART-29",
        caseId="CASE-IRP-2026-001",
        actualCollections=0,
        actualActions=0,
        actualNotifications=0,
    )
    fixed(
        23,
        ("parents",),
        use="method-reference-only",
        subjectInherited=False,
        evidenceTransferred=False,
        authorityTransferred=False,
        incidentDeclared=False,
        parentStateChanged=False,
    )
    fixed(
        23,
        ("decision",),
        id="DEC-IR23-001",
        owner="ROLE-IR23-DECISION-OWNER",
        openedAt="2026-10-01T00:00:00Z",
        deadline="2026-10-03T00:00:00Z",
    )
    fixed(
        23,
        ("pipeline",),
        deliveryStatus="planned-not-delivered",
        receiptId=None,
        processingDeadline="2026-10-02T18:00:00Z",
        analysisDeadline="2026-10-02T21:00:00Z",
        distributionDeadline="2026-10-02T22:00:00Z",
    )
    for i, status in enumerate(
        ("Satisfied", "Partially satisfied", "Collecting", "Planned", "Blocked")
    ):
        fixed(
            23,
            ("requirements", i),
            id=f"IR23-R{i + 1}",
            status=status,
            decisionId="DEC-IR23-001",
        )
    for i, chapter in enumerate((24, 25, 26)):
        fixed(
            23,
            ("handoffs", i),
            id=f"HOF-IR23-{chapter}",
            targetChapter=chapter,
            status="planned-not-delivered",
            receiptId=None,
            executionAuthorized=False,
            owner="ROLE-IR23-ANALYSIS",
            deadline="2026-10-02T22:00:00Z",
        )
    fixed(
        24,
        ("record",),
        id="EST-2026-024-001",
        artifactId="ART-30",
        caseId="CASE-OS24-001",
        relationship="independent",
        decisionId="DR-OS24-001",
        asOf="2026-10-04T03:00:00Z",
        decisionDeadline="2026-10-05T03:00:00Z",
        actualCollections=0,
        actualActions=0,
        actualNotifications=0,
        parentEvidenceInherited=False,
        parentAuthorityInherited=False,
        realWorldTruthCertified=False,
    )
    for i, chapter, ident in (
        (0, 10, "ASR-2026-010"),
        (1, 23, "IRCP-2026-023-001"),
        (2, 25, "ART-12"),
    ):
        fixed(
            24,
            ("methodReferences", i),
            id=f"REF-EV24-{chapter:03}",
            chapter=chapter,
            recordId=ident,
            relationship="method-reference-only",
            received=False,
        )
    for i, item, claim, use, credibility in (
        (5, 6, 3, "Direct evidence", "supported"),
        (9, 6, 4, "Direct evidence", "supported"),
        (8, 9, 3, "Lead", "limited"),
        (10, 9, 4, "Lead", "limited"),
        (7, 8, 4, "Excluded", "unverified"),
    ):
        fixed(
            24,
            ("evaluations", i),
            id=f"EV-EV24-{i + 1:03}",
            itemId=f"ITEM-EV24-{item:03}",
            claimId=f"CLM-EV24-{claim:03}",
            use=use,
        )
        fixed(24, ("evaluations", i, "credibility"), value=credibility)
    for i, chapter in enumerate((25, 26)):
        fixed(
            24,
            ("handoffs", i),
            id=f"HOF-EV24-{chapter}",
            chapter=chapter,
            status="planned-not-delivered",
            receipt=None,
            executionAuthorized=False,
            evidenceIds=[f"EV-EV24-{j:03}" for j in range(1, 12)],
            gapIds=[f"GAP-EV24-{j:03}" for j in range(1, 12)],
            deadline="2026-10-05T01:00:00Z",
        )
    fixed(25, ("attributionAssessment",), ladderLevel="L2", confidence="中")
    fixed(25, ("sourceEvaluationJudgments", 0), id="SEJ-2026-025-001")
    fixed(
        25, ("reassessment",), id="REA-2026-025", reviewDate="2026-08-08T10:00:00+09:00"
    )
    fixed(
        25,
        ("lineage", "circularReportingCandidates", 0),
        id="CR-2026-025-001",
        sourceNoteIds=[f"SN-2026-025-{j:03}" for j in (4, 5, 7)],
        sameOriginRepublication=True,
        doNotCountAsIndependent=True,
    )
    for i, (a, b, relation) in enumerate(
        ((4, 5, "republishes"), (4, 7, "derived-from"), (5, 7, "cites"))
    ):
        fixed(
            25,
            ("lineage", "edges", i),
            id=f"LIN-2026-025-{i + 1:03}",
            **{"from": f"SN-2026-025-{a:03}", "to": f"SN-2026-025-{b:03}"},
            relationship=relation,
            independenceEffect="counts-as-same",
        )
    fixed(
        25,
        ("negativeFindings", 0),
        id="NEG-2026-025-001",
        relatedEvidenceIds=["EVD-2026-025-008"],
        gapId="GAP-2026-025-001",
    )
    fixed(
        26,
        ("record",),
        id="CDP-2026-026-001",
        relation="refines",
        asOf="2026-07-29T11:00:00Z",
        cutoff="2026-07-29T09:00:00Z",
        deadline="2026-07-30T01:00:00Z",
        attributionCeiling="L2",
    )
    for key, parent in (
        ("caseId", "caseId"),
        ("parentCaseId", "caseId"),
        ("parentArtifactId", "artifactId"),
        ("parentJudgmentId", "analyticJudgmentId"),
        ("parentDecisionId", "decisionId"),
    ):
        link(26, ("record", key), 25, (parent,))
    link(26, ("requirement", "id"), 25, ("intelligenceRequirementId",))
    link(26, ("requirement", "decisionRequirementId"), 25, ("decisionRequirementId",))
    fixed(26, ("requirement",), owner="SYNTH-CISO")
    for i, chapter, artifact, record in (
        (0, 23, "ART-29", "IRCP-2026-023-001"),
        (1, 24, "ART-30", "EST-2026-024-001"),
    ):
        fixed(
            26,
            ("methodReferences", i),
            id=f"MREF-CTI26-{chapter:03}",
            chapter=chapter,
            artifactId=artifact,
            recordId=record,
            relation="method-only",
            evidenceReceived=False,
            receiptId=None,
        )
        link(26, ("methodReferences", i, "recordId"), chapter, ("record", "id"))
        link(
            26, ("methodReferences", i, "artifactId"), chapter, ("record", "artifactId")
        )
    link(24, ("methodReferences", 1, "recordId"), 23, ("record", "id"))
    link(24, ("methodReferences", 2, "recordId"), 25, ("artifactId",))
    groups = (
        "IG-INT-001",
        "IG-INT-002",
        "IG-EXT-001",
        "IG-EXT-002",
        "IG-EXT-002",
        "IG-EXT-003",
        "IG-EXT-002",
        "IG-INT-003",
    )
    for i, group in enumerate(groups):
        fixed(
            25,
            ("sourceNotes", i),
            id=f"SN-2026-025-{i + 1:03}",
            independenceGroupId=group,
            synthetic=True,
        )
        fixed(
            25,
            ("evidence", i),
            id=f"EVD-2026-025-{i + 1:03}",
            sourceNoteId=f"SN-2026-025-{i + 1:03}",
        )
        fixed(
            26,
            ("evidence", i),
            parentArtifactId="ART-12",
            synthetic=True,
            newObservation=False,
        )
        link(26, ("evidence", i, "id"), 25, ("evidence", i, "id"))
        link(26, ("evidence", i, "sourceId"), 25, ("evidence", i, "sourceNoteId"))
        link(
            26,
            ("evidence", i, "independenceGroupId"),
            25,
            ("sourceNotes", i, "independenceGroupId"),
        )
    # KJ001 carries all three parent alternatives. KJ002/003 are supplied
    # child-local alternatives, not additional Chapter 25 hypotheses.
    for i in range(3):
        fixed(
            25,
            ("alternativeHypotheses", i),
            id=f"ALT-2026-025-{i + 1:03}",
        )
        link(
            26,
            ("judgments", 0, "alternativeIds", i),
            25,
            ("alternativeHypotheses", i, "id"),
        )
    for i, alternatives in enumerate(
        (
            [f"ALT-2026-025-{j:03}" for j in (1, 2, 3)],
            ["ALT-CTI26-SUCCESS", "ALT-CTI26-NO-SUCCESS"],
            ["ALT-CTI26-NEW-ORIGIN"],
        )
    ):
        fixed(26, ("judgments", i), alternativeIds=alternatives)
    for i, parent, confidence, evidence, gaps, origins in (
        (0, "AJ-2026-025", "中", (1, 2, 3, 4), (3, 4), 4),
        (1, "AJ-2026-025", "低", (8,), (1,), 1),
        (2, "SEJ-2026-025-001", "中", (4, 5, 7), (2,), 1),
    ):
        fixed(
            26,
            ("judgments", i),
            id=f"KJ-CTI26-{i + 1:03}",
            parentJudgmentId=parent,
            confidence=confidence,
            evidenceIds=[f"EVD-2026-025-{j:03}" for j in evidence],
            sourceIds=[f"SN-2026-025-{j:03}" for j in evidence],
            gapIds=[f"GAP-2026-025-{j:03}" for j in gaps],
            attributionLevel="L2",
            successDetermined=False,
            stixConfidence=None,
            independentOrigins=origins,
        )
        link(
            26,
            ("judgments", i, "parentJudgmentId"),
            25,
            ("analyticJudgmentId",)
            if i < 2
            else ("sourceEvaluationJudgments", 0, "id"),
        )
    for i in range(3):
        fixed(
            26,
            ("recommendations", i),
            id=f"REC-CTI26-{i + 1:03}",
            parentRecommendationId=f"REC-2026-025-{i + 1:03}",
            executionStatus="not-executed",
            authorityGranted=False,
        )
    for i, suffix, artifact, audience, purpose in (
        (0, "TECH", "ART-08", "SYNTH-SOC Lead", "tactical-operational"),
        (1, "EXEC", "ART-09", "SYNTH-CISO", "strategic"),
    ):
        fixed(
            26,
            ("products", i),
            id=f"PRD-CTI26-{suffix}",
            artifactId=artifact,
            audience=audience,
            purpose=purpose,
            version=1,
            requirementId="IR-2026-025",
            status="prepared-not-delivered",
            cutoff="2026-07-29T09:00:00Z",
            preparedAt="2026-07-29T10:00:00Z",
            deadline="2026-07-30T01:00:00Z",
            expiresAt="2026-07-30T01:00:00Z",
            judgmentIds=[f"KJ-CTI26-{j:03}" for j in (1, 2, 3)],
            recommendationIds=[f"REC-CTI26-{j:03}" for j in (1, 2, 3)],
            sharingLabel="TLP:CLEAR",
            actionPermission=False,
            delivered=False,
            receiptId=None,
            stixObjectIds=[],
            feedbackId=f"FDB-CTI26-{suffix}",
            reassessmentId="REA-CTI26-001",
            supersedes=None,
        )
        fixed(
            26,
            ("feedback", i),
            id=f"FDB-CTI26-{suffix}",
            productId=f"PRD-CTI26-{suffix}",
            audience=audience,
            status="planned-not-received",
            answer=None,
            receiptId=None,
        )
        link(26, ("products", i, "requirementId"), 25, ("intelligenceRequirementId",))
    fixed(
        26,
        ("decision",),
        id="DEC-CTI26-001",
        status="synthetic-representation",
        parentDecisionId="DEC-2026-025",
        selectedOptionId="OPT-CTI26-A",
        productId="PRD-CTI26-EXEC",
        authorityGranted=False,
        executed=False,
    )
    link(26, ("decision", "parentDecisionId"), 25, ("decisionId",))
    fixed(
        26,
        ("reassessment",),
        id="REA-CTI26-001",
        parentReassessmentId="REA-2026-025",
        at="2026-07-30T00:30:00Z",
        supersedingProductId=None,
        stixObjectRevoked=False,
    )
    link(26, ("reassessment", "parentReassessmentId"), 25, ("reassessmentId",))
    fixed(
        26,
        ("handoff",),
        id="HOF-CTI26-029",
        chapter=29,
        productIds=["PRD-CTI26-TECH", "PRD-CTI26-EXEC"],
        status="planned-not-delivered",
        receiptId=None,
        authorityGranted=False,
    )
    fixed(
        26,
        ("exchangeExample",),
        id="CASE-STIX26-DEMO",
        relation="independent",
        purpose="structure-only-not-evidence",
        adoptedEvidenceIds=[],
        contributesToJudgment=False,
        networkExecuted=False,
        bundleProfile="STIX21-STRUCTURE-ONLY",
        taxiiProfile="TAXII21-OFFLINE-ONLY",
    )
    fixed("taxii", (), synthetic=True, networkExecuted=False, caseId="CASE-STIX26-DEMO")
    fixed("taxii", ("collection",), can_read=True, can_write=False)
    fixed("taxii", ("response",), status=200)
    fixed("stix", (), type="bundle", id="bundle--2e2ba4f9-3ce8-4fd5-9f99-71a7c4f7a42c")
    link("taxii", ("caseId",), 26, ("exchangeExample", "id"))
    return checks


def boundary_errors(data):
    if set(data) != set(SOURCES):
        return ["P4-source-inventory"]
    errors = []
    try:
        for label, path, value in boundaries(data):
            try:
                if not same(at(data, path), value):
                    errors.append(label)
            except (KeyError, IndexError, TypeError):
                errors.append(label)
        # Exact supplied inventories, not general STIX/TAXII conformance.
        for n, key, count in (
            (23, "requirements", 5),
            (23, "collections", 8),
            (24, "evaluations", 11),
            (24, "handoffs", 2),
            (25, "evidence", 8),
            (25, "alternativeHypotheses", 3),
            (26, "evidence", 8),
            (26, "products", 2),
            (26, "judgments", 3),
            ("stix", "objects", 13),
        ):
            if type(data[n][key]) is not list or len(data[n][key]) != count:
                errors.append(f"P4-inventory-{n}-{key}")
        if not same(
            data["stix"]["objects"], data["taxii"]["response"]["envelope"]["objects"]
        ):
            errors.append("P4-exchange-object-binding")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        errors.append("P4-reference-shape: " + str(exc))
    return errors


def field_inventory(document):
    return [
        [f.field_type, f.element_kind, f.attribute, f.metadata_value("level"), f.text]
        for f in document.fields
    ]


def scan_errors(document):
    errors = [f"{d.location}: {d.code}" for d in document.diagnostics]
    for field in document.fields:
        findings = []
        if is_policy_scan_field(field):
            findings += scan_action_text(field.normalized_text, location=field.location)
        if is_policy_scan_field(field) or (
            field.field_type == "destination"
            and is_absolute_destination(field.normalized_text)
        ):
            findings += scan_host_policy(field.normalized_text, location=field.location)
        errors += [f"{f.location}: {f.category}" for f in findings]
    return errors


def document_errors(document, contract):
    return scan_errors(document) + (
        [] if field_inventory(document) == contract["fields"] else ["P4-reader-fields"]
    )


def repository_errors(root, contract):
    errors = []
    scripts = load(root, "package.json")["scripts"]
    steps = scripts["sync:docs"].split(" && ")
    if (
        scripts.get("check:part04") != "python3 scripts/check_part04_contract.py"
        or scripts["test"].split(" && ").count("npm run check:part04") != 1
        or steps.count(PREFLIGHT) != 1
        or steps[-5:]
        != [
            PREFLIGHT,
            "python3 scripts/check_part03_contract.py --no-regressions",
            "python3 scripts/check_part02_contract.py --no-regressions",
            "python3 scripts/sync_book_site.py --output docs",
            "npm run copy:notices",
        ]
    ):
        errors.append("P4-entrypoints")
    pages = load(root, "site-pages.json")["pages"]
    if (
        pages.count(ROUTE) != 1
        or sum(p["source"] == DOCUMENT for p in pages) != 1
        or sum(p["destination"] == ROUTE["destination"] for p in pages) != 1
    ):
        errors.append("P4-route")
    if f"({DOCUMENT.removeprefix('cases/')})" not in read_regular(
        root, "cases/index.md"
    ):
        errors.append("P4-reader-entry")
    if any(
        contract.get(k) != v
        for k, v in (
            ("version", VERSION),
            ("projection", PROJECTION_VERSION),
            ("policy", POLICY_VERSION),
            ("sourceFiles", list(SOURCES.values())),
        )
    ):
        errors.append("P4-contract-owner")
    return errors


def regressions(data, document, contract, corpus):
    passed = []

    def check(label, condition):
        if not condition:
            raise ValueError("P4-regression: " + label)
        passed.append(label)

    check(
        "canonical",
        not boundary_errors(data) and not document_errors(document, contract),
    )
    check("source-order", not boundary_errors(dict(reversed(list(data.items())))))
    check("typed-json", not same(False, 0) and not same(True, 1))
    labels = [label for label, _, _ in boundaries(data)]
    check("unique-boundary-labels", len(labels) == len(set(labels)))
    for label, path, _ in boundaries(data):
        changed = deepcopy(data)
        del at(changed, path[:-1])[path[-1]]
        check(label + "-missing", bool(boundary_errors(changed)))
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = "not-the-supplied-value"
        check(label + "-changed", label in boundary_errors(changed))
    for probe in corpus["records"]:
        changed = deepcopy(data)
        for mutation in probe["mutations"]:
            path = (mutation["source"], *mutation["path"])
            at(changed, path[:-1])[path[-1]] = mutation["value"]
        check(probe["id"], probe["expectedCode"] in boundary_errors(changed))
    for i in range(len(document.fields)):
        changed = replace(
            document, fields=document.fields[:i] + document.fields[i + 1 :]
        )
        check(
            f"field-{i}-missing",
            "P4-reader-fields" in document_errors(changed, contract),
        )
    projected = project_documents(
        [(p["id"], p["source"]) for p in corpus["publication"]]
    )
    for probe in corpus["publication"]:
        doc = projected.document(probe["id"])
        findings = scan_errors(doc)
        check(probe["id"], bool(findings) == probe["unsafe"])
        check(
            probe["id"] + "-diagnostics",
            [d.code for d in doc.diagnostics] == probe["diagnosticCodes"],
        )
        if probe["findingCategory"]:
            check(
                probe["id"] + "-category",
                any(f.endswith(": " + probe["findingCategory"]) for f in findings),
            )
    all_probes = corpus["records"] + corpus["publication"]
    ids = [p["id"] for p in all_probes]
    check(
        "corpus-owner",
        corpus["version"] == VERSION
        and len(ids) == len(set(ids))
        and all(p.get("invariant") for p in all_probes),
    )
    check(
        "corpus-count",
        len(corpus["records"]) == 42 and len(corpus["publication"]) == 12,
    )
    check("boundary-count", len(labels) == 442)
    scratch = ROOT / ".tmp"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="part04-input-", dir=scratch) as directory:
        root = Path(directory)
        path = root / SOURCES[23]
        path.parent.mkdir(parents=True)

        def rejected(label, operation):
            try:
                operation()
            except (OSError, ValueError, ManifestError):
                check(label, True)
            else:
                check(label, False)

        for label, raw in (
            ("duplicate-key", b'{"a":1,"a":2}'),
            ("non-finite", b'{"a":NaN}'),
            ("invalid-utf8", b"\xff"),
            ("oversize", b" " * 1048577),
        ):
            path.write_bytes(raw)
            rejected(label, lambda: load(root, SOURCES[23]))
        path.unlink()
        rejected("missing-file", lambda: read_regular(root, SOURCES[23]))
        path.symlink_to(root / "absent")
        rejected("symlink", lambda: read_regular(root, SOURCES[23]))
        path.unlink()
        os.mkfifo(path)
        rejected("fifo", lambda: read_regular(root, SOURCES[23]))
        path.unlink()
        rejected("unowned-path", lambda: read_regular(root, "../outside.json"))
        path.write_text('{"ok":true}', encoding="utf-8")
        check("valid-input", load(root, SOURCES[23]) == {"ok": True})
    return passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        data = {n: load(ROOT, p) for n, p in SOURCES.items()}
        contract = load(ROOT, CONTRACT)
        document = project_documents({DOCUMENT: read_regular(ROOT, DOCUMENT)}).document(
            DOCUMENT
        )
        errors = (
            boundary_errors(data)
            + document_errors(document, contract)
            + repository_errors(ROOT, contract)
        )
        if errors:
            raise ValueError("; ".join(errors))
        passed = (
            []
            if args.no_regressions
            else regressions(data, document, contract, load(ROOT, CORPUS))
        )
        print(
            f"Part IV contract passed: {len(boundaries(data))} boundary observations; "
            f"{len(document.fields)} typed fields; {len(passed)} finite regressions; "
            f"Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; "
            "references are not evidence receipt, delivery or authority."
        )
        return 0
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        ManifestError,
        ProjectionRuntimeError,
    ) as exc:
        print(f"Part IV contract failed closed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
