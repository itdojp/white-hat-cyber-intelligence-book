"""Bounded semantic, publication and filesystem counterexamples for Chapter 29."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import tempfile

from scripts.chapter29_model import (
    DOCUMENTS, STATUSES,
    model_errors, portfolio_state, read_regular, strict, require,
)
from scripts.check_editorial_input_manifest import ManifestError


def run_regressions(data, schema, bindings, pub, projection, root):
    from scripts.check_chapter29_contract import (
        chapter_navigation_errors, document_errors, repository_errors,
    )
    from scripts.publication_projection import project_documents, is_policy_scan_field

    count = 0
    site = strict((root / "site-pages.json").read_bytes())
    require(not chapter_navigation_errors(site), "canonical-chapter-navigation")
    for chapter, order in [(29, 72), (29, 213), (28, 215)]:
        changed = deepcopy(site)
        source = (DOCUMENTS[0] if chapter == 29
                  else "manuscript/28-ai-assisted-analysis-assurance.md")
        next(r for r in changed["pages"] if r["source"] == source)["order"] = order
        require(bool(chapter_navigation_errors(changed)), f"chapter-order-regression-{chapter}-{order}")
        count += 1
    cases = strict((root / "tests/fixtures/chapter29/state-corpus.json").read_bytes())
    require([c["expected"] for c in cases] == list(STATUSES), "six-state-corpus")
    for c in cases:
        require(portfolio_state(**c["input"]) == c["expected"], c["id"])
        count += 1
    for bad in [dict(assembled=False, reviewed=True, sufficient=True, approved=False, superseded=False),
                dict(assembled=True, reviewed=True, sufficient=False, approved=True, superseded=False),
                dict(assembled=True, reviewed=True, sufficient=True, approved=False, superseded=True),
                dict(assembled=1, reviewed=True, sufficient=True, approved=False, superseded=False)]:
        try:
            portfolio_state(**bad)
        except ValueError:
            count += 1
        else:
            raise ValueError("CAP29 invalid transition accepted")

    def rejects(label, path, value):
        nonlocal count
        d = deepcopy(data)
        target = d
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        try:
            result = model_errors(d, schema, bindings)
        except ManifestError:
            result = ["schema rejected"]
        require(bool(result), "counterexample-accepted: " + label)
        count += 1

    require(not model_errors(data, schema, bindings), "canonical-model")
    for i in range(32):
        for key, value in [("recordId", "borrowed-record"), ("sourceCaseId", "borrowed-case"),
                           ("versionSha256", "0" * 64), ("relationToFinal", "supersedes"),
                           ("evidenceTransfer", True), ("authorityTransfer", True),
                           ("parentChanged", True), ("receiptCreated", True),
                           ("integrationOwner", "different-owner")]:
            rejects(f"parent-{i}-{key}", ("artifacts", i, key), value)
        rejects(f"state-{i}", ("artifacts", i, "nativeState", "verbatim"), "Passed")
    rejects("missing-artifact", ("artifacts",), data["artifacts"][:-1])
    rejects("duplicate-artifact", ("artifacts", 1), data["artifacts"][0])
    rejects("collapse-finding-retest", ("stages", 4, "artifactIds"), ["ART-04"])
    rejects("collapse-timeline-rca", ("stages", 7, "artifactIds"), ["ART-07"])
    for i in range(12):
        rejects(f"unreachable-{i}", ("stages", i, "inputIds"), ["unknown-step"])
    for i in range(4):
        rejects(f"invent-observation-{i}", ("documentaryEvidence", i, "systemObservation"), True)
        rejects(f"wrong-proof-{i}", ("documentaryEvidence", i, "line"), 1)
        rejects(f"wrong-gap-owner-{i}", ("actions", i, "owner"), "other-owner")
        rejects(f"wrong-gap-deadline-{i}", ("actions", i, "dueAt"), "2026-10-29T00:00:00Z")
        rejects(f"action-executed-{i}", ("actions", i, "executed"), True)
    for i in (0, 3):
        rejects(f"missing-is-not-inconclusive-{i}", ("gaps", i, "kind"), "Inconclusive")
    rejects("inconclusive-is-not-missing", ("gaps", 1, "kind"), "Not collected")
    for i in range(2):
        rejects(f"brief-evidence-{i}", ("briefs", i, "evidenceIds"), ["AI-output"])
        rejects(f"brief-hides-gap-{i}", ("briefs", i, "gapIds"), [])
        rejects(f"brief-delivered-{i}", ("briefs", i, "deliveryStatus"), "delivered")
    for path, value in [(("executionAuthorized",), True), (("networkRequired",), True),
                        (("actualActions",), 1), (("actualCollections",), 1),
                        (("actualModelCalls",), 1), (("actualDeliveries",), 1),
                        (("decision", "approval"), "approved"),
                        (("decision", "receiptId"), "received"),
                        (("decision", "realAuthorization"), True),
                        (("record", "status"), "Approved"),
                        (("record", "sourceCutoff"), "2026-07-22T00:00:00Z"),
                        (("record", "deadline"), "2026-10-20T00:00:00Z"),
                        (("decision", "recommendedOption"), "OPT-CAP29-RESUME"),
                        (("options", 1, "requiredClosedGaps"), []),
                        (("judgment", "evidenceIds"), ["AI-output"]),
                        (("reassessment", "actionIds"), []),
                        (("reassessment", "triggers"), ["expiry"]),
                        (("reviews", 0, "result"), "real-human-approved"),
                        (("sourceIds",), ["AI-output"])]:
        rejects(str(path), path, value)
    # Unapproved prose/field drift cannot be published even if its semantic role is unchanged.
    for doc in projection.documents:
        spec = pub["documents"][doc.document_id]
        require(not document_errors(doc, spec, data), "canonical-projection")
        for field in doc.fields:
            changed = replace(field, text=field.text + " altered", normalized_text=field.normalized_text + " altered")
            changed_doc = replace(doc, fields=tuple(changed if f.ordinal == field.ordinal else f for f in doc.fields))
            require(bool(document_errors(changed_doc, spec, data)), "projected-field-drift")
            count += 1
    # Whole documents include preamble/tail; shared owners handle unsafe syntax.
    samples = {}
    for i, doc in enumerate(DOCUMENTS):
        original = (root / doc).read_text()
        for label, addition in [("action", "実Tokenを取得する。"),
                                ("host", "https://real-target.net/"),
                                ("syntax", "{% include missing.html %}")]:
            samples[f"{i}-{label}"] = original + "\n\n" + addition + "\n"
    for doc in project_documents(samples).documents:
        i = int(doc.document_id.split("-")[0])
        label = doc.document_id.split("-")[1]
        if label == "syntax":
            require(bool(doc.diagnostics), "unsupported-syntax-diagnostic")
        else:
            from scripts.content_safety_policy import scan_action_text, scan_host_policy
            tail = [f for f in doc.fields if is_policy_scan_field(f)][-1]
            scanner = scan_action_text if label == "action" else scan_host_policy
            require(bool(scanner(tail.normalized_text, location=tail.location)), "shared-tail-detection")
        require(bool(document_errors(doc, pub["documents"][DOCUMENTS[i]], data)), "tail-safety")
        count += 1
    # Filesystem boundary probes only in this worktree's owned scratch directory.
    tmp = root / ".tmp"
    tmp.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chapter29-", dir=tmp) as directory:
        folder = Path(directory)
        (folder / "known").write_text("known")
        require(read_regular(folder, "known", {"known"}) == b"known", "reader-positive")
        (folder / "alias").symlink_to("known")
        (folder / "big").write_bytes(b"x" * 1_048_577)
        (folder / "directory").mkdir()
        for name, allowed in [("alias", {"alias"}), ("big", {"big"}),
                              ("directory", {"directory"}), ("../known", {"../known"}),
                              ("unknown", {"known"})]:
            try:
                read_regular(folder, name, allowed)
            except (OSError, ValueError):
                count += 1
            else:
                raise ValueError("CAP29 file boundary accepted: " + name)
    for raw in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}']:
        try:
            strict(raw)
        except (ValueError, ManifestError):
            count += 1
        else:
            raise ValueError("CAP29 non-strict JSON accepted")
    # Repository joins are checked independently of the model and publication hashes.
    require(bool(repository_errors(root, data, bindings, pub)), "repository-positive")
    for key in ("parents", "artifacts", "documentaryEvidence", "stages"):
        b = deepcopy(bindings)
        if key == "parents":
            b[key][next(iter(b[key]))] = "0" * 64
            try:
                repository_errors(root, data, b, pub)
            except ValueError:
                count += 1
            else:
                raise ValueError("CAP29 parent hash drift accepted")
        else:
            b[key] = []
            require(bool(model_errors(data, schema, b)), "binding-drift")
            count += 1
    return count
