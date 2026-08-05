#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.render_reference_baseline import (  # noqa: E402
    render as render_reference_baseline,
)
from scripts.sync_book_site import (  # noqa: E402
    SitePageRegistryError,
    parse_registry_data,
)

ERRORS: list[str] = []

EXPECTED_CHAPTER02_PAGES = {
    (
        "manuscript/02-law-ethics-authorization.md",
        "chapters/chapter-02/index.md",
        "chapters",
        45,
    ),
    (
        "templates/authorization-checklist.md",
        "templates/authorization-checklist/index.md",
        "additional",
        232,
    ),
    (
        "cases/ch02-authorization-decision-example.md",
        "cases/chapter-02-authorization-decision/index.md",
        "additional",
        233,
    ),
}


def error(message: str) -> None:
    ERRORS.append(message)


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        error(f"missing required file: {relative}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        error(f"{relative}: not valid UTF-8: {exc}")
        return ""


def load_json(relative: str) -> dict:
    text = read_text(relative)
    if not text:
        return {}
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        error(f"{relative}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        error(f"{relative}: root must be an object")
        return {}
    return value


def require_tokens(relative: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in text:
            error(f"{relative}: missing required token {token!r}")


def chapter02_page_contract_errors(registry: dict, label: str) -> list[str]:
    messages: list[str] = []
    pages = registry.get("pages", [])
    if not isinstance(pages, list):
        return [f"{label}: pages must be an array"]

    actual_tuples = [
        (
            item.get("source"),
            item.get("destination"),
            item.get("section"),
            item.get("order"),
        )
        for item in pages
        if isinstance(item, dict)
    ]
    tuple_counts = Counter(actual_tuples)
    route_counts = Counter(item[:2] for item in actual_tuples)
    for expected in sorted(EXPECTED_CHAPTER02_PAGES):
        tuple_count = tuple_counts[expected]
        if tuple_count != 1:
            messages.append(
                f"{label}: expected Chapter 2 page tuple exactly once: "
                f"{expected!r}; found {tuple_count}"
            )
        route_count = route_counts[expected[:2]]
        if route_count != 1:
            messages.append(
                f"{label}: expected Chapter 2 source/destination exactly once: "
                f"{expected[:2]!r}; found {route_count}"
            )
    return messages


def registry_mutation_is_rejected(registry: dict, label: str) -> bool:
    try:
        parsed = parse_registry_data(registry, label)
    except SitePageRegistryError:
        return True
    return bool(chapter02_page_contract_errors(parsed, label))


def source_ids(text: str) -> set[str]:
    return set(re.findall(r"\bSRC-[A-Z0-9-]+\b", text))


def chapter_body_and_references(text: str) -> tuple[str, str]:
    marker = "## 参考文献・Source Note ID"
    if marker not in text:
        return text, ""
    body, references = text.split(marker, 1)
    return body, references


def check_reserved_names(relative: str, text: str) -> None:
    allowed_suffixes = (".example", ".test", ".invalid", ".localhost")
    for raw_url in re.findall(r"https?://[^\s`)\]>]+", text):
        host = (urlparse(raw_url).hostname or "").lower()
        if host and not host.endswith(allowed_suffixes):
            error(f"{relative}: non-reserved URL in synthetic content: {raw_url}")

    domain_pattern = re.compile(
        r"(?<![A-Za-z0-9_-])(?:[A-Za-z0-9-]+\.)+(?:com|net|org|jp|io|dev|app|cloud)(?![A-Za-z0-9_-])",
        re.IGNORECASE,
    )
    for domain in domain_pattern.findall(text):
        error(f"{relative}: possible real domain in synthetic content: {domain}")


def main() -> int:
    required_files = (
        "manuscript/02-law-ethics-authorization.md",
        "templates/authorization-checklist.md",
        "cases/ch02-authorization-decision-example.md",
        "scripts/check_chapter02_contract.py",
        "site-pages.json",
        "artifact-index.md",
        "figure-index.md",
        "glossary.md",
        "cases/index.md",
        "index.md",
        "book-config.json",
        "references/sources.json",
        "references/reference-baseline.md",
        "references/ch02-source-review-2026-08-05.md",
        "package.json",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            error(f"missing required file: {relative}")

    config = load_json("book-config.json")
    chapters = config.get("structure", {}).get("chapters", [])
    chapter_config = next(
        (
            item
            for item in chapters
            if isinstance(item, dict)
            and item.get("id") == "ch02-law-ethics-authorization"
        ),
        None,
    )
    expected_objectives = [
        "許可とスコープを文書化できる",
        "停止条件を定義できる",
        "責任ある開示の流れを説明できる",
    ]
    if chapter_config is None:
        error("book-config.json: missing ch02-law-ethics-authorization")
    elif chapter_config.get("objectives") != expected_objectives:
        error("book-config.json: chapter 2 learning objectives changed unexpectedly")

    chapter_path = "manuscript/02-law-ethics-authorization.md"
    chapter = read_text(chapter_path)
    require_tokens(
        chapter_path,
        chapter,
        (
            "## この章の位置付け",
            "## 学習目標",
            "## 前提知識",
            "## 導入ケース",
            "Authority Gate",
            "Scope Gate",
            "Safety Gate",
            "Disclosure Gate",
            "F-02-01",
            "T-02-01",
            "書面による許可",
            "Data、Secret、証拠の取扱い",
            "委託、再委託、Cloud / SaaS",
            "脆弱性を発見したとき",
            "Stop condition",
            "Cleanup",
            "## 7. 四つの視点",
            "## 8. Handoff Contract",
            "## 9. 安全な演習",
            "ART-13 Authorization Checklist",
            "## 11. 評価基準",
            "## 12. よくある誤解",
            "## 章のまとめ",
            "## 次に学ぶこと",
            "## 参考文献・Source Note ID",
            "SRC-JP-LAW-001",
            "SRC-IPA-VDP-001",
            "Proceed with conditions",
            "Do not proceed",
            "Escalate",
            "## 本章の責任境界",
            "### OWN",
            "### BRIDGE",
            "### DELEGATE",
            "本書は、実務上のAuthorization Gateと後続工程へのHandoffに責任を持つ。",
            "本章は法的助言を提供せず、個別事案の法的判断と法令解釈は専門家へ委譲する。",
            "委譲先へのリンクを読まなくても、第2章の論旨と運用判断は単独で成立する。",
            "個別事案の法的助言と法令解釈は、適格な法務・契約専門家へ委譲する",
            "第8章の安全なLabとEvidence取扱い",
            "第9章のRules of Engagement",
            "第10章のReconnaissance / OSINT境界",
            "第15章のFinding、Remediation、Retest、Responsible Disclosure",
            "第19章のIncidentとPersonal Data対応",
            (
                "詳細な攻撃技法と脆弱性の悪用は、許可済み評価の専門的な方法、"
                "成果物、安全境界を詳述する[実務で使えるペネトレーションテスト大全]"
                "(https://itdojp.github.io/pentest-learning-book/)へ委譲する"
            ),
            (
                "認証・認可Protocol内部と安全な実装は、OAuth、OIDC、SAML等の設計と"
                "実装を詳述する[実践 認証認可システム設計]"
                "(https://itdojp.github.io/practical-auth-book/)へ委譲する"
            ),
            (
                "Infrastructure Hardeningと防御実装は、Network、OS、Cloud、Containerの"
                "Security実装を詳述する[インフラエンジニアのための情報セキュリティ実装ガイド]"
                "(https://itdojp.github.io/it-infra-security-guide-book/)へ委譲する"
            ),
        ),
    )
    if re.search(r"https://github\.com/[^\s)]+/blob/main(?:/|\b)", chapter):
        error(
            f"{chapter_path}: mutable GitHub blob/main URL must not be used as a "
            "delegated publication target"
        )
    for forbidden in (
        "善意の研究であれば明示的な許可は不要である。",
        "管理者権限があれば業務上の承認も不要である。",
        "脆弱性を発見したら影響を最大まで実証する。",
        "届出後は関係者との調整を待たず公開する。",
    ):
        if forbidden in chapter:
            error(f"{chapter_path}: unsafe or unsupported assertion {forbidden!r}")

    body, references = chapter_body_and_references(chapter)
    used_ids = source_ids(body)
    listed_ids = source_ids(references)
    expected_source_ids = {"SRC-JP-LAW-001", "SRC-IPA-VDP-001"}
    if used_ids != expected_source_ids:
        error(
            f"{chapter_path}: body source IDs {sorted(used_ids)} != expected {sorted(expected_source_ids)}"
        )
    if listed_ids != used_ids:
        error(
            f"{chapter_path}: chapter-end source IDs {sorted(listed_ids)} != body {sorted(used_ids)}"
        )

    template_path = "templates/authorization-checklist.md"
    template = read_text(template_path)
    require_tokens(
        template_path,
        template,
        (
            "Artifact ID | `ART-13`",
            "Authorization Record ID",
            "Parent Case ID",
            "Relation | `refines` / `supersedes` / `independent`",
            "Decision Requirement ID",
            "Available decisions | Proceed / Proceed with conditions / Do not proceed / Escalate",
            "## 2. Authority Gate",
            "## 3. Scope Gate",
            "## 4. Safety Gate",
            "## 5. Disclosure Gate",
            "Authority evidence",
            "Legal, Contractual, and Policy Questions",
            "Conditions",
            "Decision Record",
            "RoE Handoff",
            "Reassessment",
            "Traceability Check",
            "Technical correctness",
            "Safety / authorization",
            "Legal / contractual source quality",
            "Evidence / traceability",
            "Decision usefulness",
        ),
    )

    example_path = "cases/ch02-authorization-decision-example.md"
    example = read_text(example_path)
    require_tokens(
        example_path,
        example,
        (
            "ART-13",
            "AUTH-CASE-2026-001",
            "CASE-2026-001",
            "| Relation | `refines` |",
            "DR-AUTH-2026-001",
            "EVD-AUTH-2026-001",
            "COND-AUTH-2026-001",
            "DEC-AUTH-2026-001",
            "HO-AUTH-2026-001",
            "REA-AUTH-2026-001",
            "Proceed with conditions",
            "tenant-auth-lab-01.test",
            "billing-bridge.example",
            "Production credentialを操作しない",
            "外部Networkをdefault denyにする",
            "想定外脆弱性発見時は直ちに停止する",
            "この表は合成Case内の記入例であり、実際の章Gateまたは法的承認の証跡ではない。",
            "SYNTH-REV-AUTH-TECH-001",
            "SYNTH-REV-AUTH-SAFE-001",
            "SYNTH-REV-AUTH-LAW-001",
            "SYNTH-REV-AUTH-EVD-001",
            "SYNTH-REV-AUTH-DEC-001",
        ),
    )
    check_reserved_names(example_path, example)

    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        re.compile(r"(?i)(?:password|api[_-]?key|secret|token)\s*[:=]\s*[A-Za-z0-9+/=_-]{16,}"),
    )
    for pattern in secret_patterns:
        if pattern.search(example):
            error(f"{example_path}: possible real credential or secret pattern detected")

    raw_registry = load_json("site-pages.json")
    try:
        registry = parse_registry_data(raw_registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: invalid registry: {exc}")
        registry = {}
    for message in chapter02_page_contract_errors(registry, "site-pages.json"):
        error(message)

    pages = raw_registry.get("pages", [])
    chapter_page = next(
        (
            item
            for item in pages
            if isinstance(item, dict)
            and item.get("source") == "manuscript/02-law-ethics-authorization.md"
        ),
        None,
    ) if isinstance(pages, list) else None
    if chapter_page is None:
        error("site-pages.json: missing Chapter 2 manuscript page for negative regressions")
    else:
        negative_registries: list[tuple[str, dict]] = []

        mutation = deepcopy(raw_registry)
        mutation["schemaVersion"] = "0.0.0"
        negative_registries.append(("schemaVersion drift", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["section"] = "additional"
        negative_registries.append(("section drift", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["order"] = 46
        negative_registries.append(("order drift", mutation))

        mutation = deepcopy(raw_registry)
        duplicated_page = next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )
        mutation["pages"].append(deepcopy(duplicated_page))
        negative_registries.append(("duplicate page", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["unexpectedKey"] = True
        negative_registries.append(("unknown page key", mutation))

        for mutation_name, mutated_registry in negative_registries:
            if not registry_mutation_is_rejected(
                mutated_registry,
                f"site-pages.json negative regression ({mutation_name})",
            ):
                error(
                    "site-pages.json: negative registry mutation was accepted: "
                    f"{mutation_name}"
                )

    artifact_index = read_text("artifact-index.md")
    require_tokens(
        "artifact-index.md",
        artifact_index,
        (
            "| ART-13 | Authorization Checklist | 2, 9 | `templates/authorization-checklist.md` |",
            "cases/ch02-authorization-decision-example.md",
        ),
    )

    figure_index = read_text("figure-index.md")
    require_tokens(
        "figure-index.md",
        figure_index,
        (
            "F-02-01",
            "Authorization Decision Gate",
            "T-02-01",
            "許容性判断の層",
        ),
    )

    glossary = read_text("glossary.md")
    require_tokens(
        "glossary.md",
        glossary,
        (
            "| Authority |",
            "| Authorization |",
            "| Data Owner |",
            "| Responsible Disclosure |",
            "| Rules of Engagement |",
            "| Scope |",
        ),
    )

    cases_index = read_text("cases/index.md")
    index = read_text("index.md")
    require_tokens(
        "cases/index.md",
        cases_index,
        (
            "ch02-authorization-decision-example.md",
            "Authorization Checklist",
        ),
    )
    require_tokens(
        "index.md",
        index,
        (
            "manuscript/02-law-ethics-authorization.md",
            "templates/authorization-checklist.md",
            "cases/ch02-authorization-decision-example.md",
        ),
    )

    sources = load_json("references/sources.json")
    if sources.get("checkedAt") != "2026-07-25":
        error(
            "references/sources.json: registry-level checkedAt must remain 2026-07-25; "
            "only the two Chapter 2 source entries were re-audited"
        )
    source_entries = {
        item.get("id"): item
        for item in sources.get("sources", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for source_id in sorted(expected_source_ids):
        entry = source_entries.get(source_id)
        if entry is None:
            error(f"references/sources.json: missing {source_id}")
            continue
        chapters = entry.get("chapters", [])
        if 2 not in chapters:
            error(f"references/sources.json: {source_id} does not map chapter 2")

    expected_source_metadata = {
        "SRC-JP-LAW-001": {
            "version": "current display effective 2025-06-01",
            "checkedAt": "2026-08-05",
            "nextReviewAt": "2026-11-05",
            "noteMarkers": (
                "e-Gov current display was rechecked on 2026-08-05",
                "law effective from 2025-06-01",
                "confirm current text before publication",
                "book is not legal advice",
            ),
        },
        "SRC-IPA-VDP-001": {
            "version": "2024 edition",
            "checkedAt": "2026-08-05",
            "nextReviewAt": "2026-11-05",
            "noteMarkers": (
                "official IPA page and linked 2024 edition guideline were rechecked on 2026-08-05",
                "official page showed last update 2026-04-06",
                "current page and linked guideline must be rechecked at publication time",
            ),
        },
    }
    for source_id, expected in expected_source_metadata.items():
        entry = source_entries.get(source_id)
        if entry is None:
            continue
        for field in ("version", "checkedAt", "nextReviewAt"):
            if entry.get(field) != expected[field]:
                error(
                    f"references/sources.json: {source_id}.{field} "
                    f"must be {expected[field]!r}"
                )
        notes = entry.get("notes")
        if not isinstance(notes, str):
            error(f"references/sources.json: {source_id}.notes must be a string")
            continue
        for marker in expected["noteMarkers"]:
            if marker not in notes:
                error(
                    f"references/sources.json: {source_id}.notes missing marker {marker!r}"
                )

    audit_note_path = "references/ch02-source-review-2026-08-05.md"
    audit_note = read_text(audit_note_path)
    require_tokens(
        audit_note_path,
        audit_note,
        (
            "SRC-JP-LAW-001",
            "2025-06-01施行表示",
            "SRC-IPA-VDP-001",
            "2024年版",
            "2026-04-06",
            "Checked at | 2026-08-05",
        ),
    )

    baseline_path = "references/reference-baseline.md"
    baseline = read_text(baseline_path)
    if baseline != render_reference_baseline():
        error(f"{baseline_path}: out of sync with references/sources.json")

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter02") != "python3 scripts/check_chapter02_contract.py":
        error("package.json: missing check:chapter02 script")
    if "check:chapter02" not in scripts.get("test", ""):
        error("package.json: npm test does not include check:chapter02")

    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1

    print(
        "chapter 2 contract passed: manuscript, authorization artifact, synthetic case, "
        "source mapping, publication registry, safety boundary, and handoff traceability"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
