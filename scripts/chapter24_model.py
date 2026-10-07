"""Layer A: finite authored source lineage/evaluation, not a collection or truth engine.

Shared Projection owns rendering; shared Policy owns action/host grammar. Hashes
identify supplied UTF-8 strings, not authenticity, authority or legal admissibility.
"""

from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import os
from pathlib import PurePosixPath
import stat
from scripts.check_editorial_input_manifest import (
    _reject_constant,
    _reject_duplicate_keys,
    validate_schema_instance,
    validate_supported_schema_nodes,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

VERSION = "1.0.0"
DATA = "cases/fixtures/ch24-source-evaluation.json"
SCHEMA = "schemas/ch24-source-evaluation.schema.json"
CONTRACT = "tests/fixtures/chapter24/publication-contract.json"
CORPUS = "tests/fixtures/chapter24/comparison-corpus.json"
DOCUMENTS = (
    "manuscript/24-osint-provenance-sources.md",
    "templates/evidence-source-evaluation-table.md",
    "cases/ch24-source-evaluation-example.md",
    "references/ch24-source-review-2026-09-27.md",
)
SOURCES = ("SRC-BERKELEY-001", "SRC-ICD203-001")
PARENTS = (
    "WRITING_GUIDE.md",
    "SOURCE_POLICY.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "manuscript/10-recon-osint-boundary.md",
    "cases/fixtures/ch10-attack-surface.json",
    "manuscript/23-intelligence-requirements.md",
    "cases/fixtures/ch23-intelligence-requirements.json",
    "manuscript/25-structured-analysis-attribution.md",
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
    "book-config.json",
)
USES = ("Direct evidence", "Context", "Lead", "Unverified", "Excluded")


def require(condition, label):
    if not condition:
        raise ValueError("EV24: " + label)


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


def instant(value):
    require(type(value) is str and len(value) == 20, "UTC format")
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    require(
        2000 <= result.year <= 2099 and result.strftime("%Y-%m-%dT%H:%M:%SZ") == value,
        "canonical UTC",
    )
    return result


def read_regular(root, relative):
    """Fixed bounded input set; not a concurrent hostile-rename sandbox."""
    require(relative in INPUTS and not root.is_symlink(), "fixed input/root")
    root = root.resolve(strict=True)
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        require(not path.is_symlink(), "symlink input/ancestor")
    require(path.resolve(strict=True).is_relative_to(root), "input containment")
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
                        "/".join(path) or title,
                        v if isinstance(v, str) else json.dumps(v, ensure_ascii=False),
                    )
                    for path, v in leaves(group)
                ],
            )


def idset(values, label):
    require(
        type(values) is list and len(values) == len(set(values)), label + " unique refs"
    )
    return set(values)


def by_id(rows, label):
    ids = [row["id"] for row in rows]
    idset(ids, label)
    return dict(zip(ids, rows, strict=True))


def identifier(prefix, number):
    return f"{prefix}-EV24-{number:03}"


