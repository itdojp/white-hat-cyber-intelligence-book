#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import sync_site_source as base  # noqa: E402
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION as CONTENT_SAFETY_POLICY_VERSION,
    SafetyFinding,
    scan_fields,
)

REGISTRY_PATH = ROOT / "site-pages.json"
SCHEMA_VERSION = "1.1.0"
DIRECTORY_RE = re.compile(r"^[A-Za-z0-9_-]+$")
STATIC_PATH_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*\.json$")
LINE_TERMINATOR_RE = re.compile(r"[\r\n\u2028\u2029]")
ALLOWED_SECTIONS = set(base.SECTION_ORDER)
ALLOWED_CANONICAL_DIRECTORIES = {"cases", "schemas"}
RESERVED_DESTINATION_ROOTS = {
    "_data",
    "_includes",
    "_layouts",
    "assets",
}
STATIC_DESTINATION_ROOT = "downloads"
ALLOWED_STATIC_SUFFIXES = {".json"}
MAX_STATIC_FILE_BYTES = 1024 * 1024


@dataclass(frozen=True)
class StaticFile:
    source: str
    destination: str


STATIC_FILES: tuple[StaticFile, ...] = ()
BASE_REWRITE_LINKS = base.rewrite_links
BASE_GENERATE = base.generate


class SitePageRegistryError(base.SiteGenerationError):
    pass


def lexical_absolute(path: Path) -> Path:
    return Path(os.path.abspath(path))


def require_repository_path(
    root: Path,
    path: Path,
    label: str,
    *,
    kind: str,
) -> Path:
    """Validate an existing repository path without following symlinks outside root."""
    lexical_root = lexical_absolute(root)
    lexical_path = lexical_absolute(path)
    try:
        relative = lexical_path.relative_to(lexical_root)
    except ValueError as exc:
        raise SitePageRegistryError(
            f"{label} is outside the repository root: {lexical_path}"
        ) from exc

    current = lexical_root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise SitePageRegistryError(
                f"{label} must not contain a symbolic-link component: {current}"
            )

    if kind == "file" and not lexical_path.is_file():
        raise SitePageRegistryError(f"{label} is not a regular file: {lexical_path}")
    if kind == "directory" and not lexical_path.is_dir():
        raise SitePageRegistryError(f"{label} is not a directory: {lexical_path}")

    try:
        resolved_root = lexical_root.resolve(strict=True)
        resolved_path = lexical_path.resolve(strict=True)
    except OSError as exc:
        raise SitePageRegistryError(f"cannot resolve {label}: {exc}") from exc
    if resolved_path != resolved_root and resolved_root not in resolved_path.parents:
        raise SitePageRegistryError(
            f"{label} resolves outside the repository root: {resolved_path}"
        )
    return resolved_path


def validate_canonical_tree(root: Path, directory: Path, label: str) -> None:
    require_repository_path(root, directory, label, kind="directory")
    for candidate in sorted(directory.rglob("*")):
        candidate_label = f"{label}/{candidate.relative_to(directory).as_posix()}"
        if candidate.is_symlink():
            raise SitePageRegistryError(
                f"{candidate_label} must not be a symbolic link"
            )
        if candidate.is_dir():
            require_repository_path(root, candidate, candidate_label, kind="directory")
        elif candidate.is_file():
            require_repository_path(root, candidate, candidate_label, kind="file")
        else:
            raise SitePageRegistryError(
                f"{candidate_label} must be a regular file or directory"
            )


def schema_markdown_path(value: object, label: str) -> str:
    """Enforce the schema pattern and the repository's safe relative-path policy."""
    if not isinstance(value, str):
        raise SitePageRegistryError(f"{label} must be a string")
    if LINE_TERMINATOR_RE.search(value):
        raise SitePageRegistryError(
            f"{label} must not contain CR, LF, U+2028, or U+2029"
        )
    # Validate the raw JSON value before pathlib normalizes a trailing slash.
    # For example, Path("cases/example.md/") becomes "cases/example.md".
    if not value.endswith(".md"):
        raise SitePageRegistryError(f"{label} must end in .md: {value}")
    try:
        path = base.safe_relative_path(value, label).as_posix()
    except base.SiteGenerationError as exc:
        raise SitePageRegistryError(str(exc)) from exc
    if not path.endswith(".md"):
        raise SitePageRegistryError(f"{label} must end in .md: {path}")
    return path


