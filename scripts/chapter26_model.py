"""Finite authored CTI product and independent exchange profile (Layer A).

Not a general STIX/TAXII validator, parser, truth engine or authorization system.
Rendering and action/host grammar belong exclusively to the shared owners.
"""

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import PurePosixPath
import stat
from uuid import UUID, uuid5

from scripts.check_editorial_input_manifest import (
    _reject_constant,
    _reject_duplicate_keys,
    validate_schema_instance,
    validate_supported_schema_nodes,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

VERSION = "1.0.0"
DATA = "cases/fixtures/ch26-cti-distribution.json"
BUNDLE = "cases/fixtures/ch26-stix-bundle.json"
TAXII = "cases/fixtures/ch26-taxii-exchange.json"
SCHEMAS = tuple(
    p.replace("cases/fixtures/", "schemas/").replace(".json", ".schema.json")
    for p in (DATA, BUNDLE, TAXII)
)
CONTRACT = "tests/fixtures/chapter26/publication-contract.json"
CORPUS = "tests/fixtures/chapter26/comparison-corpus.json"
DOCUMENTS = (
    "manuscript/26-cti-distribution.md",
    "templates/cti-report.md",
    "templates/executive-brief.md",
    "cases/ch26-cti-distribution-example.md",
    "references/ch26-source-review-2026-09-28.md",
)
SOURCES = (
    "SRC-STIX-001",
    "SRC-TAXII-001",
    "SRC-ATTACK-001",
    "SRC-ICD203-001",
    "SRC-TLP-001",
)
PARENT_DATA = "cases/fixtures/ch25-structured-analysis-attribution-dataset.json"
PARENTS = (
    "WRITING_GUIDE.md",
    "SOURCE_POLICY.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "manuscript/23-intelligence-requirements.md",
    "cases/fixtures/ch23-intelligence-requirements.json",
    "manuscript/24-osint-provenance-sources.md",
    "cases/fixtures/ch24-source-evaluation.json",
    "manuscript/25-structured-analysis-attribution.md",
    PARENT_DATA,
    "cases/ch25-structured-analysis-attribution-example.md",
    "templates/analytic-judgment-record.md",
    "scripts/content_safety_policy.py",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
    "scripts/sync_site_source.py",
    "scripts/sync_book_site.py",
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
    BUNDLE,
    TAXII,
    *SCHEMAS,
    CONTRACT,
    CORPUS,
    *DOCUMENTS,
    *PARENTS,
    *INDEX_PATHS,
    "package.json",
    "site-pages.json",
    "references/sources.json",
    "book-config.json",
)


def require(condition, label):
    if not condition:
        raise ValueError("CTI26: " + label)


def strict(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


def read_regular(root, relative):
    """Bounded fixed inputs; not protection against concurrent hostile renames."""
    require(relative in INPUTS and not root.is_symlink(), "fixed input/root")
    root = root.resolve(strict=True)
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        require(not path.is_symlink(), "symlink input/ancestor")
    require(path.resolve(strict=True).is_relative_to(root), "input containment")
    require(
        hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_NONBLOCK"),
        "POSIX input flags required",
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


def instant(value, milliseconds=False):
    fmt = "%Y-%m-%dT%H:%M:%S.000Z" if milliseconds else "%Y-%m-%dT%H:%M:%SZ"
    require(type(value) is str, "UTC format")
    result = datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
    require(
        2000 <= result.year <= 2099 and result.strftime(fmt) == value, "canonical UTC"
    )
    return result


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
    for key, value in data.items():
        groups = (
            [(row["id"], row) for row in value]
            if isinstance(value, list)
            else [(key, value)]
        )
        for title, group in groups:
            yield (
                title,
                [
                    (
                        "/".join(path) or "value",
                        json.dumps(v, ensure_ascii=False, separators=(",", ":"))
                        if not isinstance(v, str)
                        else v,
                    )
                    for path, v in leaves(group)
                ],
            )


def idset(values, label):
    require(
        type(values) is list
        and all(type(v) is str for v in values)
        and len(values) == len(set(values)),
        label + " unique refs",
    )
    return set(values)


def by_id(rows, label):
    ids = [r["id"] for r in rows]
    idset(ids, label)
    return dict(zip(ids, rows, strict=True))


def seq(prefix, numbers):
    return {f"{prefix}-2026-025-{n:03}" for n in numbers}


def evaluate(data):
    """Validate finite bindings independently of snapshots; no prose truth inference."""
    require(data["schemaVersion"] == VERSION, "model version")
    for k, v in (
        ("synthetic", True),
        ("readOnly", True),
        ("networkRequired", False),
        ("executionAuthorized", False),
    ):
        require(data[k] is v, "safety flags")
    r = data["record"]
    expected = {
        "id": "CDP-2026-026-001",
        "caseId": "CASE-2026-025",
        "parentCaseId": "CASE-2026-025",
        "relation": "refines",
        "parentArtifactId": "ART-12",
        "parentJudgmentId": "AJ-2026-025",
        "parentDecisionId": "DEC-2026-025",
        "attributionCeiling": "L2",
    }
    require(
        all(r[k] == v for k, v in expected.items()), "parent identity / attribution"
    )
    require(
        r["cutoff"] == "2026-07-29T09:00:00Z"
        and r["deadline"] == "2026-07-30T01:00:00Z",
        "parent cutoff/deadline",
    )
    require(
        instant(r["cutoff"]) <= instant(r["asOf"]) < instant(r["deadline"]),
        "record time order",
    )
    q = data["requirement"]
    require(
        q["id"] == "IR-2026-025"
        and q["decisionRequirementId"] == "DR-2026-025"
        and q["owner"] == "SYNTH-CISO",
        "requirement identity",
    )
    methods = by_id(data["methodReferences"], "methods")
    require(set(methods) == {"MREF-CTI26-023", "MREF-CTI26-024"}, "method inventory")
    for n, artifact, record in (
        (23, "ART-29", "IRCP-2026-023-001"),
        (24, "ART-30", "EST-2026-024-001"),
    ):
        m = methods[f"MREF-CTI26-{n:03}"]
        require(
            m["chapter"] == n
            and m["artifactId"] == artifact
            and m["recordId"] == record
            and m["relation"] == "method-only"
            and m["evidenceReceived"] is False
            and m["receiptId"] is None,
            "method-only noninheritance",
        )
    evidence = by_id(data["evidence"], "evidence")
    require(set(evidence) == seq("EVD", range(1, 9)), "parent evidence inventory")
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
    for n, group in enumerate(groups, 1):
        e = evidence[f"EVD-2026-025-{n:03}"]
        require(
            e["sourceId"] == f"SN-2026-025-{n:03}"
            and e["parentArtifactId"] == "ART-12"
            and e["independenceGroupId"] == group
            and e["synthetic"] is True
            and e["newObservation"] is False,
            "evidence/source/origin binding",
        )
    alternatives = by_id(data["alternatives"], "alternatives")
    require(
        set(alternatives)
        == {"ALT-CTI26-SUCCESS", "ALT-CTI26-NO-SUCCESS", "ALT-CTI26-NEW-ORIGIN"},
        "focused alternative inventory",
    )
    for aid, focus, parent, ev, gaps, state in (
        (
            "ALT-CTI26-SUCCESS",
            "Q-CTI26-FOLLOWON",
            "TH-2026-025-003",
            (8,),
            (1,),
            "unresolved",
        ),
        (
            "ALT-CTI26-NO-SUCCESS",
            "Q-CTI26-FOLLOWON",
            "TH-2026-025-003",
            (8,),
            (1,),
            "unresolved",
        ),
        (
            "ALT-CTI26-NEW-ORIGIN",
            "Q-CTI26-ORIGINS",
            "SEH-2026-025-001",
            (4, 5, 7),
            (2,),
            "not-supported-by-supplied-lineage",
        ),
    ):
        a = alternatives[aid]
        require(
            a["focusQuestion"] == focus
            and a["parentHypothesisId"] == parent
            and a["disposition"] == state
            and idset(a["evidenceIds"], "alternative evidence") == seq("EVD", ev)
            and idset(a["gapIds"], "alternative gaps") == seq("GAP", gaps),
            "alternative focus/binding",
        )
    judgments = by_id(data["judgments"], "judgments")
    require(
        set(judgments) == {f"KJ-CTI26-{n:03}" for n in (1, 2, 3)}, "judgment inventory"
    )
    for n, ev, gaps, alternative_ids, confidence, parent in (
        (1, (1, 2, 3, 4), (3, 4), seq("ALT", (1, 2, 3)), "中", "AJ-2026-025"),
        (
            2,
            (8,),
            (1,),
            {"ALT-CTI26-SUCCESS", "ALT-CTI26-NO-SUCCESS"},
            "低",
            "AJ-2026-025",
        ),
        (3, (4, 5, 7), (2,), {"ALT-CTI26-NEW-ORIGIN"}, "中", "SEJ-2026-025-001"),
    ):
        j = judgments[f"KJ-CTI26-{n:03}"]
        require(
            idset(j["evidenceIds"], "judgment evidence") == seq("EVD", ev)
            and idset(j["sourceIds"], "judgment source") == seq("SN", ev),
            "judgment evidence/source binding",
        )
        require(
            idset(j["gapIds"], "gaps") == seq("GAP", gaps)
            and idset(j["alternativeIds"], "alternatives") == alternative_ids,
            "judgment gap/alternative binding",
        )
        require(
            j["parentJudgmentId"] == parent
            and j["confidence"] == confidence
            and j["attributionLevel"] == "L2"
            and j["successDetermined"] is False
            and j["stixConfidence"] is None,
            "judgment boundary/confidence",
        )
        origins = {evidence[e]["independenceGroupId"] for e in j["evidenceIds"]}
        require(
            type(j["independentOrigins"]) is int
            and j["independentOrigins"] == len(origins),
            "independent origin count",
        )
    recs = by_id(data["recommendations"], "recommendations")
    require(
        set(recs) == {f"REC-CTI26-{n:03}" for n in (1, 2, 3)},
        "recommendation inventory",
    )
    for n, purpose, owner in (
        (1, "tactical", "SYNTH-SOC Lead"),
        (2, "operational", "SYNTH-Identity Lead"),
        (3, "strategic", "SYNTH-CISO"),
    ):
        rec = recs[f"REC-CTI26-{n:03}"]
        require(
            rec["purpose"] == purpose
            and rec["owner"] == owner
            and rec["parentRecommendationId"] == f"REC-2026-025-{n:03}"
            and rec["judgmentIds"] == [f"KJ-CTI26-{n:03}"],
            "recommendation binding",
        )
        require(
            rec["executionStatus"] == "not-executed"
            and rec["authorityGranted"] is False,
            "recommendation not authority",
        )
    products = by_id(data["products"], "products")
    require(
        set(products) == {"PRD-CTI26-TECH", "PRD-CTI26-EXEC"}, "two product inventory"
    )
    feedback = by_id(data["feedback"], "feedback")
    require(set(feedback) == {"FDB-CTI26-TECH", "FDB-CTI26-EXEC"}, "feedback inventory")
    for suffix, artifact, audience, purpose in (
        ("TECH", "ART-08", "SYNTH-SOC Lead", "tactical-operational"),
        ("EXEC", "ART-09", "SYNTH-CISO", "strategic"),
    ):
        p = products["PRD-CTI26-" + suffix]
        require(
            p["artifactId"] == artifact
            and p["audience"] == audience
            and p["purpose"] == purpose
            and p["requirementId"] == q["id"],
            "product audience/artifact/purpose",
        )
        require(
            p["status"] == "prepared-not-delivered"
            and p["delivered"] is False
            and p["receiptId"] is None
            and p["actionPermission"] is False,
            "product not delivered/authorized",
        )
        require(
            type(p["version"]) is int
            and p["version"] == 1
            and p["supersedes"] is None
            and p["stixObjectIds"] == [],
            "product version / independent demo not evidence",
        )
        require(
            p["cutoff"] == r["cutoff"]
            and p["deadline"] == r["deadline"]
            and instant(p["cutoff"])
            <= instant(p["preparedAt"])
            <= instant(r["asOf"])
            < instant(p["expiresAt"])
            <= instant(p["deadline"]),
            "product temporal boundary",
        )
        require(
            idset(p["judgmentIds"], "product judgments") == set(judgments)
            and idset(p["recommendationIds"], "product recommendations") == set(recs),
            "same evidence two products",
        )
        require(
            p["sharingLabel"] == "TLP:CLEAR"
            and p["classification"] == "教育用公開合成資料",
            "authored public sharing boundary",
        )
        require(
            p["feedbackId"] == "FDB-CTI26-" + suffix
            and p["reassessmentId"] == "REA-CTI26-001",
            "product lifecycle binding",
        )
        f = feedback[p["feedbackId"]]
        require(
            f["productId"] == p["id"]
            and f["audience"] == audience
            and f["status"] == "planned-not-received"
            and f["answer"] is None
            and f["receiptId"] is None,
            "feedback not received",
        )
    options = by_id(data["options"], "options")
    require(
        set(options) == {"OPT-CTI26-A", "OPT-CTI26-B", "OPT-CTI26-C"},
        "options inventory",
    )
    require(
        all(
            o["parentDecisionPreserved"] is (k == "OPT-CTI26-A")
            for k, o in options.items()
        ),
        "parent option preservation",
    )
    decision = data["decision"]
    require(
        decision["id"] == "DEC-CTI26-001"
        and decision["parentDecisionId"] == "DEC-2026-025"
        and decision["selectedOptionId"] == "OPT-CTI26-A"
        and decision["owner"] == "SYNTH-CISO"
        and decision["productId"] == "PRD-CTI26-EXEC",
        "decision binding",
    )
    require(
        decision["status"] == "synthetic-representation"
        and decision["executed"] is False
        and decision["authorityGranted"] is False,
        "decision not execution",
    )
    rea = data["reassessment"]
    require(
        rea["id"] == "REA-CTI26-001"
        and rea["parentReassessmentId"] == "REA-2026-025"
        and instant(r["asOf"])
        < instant(rea["at"])
        < min(instant(p["expiresAt"]) for p in products.values()),
        "reassessment before expiry",
    )
    require(
        idset(rea["triggerGapIds"], "reassessment gaps") == seq("GAP", (1, 2, 3, 4))
        and rea["supersedingProductId"] is None
        and rea["stixObjectRevoked"] is False,
        "product correction not STIX revocation",
    )
    h = data["handoff"]
    require(
        h["id"] == "HOF-CTI26-029"
        and h["chapter"] == 29
        and h["audience"] == "SYNTH-Capstone coordinator"
        and idset(h["productIds"], "handoff products") == set(products),
        "handoff binding",
    )
    require(
        h["status"] == "planned-not-delivered"
        and h["receiptId"] is None
        and h["authorityGranted"] is False,
        "handoff not delivered",
    )
    x = data["exchangeExample"]
    require(
        x["id"] == "CASE-STIX26-DEMO"
        and x["relation"] == "independent"
        and x["purpose"] == "structure-only-not-evidence"
        and x["bundleProfile"] == "STIX21-STRUCTURE-ONLY"
        and x["taxiiProfile"] == "TAXII21-OFFLINE-ONLY"
        and x["adoptedEvidenceIds"] == []
        and x["contributesToJudgment"] is False
        and x["networkExecuted"] is False,
        "independent exchange boundary",
    )
    return {
        "products": sorted(products),
        "judgments": sorted(judgments),
        "origins": {k: judgments[k]["independentOrigins"] for k in sorted(judgments)},
        "delivered": 0,
        "executed": 0,
        "attributionCeiling": "L2",
        "demoEvidenceAdopted": 0,
    }


def validate_bundle(bundle):
    """The supplied 13-object profile only; not arbitrary STIX conformance."""
    require(
        bundle["type"] == "bundle" and "spec_version" not in bundle,
        "bundle type/no version",
    )
    objects = by_id(bundle["objects"], "STIX objects")
    counts = Counter(o["type"] for o in objects.values())
    expected = {
        "threat-actor": 1,
        "campaign": 1,
        "malware": 1,
        "infrastructure": 1,
        "domain-name": 1,
        "observed-data": 1,
        "indicator": 1,
        "attack-pattern": 1,
        "relationship": 5,
    }
    require(counts == expected, "finite STIX type inventory")
    uuids = []
    for o in [bundle, *objects.values()]:
        prefix, value = o["id"].split("--")
        u = UUID(value)
        require(
            prefix == o["type"]
            and str(u) == value
            and u.version == (5 if prefix == "domain-name" else 4),
            "STIX identifier/version",
        )
        uuids.append(value)
        if prefix == "bundle":
            continue
        require(o["spec_version"] == "2.1", "STIX specification version")
        if prefix != "domain-name":
            require(
                instant(o["created"], True) <= instant(o["modified"], True),
                "STIX modified before created",
            )
            require(
                o["created"] == "2026-10-06T00:00:00.000Z"
                and o["modified"] == o["created"],
                "fixed independent demo time",
            )
            require(o["lang"] == "en", "demo language")
            if prefix != "relationship":
                require(o["labels"] == ["synthetic-structure-only"], "demo labeling")
    require(len(uuids) == len(set(uuids)), "UUID reuse across types")
    types = {o["type"]: o for o in objects.values() if o["type"] != "relationship"}
    domain = types["domain-name"]
    require(domain["value"] == "relay-demo.example", "reserved demo domain")
    name = json.dumps({"value": domain["value"]}, sort_keys=True, separators=(",", ":"))
    require(
        domain["id"]
        == "domain-name--"
        + str(uuid5(UUID("00abedb4-aa42-466c-9c01-fed23315a9b7"), name)),
        "SCO deterministic identity",
    )
    obs = types["observed-data"]
    require(
        obs["object_refs"] == [domain["id"]]
        and type(obs["number_observed"]) is int
        and obs["number_observed"] == 1,
        "observed data binding/count",
    )
    require(
        instant(obs["first_observed"], True)
        <= instant(obs["last_observed"], True)
        <= instant(obs["created"], True)
        and obs["first_observed"] == obs["created"],
        "observation time",
    )
    ind = types["indicator"]
    require(
        ind["pattern_type"] == "stix"
        and ind["pattern_version"] == "2.1"
        and ind["pattern"] == "[domain-name:value = 'relay-demo.example']",
        "finite pattern equality",
    )
    require(
        ind["valid_from"] == ind["created"]
        and instant(ind["valid_from"], True) < instant(ind["valid_until"], True)
        and ind["valid_until"] == "2026-10-07T00:00:00.000Z",
        "indicator validity window",
    )
    require(
        types["malware"]["is_family"] is False
        and types["malware"]["malware_types"] == ["unknown"]
        and types["threat-actor"]["threat_actor_types"] == ["unknown"]
        and types["infrastructure"]["infrastructure_types"] == ["unknown"],
        "fictional types not capabilities",
    )
    for t, o in types.items():
        if t not in ("domain-name", "observed-data"):
            require(o["name"].startswith("SYNTH-Training "), "synthetic entity name")
    triples = []
    for o in objects.values():
        if o["type"] == "relationship":
            require(
                o["source_ref"] in objects
                and o["target_ref"] in objects
                and o["source_ref"] != o["target_ref"],
                "relationship endpoints",
            )
            triples.append(
                (
                    objects[o["source_ref"]]["type"],
                    o["relationship_type"],
                    objects[o["target_ref"]]["type"],
                )
            )
    require(
        len(triples) == len(set(triples))
        and set(triples)
        == {
            ("campaign", "attributed-to", "threat-actor"),
            ("threat-actor", "uses", "malware"),
            ("campaign", "uses", "infrastructure"),
            ("campaign", "uses", "attack-pattern"),
            ("indicator", "indicates", "attack-pattern"),
        },
        "finite relationship semantics",
    )
    return sorted(objects)


def validate_taxii(taxii, bundle):
    require(
        taxii["schemaVersion"] == VERSION
        and taxii["synthetic"] is True
        and taxii["networkExecuted"] is False
        and taxii["caseId"] == "CASE-STIX26-DEMO",
        "offline TAXII boundary",
    )
    c = taxii["collection"]
    u = UUID(c["id"])
    require(
        str(u) == c["id"]
        and u.version == 4
        and c["title"] == "SYNTH-Training Collection"
        and c["can_read"] is True
        and c["can_write"] is False
        and c["media_types"] == ["application/stix+json;version=2.1"],
        "finite collection",
    )
    require(
        taxii["request"]
        == {
            "method": "GET",
            "url": "https://taxii.example/training/collections/"
            + c["id"]
            + "/objects/",
            "accept": "application/taxii+json;version=2.1",
        },
        "reserved offline request",
    )
    r = taxii["response"]
    require(
        type(r["status"]) is int
        and r["status"] == 200
        and r["contentType"] == "application/taxii+json;version=2.1"
        and r["envelope"]["more"] is False,
        "offline response metadata",
    )
    require(
        by_id(r["envelope"]["objects"], "TAXII objects")
        == by_id(bundle["objects"], "bundle objects"),
        "TAXII objects equality, not Bundle wrapping",
    )


def validate_model(data, bundle, taxii, schemas, contract):
    errors = []
    for name, value, schema in zip(
        (DATA, BUNDLE, TAXII), (data, bundle, taxii), schemas, strict=True
    ):
        validate_supported_schema_nodes(schema, "schema", schema)
        validate_schema_instance(value, schema)
        require(
            digest(value) == contract["dataDigests"][name], "supplied data snapshot"
        )
        for path, v in leaves(value):
            if isinstance(v, str):
                require(v.strip() and len(v) <= 2048, "nonblank bounded text")
                for finding in (
                    *scan_action_text(v, location=name + ":" + "/".join(path)),
                    *scan_host_policy(v, location=name + ":" + "/".join(path)),
                ):
                    errors.append(
                        f"{name}: {'/'.join(path)}: {finding.category}: {finding.reason}"
                    )
    evaluate(data)
    validate_bundle(bundle)
    validate_taxii(taxii, bundle)
    return errors
