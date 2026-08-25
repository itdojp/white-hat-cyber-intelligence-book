#!/usr/bin/env python3
"""One exact, chapter-independent publication projection owner.

The public API batches Markdown through the repository's locked production
Jekyll/Kramdown GFM parser.  It returns deterministic typed publication fields;
it does not implement the Content Safety Policy or any chapter semantics.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import html
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import unicodedata
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts" / "_publication_projection_renderer.rb"
PROJECTION_VERSION = "1.0.0"
PROTOCOL_VERSION = "1"
EXPECTED_RENDERER = {
    "ruby_series": "3.3",
    "jekyll": "4.4.1",
    "kramdown": "2.5.2",
    "kramdown_parser": "Kramdown::Parser::GFM",
    "kramdown_parser_gfm": "1.1.0",
    "kramdown_hard_wrap": "false",
    "liquid": "4.0.4",
    "production_base_scheme": "https",
    "syntax_highlighter": "rouge",
}
FIELD_TYPES = frozenset(
    {
        "reader_visible_text",
        "reader_visible_attribute",
        "destination",
        "hidden_metadata",
    }
)
SCANNABLE_TEXT_TYPES = frozenset({"reader_visible_text", "reader_visible_attribute"})
MAX_DOCUMENTS = 256
MAX_DOCUMENT_BYTES = 2_000_000
MAX_TOTAL_BYTES = 8_000_000
RENDER_TIMEOUT_SECONDS = 45
RENDER_MAX_ADDRESS_SPACE_BYTES = 384 * 1024 * 1024
RENDER_MAX_CPU_SECONDS = 30
UNSUPPORTED_SOURCE_CODE = "PP1001"
UNSAFE_DESTINATION_CODE = "PP1002"

_EXECUTABLE_DESTINATION_SCHEMES = frozenset({"javascript", "vbscript", "file"})
_NETWORK_SPECIAL_SCHEMES = frozenset({"ftp", "http", "https", "ws", "wss"})
_C0_CONTROL_OR_SPACE = "".join(chr(value) for value in range(0x21))
_POLICY_SOURCE_PUNCTUATION = frozenset("[]()*~`\\")


class ProjectionRuntimeError(RuntimeError):
    """The locked renderer could not provide a trustworthy projection."""


@dataclass(frozen=True)
class ProjectionDiagnostic:
    """One deterministic, fail-closed shared projection diagnostic."""

    code: str
    document_id: str
    line: int
    kind: str
    reason: str

    @property
    def location(self) -> str:
        return f"{self.document_id}:L{self.line}"


@dataclass(frozen=True)
class ProjectionField:
    """One typed reader/publication field in stable renderer order."""

    document_id: str
    field_type: str
    text: str
    normalized_text: str
    line: int
    ordinal: int
    element_kind: str
    attribute: str | None
    metadata: tuple[tuple[str, str | int | bool], ...]

    @property
    def location(self) -> str:
        return f"{self.document_id}:L{self.line}:F{self.ordinal}"

    def metadata_value(self, name: str) -> str | int | bool | None:
        return dict(self.metadata).get(name)


@dataclass(frozen=True)
class ProjectedDocument:
    """Projection result for one input document."""

    document_id: str
    fields: tuple[ProjectionField, ...]
    diagnostics: tuple[ProjectionDiagnostic, ...]
    rendered_html: str


@dataclass(frozen=True)
class ProjectionResult:
    """Validated result for one deterministic batch."""

    projection_version: str
    runtime: tuple[tuple[str, str], ...]
    documents: tuple[ProjectedDocument, ...]

    @property
    def fields(self) -> tuple[ProjectionField, ...]:
        return tuple(field for document in self.documents for field in document.fields)

    @property
    def diagnostics(self) -> tuple[ProjectionDiagnostic, ...]:
        return tuple(
            diagnostic
            for document in self.documents
            for diagnostic in document.diagnostics
        )

    def document(self, document_id: str) -> ProjectedDocument:
        matches = [item for item in self.documents if item.document_id == document_id]
        if len(matches) != 1:
            raise KeyError(f"projection document {document_id!r} is not unique")
        return matches[0]


def _materialize_documents(
    documents: Mapping[str, str] | Iterable[tuple[str, str]],
) -> list[tuple[str, str]]:
    if isinstance(documents, Mapping):
        materialized = list(documents.items())
    elif isinstance(documents, (str, bytes)):
        raise TypeError("documents must contain (document_id, source) pairs")
    else:
        try:
            materialized = list(documents)
        except Exception as exc:
            raise TypeError("documents must be iterable") from exc

    if not materialized:
        raise ValueError("at least one publication document is required")
    if len(materialized) > MAX_DOCUMENTS:
        raise ValueError(f"publication document count exceeds {MAX_DOCUMENTS}")

    checked: list[tuple[str, str]] = []
    seen: set[str] = set()
    total_bytes = 0
    for index, item in enumerate(materialized):
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            raise TypeError(f"documents[{index}] must contain document_id and source")
        document_id, source = item
        if not isinstance(document_id, str) or not document_id.strip():
            raise TypeError(
                f"documents[{index}].document_id must be a non-empty string"
            )
        if document_id in seen:
            raise ValueError(f"duplicate publication document_id: {document_id}")
        if not isinstance(source, str):
            raise TypeError(f"{document_id}: source must be a string")
        try:
            size = len(source.encode("utf-8"))
        except UnicodeEncodeError as exc:
            raise ValueError(f"{document_id}: source is not valid UTF-8") from exc
        if size > MAX_DOCUMENT_BYTES:
            raise ValueError(
                f"{document_id}: source exceeds {MAX_DOCUMENT_BYTES} UTF-8 bytes"
            )
        total_bytes += size
        if total_bytes > MAX_TOTAL_BYTES:
            raise ValueError(f"publication batch exceeds {MAX_TOTAL_BYTES} UTF-8 bytes")
        seen.add(document_id)
        checked.append((document_id, source))
    return checked


def _renderer_environment() -> dict[str, str]:
    environment = os.environ.copy()
    for name in ("RUBYOPT", "RUBYLIB", "BUNDLE_PATH", "BUNDLE_BIN_PATH"):
        environment.pop(name, None)
    environment.update(
        {
            "BUNDLE_GEMFILE": str(ROOT / "Gemfile"),
            "BUNDLE_FROZEN": "true",
            "JEKYLL_ENV": "production",
            "LC_ALL": "C.UTF-8",
            "LANG": "C.UTF-8",
        }
    )
    return environment


def _limit_renderer_resources() -> None:
    """Apply Linux/Unix child limits before executing the locked Ruby runtime."""

    def bounded_limit(kind: int, target_soft: int, target_hard: int) -> None:
        current_soft, current_hard = resource.getrlimit(kind)

        def lower(current: int, target: int) -> int:
            return target if current == resource.RLIM_INFINITY else min(current, target)

        hard = lower(current_hard, target_hard)
        soft = min(lower(current_soft, target_soft), hard)
        resource.setrlimit(kind, (soft, hard))

    bounded_limit(
        resource.RLIMIT_AS,
        RENDER_MAX_ADDRESS_SPACE_BYTES,
        RENDER_MAX_ADDRESS_SPACE_BYTES,
    )
    bounded_limit(
        resource.RLIMIT_CPU,
        RENDER_MAX_CPU_SECONDS,
        RENDER_MAX_CPU_SECONDS + 1,
    )


def _run_renderer(documents: list[tuple[str, str]]) -> dict:
    payload = {
        "documents": [
            {"document_id": document_id, "source": source}
            for document_id, source in documents
        ]
    }
    try:
        completed = subprocess.run(
            ["bundle", "exec", "ruby", str(RENDERER)],
            cwd=ROOT,
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_renderer_environment(),
            preexec_fn=_limit_renderer_resources,
            timeout=RENDER_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ProjectionRuntimeError(
            f"locked publication renderer could not run: {type(exc).__name__}"
        ) from exc
    if completed.returncode != 0:
        stderr = " ".join(completed.stderr.strip().split())[:500]
        raise ProjectionRuntimeError(
            "locked publication renderer failed"
            + (f": {stderr}" if stderr else " without a diagnostic")
        )
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ProjectionRuntimeError(
            "locked publication renderer returned invalid JSON"
        ) from exc
    if not isinstance(value, dict):
        raise ProjectionRuntimeError(
            "locked publication renderer root must be an object"
        )
    return value


def _validated_runtime(raw: object) -> tuple[tuple[str, str], ...]:
    if not isinstance(raw, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in raw.items()
    ):
        raise ProjectionRuntimeError("renderer runtime handshake is malformed")
    required = {
        "ruby",
        "jekyll",
        "kramdown",
        "kramdown_parser",
        "kramdown_parser_gfm",
        "kramdown_hard_wrap",
        "liquid",
        "production_base_scheme",
        "syntax_highlighter",
    }
    if set(raw) != required:
        raise ProjectionRuntimeError("renderer runtime handshake keys changed")
    if not re.fullmatch(
        rf"{re.escape(EXPECTED_RENDERER['ruby_series'])}\.\d+", raw["ruby"]
    ):
        raise ProjectionRuntimeError(
            f"renderer Ruby {raw['ruby']!r} is not the required 3.3 series"
        )
    for name in (
        "jekyll",
        "kramdown",
        "kramdown_parser",
        "kramdown_parser_gfm",
        "kramdown_hard_wrap",
        "liquid",
        "production_base_scheme",
        "syntax_highlighter",
    ):
        if raw[name] != EXPECTED_RENDERER[name]:
            raise ProjectionRuntimeError(
                f"renderer {name} {raw[name]!r} != locked {EXPECTED_RENDERER[name]!r}"
            )
    return tuple((name, raw[name]) for name in sorted(raw))


def normalize_destination(destination: str) -> tuple[str, str | None]:
    """Return the frozen browser-special destination view and a rejection reason.

    This is deliberately finite, not a complete WHATWG URL parser.  The exact
    renderer owns Markdown destination parsing; this function only normalizes
    the finite WHATWG network-special backslash/authority forms that browsers
    treat as network navigations and rejects executable schemes.
    """

    if not isinstance(destination, str):
        raise TypeError("destination must be a string")
    value = unicodedata.normalize("NFKC", destination).strip(_C0_CONTROL_OR_SPACE)
    # WHATWG URL parsing removes ASCII tab/newline characters before scheme
    # recognition.  Apply that finite browser-special preprocessing here so an
    # entity-obfuscated value such as ``java&#x09;script:`` cannot bypass the
    # executable-scheme rejection.
    value = re.sub(r"[\t\r\n]", "", value)
    scheme_match = re.match(r"^([A-Za-z][A-Za-z0-9+.-]*):", value)
    scheme = scheme_match.group(1).casefold() if scheme_match else ""

    if scheme in _EXECUTABLE_DESTINATION_SCHEMES:
        return value, f"executable {scheme}: destination is not publishable"
    if scheme == "data":
        return value, "data: destinations are outside the frozen publication contract"

    if scheme in _NETWORK_SPECIAL_SCHEMES:
        suffix = value[len(scheme_match.group(0)) :].replace("\\", "/")
        if suffix.startswith("//"):
            normalized = f"{scheme}:{suffix}"
        elif scheme == EXPECTED_RENDERER["production_base_scheme"]:
            return (
                value,
                f"same-origin authority-less {scheme}: destination is outside "
                "the frozen publication contract",
            )
        else:
            normalized = f"{scheme}://{suffix.lstrip('/')}"
        try:
            parsed = urlsplit(normalized)
            hostname = parsed.hostname
            parsed.port
        except ValueError:
            return normalized, f"{scheme}: destination authority is malformed"
        if not hostname:
            return normalized, f"{scheme}: destination has no parseable authority"
        return normalized, None

    if re.match(r"^[\\/]{2}", value):
        normalized = "https:" + value.replace("\\", "/")
        try:
            parsed = urlsplit(normalized)
            hostname = parsed.hostname
            parsed.port
        except ValueError:
            return normalized, "scheme-relative destination authority is malformed"
        if not hostname:
            return normalized, "scheme-relative destination has no parseable authority"
        return normalized, None

    return value, None


def is_absolute_destination(destination: str) -> bool:
    """Return whether a normalized destination has an explicit URI scheme.

    Relative paths and fragments are publication/build concerns and must not be
    mistaken for host tokens by Layer C.  Absolute schemes, including non-HTTP
    forms such as FTP, WebSocket, and mailto, are passed to the shared host
    policy; executable/data schemes are separately rejected by Layer B.
    """

    if not isinstance(destination, str):
        raise TypeError("destination must be a string")
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination))


def _policy_visible_text(text: str) -> str:
    """Project rendered text into Layer C without a second markup parse.

    Layer C intentionally accepts source-like chapter fields and removes HTML,
    links, and Markdown punctuation.  Layer B has already rendered those forms.
    Remove punctuation that Layer C would otherwise reinterpret as source
    markup.  This matches Layer C's established obfuscation-resistant joining
    (for example, ``key*logger`` remains ``keylogger``).  A numeric-entity
    sentinel is deliberately not
    used: after Layer C's one entity-decode pass its semicolon would become a
    clause boundary and could change the bounded-analysis grammar.  Ampersands
    and angle brackets are still double-escaped below so rendered literals
    cannot become an entity or HTML tag.  Ordinary reader characters such as
    underscores are preserved verbatim for Policy matching.
    """

    protected: list[str] = []
    for character in text:
        if character in _POLICY_SOURCE_PUNCTUATION:
            continue
        else:
            protected.append(
                html.escape(html.escape(character, quote=False), quote=False)
            )
    return "".join(protected)


def _reader_visible_attribute(text: str) -> str:
    """Normalize an already browser-decoded renderer attribute value."""

    return re.sub(r"[\t\r\n\f\v ]+", " ", text).strip()


def _integer(raw: object, *, label: str, minimum: int = 0) -> int:
    if not isinstance(raw, int) or isinstance(raw, bool) or raw < minimum:
        raise ProjectionRuntimeError(f"{label} must be an integer >= {minimum}")
    return raw


def _string(raw: object, *, label: str, allow_empty: bool = False) -> str:
    if not isinstance(raw, str) or (not allow_empty and not raw):
        qualifier = "a string" if allow_empty else "a non-empty string"
        raise ProjectionRuntimeError(f"{label} must be {qualifier}")
    return raw


def _metadata(raw: object, *, label: str) -> tuple[tuple[str, str | int | bool], ...]:
    if not isinstance(raw, dict):
        raise ProjectionRuntimeError(f"{label} must be an object")
    values: list[tuple[str, str | int | bool]] = []
    for key, value in raw.items():
        if not isinstance(key, str) or not isinstance(value, (str, int, bool)):
            raise ProjectionRuntimeError(
                f"{label} supports only string keys and scalar values"
            )
        values.append((key, value))
    return tuple(sorted(values))


def _validate_document(
    raw: object,
    *,
    expected_document_id: str,
) -> ProjectedDocument:
    if not isinstance(raw, dict) or set(raw) != {
        "document_id",
        "fields",
        "unsupported",
        "rendered_html",
    }:
        raise ProjectionRuntimeError(
            f"{expected_document_id}: renderer document schema changed"
        )
    document_id = _string(raw["document_id"], label="document_id")
    if document_id != expected_document_id:
        raise ProjectionRuntimeError(
            f"renderer document order/id changed: {document_id!r} != {expected_document_id!r}"
        )
    if not isinstance(raw["fields"], list) or not isinstance(raw["unsupported"], list):
        raise ProjectionRuntimeError(
            f"{document_id}: fields/unsupported must be arrays"
        )
    rendered_html = _string(
        raw["rendered_html"],
        label=f"{document_id}.rendered_html",
        allow_empty=True,
    )

    fields: list[ProjectionField] = []
    diagnostics: list[ProjectionDiagnostic] = []
    seen_fields: set[tuple] = set()
    for index, item in enumerate(raw["fields"]):
        label = f"{document_id}.fields[{index}]"
        if not isinstance(item, dict) or set(item) != {
            "type",
            "text",
            "line",
            "element_kind",
            "attribute",
            "metadata",
            "ordinal",
        }:
            raise ProjectionRuntimeError(f"{label}: schema changed")
        field_type = _string(item["type"], label=f"{label}.type")
        if field_type not in FIELD_TYPES:
            raise ProjectionRuntimeError(f"{label}: unknown field type {field_type!r}")
        element_kind = _string(item["element_kind"], label=f"{label}.element_kind")
        text = _string(item["text"], label=f"{label}.text")
        if field_type == "reader_visible_attribute":
            text = _reader_visible_attribute(
                text,
            )
            if not text:
                raise ProjectionRuntimeError(
                    f"{label}.text became empty after attribute projection"
                )
        line = _integer(item["line"], label=f"{label}.line", minimum=1)
        ordinal = _integer(item["ordinal"], label=f"{label}.ordinal")
        if ordinal != index:
            raise ProjectionRuntimeError(f"{label}: ordinal must equal renderer order")
        attribute = item["attribute"]
        if attribute is not None and not isinstance(attribute, str):
            raise ProjectionRuntimeError(f"{label}.attribute must be string or null")
        metadata = _metadata(item["metadata"], label=f"{label}.metadata")
        metadata_values = dict(metadata)
        if set(metadata_values) - {"level", "scan_owner"}:
            raise ProjectionRuntimeError(f"{label}.metadata has an unknown owner key")
        level = metadata_values.get("level")
        if level is not None and (
            type(level) is not int
            or not 1 <= level <= 6
            or field_type != "reader_visible_text"
            or element_kind != "heading"
            or attribute is not None
        ):
            raise ProjectionRuntimeError(f"{label}.metadata.level context changed")
        scan_owner = metadata_values.get("scan_owner")
        if scan_owner == "following_body":
            valid_owner_context = (
                field_type == "reader_visible_text"
                and element_kind == "heading"
                and attribute is None
                and type(level) is int
            )
        elif scan_owner == "inline_parent":
            valid_owner_context = (
                field_type == "reader_visible_attribute"
                and (element_kind, attribute)
                in {
                    ("link", "title"),
                    ("image", "alt"),
                    ("image", "title"),
                    ("abbreviation", "title"),
                }
            )
        else:
            valid_owner_context = scan_owner is None
        if not valid_owner_context:
            raise ProjectionRuntimeError(
                f"{label}.metadata.scan_owner is unknown or out of context"
            )
        normalized_text = (
            _policy_visible_text(text) if field_type in SCANNABLE_TEXT_TYPES else text
        )
        if field_type == "destination":
            normalized_text, rejection = normalize_destination(text)
            if rejection:
                diagnostics.append(
                    ProjectionDiagnostic(
                        code=UNSAFE_DESTINATION_CODE,
                        document_id=document_id,
                        line=line,
                        kind="unsafe-destination",
                        reason=rejection,
                    )
                )
        key = (
            field_type,
            text,
            normalized_text,
            line,
            element_kind,
            attribute,
            metadata,
        )
        if key in seen_fields:
            raise ProjectionRuntimeError(
                f"{label}: renderer returned a duplicate field"
            )
        seen_fields.add(key)
        fields.append(
            ProjectionField(
                document_id=document_id,
                field_type=field_type,
                text=text,
                normalized_text=normalized_text,
                line=line,
                ordinal=ordinal,
                element_kind=element_kind,
                attribute=attribute,
                metadata=metadata,
            )
        )

    for index, item in enumerate(raw["unsupported"]):
        label = f"{document_id}.unsupported[{index}]"
        if not isinstance(item, dict) or set(item) != {"kind", "line", "reason"}:
            raise ProjectionRuntimeError(f"{label}: schema changed")
        diagnostics.append(
            ProjectionDiagnostic(
                code=UNSUPPORTED_SOURCE_CODE,
                document_id=document_id,
                line=_integer(item["line"], label=f"{label}.line", minimum=1),
                kind=_string(item["kind"], label=f"{label}.kind"),
                reason=_string(item["reason"], label=f"{label}.reason"),
            )
        )

    ordered_diagnostics = tuple(
        sorted(
            set(diagnostics),
            key=lambda item: (
                item.document_id,
                item.line,
                item.code,
                item.kind,
                item.reason,
            ),
        )
    )
    return ProjectedDocument(
        document_id=document_id,
        fields=tuple(fields),
        diagnostics=ordered_diagnostics,
        rendered_html=rendered_html,
    )


def project_documents(
    documents: Mapping[str, str] | Iterable[tuple[str, str]],
) -> ProjectionResult:
    """Project a finite ordered document batch with the exact locked renderer."""

    materialized = _materialize_documents(documents)
    raw = _run_renderer(materialized)
    if set(raw) != {
        "protocol_version",
        "projection_version",
        "runtime",
        "documents",
    }:
        raise ProjectionRuntimeError("renderer response schema changed")
    if raw["protocol_version"] != PROTOCOL_VERSION:
        raise ProjectionRuntimeError("renderer protocol version mismatch")
    if raw["projection_version"] != PROJECTION_VERSION:
        raise ProjectionRuntimeError("renderer projection version mismatch")
    runtime = _validated_runtime(raw["runtime"])
    if not isinstance(raw["documents"], list) or len(raw["documents"]) != len(
        materialized
    ):
        raise ProjectionRuntimeError("renderer document count changed")
    projected = tuple(
        _validate_document(item, expected_document_id=document_id)
        for (document_id, _), item in zip(materialized, raw["documents"], strict=True)
    )
    return ProjectionResult(
        projection_version=PROJECTION_VERSION,
        runtime=runtime,
        documents=projected,
    )


def scannable_text_fields(
    result: ProjectionResult,
) -> tuple[ProjectionField, ...]:
    """Return non-overlapping reader-visible Policy owners in stable order."""

    return tuple(field for field in result.fields if is_policy_scan_field(field))


def is_policy_scan_field(field: ProjectionField) -> bool:
    """Return whether a visible field owns its Layer C scan.

    Associated heading and inline attribute text (link/image titles, image alt,
    and abbreviation titles) remain typed visible fields while their structural
    parent owns the combined semantic scan.  Metadata prevents scanning the same
    reader-visible value twice while preserving the complete typed projection.
    """

    if not isinstance(field, ProjectionField):
        raise TypeError("field must be ProjectionField")
    return (
        field.field_type in SCANNABLE_TEXT_TYPES
        and field.metadata_value("scan_owner") is None
    )


def destination_fields(result: ProjectionResult) -> tuple[ProjectionField, ...]:
    """Return link/image destinations in stable projection order."""

    return tuple(field for field in result.fields if field.field_type == "destination")


__all__ = (
    "EXPECTED_RENDERER",
    "FIELD_TYPES",
    "PROJECTION_VERSION",
    "ProjectedDocument",
    "ProjectionDiagnostic",
    "ProjectionField",
    "ProjectionResult",
    "ProjectionRuntimeError",
    "UNSAFE_DESTINATION_CODE",
    "UNSUPPORTED_SOURCE_CODE",
    "destination_fields",
    "is_absolute_destination",
    "is_policy_scan_field",
    "normalize_destination",
    "project_documents",
    "scannable_text_fields",
)