def schema_static_path(value: object, label: str) -> str:
    """Validate a static artifact path before source/destination policy checks."""
    if not isinstance(value, str):
        raise SitePageRegistryError(f"{label} must be a string")
    if LINE_TERMINATOR_RE.search(value):
        raise SitePageRegistryError(
            f"{label} must not contain CR, LF, U+2028, or U+2029"
        )
    if not any(value.endswith(suffix) for suffix in ALLOWED_STATIC_SUFFIXES):
        raise SitePageRegistryError(
            f"{label} must end in an approved static artifact suffix: {value}"
        )
    try:
        path = base.safe_relative_path(value, label)
    except base.SiteGenerationError as exc:
        raise SitePageRegistryError(str(exc)) from exc
    normalized = path.as_posix()
    if normalized != value or not STATIC_PATH_RE.fullmatch(value):
        raise SitePageRegistryError(
            f"{label} must be a normalized URL-safe relative JSON path: {value}"
        )
    if any(part.startswith((".", "_")) for part in path.parts):
        raise SitePageRegistryError(
            f"{label} must not use hidden or Jekyll-reserved path components: "
            f"{normalized}"
        )
    if path.suffix not in ALLOWED_STATIC_SUFFIXES:
        raise SitePageRegistryError(
            f"{label} must use an approved static artifact suffix: {normalized}"
        )
    return normalized


def validate_static_json(data: bytes, label: str) -> None:
    if not data:
        raise SitePageRegistryError(f"{label} must not be empty")
    if len(data) > MAX_STATIC_FILE_BYTES:
        raise SitePageRegistryError(
            f"{label} exceeds the {MAX_STATIC_FILE_BYTES}-byte publication limit"
        )
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SitePageRegistryError(f"{label} must be UTF-8 JSON") from exc

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-standard JSON constant: {value}")

    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        decoded = json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise SitePageRegistryError(
            f"{label} must be strict RFC-compatible JSON: {exc}"
        ) from exc
    if not isinstance(decoded, (dict, list)):
        raise SitePageRegistryError(
            f"{label} JSON root must be an object or array"
        )


def published_page_title_findings(
    registry: dict,
    label: str = "site-pages.json",
) -> list[SafetyFinding]:
    """Scan every explicit reader-visible registry title through the shared Policy."""

    fields: list[tuple[str, str]] = []
    for index, item in enumerate(registry.get("pages", [])):
        if not isinstance(item, dict):
            continue
        title = item.get("title")
        if not isinstance(title, str):
            continue
        source = item.get("source", "<invalid-source>")
        destination = item.get("destination", "<invalid-destination>")
        location = (
            f"{label}: pages[{index}].title "
            f"({source} -> {destination})"
        )
        fields.append((location, title))
    return scan_fields(fields)


