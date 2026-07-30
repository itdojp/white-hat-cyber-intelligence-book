#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_ASSETS = (
    "assets/css/main.css",
    "assets/css/mobile-responsive.css",
    "assets/css/syntax-highlighting.css",
    "assets/js/code-copy-lightweight.js",
    "assets/js/search.js",
    "assets/js/theme.js",
)


def expected_html(destination: str, site: Path) -> Path:
    if destination == "index.md":
        return site / "index.html"
    if destination.endswith("/index.md"):
        return site / destination[: -len("index.md")] / "index.html"
    return site / Path(destination).with_suffix(".html")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="docs")
    parser.add_argument("--site", default="_site")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    site = Path(args.site).resolve()
    manifest_path = source / "_data" / "build-manifest.json"
    errors: list[str] = []

    if not manifest_path.is_file():
        print(f"ERROR: missing site-source manifest: {manifest_path}")
        return 1
    if not site.is_dir():
        print(f"ERROR: missing built site directory: {site}")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_pages = [
        expected_html(item["destination"], site)
        for item in manifest.get("pages", [])
    ]
    for page in expected_pages:
        if not page.is_file() or page.stat().st_size == 0:
            errors.append(f"missing or empty page: {page.relative_to(site)}")

    for asset in REQUIRED_ASSETS:
        path = site / asset
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty asset: {asset}")

    index_path = site / "index.html"
    if index_path.is_file():
        index = index_path.read_text(encoding="utf-8")
        for marker in (
            "<html",
            "ホワイトハッカーとサイバーインテリジェンス実践体系",
            "book-layout",
            "assets/css/main.css",
        ):
            if marker not in index:
                errors.append(f"index.html: missing marker {marker!r}")

    generated_markdown = sorted(site.rglob("*.md"))
    if generated_markdown:
        errors.append(
            "built site contains unrendered Markdown: "
            + ", ".join(path.relative_to(site).as_posix() for path in generated_markdown[:10])
        )

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1

    print(
        f"built site smoke check passed: {len(expected_pages)} pages, "
        f"{len(REQUIRED_ASSETS)} assets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
