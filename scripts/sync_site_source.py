#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "book-config.json"
REVISION_PATH = ROOT / ".book-formatter" / "revision.json"
DEFAULT_OUTPUT = ROOT / "docs"
REPOSITORY_URL = "https://github.com/itdojp/white-hat-cyber-intelligence-book"
CODE_FENCE_RE = re.compile(r"^\s*```")
LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
IGNORE_SCHEMES = {"http", "https", "mailto", "tel", "data"}


@dataclass(frozen=True)
class Page:
    source: str
    destination: str
    section: str
    order: int
    title: str | None = None


PAGES: tuple[Page, ...] = (
    Page("index.md", "index.md", "home", 0),
    Page("quickstart.md", "quickstart/index.md", "introduction", 10),
    Page("concept-map.md", "concept-map/index.md", "introduction", 20),
    Page("manuscript/00-reading-guide.md", "reading-guide/index.md", "introduction", 30),
    Page("manuscript/01-integrated-discipline.md", "chapters/chapter-01/index.md", "chapters", 40),
    Page("artifact-index.md", "artifact-index/index.md", "additional", 100),
    Page("troubleshooting.md", "troubleshooting/index.md", "additional", 110),
    Page("figure-index.md", "figure-index/index.md", "additional", 120),
    Page("templates/learning-route-plan.md", "templates/learning-route-plan/index.md", "additional", 130),
    Page("templates/rules-of-engagement.md", "templates/rules-of-engagement/index.md", "additional", 140),
    Page("templates/threat-model.md", "templates/threat-model/index.md", "additional", 150),
    Page("templates/finding-report.md", "templates/finding-report/index.md", "additional", 160),
    Page("templates/detection-validation.md", "templates/detection-validation/index.md", "additional", 170),
    Page("templates/hunt-report.md", "templates/hunt-report/index.md", "additional", 180),
    Page("templates/incident-timeline.md", "templates/incident-timeline/index.md", "additional", 190),
    Page("templates/cti-report.md", "templates/cti-report/index.md", "additional", 200),
    Page("templates/executive-brief.md", "templates/executive-brief/index.md", "additional", 210),
    Page("title.md", "title/index.md", "resources", 300),
    Page("preface.md", "preface/index.md", "resources", 310),
    Page("TOC.md", "toc/index.md", "resources", 320),
    Page("references/reference-baseline.md", "source-notes/index.md", "resources", 330),
    Page("SAFETY_SCOPE.md", "safety-scope/index.md", "resources", 340),
    Page("legal-notice.md", "legal-notice/index.md", "resources", 350),
    Page("LICENSE.md", "license/index.md", "resources", 360),
    Page("copyright.md", "copyright/index.md", "resources", 370),
    Page("CHANGELOG.md", "changelog/index.md", "resources", 380),
    Page("colophon.md", "colophon/index.md", "resources", 390),
    Page("glossary.md", "appendices/glossary/index.md", "appendices", 400),
    Page("LAB_ARCHITECTURE.md", "appendices/lab-guide/index.md", "appendices", 410),
    Page("CROSS_BOOK_MAP.md", "appendices/cross-book-map/index.md", "appendices", 420),
    Page("afterword.md", "afterword/index.md", "afterword", 500),
)

DIRECTORY_ROUTES = {
    "templates": "artifact-index/index.md",
    "references": "source-notes/index.md",
}

SECTION_ORDER = (
    "introduction",
    "chapters",
    "additional",
    "resources",
    "appendices",
    "afterword",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def verify_formatter_checkout(path: Path, expected_commit: str) -> None:
    git_dir = path / ".git"
    if not git_dir.exists():
        return
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    )
    actual = result.stdout.strip()
    if actual != expected_commit:
        raise RuntimeError(
            f"book-formatter checkout is {actual}; expected {expected_commit}"
        )


def read_shared_components(formatter_dir: Path | None) -> tuple[dict[str, bytes], dict]:
    revision = load_json(REVISION_PATH)
    expected_commit = revision["commit"]
    if formatter_dir is not None:
        formatter_dir = formatter_dir.resolve()
        if not formatter_dir.is_dir():
            raise FileNotFoundError(f"book-formatter directory not found: {formatter_dir}")
        verify_formatter_checkout(formatter_dir, expected_commit)

    output: dict[str, bytes] = {}
    for name, component in sorted(revision["components"].items()):
        source_path = component["path"]
        expected_blob = component["blobSha"]
        if formatter_dir is not None:
            data = (formatter_dir / source_path).read_bytes()
        else:
            url = (
                "https://raw.githubusercontent.com/itdojp/book-formatter/"
                f"{expected_commit}/{quote(source_path, safe='/')}"
            )
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "white-hat-cyber-intelligence-book-build"},
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
        actual_blob = git_blob_sha(data)
        if actual_blob != expected_blob:
            raise RuntimeError(
                f"{name}: Git blob SHA mismatch: {actual_blob} != {expected_blob}"
            )
        output[name] = data
    return output, revision