def parse_registry_data(value: object, label: str = "site-pages.json") -> dict:
    """Enforce every constraint declared by schemas/site-pages.schema.json."""
    if not isinstance(value, dict):
        raise SitePageRegistryError(f"{label} root must be a JSON object")
    registry = dict(value)

    allowed_keys = {
        "schemaVersion",
        "canonicalDirectories",
        "pages",
        "directoryRoutes",
        "staticFiles",
    }
    required_keys = {
        "schemaVersion",
        "canonicalDirectories",
        "pages",
        "directoryRoutes",
    }
    unknown = set(registry) - allowed_keys
    if unknown:
        raise SitePageRegistryError(
            f"{label} has unknown keys: {sorted(unknown)}"
        )
    missing = required_keys - set(registry)
    if missing:
        raise SitePageRegistryError(
            f"{label} is missing keys: {sorted(missing)}"
        )
    if registry.get("schemaVersion") != SCHEMA_VERSION:
        raise SitePageRegistryError(
            f"{label} schemaVersion must be {SCHEMA_VERSION}"
        )

    canonical_directories = registry["canonicalDirectories"]
    if not isinstance(canonical_directories, list):
        raise SitePageRegistryError("canonicalDirectories must be an array")
    seen_directories: set[str] = set()
    for index, directory in enumerate(canonical_directories):
        if not isinstance(directory, str) or not DIRECTORY_RE.fullmatch(directory):
            raise SitePageRegistryError(
                f"canonicalDirectories[{index}] is invalid: {directory!r}"
            )
        if directory not in ALLOWED_CANONICAL_DIRECTORIES:
            raise SitePageRegistryError(
                f"canonicalDirectories[{index}] is not an approved publication root: "
                f"{directory!r}"
            )
        if directory in seen_directories:
            raise SitePageRegistryError(
                f"canonicalDirectories contains duplicate value: {directory}"
            )
        seen_directories.add(directory)

    pages = registry["pages"]
    if not isinstance(pages, list):
        raise SitePageRegistryError("pages must be an array")
    allowed_page_keys = {"source", "destination", "section", "order", "title"}
    required_page_keys = {"source", "destination", "section", "order", "title"}
    for index, item in enumerate(pages):
        if not isinstance(item, dict):
            raise SitePageRegistryError(f"pages[{index}] must be an object")
        unknown_page_keys = set(item) - allowed_page_keys
        if unknown_page_keys:
            raise SitePageRegistryError(
                f"pages[{index}] has unknown keys: {sorted(unknown_page_keys)}"
            )
        missing_page_keys = required_page_keys - set(item)
        if missing_page_keys:
            raise SitePageRegistryError(
                f"pages[{index}] is missing keys: {sorted(missing_page_keys)}"
            )
        schema_markdown_path(item["source"], f"pages[{index}].source")
        schema_markdown_path(item["destination"], f"pages[{index}].destination")
        if item["section"] not in ALLOWED_SECTIONS:
            raise SitePageRegistryError(
                f"pages[{index}].section is invalid: {item['section']!r}"
            )
        order = item["order"]
        if (
            isinstance(order, bool)
            or not isinstance(order, (int, float))
            or order < 0
            or (isinstance(order, float) and not order.is_integer())
        ):
            raise SitePageRegistryError(
                f"pages[{index}].order must be a non-negative integer"
            )
        item["order"] = int(order)
        title = item["title"]
        if not isinstance(title, str) or not title:
            raise SitePageRegistryError(
                f"pages[{index}].title must be a non-empty string"
            )
        if LINE_TERMINATOR_RE.search(title):
            raise SitePageRegistryError(
                f"pages[{index}].title must not contain CR, LF, U+2028, or U+2029"
            )

    title_findings = published_page_title_findings(registry, label)
    if title_findings:
        details = "; ".join(
            f"{finding.location}: [{finding.category}] {finding.reason}: "
            f"{finding.normalized_excerpt!r}"
            for finding in title_findings
        )
        raise SitePageRegistryError(
            f"page title violates Content Safety Policy "
            f"{CONTENT_SAFETY_POLICY_VERSION}: {details}"
        )

    directory_routes = registry["directoryRoutes"]
    if not isinstance(directory_routes, dict):
        raise SitePageRegistryError("directoryRoutes must be an object")
    for directory, destination in directory_routes.items():
        if not isinstance(directory, str) or not DIRECTORY_RE.fullmatch(directory):
            raise SitePageRegistryError(
                f"directoryRoutes key is invalid: {directory!r}"
            )
        if directory not in seen_directories:
            raise SitePageRegistryError(
                f"directoryRoutes key must name a declared canonical directory: "
                f"{directory!r}"
            )
        schema_markdown_path(destination, f"directoryRoutes.{directory}")

    static_files = registry.setdefault("staticFiles", [])
    if not isinstance(static_files, list):
        raise SitePageRegistryError("staticFiles must be an array")
    allowed_static_keys = {"source", "destination"}
    seen_static_items: set[tuple[str, str]] = set()
    for index, item in enumerate(static_files):
        if not isinstance(item, dict):
            raise SitePageRegistryError(f"staticFiles[{index}] must be an object")
        unknown_static_keys = set(item) - allowed_static_keys
        if unknown_static_keys:
            raise SitePageRegistryError(
                f"staticFiles[{index}] has unknown keys: "
                f"{sorted(unknown_static_keys)}"
            )
        missing_static_keys = allowed_static_keys - set(item)
        if missing_static_keys:
            raise SitePageRegistryError(
                f"staticFiles[{index}] is missing keys: "
                f"{sorted(missing_static_keys)}"
            )
        source = schema_static_path(
            item["source"], f"staticFiles[{index}].source"
        )
        destination = validate_static_destination(
            item["destination"], f"staticFiles[{index}].destination"
        )
        static_item = (source, destination)
        if static_item in seen_static_items:
            raise SitePageRegistryError(
                f"staticFiles contains duplicate value: {static_item}"
            )
        seen_static_items.add(static_item)

    return registry


def load_registry() -> dict:
    require_repository_path(
        ROOT,
        REGISTRY_PATH,
        "site-pages.json",
        kind="file",
    )
    try:
        decoded = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SitePageRegistryError(f"invalid page registry JSON: {exc}") from exc
    return parse_registry_data(decoded)


