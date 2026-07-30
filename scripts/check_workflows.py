#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
EXPECTED_WORKFLOWS = {
    "contract.yml",
    "book-qa.yml",
    "pages.yml",
}
PINNED_FORMATTER = "69eb5c12f5a750b65614bc9bbbc3d7abd5aa6f6c"
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)


def top_level_block(text: str, key: str) -> str | None:
    lines = text.splitlines()
    marker = f"{key}:"
    for index, line in enumerate(lines):
        if line != marker:
            continue
        block: list[str] = []
        for candidate in lines[index + 1 :]:
            if candidate and not candidate.startswith((" ", "\t")):
                break
            block.append(candidate)
        return "\n".join(block)
    return None


def job_block(text: str, job: str) -> str | None:
    pattern = re.compile(
        rf"(?ms)^  {re.escape(job)}:\s*\n(?P<body>.*?)(?=^  [A-Za-z0-9_-]+:\s*\n|\Z)"
    )
    match = pattern.search(text)
    return match.group("body") if match else None


def indentation(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def check_checkout_credentials(path: Path, text: str, errors: list[str]) -> None:
    lines = text.splitlines()
    checkout_indexes = [
        index
        for index, line in enumerate(lines)
        if re.match(r"^\s+uses:\s+actions/checkout@[0-9a-f]{40}(?:\s+#.*)?$", line)
    ]
    expected_checkout_count = sum(
        1 for action in USES_RE.findall(text) if action.startswith("actions/checkout@")
    )
    if len(checkout_indexes) != expected_checkout_count:
        errors.append(
            f"{path.relative_to(ROOT)}: could not locate every checkout step"
        )
        return

    for index in checkout_indexes:
        uses_indent = indentation(lines[index])
        step_start = index
        while step_start > 0:
            previous = lines[step_start - 1]
            if re.match(r"^\s*- name:", previous) and indentation(previous) < uses_indent:
                step_start -= 1
                break
            step_start -= 1

        step_end = len(lines)
        for candidate_index in range(index + 1, len(lines)):
            candidate = lines[candidate_index]
            if re.match(r"^\s*- name:", candidate) and indentation(candidate) < uses_indent:
                step_end = candidate_index
                break

        step_text = "\n".join(lines[step_start:step_end])
        step_name = next(
            (
                line.strip().removeprefix("- name:").strip()
                for line in lines[step_start : index + 1]
                if re.match(r"^\s*- name:", line)
            ),
            "checkout step",
        )
        if "persist-credentials: false" not in step_text:
            errors.append(
                f"{path.relative_to(ROOT)}: {step_name} must set "
                "persist-credentials: false"
            )


def main() -> int:
    errors: list[str] = []
    workflows = {path.name: path for path in WORKFLOW_DIR.glob("*.yml")}
    workflows.update({path.name: path for path in WORKFLOW_DIR.glob("*.yaml")})

    missing = EXPECTED_WORKFLOWS - set(workflows)
    if missing:
        errors.append(f"missing workflows: {sorted(missing)}")

    for _, path in sorted(workflows.items()):
        text = path.read_text(encoding="utf-8")
        if "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing Node 24 action guard")
        for action in USES_RE.findall(text):
            if action.startswith("./"):
                continue
            if "@" not in action:
                errors.append(f"{path.relative_to(ROOT)}: action has no ref: {action}")
                continue
            repository, ref = action.rsplit("@", 1)
            if not repository or not FULL_SHA_RE.fullmatch(ref):
                errors.append(
                    f"{path.relative_to(ROOT)}: action must use a full immutable SHA: {action}"
                )
        check_checkout_credentials(path, text, errors)

    for name in ("contract.yml", "book-qa.yml", "pages.yml"):
        path = workflows.get(name)
        if path and PINNED_FORMATTER not in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)}: missing pinned book-formatter commit")

    contract = workflows.get("contract.yml")
    if contract:
        text = contract.read_text(encoding="utf-8")
        for required in ("npm test", "BOOK_FORMATTER_DIR", "contents: read"):
            if required not in text:
                errors.append(f"contract.yml: missing {required!r}")
        if "npm ci --ignore-scripts" not in text:
            errors.append("contract.yml: repository npm install must ignore lifecycle scripts")

    book_qa = workflows.get("book-qa.yml")
    if book_qa:
        text = book_qa.read_text(encoding="utf-8")
        for required in (
            "npm run sync:docs",
            "check-unicode.js",
            "check-textlint.js",
            "check-links.js",
            "check-layout-risk.js",
            "check-markdown-structure.js",
            "bundle exec jekyll build",
            "scripts/check_built_site.py",
            "npm ci --prefix .work/book-formatter --ignore-scripts",
        ):
            if required not in text:
                errors.append(f"book-qa.yml: missing {required!r}")

    pages = workflows.get("pages.yml")
    if pages:
        text = pages.read_text(encoding="utf-8")
        if re.search(r"^\s*pull_request\s*:", text, re.MULTILINE):
            errors.append("pages.yml: deployment workflow must not run on pull_request")
        for required in (
            "branches: [main]",
            "actions/configure-pages@",
            "actions/upload-pages-artifact@",
            "actions/deploy-pages@",
            "npm ci --prefix .work/book-formatter --ignore-scripts",
        ):
            if required not in text:
                errors.append(f"pages.yml: missing {required!r}")

        workflow_permissions = top_level_block(text, "permissions")
        if workflow_permissions is None or "contents: read" not in workflow_permissions:
            errors.append("pages.yml: top-level permissions must default to contents: read")
        if workflow_permissions and "id-token:" in workflow_permissions:
            errors.append("pages.yml: top-level permissions must not grant id-token")
        if workflow_permissions and "pages:" in workflow_permissions:
            errors.append("pages.yml: top-level permissions must not grant pages write")

        build = job_block(text, "build")
        deploy = job_block(text, "deploy")
        if build is None:
            errors.append("pages.yml: missing build job")
        else:
            if "contents: read" not in build or "pages: write" not in build:
                errors.append("pages.yml: build job must have contents: read and pages: write")
            if "id-token:" in build:
                errors.append("pages.yml: build job must not receive id-token permission")
        if deploy is None:
            errors.append("pages.yml: missing deploy job")
        else:
            if "pages: write" not in deploy or "id-token: write" not in deploy:
                errors.append("pages.yml: deploy job must have pages: write and id-token: write")
            if "contents:" in deploy:
                errors.append("pages.yml: deploy job does not require contents permission")

    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "docs", "_site", "build"],
        check=True,
        text=True,
        capture_output=True,
    )
    tracked_generated = [line for line in result.stdout.splitlines() if line.strip()]
    if tracked_generated:
        errors.append(
            "generated output must not be tracked: " + ", ".join(tracked_generated)
        )

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1

    print(
        f"workflow contract passed: {len(workflows)} workflows, immutable action refs, "
        "non-persistent checkout credentials, ignored npm lifecycle scripts, "
        "least-privilege Pages jobs, pinned formatter, generated output untracked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