def strip_front_matter(text: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[index + 1 :]).lstrip("\n")
    raise ValueError("front matter start found without closing delimiter")


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip().replace("　", " ")
    return fallback


def parse_link_target(raw: str) -> tuple[str, str, str, str] | None:
    stripped = raw.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("<") and ">" in stripped:
        url = stripped[1 : stripped.index(">")]
        suffix = stripped[stripped.index(">") + 1 :]
        prefix = "<"
        closing = ">"
    else:
        parts = stripped.split(maxsplit=1)
        url = parts[0]
        suffix = " " + parts[1] if len(parts) > 1 else ""
        prefix = ""
        closing = ""
    parsed = urlparse(url)
    if parsed.scheme in IGNORE_SCHEMES or parsed.scheme or url.startswith("//"):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    query = f"?{parsed.query}" if parsed.query else ""
    return path, fragment, query, f"{prefix}{{url}}{closing}{suffix}"


def site_dir(destination: str) -> str:
    if destination == "index.md":
        return "."
    if destination.endswith("/index.md"):
        return destination[: -len("/index.md")]
    return destination.rsplit("/", 1)[0]


def relative_site_link(current_destination: str, target_destination: str, fragment: str = "") -> str:
    current_dir = site_dir(current_destination)
    target_dir = site_dir(target_destination)
    relative = posixpath.relpath(target_dir, current_dir)
    if relative == ".":
        return fragment or "./"
    return relative.rstrip("/") + "/" + fragment


def repository_link(target: Path, fragment: str) -> str:
    relative = target.relative_to(ROOT).as_posix()
    kind = "tree" if target.is_dir() else "blob"
    return f"{REPOSITORY_URL}/{kind}/main/{quote(relative, safe='/')}{fragment}"


def rewrite_links(
    markdown: str,
    source: str,
    destination: str,
    source_to_destination: dict[str, str],
) -> str:
    source_path = (ROOT / source).resolve()
    lines: list[str] = []
    in_code = False
    for line in markdown.splitlines():
        if CODE_FENCE_RE.match(line):
            in_code = not in_code
            lines.append(line)
            continue
        if in_code:
            lines.append(line)
            continue

        def replace(match: re.Match[str]) -> str:
            before, raw, after = match.groups()
            parsed = parse_link_target(raw)
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

            if target_relative in source_to_destination:
                url = relative_site_link(
                    destination,
                    source_to_destination[target_relative],
                    fragment,
                )
                return before + formatter.format(url=url) + after

            directory_key = target_relative.rstrip("/")
            if target.is_dir() and directory_key in DIRECTORY_ROUTES:
                url = relative_site_link(
                    destination,
                    DIRECTORY_ROUTES[directory_key],
                    fragment,
                )
                return before + formatter.format(url=url) + after

            if target.exists():
                return before + formatter.format(url=repository_link(target, fragment)) + after
            return match.group(0)

        lines.append(LINK_RE.sub(replace, line))
    return "\n".join(lines).rstrip() + "\n"


def render_page(page: Page, source_to_destination: dict[str, str]) -> tuple[str, str]:
    source_path = ROOT / page.source
    if not source_path.is_file():
        raise FileNotFoundError(f"missing canonical source: {page.source}")
    raw = source_path.read_text(encoding="utf-8")
    body = strip_front_matter(raw)
    title = page.title or extract_title(body, page.source)
    body = rewrite_links(body, page.source, page.destination, source_to_destination)
    front_matter = [
        "---",
        "layout: book",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"source_path: {json.dumps(page.source, ensure_ascii=False)}",
        f"order: {page.order}",
        f"book_section: {json.dumps(page.section, ensure_ascii=False)}",
        "---",
        "",
    ]
    return "\n".join(front_matter) + body, title


def destination_url(destination: str) -> str:
    if destination == "index.md":
        return "/"
    if destination.endswith("/index.md"):
        return "/" + destination[: -len("index.md")]
    return "/" + destination.removesuffix(".md") + "/"


def render_navigation(titles: dict[str, str]) -> str:
    lines: list[str] = []
    for section in SECTION_ORDER:
        entries = [page for page in PAGES if page.section == section]
        if not entries:
            continue
        lines.append(f"{section}:")
        for page in entries:
            lines.append(f"  - title: {json.dumps(titles[page.source], ensure_ascii=False)}")
            lines.append(f"    path: {json.dumps(destination_url(page.destination))}")
    return "\n".join(lines) + "\n"