def validate_destination(raw: str, label: str) -> str:
    destination = schema_markdown_path(raw, label)
    path = Path(destination)
    if not destination.endswith("/index.md"):
        raise SitePageRegistryError(
            f"{label} must be a pretty-route Markdown destination ending in /index.md: "
            f"{destination}"
        )
    if any(part.startswith((".", "_")) for part in path.parts):
        raise SitePageRegistryError(
            f"{label} must not use hidden or Jekyll-reserved path components: "
            f"{destination}"
        )
    if path.parts[0] in RESERVED_DESTINATION_ROOTS:
        raise SitePageRegistryError(
            f"{label} must not overwrite generated publication internals: {destination}"
        )
    return destination


def validate_static_destination(raw: str, label: str) -> str:
    destination = schema_static_path(raw, label)
    path = Path(destination)
    if path.parts[0] != STATIC_DESTINATION_ROOT or len(path.parts) < 2:
        raise SitePageRegistryError(
            f"{label} must be below {STATIC_DESTINATION_ROOT}/: {destination}"
        )
    return destination


def rewrite_registered_links(
    markdown: str,
    source: str,
    destination: str,
    source_to_destination: dict[str, str],
) -> str:
    # The common generator treats every registered target as a pretty-route page.
    # Static artifacts retain their filename, so rewrite them separately first.
    static_targets = {item.source: item.destination for item in STATIC_FILES}
    if not static_targets:
        return BASE_REWRITE_LINKS(
            markdown, source, destination, source_to_destination
        )

    source_path = ROOT / source
    current_dir = base.site_dir(destination)
    lines: list[str] = []
    in_code = False
    for line in markdown.splitlines():
        if base.CODE_FENCE_RE.match(line):
            in_code = not in_code
            lines.append(line)
            continue
        if in_code:
            lines.append(line)
            continue

        def replace(match: re.Match[str]) -> str:
            before, raw, after = match.groups()
            parsed = base.parse_link_target(raw)
            if parsed is None:
                return match.group(0)
            path, fragment, query, formatter = parsed
            if query:
                return match.group(0)
            target = (source_path.parent / path).resolve()
            try:
                target_relative = target.relative_to(ROOT).as_posix()
            except ValueError:
                return match.group(0)
            static_destination = static_targets.get(target_relative)
            if static_destination is None:
                return match.group(0)
            relative = posixpath.relpath(static_destination, current_dir)
            return before + formatter.format(url=relative + fragment) + after

        lines.append(base.LINK_RE.sub(replace, line))

    if in_code:
        raise SitePageRegistryError(
            f"{source}: unbalanced code fence during static link rewrite"
        )
    static_rewritten = "\n".join(lines).rstrip() + "\n"
    return BASE_REWRITE_LINKS(
        static_rewritten, source, destination, source_to_destination
    )


def generate_registered_site(
    output: Path,
    components: dict[str, bytes],
    revision: dict,
) -> dict[str, str]:
    previous_rewrite_links = base.rewrite_links
    base.rewrite_links = rewrite_registered_links
    try:
        BASE_GENERATE(output, components, revision)
    finally:
        base.rewrite_links = previous_rewrite_links

    static_manifest: list[dict[str, str]] = []
    for item in STATIC_FILES:
        data = (ROOT / item.source).read_bytes()
        base.write_bytes(output, item.destination, data)
        static_manifest.append(
            {
                "source": item.source,
                "destination": item.destination,
                "sha256": base.sha256_bytes(data),
            }
        )

    manifest_path = output / "_data" / "build-manifest.json"
    manifest = base.load_json(manifest_path)
    manifest["staticFiles"] = static_manifest
    base.write_bytes(
        output,
        "_data/build-manifest.json",
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )
    return base.tree_hashes(output)


def check_registered_determinism(
    components: dict[str, bytes], revision: dict
) -> None:
    before = base.repository_state_hashes()
    with tempfile.TemporaryDirectory(
        prefix="book-site-registry-a-"
    ) as first_tmp, tempfile.TemporaryDirectory(
        prefix="book-site-registry-b-"
    ) as second_tmp:
        first = generate_registered_site(Path(first_tmp), components, revision)
        second = generate_registered_site(Path(second_tmp), components, revision)
        if first != second:
            differing = sorted(
                set(first) ^ set(second)
                | {
                    key
                    for key in set(first) & set(second)
                    if first[key] != second[key]
                }
            )
            raise SitePageRegistryError(
                f"registered site generation is not deterministic: {differing}"
            )

    after = base.repository_state_hashes()
    if before != after:
        changed = sorted(
            key
            for key in set(before) | set(after)
            if before.get(key) != after.get(key)
        )
        raise SitePageRegistryError(
            f"tracked repository files changed during generation: {changed}"
        )
    print(
        f"site source is deterministic: {len(first)} generated files; "
        f"{len(before)} tracked repository files unchanged"
    )


