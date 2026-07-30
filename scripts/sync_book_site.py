#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import sync_site_source as base  # noqa: E402

REGISTRY_PATH = ROOT / "site-pages.json"
SCHEMA_VERSION = "1.0.0"
DIRECTORY_RE = re.compile(r"^[A-Za-z0-9_-]+$")
ALLOWED_SECTIONS = set(base.SECTION_ORDER)


class SitePageRegistryError(base.SiteGenerationError):
    pass


def load_registry() -> dict:
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SitePageRegistryError(f"missing page registry: {REGISTRY_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise SitePageRegistryError(f"invalid page registry JSON: {exc}") from exc

    if registry.get("schemaVersion") != SCHEMA_VERSION:
        raise SitePageRegistryError(
            f"site-pages.json schemaVersion must be {SCHEMA_VERSION}"
        )

    for key in ("canonicalDirectories", "pages", "directoryRoutes"):
        if key not in registry:
            raise SitePageRegistryError(f"site-pages.json is missing {key}")

    if not isinstance(registry["canonicalDirectories"], list):
        raise SitePageRegistryError("canonicalDirectories must be an array")
    if not isinstance(registry["pages"], list):
        raise SitePageRegistryError("pages must be an array")
    if not isinstance(registry["directoryRoutes"], dict):
        raise SitePageRegistryError("directoryRoutes must be an object")
    return registry


def apply_registry(registry: dict) -> None:
    canonical_directories = list(base.CANONICAL_DIRECTORIES)
    for raw in registry["canonicalDirectories"]:
        if not isinstance(raw, str) or not DIRECTORY_RE.fullmatch(raw):
            raise SitePageRegistryError(
                f"invalid canonical directory name: {raw!r}"
            )
        directory = ROOT / raw
        if not directory.is_dir():
            raise SitePageRegistryError(
                f"canonical directory does not exist: {raw}"
            )
        if raw not in canonical_directories:
            canonical_directories.append(raw)
    base.CANONICAL_DIRECTORIES = tuple(canonical_directories)

    pages = list(base.PAGES)
    sources = {page.source for page in pages}
    destinations = {page.destination for page in pages}
    section_orders = {(page.section, page.order) for page in pages}

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
        destination = base.safe_relative_path(
            str(item["destination"]), f"pages[{index}].destination"
        ).as_posix()
        section = item["section"]
        order = item["order"]
        title = item.get("title")

        if not source.endswith(".md") or not (ROOT / source).is_file():
            raise SitePageRegistryError(
                f"pages[{index}].source must identify an existing Markdown file: {source}"
            )
        if not destination.endswith(".md"):
            raise SitePageRegistryError(
                f"pages[{index}].destination must end in .md: {destination}"
            )
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
        destination = base.safe_relative_path(
            str(raw_destination), f"directoryRoutes.{raw_directory}"
        ).as_posix()
        if destination not in destinations:
            raise SitePageRegistryError(
                f"directory route target is not a registered page: {destination}"
            )
        routes[raw_directory] = destination
    base.DIRECTORY_ROUTES = routes

    original_canonical_source_paths = base.canonical_source_paths

    def canonical_source_paths() -> list[Path]:
        paths = set(original_canonical_source_paths())
        paths.add(REGISTRY_PATH)
        return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())

    base.canonical_source_paths = canonical_source_paths


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