def yaml_string(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def render_config(config: dict) -> str:
    repository = config["repository"]["url"]
    return f'''title: {yaml_string(config["title"])}
subtitle: {yaml_string(config["subtitle"])}
description: {yaml_string(config["description"])}
author: {yaml_string(config["author"])}
version: {yaml_string(config["version"])}
lang: ja

url: "https://itdojp.github.io"
baseurl: "/white-hat-cyber-intelligence-book"
repository: "itdojp/white-hat-cyber-intelligence-book"
repository_url: {yaml_string(repository)}
repository_branch: "main"
show_edit_link: true
license_text: "Content licensed under CC BY-NC-SA 4.0. Code is licensed under Apache-2.0 where indicated. Commercial use of book content requires a separate agreement."

markdown: kramdown
highlighter: rouge
permalink: pretty

plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
  - jekyll-relative-links
  - jekyll-optional-front-matter

relative_links:
  enabled: true
  collections: false

kramdown:
  input: GFM
  syntax_highlighter: rouge
  syntax_highlighter_opts:
    line_numbers: false

defaults:
  - scope:
      path: ""
      type: pages
    values:
      layout: book
'''


def transform_shared_component(target: str, data: bytes) -> tuple[bytes, list[str]]:
    transforms: list[str] = []
    if target == "_layouts/book.html":
        text = data.decode("utf-8")
        old_condition = "{% if repo_url and page.path %}"
        new_condition = "{% if site.show_edit_link and repo_url and page.source_path %}"
        if text.count(old_condition) != 1 or text.count("{{ page.path }}") != 1:
            raise RuntimeError("unexpected upstream book layout edit-link contract")
        text = text.replace(old_condition, new_condition)
        text = text.replace("{{ page.path }}", "{{ page.source_path }}")
        data = text.encode("utf-8")
        transforms.append("edit-link-targets-canonical-source")
    return data, transforms


def canonical_hashes() -> dict[str, str]:
    paths = [ROOT / page.source for page in PAGES]
    paths.extend((CONFIG_PATH, REVISION_PATH))
    return {
        path.relative_to(ROOT).as_posix(): sha256_bytes(path.read_bytes())
        for path in sorted(set(paths))
    }


def write_bytes(root: Path, relative: str, data: bytes) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def generate(output: Path, components: dict[str, bytes], revision: dict) -> dict[str, str]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    source_to_destination = {page.source: page.destination for page in PAGES}
    titles: dict[str, str] = {}
    page_manifest: list[dict] = []
    for page in PAGES:
        rendered, title = render_page(page, source_to_destination)
        write_bytes(output, page.destination, rendered.encode("utf-8"))
        titles[page.source] = title
        page_manifest.append(
            {
                "source": page.source,
                "destination": page.destination,
                "sha256": sha256_bytes((ROOT / page.source).read_bytes()),
            }
        )

    config = load_json(CONFIG_PATH)
    write_bytes(output, "_config.yml", render_config(config).encode("utf-8"))
    write_bytes(output, "_data/navigation.yml", render_navigation(titles).encode("utf-8"))

    component_manifest: list[dict] = []
    for name, metadata in sorted(revision["components"].items()):
        target = metadata["target"]
        transformed, transforms = transform_shared_component(target, components[name])
        write_bytes(output, target, transformed)
        component_manifest.append(
            {
                "name": name,
                "source": metadata["path"],
                "sourceBlobSha": metadata["blobSha"],
                "target": target,
                "transforms": transforms,
                "generatedSha256": sha256_bytes(transformed),
            }
        )

    manifest = {
        "schemaVersion": "1.0.0",
        "bookFormatter": {
            "repository": revision["repository"],
            "commit": revision["commit"],
            "sharedVersion": revision["shared"]["version"],
        },
        "configSha256": sha256_bytes(CONFIG_PATH.read_bytes()),
        "pages": page_manifest,
        "components": component_manifest,
    }
    write_bytes(
        output,
        "_data/build-manifest.json",
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )
    return tree_hashes(output)


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_bytes(path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def check_determinism(components: dict[str, bytes], revision: dict) -> None:
    before = canonical_hashes()
    with tempfile.TemporaryDirectory(prefix="book-site-source-a-") as first_tmp, tempfile.TemporaryDirectory(
        prefix="book-site-source-b-"
    ) as second_tmp:
        first = generate(Path(first_tmp), components, revision)
        second = generate(Path(second_tmp), components, revision)
        if first != second:
            differing = sorted(set(first) ^ set(second) | {key for key in set(first) & set(second) if first[key] != second[key]})
            raise RuntimeError(f"site source generation is not deterministic: {differing}")
    after = canonical_hashes()
    if before != after:
        changed = sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
        raise RuntimeError(f"canonical sources changed during generation: {changed}")
    print(f"site source is deterministic: {len(first)} generated files; canonical sources unchanged")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--book-formatter-dir",
        default=os.environ.get("BOOK_FORMATTER_DIR"),
        help="Pinned itdojp/book-formatter checkout. If omitted, exact files are downloaded by commit and verified by Git blob SHA.",
    )
    args = parser.parse_args()

    formatter_dir = Path(args.book_formatter_dir) if args.book_formatter_dir else None
    components, revision = read_shared_components(formatter_dir)
    if args.check:
        check_determinism(components, revision)
        return 0

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output = output.resolve()
    if output == ROOT or ROOT not in output.parents:
        raise ValueError(f"output must be a repository subdirectory: {output}")
    hashes = generate(output, components, revision)
    print(f"generated {len(hashes)} site-source files in {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