def validated_canonical_source_paths() -> list[Path]:
    paths: set[Path] = set()
    for path in ROOT.glob("*.md"):
        if path.is_symlink():
            raise SitePageRegistryError(
                f"root canonical Markdown must not be a symbolic link: {path.name}"
            )
        if path.is_file():
            require_repository_path(ROOT, path, path.name, kind="file")
            paths.add(path)

    for directory_name in base.CANONICAL_DIRECTORIES:
        directory = ROOT / directory_name
        if not directory.exists():
            continue
        validate_canonical_tree(ROOT, directory, directory_name)
        paths.update(path for path in directory.rglob("*") if path.is_file())

    for path, path_label in (
        (base.CONFIG_PATH, "book-config.json"),
        (base.REVISION_PATH, ".book-formatter/revision.json"),
        (REGISTRY_PATH, "site-pages.json"),
    ):
        require_repository_path(ROOT, path, path_label, kind="file")
        paths.add(path)

    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def apply_registry(registry: dict) -> None:
    global STATIC_FILES
    canonical_directories = list(base.CANONICAL_DIRECTORIES)
    for raw in registry["canonicalDirectories"]:
        directory = ROOT / raw
        validate_canonical_tree(ROOT, directory, raw)
        if raw not in canonical_directories:
            canonical_directories.append(raw)
    base.CANONICAL_DIRECTORIES = tuple(canonical_directories)

    for directory_name in base.CANONICAL_DIRECTORIES:
        directory = ROOT / directory_name
        if directory.exists():
            validate_canonical_tree(ROOT, directory, directory_name)

    pages = list(base.PAGES)
    sources = {page.source for page in pages}
    destinations = {page.destination for page in pages}
    section_orders = {(page.section, page.order) for page in pages}
    allowed_source_roots = set(base.CANONICAL_DIRECTORIES)

    for index, item in enumerate(registry["pages"]):
        source = schema_markdown_path(item["source"], f"pages[{index}].source")
        source_parts = Path(source).parts
        if len(source_parts) < 2 or source_parts[0] not in allowed_source_roots:
            raise SitePageRegistryError(
                f"pages[{index}].source must be inside a declared canonical directory: "
                f"{source}"
            )
        source_path = ROOT / source
        require_repository_path(
            ROOT,
            source_path,
            f"pages[{index}].source",
            kind="file",
        )
        destination = validate_destination(
            item["destination"], f"pages[{index}].destination"
        )
        section = item["section"]
        order = item["order"]
        title = item.get("title")

        if source in sources:
            raise SitePageRegistryError(f"duplicate page source: {source}")
        if destination in destinations:
            raise SitePageRegistryError(f"duplicate page destination: {destination}")
        if (section, order) in section_orders:
            raise SitePageRegistryError(
                f"duplicate page order in section {section}: {order}"
            )

        page = base.Page(source, destination, section, order, title)
        pages.append(page)
        sources.add(source)
        destinations.add(destination)
        section_orders.add((section, order))

    section_rank = {name: index for index, name in enumerate(base.SECTION_ORDER)}
    base.PAGES = tuple(
        sorted(
            pages,
            key=lambda page: (
                section_rank.get(page.section, -1),
                page.order,
                page.destination,
            ),
        )
    )

    routes = dict(base.DIRECTORY_ROUTES)
    for raw_directory, raw_destination in registry["directoryRoutes"].items():
        if raw_directory in routes:
            raise SitePageRegistryError(
                f"directory route must not override a built-in route: {raw_directory}"
            )
        destination = validate_destination(
            raw_destination, f"directoryRoutes.{raw_directory}"
        )
        if destination not in destinations:
            raise SitePageRegistryError(
                f"directory route target is not a registered page: {destination}"
            )
        routes[raw_directory] = destination
    base.DIRECTORY_ROUTES = routes

    static_files: list[StaticFile] = []
    static_sources: set[str] = set()
    static_destinations: set[str] = set()
    for index, item in enumerate(registry["staticFiles"]):
        source = schema_static_path(
            item["source"], f"staticFiles[{index}].source"
        )
        source_parts = Path(source).parts
        if len(source_parts) < 2 or source_parts[0] not in allowed_source_roots:
            raise SitePageRegistryError(
                f"staticFiles[{index}].source must be inside a declared canonical "
                f"directory: {source}"
            )
        source_path = ROOT / source
        require_repository_path(
            ROOT,
            source_path,
            f"staticFiles[{index}].source",
            kind="file",
        )
        validate_static_json(
            source_path.read_bytes(), f"staticFiles[{index}].source"
        )
        destination = validate_static_destination(
            item["destination"], f"staticFiles[{index}].destination"
        )
        if Path(source).suffix.lower() != Path(destination).suffix.lower():
            raise SitePageRegistryError(
                f"staticFiles[{index}] must preserve the source suffix"
            )
        if source in sources or source in static_sources:
            raise SitePageRegistryError(f"duplicate publication source: {source}")
        if destination in destinations or destination in static_destinations:
            raise SitePageRegistryError(
                f"duplicate publication destination: {destination}"
            )
        static_files.append(StaticFile(source, destination))
        static_sources.add(source)
        static_destinations.add(destination)
    STATIC_FILES = tuple(
        sorted(static_files, key=lambda item: (item.destination, item.source))
    )

    base.canonical_source_paths = validated_canonical_source_paths


