#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
EXPECTED_WORKFLOWS = {"contract.yml", "book-qa.yml", "pages.yml"}
PINNED_FORMATTER = "764f644850c21983c96919d0e13706413d59c089"
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
BLOCK_SCALAR_RE = re.compile(r"^[|>](?:[+-]?[1-9]?|[1-9][+-]?)$")
SENSITIVE_COMPLEX_KEY_RE = re.compile(
    r"(?:^|[,{?]\s*)(?:['\"](?:uses|with|persist-credentials|enablement|permissions|jobs|build|deploy)['\"]|(?:uses|with|persist-credentials|enablement|permissions|jobs|build|deploy))\s*:",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ActiveLine:
    index: int
    indent: int
    sequence: bool


@dataclass(frozen=True)
class MappingLine:
    index: int
    indent: int
    sequence: bool
    key: str
    value: str


@dataclass(frozen=True)
class ParsedWorkflow:
    lines: list[str]
    active_lines: list[ActiveLine]
    entries: list[MappingLine]
    errors: list[str]


def strip_yaml_comment(line: str) -> str:
    """Remove an active YAML comment while preserving # inside quoted scalars."""
    in_single = False
    in_double = False
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and in_double:
            escaped = True
            index += 1
            continue
        if char == "'" and not in_double:
            if in_single and index + 1 < len(line) and line[index + 1] == "'":
                index += 2
                continue
            in_single = not in_single
            index += 1
            continue
        if char == '"' and not in_single:
            in_double = not in_double
            index += 1
            continue
        if (
            char == "#"
            and not in_single
            and not in_double
            and (index == 0 or line[index - 1].isspace())
        ):
            return line[:index].rstrip()
        index += 1
    return line.rstrip()


def indentation(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def parse_scalar(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise ValueError("unterminated single-quoted scalar")
        return value[1:-1].replace("''", "'")
    if value.startswith('"'):
        if len(value) < 2 or not value.endswith('"'):
            raise ValueError("unterminated double-quoted scalar")
        decoded = json.loads(value)
        if not isinstance(decoded, str):
            raise ValueError("double-quoted scalar did not decode to a string")
        return decoded
    return value


def find_mapping_separator(content: str) -> int | None:
    in_single = False
    in_double = False
    escaped = False
    index = 0
    while index < len(content):
        char = content[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and in_double:
            escaped = True
            index += 1
            continue
        if char == "'" and not in_double:
            if in_single and index + 1 < len(content) and content[index + 1] == "'":
                index += 2
                continue
            in_single = not in_single
            index += 1
            continue
        if char == '"' and not in_single:
            in_double = not in_double
            index += 1
            continue
        if char == ":" and not in_single and not in_double:
            if index + 1 == len(content) or content[index + 1].isspace():
                return index
        index += 1
    return None


def parse_mapping_line(
    raw: str,
    index: int,
) -> tuple[MappingLine | None, ActiveLine | None, str | None]:
    code = strip_yaml_comment(raw)
    if not code.strip():
        return None, None, None

    indent = indentation(code)
    content = code[indent:]
    sequence = False
    if content == "-":
        return None, ActiveLine(index, indent, True), None
    if content.startswith("-") and len(content) > 1 and content[1].isspace():
        sequence = True
        content = content[1:].lstrip()

    active = ActiveLine(index, indent, sequence)
    if not content:
        return None, active, None

    if content.startswith("?"):
        return (
            None,
            active,
            "explicit YAML mapping keys are not supported in workflow policy files",
        )
    if content.startswith("{"):
        if SENSITIVE_COMPLEX_KEY_RE.search(content):
            return (
                None,
                active,
                "flow-style mappings containing policy keys are not supported",
            )
        return None, active, None

    separator = find_mapping_separator(content)
    if separator is None:
        return None, active, None

    key_token = content[:separator].strip()
    value = content[separator + 1 :].strip()
    if not key_token:
        return None, active, "empty YAML mapping key"
    try:
        key = parse_scalar(key_token)
    except (ValueError, json.JSONDecodeError) as exc:
        return None, active, f"unsupported YAML mapping key {key_token!r}: {exc}"
    if not key:
        return None, active, "empty YAML mapping key"
    if key == "<<" or value.startswith("*"):
        return (
            None,
            active,
            "YAML aliases and merge keys are not supported in workflow policy files",
        )
    return MappingLine(index, indent, sequence, key, value), active, None


def parse_workflow(text: str, label: str) -> ParsedWorkflow:
    lines = text.splitlines()
    entries: list[MappingLine] = []
    active_lines: list[ActiveLine] = []
    errors: list[str] = []
    block_scalar_indent: int | None = None

    for index, raw in enumerate(lines):
        code = strip_yaml_comment(raw)
        if block_scalar_indent is not None:
            if not code.strip():
                continue
            if indentation(code) > block_scalar_indent:
                continue
            block_scalar_indent = None

        entry, active, parse_error = parse_mapping_line(raw, index)
        if active is not None:
            active_lines.append(active)
        if parse_error is not None:
            errors.append(f"{label}:{index + 1}: {parse_error}")
        if entry is not None:
            entries.append(entry)
            if BLOCK_SCALAR_RE.fullmatch(entry.value):
                block_scalar_indent = entry.indent

    return ParsedWorkflow(lines, active_lines, entries, errors)


def decoded_value(entry: MappingLine, label: str, errors: list[str]) -> str:
    try:
        return parse_scalar(entry.value)
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(
            f"{label}:{entry.index + 1}: invalid scalar for {entry.key!r}: {exc}"
        )
        return ""


def block_end(parsed: ParsedWorkflow, parent: MappingLine) -> int:
    for active in parsed.active_lines:
        if active.index <= parent.index:
            continue
        if active.indent <= parent.indent:
            return active.index
    return len(parsed.lines)


def direct_children(
    parsed: ParsedWorkflow,
    parent: MappingLine,
    end: int | None = None,
) -> list[MappingLine]:
    end = block_end(parsed, parent) if end is None else end
    children = [
        entry
        for entry in parsed.entries
        if parent.index < entry.index < end and entry.indent > parent.indent
    ]
    if not children:
        return []
    direct_indent = min(entry.indent for entry in children)
    return [entry for entry in children if entry.indent == direct_indent]


def find_single(entries: list[MappingLine], key: str) -> MappingLine | None:
    matches = [entry for entry in entries if entry.key == key]
    return matches[0] if len(matches) == 1 else None


def step_bounds(
    parsed: ParsedWorkflow,
    uses: MappingLine,
) -> tuple[int, int, int] | None:
    if uses.sequence:
        step_start = uses.index
        step_indent = uses.indent
    else:
        candidates = [
            active
            for active in parsed.active_lines
            if active.index < uses.index
            and active.sequence
            and active.indent < uses.indent
        ]
        if not candidates:
            return None
        start = max(candidates, key=lambda item: item.index)
        step_start = start.index
        step_indent = start.indent

    step_end = len(parsed.lines)
    for active in parsed.active_lines:
        if active.index <= uses.index:
            continue
        if active.indent < step_indent or (
            active.sequence and active.indent == step_indent
        ):
            step_end = active.index
            break
    return step_start, step_end, step_indent


def direct_step_entries(
    parsed: ParsedWorkflow,
    start: int,
    end: int,
    indent: int,
) -> list[MappingLine]:
    return [
        entry
        for entry in parsed.entries
        if start <= entry.index < end
        and (
            (entry.sequence and entry.indent == indent)
            or (not entry.sequence and entry.indent == indent + 2)
        )
    ]


def action_policy_errors(parsed: ParsedWorkflow, label: str) -> list[str]:
    errors = list(parsed.errors)
    uses_entries = [entry for entry in parsed.entries if entry.key == "uses"]
    for entry in uses_entries:
        action = decoded_value(entry, label, errors)
        if not action or action.startswith("./"):
            continue
        if "@" not in action:
            errors.append(f"{label}:{entry.index + 1}: action has no ref: {action}")
            continue
        repository, ref = action.rsplit("@", 1)
        if not repository or not FULL_SHA_RE.fullmatch(ref):
            errors.append(
                f"{label}:{entry.index + 1}: action must use a full "
                f"immutable SHA: {action}"
            )
    return errors


def checkout_credential_errors(parsed: ParsedWorkflow, label: str) -> list[str]:
    errors: list[str] = []
    for uses in [entry for entry in parsed.entries if entry.key == "uses"]:
        action = decoded_value(uses, label, errors)
        if not action.startswith("actions/checkout@"):
            continue
        bounds = step_bounds(parsed, uses)
        if bounds is None:
            errors.append(
                f"{label}:{uses.index + 1}: could not locate checkout step boundary"
            )
            continue
        start, end, indent = bounds
        step_entries = direct_step_entries(parsed, start, end, indent)
        name_entry = find_single(step_entries, "name")
        name = (
            decoded_value(name_entry, label, errors)
            if name_entry
            else "checkout step"
        )
        with_entries = [entry for entry in step_entries if entry.key == "with"]
        if len(with_entries) != 1 or with_entries[0].value:
            errors.append(f"{label}: {name} must contain one active with mapping")
            continue
        with_entry = with_entries[0]
        children = direct_children(parsed, with_entry, end)
        values = [
            entry for entry in children if entry.key == "persist-credentials"
        ]
        if len(values) != 1:
            errors.append(
                f"{label}: {name} must set active "
                "with.persist-credentials to false"
            )
            continue
        value = decoded_value(values[0], label, errors).strip().lower()
        if value != "false":
            errors.append(
                f"{label}: {name} must set active "
                "with.persist-credentials to false"
            )
    return errors


def top_level_entry(parsed: ParsedWorkflow, key: str) -> MappingLine | None:
    matches = [
        entry
        for entry in parsed.entries
        if not entry.sequence and entry.indent == 0 and entry.key == key
    ]
    return matches[0] if len(matches) == 1 else None


def nested_entry(
    parsed: ParsedWorkflow,
    parent: MappingLine,
    key: str,
) -> MappingLine | None:
    return find_single(direct_children(parsed, parent), key)


def permission_values(
    parsed: ParsedWorkflow,
    parent: MappingLine,
) -> dict[str, str]:
    values: dict[str, str] = {}
    ignored_errors: list[str] = []
    for entry in direct_children(parsed, parent):
        values[entry.key] = decoded_value(entry, "permissions", ignored_errors)
    return values


def publication_renderer_setup_errors(
    parsed: ParsedWorkflow,
    label: str,
) -> list[str]:
    """Require the locked renderer before npm test in each consuming job."""
    errors: list[str] = []
    jobs = top_level_entry(parsed, "jobs")
    if jobs is None:
        return [f"{label}: missing jobs mapping for npm test"]

    npm_test_count = 0
    for job in direct_children(parsed, jobs):
        job_end = block_end(parsed, job)
        job_entries = [
            entry
            for entry in parsed.entries
            if job.index < entry.index < job_end
        ]
        npm_test_entries = [
            entry
            for entry in job_entries
            if entry.key == "run"
            and decoded_value(entry, label, errors).strip() == "npm test"
        ]
        if not npm_test_entries:
            continue
        npm_test_count += len(npm_test_entries)

        ruby_setups = [
            entry
            for entry in job_entries
            if entry.key == "uses"
            and decoded_value(entry, label, errors).startswith("ruby/setup-ruby@")
        ]
        if len(ruby_setups) != 1:
            errors.append(
                f"{label}: job {job.key!r} running npm test must contain "
                "exactly one ruby/setup-ruby step"
            )
            continue

        setup = ruby_setups[0]
        first_test = min(entry.index for entry in npm_test_entries)
        if setup.index >= first_test:
            errors.append(
                f"{label}: job {job.key!r} must set up the locked "
                "publication renderer before npm test"
            )

        bounds = step_bounds(parsed, setup)
        if bounds is None:
            errors.append(
                f"{label}:{setup.index + 1}: could not locate "
                "ruby/setup-ruby step boundary"
            )
            continue
        start, end, indent = bounds
        step_entries = direct_step_entries(parsed, start, end, indent)
        with_entries = [entry for entry in step_entries if entry.key == "with"]
        if len(with_entries) != 1 or with_entries[0].value:
            errors.append(
                f"{label}: job {job.key!r} ruby/setup-ruby must contain "
                "one active with mapping"
            )
            continue

        values = {
            entry.key: decoded_value(entry, label, errors).strip().lower()
            for entry in direct_children(parsed, with_entries[0], end)
        }
        if values.get("ruby-version") != "3.3":
            errors.append(
                f"{label}: job {job.key!r} ruby/setup-ruby must pin "
                "ruby-version 3.3"
            )
        if values.get("bundler-cache") != "true":
            errors.append(
                f"{label}: job {job.key!r} ruby/setup-ruby must enable "
                "bundler-cache"
            )

    if npm_test_count != 1:
        errors.append(
            f"{label}: expected exactly one active 'run: npm test'; "
            f"found {npm_test_count}"
        )
    return errors


def check_parser_regressions(errors: list[str]) -> None:
    sha = "0" * 40
    valid_plain = f"""jobs:
  test:
    steps:
      - name: Checkout
        uses: actions/checkout@{sha}
        with:
          persist-credentials: false
"""
    valid_quoted = f"""jobs:
  test:
    steps:
      - \"name\": Checkout
        \"uses\": \"actions/checkout@{sha}\"
        'with':
          \"persist-credentials\": false
"""
    invalid_cases = {
        "commented false": f"""jobs:
  test:
    steps:
      - uses: actions/checkout@{sha}
        with:
          # persist-credentials: false
          fetch-depth: 1
""",
        "following unnamed step": f"""jobs:
  test:
    steps:
      - uses: actions/checkout@{sha}
      - run: echo \"persist-credentials: false\"
""",
        "active true": f"""jobs:
  test:
    steps:
      - uses: actions/checkout@{sha}
        with:
          persist-credentials: true
""",
        "quoted uses missing credentials": f"""jobs:
  test:
    steps:
      - \"uses\": actions/checkout@{sha}
""",
    }

    for name, fixture in {
        "plain": valid_plain,
        "quoted keys": valid_quoted,
    }.items():
        parsed = parse_workflow(fixture, f"parser regression {name}")
        diagnostics = action_policy_errors(
            parsed,
            name,
        ) + checkout_credential_errors(parsed, name)
        if diagnostics:
            errors.append(
                f"workflow parser regression failed for valid {name}: "
                f"{diagnostics}"
            )

    for name, fixture in invalid_cases.items():
        parsed = parse_workflow(fixture, f"parser regression {name}")
        diagnostics = checkout_credential_errors(parsed, name)
        if not diagnostics:
            errors.append(f"workflow parser regression failed to reject: {name}")

    mutable = f"""jobs:
  test:
    steps:
      - \"uses\": actions/checkout@main
        \"with\":
          \"persist-credentials\": false
"""
    parsed = parse_workflow(mutable, "parser regression quoted mutable uses")
    if not action_policy_errors(parsed, "quoted mutable uses"):
        errors.append(
            "workflow parser regression failed to reject quoted mutable uses"
        )

    flow = f"""jobs:
  test:
    steps:
      - {{ \"uses\": actions/checkout@{sha}, \"with\": {{ \"persist-credentials\": false }} }}
"""
    parsed = parse_workflow(flow, "parser regression flow mapping")
    if not parsed.errors:
        errors.append(
            "workflow parser regression failed closed on flow mapping"
        )

    valid_renderer_order = f"""jobs:
  test:
    steps:
      - uses: ruby/setup-ruby@{sha}
        with:
          ruby-version: '3.3'
          bundler-cache: true
      - run: npm test
"""
    invalid_renderer_orders = {
        "commented test": """jobs:
  test:
    steps:
      # - run: npm test
      - run: echo test
""",
        "missing setup": """jobs:
  test:
    steps:
      - run: npm test
""",
        "setup in another job": f"""jobs:
  prepare:
    steps:
      - uses: ruby/setup-ruby@{sha}
        with:
          ruby-version: '3.3'
          bundler-cache: true
  test:
    steps:
      - run: npm test
""",
        "multiple active tests": f"""jobs:
  test:
    steps:
      - uses: ruby/setup-ruby@{sha}
        with:
          ruby-version: '3.3'
          bundler-cache: true
      - run: npm test
      - run: npm test
""",
        "late setup": f"""jobs:
  test:
    steps:
      - run: npm test
      - uses: ruby/setup-ruby@{sha}
        with:
          ruby-version: '3.3'
          bundler-cache: true
""",
        "missing bundler cache": f"""jobs:
  test:
    steps:
      - uses: ruby/setup-ruby@{sha}
        with:
          ruby-version: '3.3'
      - run: npm test
""",
        "wrong ruby series": f"""jobs:
  test:
    steps:
      - uses: ruby/setup-ruby@{sha}
        with:
          ruby-version: '3.2'
          bundler-cache: true
      - run: npm test
""",
    }
    parsed = parse_workflow(
        valid_renderer_order,
        "renderer setup regression valid order",
    )
    if publication_renderer_setup_errors(parsed, "valid renderer order"):
        errors.append(
            "workflow renderer setup regression failed for valid order"
        )
    for name, fixture in invalid_renderer_orders.items():
        parsed = parse_workflow(fixture, f"renderer setup regression {name}")
        if not publication_renderer_setup_errors(parsed, name):
            errors.append(
                "workflow renderer setup regression failed to reject: " + name
            )


def main() -> int:
    errors: list[str] = []
    workflows = {path.name: path for path in WORKFLOW_DIR.glob("*.yml")}
    workflows.update({path.name: path for path in WORKFLOW_DIR.glob("*.yaml")})

    missing = EXPECTED_WORKFLOWS - set(workflows)
    if missing:
        errors.append(f"missing workflows: {sorted(missing)}")

    check_parser_regressions(errors)
    parsed_workflows: dict[str, ParsedWorkflow] = {}
    texts: dict[str, str] = {}
    for name, path in sorted(workflows.items()):
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        label = path.relative_to(ROOT).as_posix()
        parsed = parse_workflow(text, label)
        parsed_workflows[name] = parsed
        if "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24" not in text:
            errors.append(f"{label}: missing Node 24 action guard")
        errors.extend(action_policy_errors(parsed, label))
        errors.extend(checkout_credential_errors(parsed, label))
        if name in EXPECTED_WORKFLOWS:
            errors.extend(publication_renderer_setup_errors(parsed, label))

    for name in EXPECTED_WORKFLOWS:
        if name in texts and PINNED_FORMATTER not in texts[name]:
            errors.append(
                f".github/workflows/{name}: missing pinned "
                "book-formatter commit"
            )

    contract = texts.get("contract.yml")
    if contract:
        for required in ("npm test", "BOOK_FORMATTER_DIR", "contents: read"):
            if required not in contract:
                errors.append(f"contract.yml: missing {required!r}")
        if "npm ci --ignore-scripts" not in contract:
            errors.append(
                "contract.yml: repository npm install must ignore "
                "lifecycle scripts"
            )

    book_qa = texts.get("book-qa.yml")
    if book_qa:
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
            if required not in book_qa:
                errors.append(f"book-qa.yml: missing {required!r}")

    pages = texts.get("pages.yml")
    parsed_pages = parsed_workflows.get("pages.yml")
    if pages and parsed_pages:
        if any(entry.key == "pull_request" for entry in parsed_pages.entries):
            errors.append(
                "pages.yml: deployment workflow must not run on pull_request"
            )
        for required in (
            "branches: [main]",
            "actions/configure-pages@",
            "actions/upload-pages-artifact@",
            "actions/deploy-pages@",
            "npm ci --prefix .work/book-formatter --ignore-scripts",
        ):
            if required not in pages:
                errors.append(f"pages.yml: missing {required!r}")
        if any(entry.key == "enablement" for entry in parsed_pages.entries):
            errors.append(
                "pages.yml: configure-pages must not change repository "
                "enablement; Pages enablement is an operator action"
            )

        permissions = top_level_entry(parsed_pages, "permissions")
        if permissions is None:
            errors.append(
                "pages.yml: missing one top-level permissions mapping"
            )
        else:
            values = permission_values(parsed_pages, permissions)
            if values.get("contents") != "read":
                errors.append(
                    "pages.yml: top-level permissions must default to "
                    "contents: read"
                )
            if "id-token" in values:
                errors.append(
                    "pages.yml: top-level permissions must not grant id-token"
                )
            if "pages" in values:
                errors.append(
                    "pages.yml: top-level permissions must not grant "
                    "pages write"
                )

        jobs = top_level_entry(parsed_pages, "jobs")
        build = nested_entry(parsed_pages, jobs, "build") if jobs else None
        deploy = nested_entry(parsed_pages, jobs, "deploy") if jobs else None
        for job_name, job, required, forbidden in (
            (
                "build",
                build,
                {"contents": "read", "pages": "write"},
                {"id-token"},
            ),
            (
                "deploy",
                deploy,
                {"pages": "write", "id-token": "write"},
                {"contents"},
            ),
        ):
            if job is None:
                errors.append(f"pages.yml: missing {job_name} job")
                continue
            job_permissions = nested_entry(
                parsed_pages,
                job,
                "permissions",
            )
            if job_permissions is None:
                errors.append(
                    f"pages.yml: {job_name} job must define permissions"
                )
                continue
            values = permission_values(parsed_pages, job_permissions)
            for key, expected in required.items():
                if values.get(key) != expected:
                    errors.append(
                        f"pages.yml: {job_name} job permission {key} "
                        f"must be {expected}"
                    )
            for key in forbidden:
                if key in values:
                    errors.append(
                        f"pages.yml: {job_name} job must not receive "
                        f"{key} permission"
                    )

    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "docs", "_site", "build"],
        check=True,
        text=True,
        capture_output=True,
    )
    tracked_generated = [
        line for line in result.stdout.splitlines() if line.strip()
    ]
    if tracked_generated:
        errors.append(
            "generated output must not be tracked: "
            + ", ".join(tracked_generated)
        )

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1

    print(
        f"workflow contract passed: {len(workflows)} workflows, "
        "normalized YAML mapping keys, immutable action refs, "
        "non-persistent checkout credentials, ignored npm lifecycle "
        "scripts, operator-only Pages enablement, least-privilege "
        "Pages jobs, locked renderer before npm test, pinned formatter, "
        "generated output untracked"
    )
    return 0