def text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def evaluate(data):
    """Compare declared finite relationships, never infer truth from arbitrary text."""
    require(data["schemaVersion"] == VERSION, "model version")
    for key, value in (
        ("synthetic", True),
        ("readOnly", True),
        ("networkRequired", False),
        ("executionAuthorized", False),
    ):
        require(data[key] is value, "offline boundary")
    record = data["record"]
    require(
        (
            record["id"],
            record["artifactId"],
            record["caseId"],
            record["relationship"],
            record["decisionId"],
        )
        == (
            "EST-2026-024-001",
            "ART-30",
            "CASE-OS24-001",
            "independent",
            "DR-OS24-001",
        ),
        "record identity",
    )
    for key in ("actualCollections", "actualActions", "actualNotifications"):
        require(type(record[key]) is int and record[key] == 0, "zero actual operations")
    for key in (
        "parentEvidenceInherited",
        "parentAuthorityInherited",
        "realWorldTruthCertified",
    ):
        require(
            record[key] is False, "no inherited authority/evidence/truth certification"
        )
    asof, deadline = instant(record["asOf"]), instant(record["decisionDeadline"])
    require(asof < deadline, "decision deadline")
    require(
        [
            (r["chapter"], r["recordId"], r["relationship"], r["received"])
            for r in data["methodReferences"]
        ]
        == [
            (10, "ASR-2026-010", "method-reference-only", False),
            (23, "IRCP-2026-023-001", "method-reference-only", False),
            (25, "ART-12", "method-reference-only", False),
        ],
        "method references not receipt",
    )
    collections = by_id(data["collections"], "collections")
    sources = by_id(data["sources"], "sources")
    claims = by_id(data["claims"], "claims")
    items = by_id(data["items"], "items")
    transforms = by_id(data["transforms"], "transforms")
    evaluations = by_id(data["evaluations"], "evaluations")
    gaps = by_id(data["gaps"], "gaps")
    hypotheses = by_id(data["hypotheses"], "hypotheses")
    for rows, prefix, count in (
        (collections, "COL", 2),
        (sources, "OSRC", 5),
        (claims, "CLM", 4),
        (items, "ITEM", 9),
        (transforms, "TRF", 5),
        (evaluations, "EV", 11),
        (gaps, "GAP", 11),
        (hypotheses, "HYP", 2),
    ):
        require(
            set(rows) == {identifier(prefix, n) for n in range(1, count + 1)},
            "finite " + prefix + " inventory",
        )
    for c in collections.values():
        require(
            c["subject"] == "SYNTH-NOTIFY" and c["currentVersion"] == "v2",
            "collection subject/version",
        )
        require(instant(c["deadline"]) == asof, "collection cutoff")
        require(c["method"] == "supplied-record-reading", "supplied reading only")
    for obj in [*collections.values(), *sources.values()]:
        require(
            (obj["authority"], obj["terms"], obj["classification"])
            == ("supplied-only", "supplied-only", "synthetic-public"),
            "authority/terms/classification",
        )
    for s in sources.values():
        require(
            s["publisher"].startswith("SYNTH-") and s["author"].startswith("SYNTH-"),
            "known supplied publisher/author",
        )
        require(
            s["kind"] in {"original", "secondary", "aggregator", "post", "observation"},
            "AI summary is not a Source",
        )
        require(
            s["reliability"]["value"] in {"bounded", "limited", "unknown"},
            "separate source reliability",
        )
        require(s["allowedUse"] == "offline-reading-only", "allowed use")
    for c in claims.values():
        require(
            c["collectionId"] in collections and c["subject"] == "SYNTH-NOTIFY",
            "claim collection/subject",
        )
        require(
            c["version"] in {"v1", "v2"}
            and c["modality"] in {"possible", "observed", "confirmed"},
            "claim version/modality",
        )
        require(
            idset(c["hypothesisIds"], "claim hypotheses") == set(hypotheses),
            "claim hypotheses",
        )
    # Four authored roots. Distinct versions of the vendor advisory remain one observation family.
    roots = {
        identifier("ITEM", 1): (identifier("OSRC", 1), identifier("OBS", 1)),
        identifier("ITEM", 2): (identifier("OSRC", 1), identifier("OBS", 1)),
        identifier("ITEM", 5): (identifier("OSRC", 4), identifier("OBS", 2)),
        identifier("ITEM", 6): (identifier("OSRC", 5), identifier("OBS", 3)),
    }
    require(
        {x["id"] for x in items.values() if x["originKind"] == "original"}
        == set(roots),
        "finite root inventory",
    )
    outputs = {}
    for t in transforms.values():
        a, b = t["inputItemId"], t["outputItemId"]
        require(
            a in items and b in items and a != b and b not in outputs,
            "transform references/unique output",
        )
        require(
            t["kind"] in {"republication", "translation", "ai-summary", "extraction"},
            "transform kind",
        )
        require(
            t["reviewState"] in {"reviewed", "pending", "rejected"}
            and t["meaning"] in {"preserved", "changed"},
            "transform review/meaning",
        )
        require(
            items[b]["parentItemId"] == a and items[b]["originKind"] == "derived",
            "transform parent binding",
        )
        require(
            t["inputSha256"] == items[a]["contentSha256"]
            and t["outputSha256"] == items[b]["contentSha256"],
            "transform input/output hash",
        )
        require(
            instant(items[a]["acquiredAt"])
            <= instant(t["performedAt"])
            == instant(items[b]["publishedAt"]),
            "transform time order",
        )
        require(
            t["originalLanguage"] == items[a]["language"]
            and t["outputLanguage"] == items[b]["language"],
            "transform language binding",
        )
        same = items[a]["assertions"] == items[b]["assertions"]
        require(same == (t["meaning"] == "preserved"), "meaning/modality changed")
        require(
            t["meaning"] == "preserved" or t["reviewState"] == "rejected",
            "changed meaning must be rejected",
        )
        if t["kind"] == "translation":
            require(
                t["originalLanguage"] != t["outputLanguage"]
                and t["ambiguousTerm"] != "not-applicable",
                "translation ambiguity/language",
            )
        outputs[b] = t
    require(
        set(outputs) == set(items) - set(roots),
        "every derivative has exactly one transform",
    )
    groups, eligible, visiting = {}, {}, set()

    def lineage(iid):
        if iid in groups:
            return groups[iid]
        require(iid not in visiting, "lineage cycle")
        visiting.add(iid)
        row = items[iid]
        if iid in roots:
            require(
                row["parentItemId"] is None
                and (row["sourceId"], row["observationGroup"]) == roots[iid],
                "authored root binding",
            )
            group = roots[iid][1]
            # Root5 is expressly unverified. Root1 is historical, not current evidence.
            eligible[iid] = iid in {identifier("ITEM", 2), identifier("ITEM", 6)}
        else:
            parent = row["parentItemId"]
            require(parent in items, "unknown lineage parent")
            group = lineage(parent)
            t = outputs[iid]
            require(
                row["subject"] == items[parent]["subject"]
                and row["version"] == items[parent]["version"],
                "transform subject/version",
            )
            eligible[iid] = (
                eligible[parent]
                and t["reviewState"] == "reviewed"
                and t["meaning"] == "preserved"
            )
        require(row["observationGroup"] == group, "same-origin independence")
        groups[iid] = group
        visiting.remove(iid)
        return group

    # Derived captures retain their authored publisher identity; a vendor
    # lineage root does not make its republishers the vendor.
    derived_sources = {
        identifier("ITEM", item): identifier("OSRC", source)
        for item, source in {3: 2, 4: 3, 7: 1, 8: 1, 9: 5}.items()
    }
    for iid, row in items.items():
        require(
            row["sourceId"] in sources
            and row["subject"] == "SYNTH-NOTIFY"
            and row["version"] in {"v1", "v2"},
            "item source/subject/version",
        )
        if iid not in roots:
            require(
                row["sourceId"] == derived_sources[iid],
                "authored derived source binding",
            )
        require(row["originKind"] in {"original", "derived"}, "item origin kind")
        require(
            row["contentSha256"] == text_hash(row["content"]), "exact UTF8 content hash"
        )
        require(
            instant(row["publishedAt"]) <= instant(row["acquiredAt"]) <= asof
            and row["timezone"] == "UTC",
            "acquisition time order/zone",
        )
        require(
            row["acquisitionMethod"] == "author-supplied-not-network-acquisition"
            and row["mediaType"] == "text/plain; charset=utf-8",
            "synthetic acquisition/media",
        )
        assertions = set()
        for a in row["assertions"]:
            require(
                a["claimId"] in claims
                and a["relation"] in {"supports", "contradicts"}
                and a["modality"] in {"possible", "observed", "confirmed"},
                "assertion reference/type",
            )
            claim = claims[a["claimId"]]
            require(
                claim["subject"] == row["subject"]
                and claim["version"] == row["version"],
                "assertion subject/version",
            )
            if a["relation"] == "supports":
                require(a["modality"] == claim["modality"], "support modality")
            key = (a["claimId"], a["relation"])
            require(key not in assertions, "duplicate assertion")
            assertions.add(key)
        require(bool(assertions), "item assertions")
        lineage(iid)
    versions = by_id(data["versionChanges"], "version changes")
    require(set(versions) == {identifier("VER", 1)}, "finite version change")
    for v in versions.values():
        a, b = v["previousItemId"], v["currentItemId"]
        require(
            (a, b) == (identifier("ITEM", 1), identifier("ITEM", 2)), "version pair"
        )
        x, y = items[a], items[b]
        require(
            x["resourceId"] == y["resourceId"]
            and x["canonicalUrl"] == y["canonicalUrl"]
            and x["sourceId"] == y["sourceId"],
            "same resource revised version",
        )
        require(
            x["version"] != y["version"]
            and instant(x["publishedAt"]) < instant(y["publishedAt"])
            and x["contentSha256"] != y["contentSha256"],
            "distinct retained versions",
        )
    citations = by_id(data["citationLinks"], "citations")
    event_context = {identifier("ITEM", 3), identifier("ITEM", 4)}
    event_resources = {
        identifier("CITE", 1): (
            items[identifier("ITEM", 3)]["resourceId"],
            items[identifier("ITEM", 4)]["resourceId"],
        ),
        identifier("CITE", 2): (
            items[identifier("ITEM", 4)]["resourceId"],
            items[identifier("ITEM", 3)]["resourceId"],
        ),
    }
    require(set(citations) == set(event_resources), "finite citation event identities")
    for cid, event in citations.items():
        require(
            event["kind"] == "later-citation-event"
            and event["recordingMethod"] == "author-supplied-not-network-observation",
            "authored later citation event",
        )
        require(
            (event["fromResourceId"], event["toResourceId"]) == event_resources[cid]
            and event["fromResourceId"] != event["toResourceId"],
            "citation resource binding",
        )
        require(
            idset(event["contextItemIds"], "citation context") == event_context,
            "citation context item binding",
        )
        # These are separately supplied later link events; earlier captured
        # content/hashes stay immutable. They are not extra Claim observations.
        require(
            max(instant(items[i]["acquiredAt"]) for i in event_context)
            < instant(event["occurredAt"])
            <= instant(event["recordedAt"])
            <= asof,
            "citation event chronology/cutoff",
        )
        require(
            event["meaning"] == "later-mutual-reference-no-new-observation",
            "citation is not observation",
        )
    seen = set()
    direct = set()
    observations = {}
    counts = Counter()
    for e in evaluations.values():
        iid, cid = e["itemId"], e["claimId"]
        require(iid in items and cid in claims, "evaluation references")
        pair = (iid, cid, e["relation"])
        require(pair not in seen, "duplicate evaluation binding")
        seen.add(pair)
        require(
            any(
                (a["claimId"], a["relation"]) == (cid, e["relation"])
                for a in items[iid]["assertions"]
            ),
            "evaluation item claim relationship",
        )
        require(
            e["use"] in USES
            and e["credibility"]["value"] in {"supported", "limited", "unverified"},
            "separate credibility/use",
        )
        independence = e["independence"]
        require(
            idset(independence["observationGroups"], "observation groups")
            == {groups[iid]},
            "deduplicated root observation group",
        )
        value = (
            "same-origin"
            if iid in outputs
            else (
                "unknown"
                if iid == identifier("ITEM", 5)
                else "independent-in-supplied-model"
            )
        )
        require(independence["value"] == value, "declared independence")
        t = outputs.get(iid)
        if t and t["reviewState"] == "rejected":
            require(e["use"] == "Excluded", "rejected transform excluded")
        elif t and t["reviewState"] == "pending":
            require(e["use"] == "Lead", "pending transform is lead")
        elif iid == identifier("ITEM", 5):
            require(e["use"] == "Unverified", "unverified root not promoted")
        elif (
            items[iid]["version"]
            != collections[claims[cid]["collectionId"]]["currentVersion"]
        ):
            require(e["use"] == "Context", "old version context only")
        else:
            require(e["use"] == "Direct evidence", "reviewed finite evidence retained")
        grade = {
            "Direct evidence": "supported",
            "Context": "limited",
            "Lead": "limited",
            "Unverified": "unverified",
            "Excluded": "unverified",
        }
        require(
            e["credibility"]["value"] == grade[e["use"]],
            "credibility matches bounded use",
        )
        if e["use"] == "Direct evidence":
            require(eligible[iid], "current eligible evidence")
            direct.add(pair)
            observations.setdefault(cid, {"supports": set(), "contradicts": set()})[
                e["relation"]
            ].add(groups[iid])
        require(
            idset(e["hypothesisIds"], "evaluation hypotheses") == set(hypotheses),
            "evaluation hypotheses",
        )
        require(e["gapId"] in gaps, "evaluation gap")
        gap = gaps[e["gapId"]]
        require(
            gap["evaluationId"] == e["id"]
            and gap["reassessmentId"] == e["reassessmentId"],
            "gap evaluation/reassessment",
        )
        require(asof < instant(gap["deadline"]) <= deadline, "gap deadline")
        counts[e["use"]] += 1
    require(
        seen
        == {
            (iid, a["claimId"], a["relation"])
            for iid, row in items.items()
            for a in row["assertions"]
        },
        "every item assertion evaluated",
    )
    require(
        {e["gapId"] for e in evaluations.values()} == set(gaps)
        and len({e["reassessmentId"] for e in evaluations.values()})
        == len(evaluations),
        "all gaps/unique reassessments",
    )
    expected = {
        (iid, a["claimId"], a["relation"])
        for iid, row in items.items()
        if eligible[iid]
        for a in row["assertions"]
    }
    require(direct == expected, "all current support and contradiction retained")
    require(set(counts) == set(USES), "five finite uses")
    require(
        all(h["decision"] == "not-concluded" for h in hypotheses.values()),
        "hypothesis not a conclusion",
    )
    hs = by_id(data["handoffs"], "handoffs")
    require(set(hs) == {"HOF-EV24-25", "HOF-EV24-26"}, "handoff identities")
    require(
        {h["chapter"] for h in hs.values()} == {25, 26} and len(hs) == 2,
        "finite handoffs",
    )
    for h in hs.values():
        require(
            h["id"] == "HOF-EV24-" + str(h["chapter"]),
            "handoff identity/chapter binding",
        )
        require(
            h["audience"]
            == {
                "HOF-EV24-25": "SYNTH-ANALYSIS-READER",
                "HOF-EV24-26": "SYNTH-DISTRIBUTION-READER",
            }[h["id"]],
            "handoff identity/audience binding",
        )
        require(
            h["status"] == "planned-not-delivered"
            and h["receipt"] is None
            and h["executionAuthorized"] is False,
            "handoff not delivered/authorized",
        )
        require(
            idset(h["evidenceIds"], "handoff evidence") == set(evaluations)
            and idset(h["gapIds"], "handoff gaps") == set(gaps),
            "handoff includes limits/gaps",
        )
        require(
            max(instant(g["deadline"]) for g in gaps.values())
            <= instant(h["deadline"])
            <= deadline,
            "handoff timeline",
        )
    return {
        "useCounts": {u: counts[u] for u in USES},
        "currentClaimOrigins": {
            cid: {rel: sorted(values) for rel, values in relations.items()}
            for cid, relations in sorted(observations.items())
        },
        "independentOriginCount": len(
            {v for rs in observations.values() for vals in rs.values() for v in vals}
        ),
        "circularCitationEdges": len(citations),
        "actualCollections": 0,
        "handoffsDelivered": 0,
    }


def validate_model(data, schema, contract=None):
    validate_supported_schema_nodes(schema, "schema", schema)
    validate_schema_instance(data, schema)
    errors = []
    for path, value in leaves(data):
        if isinstance(value, str):
            require(
                bool(value.strip()) and len(value) <= 2048, "bounded nonblank field"
            )
            location = DATA + ":" + "/".join(path)
            errors += [
                f"{location}: {f.category}: {f.reason}"
                for f in (
                    *scan_action_text(value, location=location),
                    *scan_host_policy(value, location=location),
                )
            ]
    evaluate(data)
    if contract is not None and digest(data) != contract["dataSha256"]:
        errors.append("EV24: canonical supplied data snapshot")
    return errors