def expect_invalid_registry(
    failures: list[str],
    name: str,
    value: object,
) -> None:
    try:
        parse_registry_data(value, f"fixture {name}")
    except SitePageRegistryError:
        return
    failures.append(f"registry parser accepted {name}")


def run_registry_security_regressions() -> list[str]:
    failures: list[str] = []

    for name, value in (
        ("array root", []),
        ("string root", "not-an-object"),
        ("null root", None),
        (
            "unknown top-level property",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [],
                "directoryRoutes": {},
                "unexpected": True,
            },
        ),
        (
            "duplicate canonical directory",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": ["cases", "cases"],
                "pages": [],
                "directoryRoutes": {},
            },
        ),
        (
            "unapproved canonical directory",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": ["vendor"],
                "pages": [],
                "directoryRoutes": {},
            },
        ),
        (
            "hidden canonical directory",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": ["_data"],
                "pages": [],
                "directoryRoutes": {},
            },
        ),
        (
            "non-string page source",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": 7,
                        "destination": "cases/example/index.md",
                        "section": "additional",
                        "order": 1,
                    }
                ],
                "directoryRoutes": {},
            },
        ),
        (
            "line break in page source",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": "cases/foo\nbar.md",
                        "destination": "cases/example/index.md",
                        "section": "additional",
                        "order": 1,
                    }
                ],
                "directoryRoutes": {},
            },
        ),
        (
            "boolean page order",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": "cases/example.md",
                        "destination": "cases/example/index.md",
                        "section": "additional",
                        "order": True,
                    }
                ],
                "directoryRoutes": {},
            },
        ),
        (
            "negative page order",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": "cases/example.md",
                        "destination": "cases/example/index.md",
                        "section": "additional",
                        "order": -1,
                    }
                ],
                "directoryRoutes": {},
            },
        ),
        (
            "fractional page order",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": "cases/example.md",
                        "destination": "cases/example/index.md",
                        "section": "additional",
                        "order": 220.5,
                    }
                ],
                "directoryRoutes": {},
            },
        ),
        (
            "non-finite page order",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": "cases/example.md",
                        "destination": "cases/example/index.md",
                        "section": "additional",
                        "order": float("nan"),
                    }
                ],
                "directoryRoutes": {},
            },
        ),
        (
            "trailing slash after markdown source",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": ["cases"],
                "pages": [
                    {
                        "source": "cases/example.md/",
                        "destination": "cases/example/index.md",
                        "section": "additional",
                        "order": 1,
                    }
                ],
                "directoryRoutes": {},
            },
        ),
        (
            "unicode line separator in destination",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": "cases/example.md",
                        "destination": "cases/foo\u2028bar/index.md",
                        "section": "additional",
                        "order": 1,
                    }
                ],
                "directoryRoutes": {},
            },
        ),
        (
            "non-string directory route",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": ["cases"],
                "pages": [],
                "directoryRoutes": {"cases": 7},
            },
        ),
        (
            "undeclared directory route",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [],
                "directoryRoutes": {
                    "templates": "cases/example/index.md"
                },
            },
        ),
        (
            "markdown static artifact",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [],
                "directoryRoutes": {},
                "staticFiles": [
                    {
                        "source": "cases/example.md",
                        "destination": "downloads/example.md",
                    }
                ],
            },
        ),
        (
            "traversing static artifact",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [],
                "directoryRoutes": {},
                "staticFiles": [
                    {
                        "source": "cases/../secret.json",
                        "destination": "downloads/secret.json",
                    }
                ],
            },
        ),
        (
            "static destination outside downloads",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [],
                "directoryRoutes": {},
                "staticFiles": [
                    {
                        "source": "cases/example.json",
                        "destination": "cases/example.json",
                    }
                ],
            },
        ),
        (
            "trailing slash after static source",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [],
                "directoryRoutes": {},
                "staticFiles": [
                    {
                        "source": "cases/example.json/",
                        "destination": "downloads/example.json",
                    }
                ],
            },
        ),
        (
            "trailing slash after static destination",
            {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalDirectories": [],
                "pages": [],
                "directoryRoutes": {},
                "staticFiles": [
                    {
                        "source": "cases/example.json",
                        "destination": "downloads/example.json/",
                    }
                ],
            },
        ),
    ):
        expect_invalid_registry(failures, name, value)

    valid_registry = {
        "schemaVersion": SCHEMA_VERSION,
        "canonicalDirectories": [],
        "pages": [],
        "directoryRoutes": {},
    }
    try:
        parse_registry_data(valid_registry, "valid fixture")
    except SitePageRegistryError as exc:
        failures.append(f"registry parser rejected valid object: {exc}")

    def page_title_fixture(title: str) -> dict:
        return {
            "schemaVersion": SCHEMA_VERSION,
            "canonicalDirectories": ["cases"],
            "pages": [
                {
                    "source": "cases/example.md",
                    "destination": "cases/example/index.md",
                    "section": "additional",
                    "order": 1,
                    "title": title,
                }
            ],
            "directoryRoutes": {"cases": "cases/example/index.md"},
        }

    missing_title_fixture = page_title_fixture("Temporary title")
    del missing_title_fixture["pages"][0]["title"]
    expect_invalid_registry(
        failures,
        "published page without an explicit title",
        missing_title_fixture,
    )

    unsafe_titles = (
        "第三者の本番システムへ接続する",
        "実Tokenを取得してEvidenceにする",
        "個人情報を収集する",
        "マルウェアを実行する",
        "https://example.comへ接続する",
        "第三者の本番システムへ\n接続する",
        "実Tokenを\r取得してEvidenceにする",
        "個人情報を\u2028収集する",
        "マルウェアを\u2029実行する",
    )
    for index, title in enumerate(unsafe_titles, start=1):
        expect_invalid_registry(
            failures,
            f"unsafe published page title {index}",
            page_title_fixture(title),
        )

    safe_titles = (
        "第4章 資産、信頼境界、攻撃面、脅威モデル",
        "ART-03 Threat Model",
        "第4章 合成記入例：請求書連携OAuthアプリのAsset / Boundary / Threat Model",
        "第4章 Source Review",
        "第三者の本番システムへ接続しない",
        "マルウェア分類の危険性を分析する",
    )
    for index, title in enumerate(safe_titles, start=1):
        try:
            parse_registry_data(
                page_title_fixture(title),
                f"safe published page title {index}",
            )
        except SitePageRegistryError as exc:
            failures.append(
                f"registry parser rejected safe published page title {index}: {exc}"
            )

    location_fixture = page_title_fixture(unsafe_titles[0])
    location_findings = published_page_title_findings(
        location_fixture,
        "stable title location fixture",
    )
    expected_location = (
        "stable title location fixture: pages[0].title "
        "(cases/example.md -> cases/example/index.md)"
    )
    if not location_findings:
        failures.append("unsafe page title did not produce a Policy finding")
    elif {finding.location for finding in location_findings} != {expected_location}:
        failures.append(
            "page title finding location is not stably bound to "
            "index/source/destination"
        )

    try:
        current_registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        parsed_current_registry = parse_registry_data(
            current_registry,
            "site-pages.json canonical title fixture",
        )
        current_titles = [
            item for item in parsed_current_registry["pages"] if "title" in item
        ]
        if len(current_titles) != len(parsed_current_registry["pages"]):
            failures.append(
                "site-pages.json has a published page without an explicit title"
            )
    except (OSError, json.JSONDecodeError, SitePageRegistryError) as exc:
        failures.append(f"canonical published page title scan failed: {exc}")

    integral_order_registry = {
        "schemaVersion": SCHEMA_VERSION,
        "canonicalDirectories": [],
        "pages": [
            {
                "source": "cases/example.md",
                "destination": "cases/example/index.md",
                "section": "additional",
                "order": 220.0,
                "title": "Integral order fixture",
            }
        ],
        "directoryRoutes": {},
    }
    try:
        parsed_integral_order = parse_registry_data(
            integral_order_registry,
            "integral numeric order fixture",
        )
        normalized_order = parsed_integral_order["pages"][0]["order"]
        if normalized_order != 220 or isinstance(normalized_order, bool):
            failures.append("registry parser did not normalize integral numeric order")
    except SitePageRegistryError as exc:
        failures.append(f"registry parser rejected integral numeric order: {exc}")

    for destination in (
        "_data/injected/index.md",
        "assets/injected/index.md",
        "hidden/.private/index.md",
        "not-pretty.md",
    ):
        try:
            validate_destination(destination, "destination fixture")
        except SitePageRegistryError:
            pass
        else:
            failures.append(f"destination validator accepted {destination}")

    try:
        validate_destination("cases/example/index.md", "valid destination")
    except SitePageRegistryError as exc:
        failures.append(f"destination validator rejected valid route: {exc}")

    for destination in (
        "assets/example.json",
        "downloads.json",
        "downloads/.hidden.json",
        "downloads/example.exe",
    ):
        try:
            validate_static_destination(destination, "static destination fixture")
        except SitePageRegistryError:
            pass
        else:
            failures.append(
                f"static destination validator accepted {destination}"
            )

    try:
        validate_static_destination(
            "downloads/example.json", "valid static destination"
        )
    except SitePageRegistryError as exc:
        failures.append(f"static destination validator rejected valid path: {exc}")

    for name, data in (
        ("empty JSON", b""),
        ("non-JSON text", b"<script>alert(1)</script>"),
        ("scalar JSON", b'"not-a-document"'),
        ("duplicate JSON key", b'{"id": 1, "id": 2}'),
        ("non-standard JSON constant", b'{"value": NaN}'),
        ("oversized JSON", b'[' + b'0,' * (MAX_STATIC_FILE_BYTES // 2) + b'0]'),
    ):
        try:
            validate_static_json(data, f"{name} fixture")
        except SitePageRegistryError:
            pass
        else:
            failures.append(f"static JSON validator accepted {name}")

    try:
        validate_static_json(b'{"synthetic": true}', "valid JSON fixture")
    except SitePageRegistryError as exc:
        failures.append(f"static JSON validator rejected valid object: {exc}")

    with tempfile.TemporaryDirectory(prefix="site-registry-root-") as root_tmp, tempfile.TemporaryDirectory(
        prefix="site-registry-outside-"
    ) as outside_tmp:
        fixture_root = Path(root_tmp)
        canonical = fixture_root / "cases"
        canonical.mkdir()
        (canonical / "safe.md").write_text("# Safe\n", encoding="utf-8")
        try:
            validate_canonical_tree(fixture_root, canonical, "safe fixture")
        except SitePageRegistryError as exc:
            failures.append(f"canonical validator rejected safe tree: {exc}")

        outside_file = Path(outside_tmp) / "outside.md"
        outside_file.write_text("# Outside\n", encoding="utf-8")
        link = canonical / "escape.md"
        try:
            link.symlink_to(outside_file)
        except OSError:
            pass
        else:
            try:
                validate_canonical_tree(fixture_root, canonical, "symlink fixture")
            except SitePageRegistryError:
                pass
            else:
                failures.append("canonical validator accepted an external symlink")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(base.DEFAULT_OUTPUT))
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--book-formatter-dir",
        default=os.environ.get("BOOK_FORMATTER_DIR"),
        help=(
            "Pinned itdojp/book-formatter checkout. If omitted, exact files "
            "are downloaded by commit and verified by Git blob SHA."
        ),
    )
    args = parser.parse_args()

    registry = load_registry()
    apply_registry(registry)

    formatter_dir = Path(args.book_formatter_dir) if args.book_formatter_dir else None
    components, revision = base.read_shared_components(formatter_dir)
    if args.check:
        check_registered_determinism(components, revision)
        return 0

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output = base.validate_generated_output_path(output)
    hashes = generate_registered_site(output, components, revision)
    print(
        f"generated {len(hashes)} site-source files in {output.relative_to(ROOT)} "
        f"from {len(base.PAGES)} registered pages and "
        f"{len(STATIC_FILES)} static artifact(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
