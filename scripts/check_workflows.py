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
ACTIVE_USES_RE = re.compile(
    r"^(?P<indent> *)(?:-\s*)?uses:\s*(?P<action>[^\s]+)\s*$"
)
LIST_ITEM_RE = re.compile(r"^(?P<indent> *)-\s+")
NAME_RE = re.compile(r"^(?:-\s*)?name:\s*(?P<value>.+?)\s*$")
KEY_VALUE_RE = re.compile(r"^(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*?)\s*$")


def strip_yaml_comment(line: str) -> str:
    """Remove an active YAML comment while preserving # inside quoted scalars."""
    in_single = False
    in_double = False
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_double:
            escaped = True
            continue
        if char == "'" and not in_double:
            in_single = not in_single
            continue
        if char == '"' and not in_single:
            in_double = not in_double
            continue
        if (
            char == "#"
            and not in_single
            and not in_double
            and (index == 0 or line[index - 1].isspace())
        ):
            return line[:index].rstrip()
    return line.rstrip()


def indentation(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def active_uses(text: str) -> list[tuple[int, int, str]]:
    entries: list[tuple[int, int, str]] = []
    for index, raw in enumerate(text.splitlines()):
        code = strip_yaml_comment(raw)
        if not code.strip():
            continue
        match = ACTIVE_USES_RE.fullmatch(code)
        if match:
            entries.append((index, len(match.group("indent")), match.group("action")))
    return entries


def top_level_block(text: str, key: str) -> str | None:
    lines = text.splitlines()
    marker = f"{key}:"
    for index, raw in enumerate(lines):
        line = strip_yaml_comment(raw)
        if line != marker:
            continue
        block: list[str] = []
        for candidate_raw in lines[index + 1 :]:
            candidate = strip_yaml_comment(candidate_raw)
            if candidate and not candidate.startswith((" ", "\t")):
                break
            if candidate:
                block.append(candidate)
        return "\n".join(block)
    return None


def job_block(text: str, job: str) -> str | None:
    pattern = re.compile(
        rf"(?ms)^  {re.escape(job)}:\s*\n(?P<body>.*?)(?=^  [A-Za-z0-9_-]+:\s*\n|\Z)"
    )
    match = pattern.search(text)
    return match.group("body") if match else None


def step_bounds(
    lines: list[str],
    uses_index: int,
    uses_indent: int,
) -> tuple[int, int, int] | None:
    uses_code = strip_yaml_comment(lines[uses_index])
    if uses_code.lstrip().startswith("- uses:"):
        step_start = uses_index
        step_indent = uses_indent
    else:
        step_start = -1
        step_indent = -1
        for candidate_index in range(uses_index - 1, -1, -1):
            candidate = strip_yaml_comment(lines[candidate_index])
            if not candidate.strip():
                continue
            candidate_indent = indentation(candidate)
            if candidate_indent < uses_indent and LIST_ITEM_RE.match(candidate):
                step_start = candidate_index
                step_indent = candidate_indent
                break
            if candidate_indent == 0:
                break
        if step_start < 0:
            return None

    step_end = len(lines)
    for candidate_index in range(uses_index + 1, len(lines)):
        candidate = strip_yaml_comment(lines[candidate_index])
        if not candidate.strip():
            continue
        candidate_indent = indentation(candidate)
        if candidate_indent < step_indent:
            step_end = candidate_index
            break
        if candidate_indent == step_indent and LIST_ITEM_RE.match(candidate):
            step_end = candidate_index
            break
    return step_start, step_end, step_indent


def step_name(
    lines: list[str],
    step_start: int,
    step_end: int,
    step_indent: int,
) -> str:
    mapping_indent = step_indent + 2
    for raw in lines[step_start:step_end]:
        code = strip_yaml_comment(raw)
        if not code.strip():
            continue
        indent = indentation(code)
        candidate = code.strip()
        if indent == step_indent and candidate.startswith("- "):
            candidate = candidate[2:].lstrip()
        elif indent != mapping_indent:
            continue
        match = NAME_RE.fullmatch(candidate)
        if match:
            return match.group("value").strip().strip("'\"")
    return "checkout step"


def direct_mapping_values(
    lines: list[str],
    start: int,
    end: int,
    parent_indent: int,
    key: str,
) -> list[str]:
    active_children: list[tuple[int, str]] = []
    for raw in lines[start:end]:
        code = strip_yaml_comment(raw)
        if not code.strip():
            continue
        indent = indentation(code)
        if indent <= parent_indent:
            break
        active_children.append((indent, code.strip()))

    if not active_children:
        return []
    direct_indent = min(indent for indent, _ in active_children)
    values: list[str] = []
    for indent, candidate in active_children:
        if indent != direct_indent:
            continue
        match = KEY_VALUE_RE.fullmatch(candidate)
        if match and match.group("key") == key:
            values.append(match.group("value"))
    return values


def scalar_is_false(value: str) -> bool:
    normalized = value.strip()
    if (
        len(normalized) >= 2
        and normalized[0] == normalized[-1]
        and normalized[0] in {"'", '"'}
    ):
        normalized = normalized[1:-1].strip()
    return normalized.lower() == "false"


def checkout_credential_errors(text: str, label: str) -> list[str]:
    diagnostics: list[str] = []
    lines = text.splitlines()
    for uses_index, uses_indent, action in active_uses(text):
        if not action.startswith("actions/checkout@"):
            continue

        bounds = step_bounds(lines, uses_index, uses_indent)
        if bounds is None:
            diagnostics.append(f"{label}: could not locate checkout step boundary")
            continue
        step_start, step_end, step_indent = bounds
        name = step_name(lines, step_start, step_end, step_indent)
        mapping_indent = step_indent + 2

        with_indexes: list[int] = []
        for index in range(step_start, step_end):
            code = strip_yaml_comment(lines[index])
            if not code.strip() or indentation(code) != mapping_indent:
                continue
            if code.strip() == "with:":
                with_indexes.append(index)

        if len(with_indexes) != 1:
            diagnostics.append(
                f"{label}: {name} must contain one active with mapping"
            )
            continue

        values = direct_mapping_values(
            lines,
            with_indexes[0] + 1,
            step_end,
            mapping_indent,
            "persist-credentials",
        )
        if len(values) != 1 or not scalar_is_false(values[0]):
            diagnostics.append(
                f"{label}: {name} must set active "
                "with.persist-credentials to false"
            )
    return diagnostics


def check_checkout_parser_regressions(errors: list[str]) -> None:
    sha = "0" * 40
    cases = {
        "active false": (
            f"""jobs:
  test:
    steps:
      - name: Checkout
        uses: actions/checkout@{sha}
        with:
          persist-credentials: false
""",
            True,
        ),
        "commented false": (
            f"""jobs:
  test:
    steps:
      - uses: actions/checkout@{sha}
        with:
          # persist-credentials: false
          fetch-depth: 1
""",
            False,
        ),
        "following unnamed step": (
            f"""jobs:
  test:
    steps:
      - uses: actions/checkout@{sha}
      - run: echo \"persist-credentials: false\"
""",
            False,
        ),
        "active true": (
            f"""jobs:
  test:
    steps:
      - uses: actions/checkout@{sha}
        with:
          persist-credentials: true
""",
            False,
        ),
    }
    for name, (fixture, expected_valid) in cases.items():
        valid = not checkout_credential_errors(
            fixture,
            f"parser regression {name}",
        )
        if valid != expected_valid:
            errors.append(f"checkout parser regression failed: {name}")


def active_key_values(text: str, key: str) -> list[str]:
    values: list[str] = []
    pattern = re.compile(rf"^(?:-\s*)?{re.escape(key)}:\s*(.*?)\s*$")
    for raw in text.splitlines():
        code = strip_yaml_comment(raw)
        if not code.strip():
            continue
        match = pattern.fullmatch(code.strip())
        if match:
            values.append(match.group(1))
    return values


def main() -> int:
    errors: list[str] = []
    workflows = {path.name: path for path in WORKFLOW_DIR.glob("*.yml")}
    workflows.update({path.name: path for path in WORKFLOW_DIR.glob("*.yaml")})

    missing = EXPECTED_WORKFLOWS - set(workflows)
    if missing:
        errors.append(f"missing workflows: {sorted(missing)}")

    check_checkout_parser_regressions(errors)

    for _, path in sorted(workflows.items()):
        text = path.read_text(encoding="utf-8")
        if "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing Node 24 action guard")

        for _, _, action in active_uses(text):
            if action.startswith("./"):
                continue
            if "@" not in action:
                errors.append(f"{path.relative_to(ROOT)}: action has no ref: {action}")
                continue
            repository, ref = action.rsplit("@", 1)
            if not repository or not FULL_SHA_RE.fullmatch(ref):
                errors.append(
                    f"{path.relative_to(ROOT)}: action must use a full "
                    f"immutable SHA: {action}"
                )

        errors.extend(
            checkout_credential_errors(
                text,
                path.relative_to(ROOT).as_posix(),
            )
        )

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
            errors.append(
                "contract.yml: repository npm install must ignore lifecycle scripts"
            )

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

        if active_key_values(text, "enablement"):
            errors.append(
                "pages.yml: configure-pages must not change repository enablement; "
                "Pages enablement is an operator action"
            )

        workflow_permissions = top_level_block(text, "permissions")
        if workflow_permissions is None or "contents: read" not in workflow_permissions:
            errors.append(
                "pages.yml: top-level permissions must default to contents: read"
            )
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
                errors.append(
                    "pages.yml: build job must have contents: read and pages: write"
                )
            if "id-token:" in build:
                errors.append(
                    "pages.yml: build job must not receive id-token permission"
                )
        if deploy is None:
            errors.append("pages.yml: missing deploy job")
        else:
            if "pages: write" not in deploy or "id-token: write" not in deploy:
                errors.append(
                    "pages.yml: deploy job must have pages: write and id-token: write"
                )
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
        "parsed non-persistent checkout credentials, ignored npm lifecycle scripts, "
        "operator-only Pages enablement, least-privilege Pages jobs, pinned formatter, "
        "generated output untracked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
