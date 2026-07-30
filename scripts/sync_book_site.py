#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import sync_site_source as base  # noqa: E402

REGISTRY_PATH = ROOT / "site-pages.json"
SCHEMA_VERSION = "1.0.0"
DIRECTORY_RE = re.compile(r"^[A-Za-z0-9_-]+$")
ALLOWED_SECTIONS = set(base.SECTION_ORDER)
RESERVED_DESTINATION_ROOTS = {
    "_data",
    "_includes",
    "_layouts",
    "assets",
}


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


def parse_registry_data(value: object, label: str = "site-pages.json") -> dict:
    if not isinstance(value, dict):
        raise SitePageRegistryError(f"{label} root must be a JSON object")
    registry = value

    if registry.get("schemaVersion") != SCHEMA_VERSION:
        raise SitePageRegistryError(
            f"{label} schemaVersion must be {SCHEMA_VERSION}"
        )

    expected_keys = {
        "schemaVersion",
        "canonicalDirectories",
        "pages",
        "directoryRoutes",
    }
    unknown = set(registry) - expected_keys
    if unknown:
        raise SitePageRegistryError(
            f"{label} has unknown keys: {sorted(unknown)}"
        )
    missing = expected_keys - set(registry)
    if missing:
        raise SitePageRegistryError(
            f"{label} is missing keys: {sorted(missing)}"
        )

    if not isinstance(registry["canonicalDirectories"], list):
        raise SitePageRegistryError("canonicalDirectories must be an array")
    if not isinstance(registry["pages"], list):
        raise SitePageRegistryError("pages must be an array")
    if not isinstance(registry["directoryRoutes"], dict):
        raise SitePageRegistryError("directoryRoutes must be an object")
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
    destination = base.safe_relative_path(raw, label).as_posix()
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

    for path, label in (
        (base.CONFIG_PATH, "book-config.json"),
        (base.REVISION_PATH, ".book-formatter/revision.json"),
        (REGISTRY_PATH, "site-pages.json"),
    ):
        require_repository_path(ROOT, path, label, kind="file")
        paths.add(path)

    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def apply_registry(registry: dict) -> None:
    canonical_directories = list(base.CANONICAL_DIRECTORIES)
    for index, raw in enumerate(registry["canonicalDirectories"]):
        if not isinstance(raw, str) or not DIRECTORY_RE.fullmatch(raw):
            raise SitePageRegistryError(
                f"canonicalDirectories[{index}] is invalid: {raw!r}"
            )
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
        if not isinstance(item, dict):
            raise SitePageRegistryError(f"pages[{index}] must be an object")
        unknown = set(item) - {"source", "destination", "section", "order", "title"}
        if unknown:
            raise SitePageRegistryError(
                f"pages[{index}] has unknown keys: {sorted(unknown)}"
            )
        for key in ("source", "destination", "section", "order"):
            if key not in item:
                raise SitePageRegistryError(f"pages[{index}] is missing {key}")

        source = base.safe_relative_path(
            str(item["source"]), f"pages[{index}].source"
        ).as_posix()
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
        if not source.endswith(".md"):
            raise SitePageRegistryError(
                f"pages[{index}].source must identify a Markdown file: {source}"
            )

        destination = validate_destination(
            str(item["destination"]), f"pages[{index}].destination"
        )
        section = item["section"]
        order = item["order"]
        title = item.get("title")

        if section not in ALLOWED_SECTIONS:
            raise SitePageRegistryError(
                f"pages[{index}].section is invalid: {section!r}"
            )
        if not isinstance(order, int) or isinstance(order, bool) or order < 0:
            raise SitePageRegistryError(
                f"pages[{index}].order must be a non-negative integer"
            )
        if title is not None and (not isinstance(title, str) or not title.strip()):
            raise SitePageRegistryError(
                f"pages[{index}].title must be a non-empty string when present"
            )
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
        if not isinstance(raw_directory, str) or not DIRECTORY_RE.fullmatch(raw_directory):
            raise SitePageRegistryError(
                f"invalid directoryRoutes key: {raw_directory!r}"
            )
        destination = validate_destination(
            str(raw_destination), f"directoryRoutes.{raw_directory}"
        )
        if destination not in destinations:
            raise SitePageRegistryError(
                f"directory route target is not a registered page: {destination}"
            )
        routes[raw_directory] = destination
    base.DIRECTORY_ROUTES = routes

    base.canonical_source_paths = validated_canonical_source_paths


def run_registry_security_regressions() -> list[str]:
    failures: list[str] = []

    for label, value in (
        ("array root", []),
        ("string root", "not-an-object"),
        ("null root", None),
    ):
        try:
            parse_registry_data(value, f"fixture {label}")
        except SitePageRegistryError:
            pass
        else:
            failures.append(f"registry parser accepted {label}")

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
        base.check_determinism(components, revision)
        return 0

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output = base.validate_generated_output_path(output)
    hashes = base.generate(output, components, revision)
    print(
        f"generated {len(hashes)} site-source files in {output.relative_to(ROOT)} "
        f"from {len(base.PAGES)} registered pages"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
