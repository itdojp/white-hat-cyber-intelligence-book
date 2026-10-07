"""Finite ART-19 counterexamples. Generic syntax remains Layer B-owned."""

import ast
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from scripts.chapter10_semantics import (
    DATA_PATH,
    INPUTS,
    DOCUMENTS,
    STATES,
    validate_model,
    read_regular,
    strict_bytes,
    utc,
)
from scripts.check_chapter10_contract import (
    ROOT,
    SOURCE_IDS,
    relations,
    key,
    scan_document,
    document_errors,
    repository_errors,
)
from scripts.check_editorial_input_manifest import ManifestError
from scripts.publication_projection import project_documents, is_policy_scan_field


def at(value, path):
    for key_ in path:
        value = value[key_]
    return value


def containers(value, path=()):
    if isinstance(value, dict):
        yield path, value
        for k, v in value.items():
            yield from containers(v, path + (k,))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from containers(v, path + (i,))


def run_regressions(data, bundle, schema, contract, source, projection):
    errors, ids = [], set()

    def check(ident, ok):
        if ident in ids:
            errors.append("duplicate regression ID " + ident)
        ids.add(ident)
        if not ok:
            errors.append(ident + ": expected finite disposition was not observed")

    def validate(d=data, b=bundle, s=schema):
        return validate_model(d, b, s, contract)

    def bad(ident, path, value, which="register"):
        d, b = deepcopy(data), deepcopy(bundle)
        root = d if which == "register" else b
        at(root, path[:-1])[path[-1]] = value
        check(ident, bool(validate(d, b)))

    # PR130 / discussion_r4003440638: explicit UTF-8 for this finite tooling
    # inventory, including regression-only temporary JSON. No locale defaults.
    for module in (
        "chapter10_semantics.py",
        "check_chapter10_contract.py",
        "chapter10_regressions.py",
    ):
        tree = ast.parse((ROOT / "scripts" / module).read_bytes().decode("utf-8"))
        calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in ("read_text", "write_text")
        ]
        check(
            "CH10-UTF8-" + module,
            all(
                any(
                    kw.arg == "encoding"
                    and isinstance(kw.value, ast.Constant)
                    and kw.value.value == "utf-8"
                    for kw in call.keywords
                )
                for call in calls
            ),
        )
    check("CH10-POS-canonical", not validate())
    check(
        "CH10-POS-five-states",
        {c["verificationStatus"] for c in data["candidates"]} == set(STATES),
    )
    check(
        "CH10-POS-three-original-classes",
        {s["originalCollectionClass"] for s in data["sources"]}
        == {"Passive", "Active", "Authenticated"},
    )
    p = deepcopy(data)
    p["candidates"][1]["verificationStatus"] = "Unknown"
    check("CH10-POS-CT-withheld", not validate(p))
    p = deepcopy(data)
    p["candidates"][5].update(verificationStatus="Candidate", ownershipConfidence="Low")
    check("CH10-POS-package-withheld", not validate(p))
    p = deepcopy(data)
    p["learnerPlan"].update(summaryBytes=1024, minutes=10, retentionHours=1)
    check("CH10-POS-tighter-budget", not validate(p))
    p = deepcopy(data)
    p["candidates"][4]["judgment"] = "提供資料だけでは所有を確定しない。"
    check("CH10-POS-bounded-analysis", not validate(p))
    # All required keys and every authored object are shape-checked independently.
    for label, value in (("register", data), ("bundle", bundle)):
        for oi, (path, obj) in enumerate(containers(value), 1):
            d, b = deepcopy(data), deepcopy(bundle)
            target = at(d if label == "register" else b, path)
            target["unownedField"] = "SYNTH-UNKNOWN"
            check(f"CH10-SHAPE-{label}-{oi}-extra", bool(validate(d, b)))
            for ki, name in enumerate(obj, 1):
                d, b = deepcopy(data), deepcopy(bundle)
                del at(d if label == "register" else b, path)[name]
                check(f"CH10-SHAPE-{label}-{oi}-missing-{ki}", bool(validate(d, b)))
    negatives = [
        ("execution", ("executionAuthorized",), True),
        ("real-data", ("synthetic",), False),
        (
            "parent-expiry",
            ("parents", "authorizationExpiresAt"),
            "2026-12-31T00:00:00Z",
        ),
        ("parent-approved", ("parents", "roeStatus"), "Approved"),
        (
            "parent-scope",
            ("parents", "roeObjectIds"),
            ["OBJ-ROE09-CONFIG", "CAND-ASR10-001"],
        ),
        ("independent-case", ("parents", "independentCaseId"), "CASE-2026-001"),
        (
            "historical-deadline",
            ("parents", "historicalDeadline"),
            "2026-09-15T00:00:00Z",
        ),
        ("class-active", ("learnerPlan", "collectionClass"), "Active"),
        ("class-fourth", ("learnerPlan", "collectionClass"), "First-party inventory"),
        ("passive-network", ("learnerPlan", "networkRequests"), 1),
        ("passive-auth", ("learnerPlan", "authenticationAttempts"), 1),
        ("passive-rate", ("learnerPlan", "rateTests"), 1),
        (
            "action-mismatch",
            ("learnerPlan", "actions"),
            ["read-supplied-json", "network-request"],
        ),
        ("wrong-input", ("learnerPlan", "inputSourceIds"), ["OSRC-ASR10-999"]),
        ("cleanup-claim", ("learnerPlan", "cleanupStatus"), "verified"),
        ("retention", ("learnerPlan", "retentionHours"), 48),
        ("zero-budget", ("learnerPlan", "summaryBytes"), 0),
        ("bool-budget", ("learnerPlan", "networkRequests"), False),
        ("source-order", ("sources",), list(reversed(data["sources"]))),
        ("source-duplicate", ("sources",), data["sources"] + [data["sources"][0]]),
        ("source-lineage", ("sources", 8, "originalOriginId"), "ORIGIN-ASR10-009"),
        ("source-class", ("sources", 4, "originalCollectionClass"), "Passive"),
        ("source-terms", ("sources", 0, "termsNote"), "public means authorized"),
        ("source-hash", ("sources", 0, "contentSha256"), "0" * 64),
        ("source-hash-scope", ("sources", 0, "hashScope"), "entire JSON file"),
        ("source-future", ("sources", 0, "acquiredAt"), "2026-09-15T00:00:00Z"),
        (
            "source-before-observation",
            ("sources", 0, "acquiredAt"),
            "2026-09-13T00:00:00Z",
        ),
        ("source-PII", ("sources", 3, "personalDataFields"), ["SYNTH-PERSON-001"]),
        ("source-classification", ("sources", 3, "dataClass"), "public-personal-data"),
        (
            "source-credential",
            ("sources", 4, "credentialMaterial"),
            "SYNTH-INVALID-TOKEN",
        ),
        (
            "source-real-claim",
            ("sources", 6, "transformation"),
            "real measured response",
        ),
        (
            "candidate-duplicate",
            ("candidates",),
            data["candidates"] + [data["candidates"][0]],
        ),
        ("candidate-dangling", ("candidates", 0, "sourceIds"), ["OSRC-ASR10-999"]),
        (
            "candidate-unrelated",
            ("candidates", 0, "sourceIds"),
            ["OSRC-ASR10-002", "OSRC-ASR10-009"],
        ),
        (
            "candidate-name-merge",
            ("candidates", 3, "locator"),
            "billing-bridge.example",
        ),
        ("owner-no-confidence", ("candidates", 0, "ownershipConfidence"), "Low"),
        ("owner-no-evidence", ("candidates", 0, "ownerEvidenceSourceIds"), []),
        (
            "owner-unrelated-evidence",
            ("candidates", 0, "ownerEvidenceSourceIds"),
            ["OSRC-ASR10-002"],
        ),
        ("owner-wrong-parent", ("candidates", 0, "parentAssetId"), "ASSET-2026-003"),
        ("owner-authorized", ("candidates", 0, "nextActionAuthorization"), True),
        (
            "CT-mirror-corroboration",
            ("candidates", 1, "verificationStatus"),
            "Corroborated",
        ),
        ("CT-owner", ("candidates", 1, "verificationStatus"), "Owner confirmed"),
        ("DNS-current", ("candidates", 2, "verificationStatus"), "Owner confirmed"),
        ("DNS-measured", ("candidates", 2, "exposure"), "current reachable service"),
        ("third-party-approval", ("candidates", 3, "nextActionAuthorization"), True),
        ("dependency-hidden", ("candidates", 5, "dependency"), "none"),
        ("third-party-hidden", ("candidates", 4, "thirdPartyStatus"), "first-party"),
        ("third-party-parent", ("candidates", 3, "parentAssetId"), "ASSET-2026-001"),
        ("SaaS-owner", ("candidates", 4, "candidateOwner"), "SYNTH-BUSINESS-SYSTEMS"),
        ("SaaS-corroborated", ("candidates", 4, "verificationStatus"), "Corroborated"),
        ("package-confidence", ("candidates", 5, "ownershipConfidence"), "High"),
        ("sixth-state", ("candidates", 4, "verificationStatus"), "Unverified"),
        ("action-auto-active", ("candidates", 0, "nextAction"), "active-collection"),
        ("approval-missing", ("candidates", 0, "requiredApproval"), []),
        ("gap-no-owner", ("candidates", 0, "gapOwner"), "Unknown"),
        ("gap-past", ("candidates", 0, "dueAt"), "2026-09-13T00:00:00Z"),
        ("handoff-delivered", ("handoffs", 0, "status"), "delivered"),
        ("handoff-unknown", ("handoffs", 0, "candidateIds"), ["CAND-ASR10-005"]),
        ("handoff-provenance", ("handoffs", 1, "provenanceIds"), []),
        (
            "absence-nonexistence",
            ("limits", "negativeFinding"),
            "all other assets do not exist",
        ),
        (
            "authenticity-claim",
            ("limits", "verification"),
            "verified real source authenticity",
        ),
        ("unsafe-text", ("record", "question"), "実Credentialを再利用する。"),
        ("external-host", ("record", "question"), "https://production.example.com/"),
    ]
    for label, path, value in negatives:
        bad("CH10-SEM-" + label, path, value)
    bad("CH10-BUNDLE-acquisition", ("acquisitionOccurred",), True, "bundle")
    bad(
        "CH10-BUNDLE-duplicate",
        ("sources",),
        bundle["sources"] + [bundle["sources"][0]],
        "bundle",
    )
    bad(
        "CH10-BUNDLE-content",
        ("sources", 0, "content"),
        "SYNTH-PERSON-001 profile aggregation",
        "bundle",
    )
    d, b = deepcopy(data), deepcopy(bundle)
    b["sources"][0]["content"] = "SYNTH-PERSON-001 profile aggregation"
    d["sources"][0]["contentSha256"] = hashlib.sha256(
        b["sources"][0]["content"].encode()
    ).hexdigest()
    check("CH10-BUNDLE-rehash-not-adoption", bool(validate(d, b)))
    p = deepcopy(data)
    p["candidates"][0].update(
        verificationStatus="Unknown",
        ownershipStatus="Unverified",
        ownershipConfidence="Low",
        candidateOwner="Unknown",
        ownerEvidenceSourceIds=[],
        parentAssetId=None,
    )
    check(
        "CH10-HANDOFF-downgraded-owner",
        any("only owner-confirmed" in e for e in validate(p)),
    )
    for i, raw in enumerate(
        (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b"\xff", b"{"), 1
    ):
        try:
            strict_bytes(raw)
            rejected = False
        except (ValueError, UnicodeError, ManifestError):
            rejected = True
        check(f"CH10-JSON-{i}", rejected)
    for i, value in enumerate(
        ("20260914T000000Z", "2026-9-14T00:00:00Z", "2026-09-14T00:00:00+00:00", True),
        1,
    ):
        try:
            utc(value)
            rejected = False
        except (ValueError, TypeError):
            rejected = True
        check(f"CH10-TIME-{i}", rejected)
    for keyword in ("maxLength", "unevaluatedProperties"):
        s = deepcopy(schema)
        s[keyword] = 1
        check("CH10-SCHEMA-unsupported-" + keyword, bool(validate(s=s)))
    for di, doc in enumerate(projection.documents, 1):
        spec = contract["documents"][doc.document_id]
        check(f"CH10-DOC-{di}-canonical", not document_errors(doc, spec, data, bundle))
        pairs = list(relations(doc))
        for ri, required in enumerate(spec["required"], 1):
            index = next(i for i, (_, r) in enumerate(pairs) if r == required)
            removed = replace(doc, fields=doc.fields[:index] + doc.fields[index + 1 :])
            check(
                f"CH10-DOC-{di}-required-{ri}",
                bool(document_errors(removed, spec, data, bundle)),
            )
        for family in ("hostProvenance", "analyticProvenance"):
            for ei, relation in enumerate(spec[family], 1):
                index = next(i for i, (_, r) in enumerate(pairs) if r == relation)
                f = doc.fields[index]
                text = f.text + (
                    " 実Credentialを再利用する。"
                    if family == "analyticProvenance"
                    else " https://production.example.com/"
                )
                changed = replace(f, text=text, normalized_text=text)
                probes = {
                    "changed": replace(
                        doc,
                        fields=doc.fields[:index]
                        + (changed,)
                        + doc.fields[index + 1 :],
                    ),
                    "moved": replace(
                        doc, fields=(f,) + doc.fields[:index] + doc.fields[index + 1 :]
                    ),
                    "duplicate": replace(
                        doc, fields=doc.fields[:index] + (f,) + doc.fields[index:]
                    ),
                    "missing": replace(
                        doc, fields=doc.fields[:index] + doc.fields[index + 1 :]
                    ),
                }
                for label, probe in probes.items():
                    check(
                        f"CH10-EX-{di}-{family}-{ei}-{label}",
                        bool(scan_document(probe, spec, True)),
                    )
                expected = f"{doc.document_id}: exact provenance cardinality: expected 1, observed 0; entry={key(relation)}"
                check(
                    f"CH10-DIAG-{di}-{family}-{ei}",
                    expected in scan_document(probes["missing"], spec, True),
                )
    # The shared renderer handles these direct Chapter10 mutations; no parser
    # variants or generic grammar are reimplemented in the chapter tests.
    for di, path in enumerate(DOCUMENTS, 1):
        old = source[path]
        for where in ("preamble", "body", "tail"):
            unsafe = "\n\n実Credentialを再利用する。\n\n"
            pos = (
                0
                if where == "preamble"
                else (len(old) if where == "tail" else old.index("\n## "))
            )
            mutated = (old[:pos] + unsafe + old[pos:]).rstrip() + "\n"
            doc = project_documents({path: mutated}).documents[0]
            check(
                f"CH10-SURFACE-{di}-{where}",
                bool(scan_document(doc, contract["documents"][path])),
            )
        doc = project_documents(
            {path: old + "\n## Unexpected Chapter10 section\n\n説明。\n"}
        ).documents[0]
        check(
            f"CH10-SURFACE-{di}-section",
            bool(document_errors(doc, contract["documents"][path], data, bundle)),
        )
    path = DOCUMENTS[0]
    doc = project_documents(
        {path: source[path] + "\n{% include unknown.html %}\n"}
    ).documents[0]
    check("CH10-SURFACE-unsupported", bool(doc.diagnostics))
    text = source[path]
    # PR130 / discussion_r4003243071: Source identities belong to Layer A.
    # The existing shared renderer supplies fields; no Markdown parsing here.
    ownership_error = "Chapter10 body/reference Source ownership"
    chapter = projection.documents[0]
    before, reference = text.split("\n## 参考文献・Source Note ID\n", 1)
    for si, sid in enumerate(SOURCE_IDS, 1):
        for scope in ("body", "references", "both"):
            probe = (
                (before.replace(sid, sid + "x") if scope != "references" else before)
                + "\n## 参考文献・Source Note ID\n"
                + (reference.replace(sid, sid + "x") if scope != "body" else reference)
            )
            doc = project_documents({path: probe}).documents[0]
            check(
                f"CH10-SOURCE-{si}-{scope}-rendered-suffix",
                ownership_error
                in document_errors(doc, contract["documents"][path], data, bundle),
            )
            for suffix, replacement in (
                ("upper", sid + "X"),
                ("digit", sid + "2"),
                ("underscore", sid + "_x"),
                ("prefix", "X" + sid),
            ):
                fields = []
                for field, relation in relations(chapter):
                    in_refs = "参考文献・Source Note ID" in relation["headings"]
                    selected = scope == "both" or (scope == "references") == in_refs
                    if selected:
                        field = replace(
                            field,
                            text=field.text.replace(sid, replacement),
                            normalized_text=field.normalized_text.replace(
                                sid, replacement
                            ),
                        )
                    fields.append(field)
                check(
                    f"CH10-SOURCE-{si}-{scope}-{suffix}",
                    ownership_error
                    in document_errors(
                        replace(chapter, fields=tuple(fields)),
                        contract["documents"][path],
                        data,
                        bundle,
                    ),
                )
        # Exact IDs remain recognized next to punctuation, independently of
        # the separate frozen semantic-field/provenance assertions.
        fields = tuple(
            replace(
                f,
                text=f.text.replace(sid, "(" + sid + ")"),
                normalized_text=f.normalized_text.replace(sid, "(" + sid + ")"),
            )
            for f in chapter.fields
        )
        check(
            f"CH10-SOURCE-{si}-exact-punctuation",
            ownership_error
            not in document_errors(
                replace(chapter, fields=fields),
                contract["documents"][path],
                data,
                bundle,
            ),
        )
    start = text.index("**Purpose:**")
    end = text.index("\n1. Caseを見る前に", start)
    blocks = text[start:end].strip().split("\n\n")
    check("CH10-ORDER-inventory", len(blocks) == 5)
    if len(blocks) == 5:
        for late in range(4):
            order = [i for i in range(5) if i != late] + [late]
            probe = (
                text[:start] + "\n\n".join(blocks[i] for i in order) + "\n" + text[end:]
            )
            doc = project_documents({path: probe}).documents[0]
            check(
                f"CH10-ORDER-explanation-{late}-late",
                "Chapter10 exercise explanations before command"
                in document_errors(doc, contract["documents"][path], data, bundle),
            )
    case = projection.documents[2]
    for ri, (index, f) in enumerate(
        (
            (i, f)
            for i, f in enumerate(case.fields)
            if is_policy_scan_field(f) and f.element_kind == "table_row"
        ),
        1,
    ):
        changed = replace(
            f, text=f.text + " changed", normalized_text=f.normalized_text + " changed"
        )
        doc = replace(
            case, fields=case.fields[:index] + (changed,) + case.fields[index + 1 :]
        )
        check(
            f"CH10-PARITY-{ri:03}",
            "ART19 complete two-JSON/projected Case parity"
            in document_errors(doc, contract["documents"][DOCUMENTS[2]], data, bundle),
        )
    # Owned scratch only; real publish-before-delete probes run separately in QA.
    scratch = ROOT / ".work"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch10-tests-", dir=scratch) as directory:
        root = Path(directory)
        for relative in INPUTS:
            p = root / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / relative).read_bytes())
        for relative in INPUTS:
            p = root / relative
            raw = p.read_bytes()
            check("CH10-IO-positive-" + relative, read_regular(root, relative) == raw)
            p.unlink()
            p.symlink_to(ROOT / relative)
            try:
                read_regular(root, relative)
                rejected = False
            except (ValueError, OSError):
                rejected = True
            check("CH10-IO-symlink-" + relative, rejected)
            p.unlink()
            p.write_bytes(raw)
        p = root / DATA_PATH
        original = p.read_bytes()
        for label, raw in (("empty", b""), ("oversize", b" " * (1024 * 1024 + 1))):
            p.write_bytes(raw)
            try:
                read_regular(root, DATA_PATH)
                rejected = False
            except (ValueError, OSError):
                rejected = True
            check("CH10-IO-" + label, rejected)
        p.unlink()
        os.mkfifo(p)
        try:
            read_regular(root, DATA_PATH)
            rejected = False
        except (ValueError, OSError):
            rejected = True
        check("CH10-IO-fifo", rejected)
        p.unlink()
        p.write_bytes(original)
        ancestor = root / "cases/fixtures"
        saved = root / "saved-fixtures"
        ancestor.rename(saved)
        ancestor.symlink_to(saved, target_is_directory=True)
        try:
            read_regular(root, DATA_PATH)
            rejected = False
        except (ValueError, OSError):
            rejected = True
        check("CH10-IO-ancestor", rejected)
        ancestor.unlink()
        saved.rename(ancestor)
        for name in ("O_NOFOLLOW", "O_NONBLOCK"):
            with patch.object(os, name, None):
                try:
                    read_regular(root, DATA_PATH)
                    rejected = False
                except ValueError:
                    rejected = True
            check("CH10-IO-platform-" + name, rejected)
        for path in (
            "../outside.json",
            "/absolute.json",
            "cases/fixtures/unowned.json",
        ):
            try:
                read_regular(root, path)
                rejected = False
            except ValueError:
                rejected = True
            check("CH10-IO-inventory-" + path, rejected)
        # Repository-specific routes, source and preflight errors must be caught.
        for relative in (
            "package.json",
            "site-pages.json",
            "references/sources.json",
            *contract["indices"],
        ):
            p = root / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / relative).read_bytes())
        check("CH10-REPO-positive", not repository_errors(contract, root))
        path = root / "package.json"
        baseline = json.loads(path.read_text(encoding="utf-8"))
        for label, replacement in (
            ("missing", ""),
            (
                "after-generator",
                baseline["scripts"]["sync:docs"]
                + " && python3 scripts/check_chapter10_contract.py --no-regressions",
            ),
        ):
            p = deepcopy(baseline)
            p["scripts"]["sync:docs"] = replacement
            path.write_text(json.dumps(p), encoding="utf-8")
            check(
                "CH10-REPO-preflight-" + label, bool(repository_errors(contract, root))
            )
        path.write_text(json.dumps(baseline), encoding="utf-8")
    return len(ids), errors
