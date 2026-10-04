#!/usr/bin/env python3
"""Finite Issue #110 navigation/boundary checks; not a learning assessor.

The shared locked publication projection owns Markdown, links and visibility.
The shared Content Safety Policy owns safety grammar. This module only checks
the declared beginner route and required authored reader-boundary markers.
It does not prove the learner's understanding or the underlying Case evidence.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION, scan_fields, scan_host_policy,
)
from scripts.check_editorial_input_manifest import (  # noqa: E402
    _reject_constant, _reject_duplicate_keys,
)
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION,
    destination_fields,
    is_absolute_destination,
    project_documents,
    scannable_text_fields,
)

GUIDE = "cases/first-artifact-walkthrough.md"
INPUTS = ("quickstart.md", GUIDE, "site-pages.json", "package.json")
ROUTE = {
    "source": GUIDE,
    "destination": "cases/first-artifact-walkthrough/index.md",
    "section": "additional",
    "order": 340,
    "title": "最初の成果物：判断と証拠不足の読解",
}
HEADINGS = (
    ROUTE["title"], "この読解の範囲", "1. 五つの要素を読む",
    "判断要求", "一つの脅威仮説", "一つの観測計画", "一つの証拠不足",
    "次の判断", "2. 空Templateへ必要な欄から戻る", "3. 誤った結論を直す",
    "4. 提出と自己点検", "5. 完全例と次の学習へ",
)
MARKERS = (
    "学習用の抜粋", "実行・収集・承認を行わない", "現在の操作許可に転用しない",
    "DR-2026-001", "TH-2026-003", "OBS-2026-003", "VAL-2026-003",
    "NEG-2026-001", "EVD-2026-004", "HUNT-2026-001", "Inconclusive",
    "72日", "18日", "Not collected", "Draft", "Owner", "確認期限",
    "実務上の必須欄を免除したことにはならない", "誤った例", "Reassessment Due",
    "読者による試行は未実施", "AIのレビューやCI成功を読者試行として数えない",
)
DESTINATIONS = {
    "quickstart.md": (
        "../cases/first-artifact-walkthrough/",
        "../templates/integrated-security-case-map/",
        "../cases/chapter-01-integrated-security-case/",
        "../reading-guide/", "../chapters/chapter-01/",
    ),
    GUIDE: (
        "../chapter-01-integrated-security-case/",
        "../../templates/integrated-security-case-map/", "../../quickstart/",
        "../../reading-guide/", "../../chapters/chapter-01/",
    ),
}


def read_input(root: Path, relative: str) -> str:
    """Read bounded fixed inputs without following symlinks or opening devices."""
    if relative not in INPUTS or root.is_symlink():
        raise ValueError("LR-fixed-input")
    path = root / relative
    if any(p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root)):
        raise ValueError(f"LR-symlink: {relative}")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError(f"LR-not-regular: {relative}")
        raw = stream.read(1_048_577)
    if len(raw) > 1_048_576:
        raise ValueError(f"LR-input-size: {relative}")
    return raw.decode("utf-8")


def check_route(registry: dict, package: dict) -> list[str]:
    if not isinstance(registry, dict) or not isinstance(package, dict):
        raise ValueError("LR-json-root: expected object")
    errors = []
    pages = registry.get("pages", [])
    if not isinstance(pages, list) or any(not isinstance(p, dict) for p in pages):
        raise ValueError("LR-pages: expected array of objects")
    if [p for p in pages if p.get("source") == GUIDE] != [ROUTE]:
        errors.append("LR-route: learning route missing, duplicated or changed")
    if sum(p.get("destination") == ROUTE["destination"] for p in pages) != 1:
        errors.append("LR-destination: route must have one owner")
    if sum((p.get("section"), p.get("order")) == (ROUTE["section"], ROUTE["order"])
           for p in pages) != 1:
        errors.append("LR-order: navigation order must have one owner")
    scripts = package.get("scripts", {})
    if not isinstance(scripts, dict) or not isinstance(scripts.get("test", ""), str):
        raise ValueError("LR-scripts: expected string test command")
    if scripts.get("check:learning-route") != (
        "python3 scripts/check_learning_route.py && python3 tests/test_learning_route.py"
    ):
        errors.append("LR-command: checker/unit invocation drift")
    if "npm run check:learning-route" not in scripts.get("test", "").split(" && "):
        errors.append("LR-test-owner: learning route is not owned by npm test")
    return errors


def check_documents(documents: dict[str, str]) -> list[str]:
    if set(documents) != {"quickstart.md", GUIDE}:
        return ["LR-document-set: unexpected or missing document"]
    result = project_documents(documents)
    errors = [f"{d.code}: {d.location}: {d.reason}" for d in result.diagnostics]
    errors.extend(
        f"LR-safety: {finding.location}: {finding.category}"
        for finding in scan_fields((f.location, f.normalized_text) for f in scannable_text_fields(result))
    )
    for field in destination_fields(result):
        if is_absolute_destination(field.normalized_text):
            errors.extend(
                f"LR-safety: {finding.location}: {finding.category}"
                for finding in scan_host_policy(field.normalized_text, location=field.location)
            )
    guide_fields = [f for f in result.fields if f.document_id == GUIDE]
    headings = [f.text for f in guide_fields if f.element_kind == "heading"
                and f.field_type == "reader_visible_text"]
    if headings != list(HEADINGS):
        errors.append("LR-heading-inventory: reviewed reader surface changed")
    visible = "\n".join(f.text for f in guide_fields if f.field_type == "reader_visible_text")
    errors.extend(f"LR-boundary-marker: {token}" for token in MARKERS if token not in visible)
    for document_id, required in DESTINATIONS.items():
        actual = {f.text for f in destination_fields(result) if f.document_id == document_id}
        errors.extend(f"LR-link: {document_id}: {target}" for target in required if target not in actual)
    return errors


def main() -> int:
    try:
        inputs = {name: read_input(ROOT, name) for name in INPUTS}
        registry, package = (
            json.loads(inputs[name], object_pairs_hook=_reject_duplicate_keys,
                       parse_constant=_reject_constant)
            for name in ("site-pages.json", "package.json")
        )
        errors = check_route(registry, package)
        errors.extend(check_documents({name: inputs[name] for name in ("quickstart.md", GUIDE)}))
    except (OSError, ValueError, TypeError, RuntimeError, KeyError) as exc:
        print(f"Learning route failed closed: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"Learning route passed: 2 reader surfaces; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
