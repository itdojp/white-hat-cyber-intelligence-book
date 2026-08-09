#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import subprocess
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
SCHEMA_PATH = ROOT / "schemas/site-pages.schema.json"
SCHEMA_VERSION = "1.1.0"
DIRECTORY_RE = re.compile(r"^[A-Za-z0-9_-]+$")
STATIC_PATH_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*\.json$")
LINE_TERMINATOR_RE = re.compile(r"[\r\n\u2028\u2029]")
# Freeze the Python-compatible whitespace set, the Unicode 15.0 Cc, Cs, Cf,
# and Mark sets, and the finite invisible-base corpus used by the schema and
# parser.  Do not derive these tables from
# the runner's Unicode database: the publication contract must remain stable
# when Python or Node ships another Unicode database.  Cc controls are rejected
# anywhere in a published navigation title because they are not portable,
# reader-visible navigation content; Cs is rejected because an unpaired
# surrogate is not a Unicode scalar value and cannot be encoded as strict
# UTF-8.  Valid astral scalar values and emoji remain allowed.
PAGE_TITLE_WHITESPACE_UNICODE_VERSION = "15.0.0"
PAGE_TITLE_WHITESPACE_RANGES = (
    (0x0009, 0x000D),
    (0x001C, 0x0020),
    (0x0085, 0x0085),
    (0x00A0, 0x00A0),
    (0x1680, 0x1680),
    (0x2000, 0x200A),
    (0x2028, 0x2029),
    (0x202F, 0x202F),
    (0x205F, 0x205F),
    (0x3000, 0x3000),
)
PAGE_TITLE_CONTROL_UNICODE_VERSION = "15.0.0"
PAGE_TITLE_CONTROL_RANGES = (
    (0x0000, 0x001F),
    (0x007F, 0x009F),
)
PAGE_TITLE_SURROGATE_UNICODE_VERSION = "15.0.0"
PAGE_TITLE_SURROGATE_RANGES = (
    (0xD800, 0xDFFF),
)
PAGE_TITLE_FORMAT_CONTROL_UNICODE_VERSION = "15.0.0"
PAGE_TITLE_FORMAT_CONTROL_RANGES = (
    (0x00AD, 0x00AD),
    (0x0600, 0x0605),
    (0x061C, 0x061C),
    (0x06DD, 0x06DD),
    (0x070F, 0x070F),
    (0x0890, 0x0891),
    (0x08E2, 0x08E2),
    (0x180E, 0x180E),
    (0x200B, 0x200F),
    (0x202A, 0x202E),
    (0x2060, 0x2064),
    (0x2066, 0x206F),
    (0xFEFF, 0xFEFF),
    (0xFFF9, 0xFFFB),
    (0x110BD, 0x110BD),
    (0x110CD, 0x110CD),
    (0x13430, 0x1343F),
    (0x1BCA0, 0x1BCA3),
    (0x1D173, 0x1D17A),
    (0xE0001, 0xE0001),
    (0xE0020, 0xE007F),
)
PAGE_TITLE_MARK_UNICODE_VERSION = "15.0.0"
PAGE_TITLE_MARK_RANGES = (
    (0x0300, 0x036F),
    (0x0483, 0x0489),
    (0x0591, 0x05BD),
    (0x05BF, 0x05BF),
    (0x05C1, 0x05C2),
    (0x05C4, 0x05C5),
    (0x05C7, 0x05C7),
    (0x0610, 0x061A),
    (0x064B, 0x065F),
    (0x0670, 0x0670),
    (0x06D6, 0x06DC),
    (0x06DF, 0x06E4),
    (0x06E7, 0x06E8),
    (0x06EA, 0x06ED),
    (0x0711, 0x0711),
    (0x0730, 0x074A),
    (0x07A6, 0x07B0),
    (0x07EB, 0x07F3),
    (0x07FD, 0x07FD),
    (0x0816, 0x0819),
    (0x081B, 0x0823),
    (0x0825, 0x0827),
    (0x0829, 0x082D),
    (0x0859, 0x085B),
    (0x0898, 0x089F),
    (0x08CA, 0x08E1),
    (0x08E3, 0x0903),
    (0x093A, 0x093C),
    (0x093E, 0x094F),
    (0x0951, 0x0957),
    (0x0962, 0x0963),
    (0x0981, 0x0983),
    (0x09BC, 0x09BC),
    (0x09BE, 0x09C4),
    (0x09C7, 0x09C8),
    (0x09CB, 0x09CD),
    (0x09D7, 0x09D7),
    (0x09E2, 0x09E3),
    (0x09FE, 0x09FE),
    (0x0A01, 0x0A03),
    (0x0A3C, 0x0A3C),
    (0x0A3E, 0x0A42),
    (0x0A47, 0x0A48),
    (0x0A4B, 0x0A4D),
    (0x0A51, 0x0A51),
    (0x0A70, 0x0A71),
    (0x0A75, 0x0A75),
    (0x0A81, 0x0A83),
    (0x0ABC, 0x0ABC),
    (0x0ABE, 0x0AC5),
    (0x0AC7, 0x0AC9),
    (0x0ACB, 0x0ACD),
    (0x0AE2, 0x0AE3),
    (0x0AFA, 0x0AFF),
    (0x0B01, 0x0B03),
    (0x0B3C, 0x0B3C),
    (0x0B3E, 0x0B44),
    (0x0B47, 0x0B48),
    (0x0B4B, 0x0B4D),
    (0x0B55, 0x0B57),
    (0x0B62, 0x0B63),
    (0x0B82, 0x0B82),
    (0x0BBE, 0x0BC2),
    (0x0BC6, 0x0BC8),
    (0x0BCA, 0x0BCD),
    (0x0BD7, 0x0BD7),
    (0x0C00, 0x0C04),
    (0x0C3C, 0x0C3C),
    (0x0C3E, 0x0C44),
    (0x0C46, 0x0C48),
    (0x0C4A, 0x0C4D),
    (0x0C55, 0x0C56),
    (0x0C62, 0x0C63),
    (0x0C81, 0x0C83),
    (0x0CBC, 0x0CBC),
    (0x0CBE, 0x0CC4),
    (0x0CC6, 0x0CC8),
    (0x0CCA, 0x0CCD),
    (0x0CD5, 0x0CD6),
    (0x0CE2, 0x0CE3),
    (0x0CF3, 0x0CF3),
    (0x0D00, 0x0D03),
    (0x0D3B, 0x0D3C),
    (0x0D3E, 0x0D44),
    (0x0D46, 0x0D48),
    (0x0D4A, 0x0D4D),
    (0x0D57, 0x0D57),
    (0x0D62, 0x0D63),
    (0x0D81, 0x0D83),
    (0x0DCA, 0x0DCA),
    (0x0DCF, 0x0DD4),
    (0x0DD6, 0x0DD6),
    (0x0DD8, 0x0DDF),
    (0x0DF2, 0x0DF3),
    (0x0E31, 0x0E31),
    (0x0E34, 0x0E3A),
    (0x0E47, 0x0E4E),
    (0x0EB1, 0x0EB1),
    (0x0EB4, 0x0EBC),
    (0x0EC8, 0x0ECE),
    (0x0F18, 0x0F19),
    (0x0F35, 0x0F35),
    (0x0F37, 0x0F37),
    (0x0F39, 0x0F39),
    (0x0F3E, 0x0F3F),
    (0x0F71, 0x0F84),
    (0x0F86, 0x0F87),
    (0x0F8D, 0x0F97),
    (0x0F99, 0x0FBC),
    (0x0FC6, 0x0FC6),
    (0x102B, 0x103E),
    (0x1056, 0x1059),
    (0x105E, 0x1060),
    (0x1062, 0x1064),
    (0x1067, 0x106D),
    (0x1071, 0x1074),
    (0x1082, 0x108D),
    (0x108F, 0x108F),
    (0x109A, 0x109D),
    (0x135D, 0x135F),
    (0x1712, 0x1715),
    (0x1732, 0x1734),
    (0x1752, 0x1753),
    (0x1772, 0x1773),
    (0x17B4, 0x17D3),
    (0x17DD, 0x17DD),
    (0x180B, 0x180D),
    (0x180F, 0x180F),
    (0x1885, 0x1886),
    (0x18A9, 0x18A9),
    (0x1920, 0x192B),
    (0x1930, 0x193B),
    (0x1A17, 0x1A1B),
    (0x1A55, 0x1A5E),
    (0x1A60, 0x1A7C),
    (0x1A7F, 0x1A7F),
    (0x1AB0, 0x1ACE),
    (0x1B00, 0x1B04),
    (0x1B34, 0x1B44),
    (0x1B6B, 0x1B73),
    (0x1B80, 0x1B82),
    (0x1BA1, 0x1BAD),
    (0x1BE6, 0x1BF3),
    (0x1C24, 0x1C37),
    (0x1CD0, 0x1CD2),
    (0x1CD4, 0x1CE8),
    (0x1CED, 0x1CED),
    (0x1CF4, 0x1CF4),
    (0x1CF7, 0x1CF9),
    (0x1DC0, 0x1DFF),
    (0x20D0, 0x20F0),
    (0x2CEF, 0x2CF1),
    (0x2D7F, 0x2D7F),
    (0x2DE0, 0x2DFF),
    (0x302A, 0x302F),
    (0x3099, 0x309A),
    (0xA66F, 0xA672),
    (0xA674, 0xA67D),
    (0xA69E, 0xA69F),
    (0xA6F0, 0xA6F1),
    (0xA802, 0xA802),
    (0xA806, 0xA806),
    (0xA80B, 0xA80B),
    (0xA823, 0xA827),
    (0xA82C, 0xA82C),
    (0xA880, 0xA881),
    (0xA8B4, 0xA8C5),
    (0xA8E0, 0xA8F1),
    (0xA8FF, 0xA8FF),
    (0xA926, 0xA92D),
    (0xA947, 0xA953),
    (0xA980, 0xA983),
    (0xA9B3, 0xA9C0),
    (0xA9E5, 0xA9E5),
    (0xAA29, 0xAA36),
    (0xAA43, 0xAA43),
    (0xAA4C, 0xAA4D),
    (0xAA7B, 0xAA7D),
    (0xAAB0, 0xAAB0),
    (0xAAB2, 0xAAB4),
    (0xAAB7, 0xAAB8),
    (0xAABE, 0xAABF),
    (0xAAC1, 0xAAC1),
    (0xAAEB, 0xAAEF),
    (0xAAF5, 0xAAF6),
    (0xABE3, 0xABEA),
    (0xABEC, 0xABED),
    (0xFB1E, 0xFB1E),
    (0xFE00, 0xFE0F),
    (0xFE20, 0xFE2F),
    (0x101FD, 0x101FD),
    (0x102E0, 0x102E0),
    (0x10376, 0x1037A),
    (0x10A01, 0x10A03),
    (0x10A05, 0x10A06),
    (0x10A0C, 0x10A0F),
    (0x10A38, 0x10A3A),
    (0x10A3F, 0x10A3F),
    (0x10AE5, 0x10AE6),
    (0x10D24, 0x10D27),
    (0x10EAB, 0x10EAC),
    (0x10EFD, 0x10EFF),
    (0x10F46, 0x10F50),
    (0x10F82, 0x10F85),
    (0x11000, 0x11002),
    (0x11038, 0x11046),
    (0x11070, 0x11070),
    (0x11073, 0x11074),
    (0x1107F, 0x11082),
    (0x110B0, 0x110BA),
    (0x110C2, 0x110C2),
    (0x11100, 0x11102),
    (0x11127, 0x11134),
    (0x11145, 0x11146),
    (0x11173, 0x11173),
    (0x11180, 0x11182),
    (0x111B3, 0x111C0),
    (0x111C9, 0x111CC),
    (0x111CE, 0x111CF),
    (0x1122C, 0x11237),
    (0x1123E, 0x1123E),
    (0x11241, 0x11241),
    (0x112DF, 0x112EA),
    (0x11300, 0x11303),
    (0x1133B, 0x1133C),
    (0x1133E, 0x11344),
    (0x11347, 0x11348),
    (0x1134B, 0x1134D),
    (0x11357, 0x11357),
    (0x11362, 0x11363),
    (0x11366, 0x1136C),
    (0x11370, 0x11374),
    (0x11435, 0x11446),
    (0x1145E, 0x1145E),
    (0x114B0, 0x114C3),
    (0x115AF, 0x115B5),
    (0x115B8, 0x115C0),
    (0x115DC, 0x115DD),
    (0x11630, 0x11640),
    (0x116AB, 0x116B7),
    (0x1171D, 0x1172B),
    (0x1182C, 0x1183A),
    (0x11930, 0x11935),
    (0x11937, 0x11938),
    (0x1193B, 0x1193E),
    (0x11940, 0x11940),
    (0x11942, 0x11943),
    (0x119D1, 0x119D7),
    (0x119DA, 0x119E0),
    (0x119E4, 0x119E4),
    (0x11A01, 0x11A0A),
    (0x11A33, 0x11A39),
    (0x11A3B, 0x11A3E),
    (0x11A47, 0x11A47),
    (0x11A51, 0x11A5B),
    (0x11A8A, 0x11A99),
    (0x11C2F, 0x11C36),
    (0x11C38, 0x11C3F),
    (0x11C92, 0x11CA7),
    (0x11CA9, 0x11CB6),
    (0x11D31, 0x11D36),
    (0x11D3A, 0x11D3A),
    (0x11D3C, 0x11D3D),
    (0x11D3F, 0x11D45),
    (0x11D47, 0x11D47),
    (0x11D8A, 0x11D8E),
    (0x11D90, 0x11D91),
    (0x11D93, 0x11D97),
    (0x11EF3, 0x11EF6),
    (0x11F00, 0x11F01),
    (0x11F03, 0x11F03),
    (0x11F34, 0x11F3A),
    (0x11F3E, 0x11F42),
    (0x13440, 0x13440),
    (0x13447, 0x13455),
    (0x16AF0, 0x16AF4),
    (0x16B30, 0x16B36),
    (0x16F4F, 0x16F4F),
    (0x16F51, 0x16F87),
    (0x16F8F, 0x16F92),
    (0x16FE4, 0x16FE4),
    (0x16FF0, 0x16FF1),
    (0x1BC9D, 0x1BC9E),
    (0x1CF00, 0x1CF2D),
    (0x1CF30, 0x1CF46),
    (0x1D165, 0x1D169),
    (0x1D16D, 0x1D172),
    (0x1D17B, 0x1D182),
    (0x1D185, 0x1D18B),
    (0x1D1AA, 0x1D1AD),
    (0x1D242, 0x1D244),
    (0x1DA00, 0x1DA36),
    (0x1DA3B, 0x1DA6C),
    (0x1DA75, 0x1DA75),
    (0x1DA84, 0x1DA84),
    (0x1DA9B, 0x1DA9F),
    (0x1DAA1, 0x1DAAF),
    (0x1E000, 0x1E006),
    (0x1E008, 0x1E018),
    (0x1E01B, 0x1E021),
    (0x1E023, 0x1E024),
    (0x1E026, 0x1E02A),
    (0x1E08F, 0x1E08F),
    (0x1E130, 0x1E136),
    (0x1E2AE, 0x1E2AE),
    (0x1E2EC, 0x1E2EF),
    (0x1E4EC, 0x1E4EF),
    (0x1E8D0, 0x1E8D6),
    (0x1E944, 0x1E94A),
    (0xE0100, 0xE01EF),
)
# Unicode assigns these characters base categories, but their defined glyph is
# intentionally blank/filler-like in ordinary navigation rendering.  Keep the
# verified finite Unicode 15.0 corpus explicit: it prevents an invisible-only
# page title without claiming to classify every visually blank glyph.
PAGE_TITLE_INVISIBLE_BASE_UNICODE_VERSION = "15.0.0"
PAGE_TITLE_INVISIBLE_BASE_RANGES = (
    (0x115F, 0x115F),  # HANGUL CHOSEONG FILLER
    (0x2800, 0x2800),  # BRAILLE PATTERN BLANK
    (0x3164, 0x3164),  # HANGUL FILLER
    (0xFFA0, 0xFFA0),  # HALFWIDTH HANGUL FILLER
)
PAGE_TITLE_WHITESPACE_CODEPOINTS = frozenset(
    codepoint
    for start, end in PAGE_TITLE_WHITESPACE_RANGES
    for codepoint in range(start, end + 1)
)
PAGE_TITLE_CONTROL_CODEPOINTS = frozenset(
    codepoint
    for start, end in PAGE_TITLE_CONTROL_RANGES
    for codepoint in range(start, end + 1)
)
PAGE_TITLE_SURROGATE_CODEPOINTS = frozenset(
    codepoint
    for start, end in PAGE_TITLE_SURROGATE_RANGES
    for codepoint in range(start, end + 1)
)
PAGE_TITLE_FORMAT_CONTROL_CODEPOINTS = frozenset(
    codepoint
    for start, end in PAGE_TITLE_FORMAT_CONTROL_RANGES
    for codepoint in range(start, end + 1)
)
PAGE_TITLE_MARK_CODEPOINTS = frozenset(
    codepoint
    for start, end in PAGE_TITLE_MARK_RANGES
    for codepoint in range(start, end + 1)
)
PAGE_TITLE_INVISIBLE_BASE_CODEPOINTS = frozenset(
    codepoint
    for start, end in PAGE_TITLE_INVISIBLE_BASE_RANGES
    for codepoint in range(start, end + 1)
)
PAGE_TITLE_NON_BASE_CODEPOINTS = (
    PAGE_TITLE_WHITESPACE_CODEPOINTS
    | PAGE_TITLE_CONTROL_CODEPOINTS
    | PAGE_TITLE_FORMAT_CONTROL_CODEPOINTS
    | PAGE_TITLE_MARK_CODEPOINTS
    | PAGE_TITLE_INVISIBLE_BASE_CODEPOINTS
)
PAGE_TITLE_FORBIDDEN_ANYWHERE_CODEPOINTS = (
    PAGE_TITLE_CONTROL_CODEPOINTS | PAGE_TITLE_SURROGATE_CODEPOINTS
)


def _ranges_for_codepoints(codepoints: frozenset[int]) -> tuple[tuple[int, int], ...]:
    """Compress a frozen code-point set into deterministic inclusive ranges."""

    ranges: list[list[int]] = []
    for codepoint in sorted(codepoints):
        if not ranges or codepoint != ranges[-1][1] + 1:
            ranges.append([codepoint, codepoint])
        else:
            ranges[-1][1] = codepoint
    return tuple((start, end) for start, end in ranges)


PAGE_TITLE_NON_BASE_BMP_RANGES = tuple(
    (start, end)
    for start, end in _ranges_for_codepoints(PAGE_TITLE_NON_BASE_CODEPOINTS)
    if end <= 0xFFFF
)
PAGE_TITLE_NON_BASE_BMP_SCHEMA_CLASS = "".join(
    f"\\u{start:04X}"
    if start == end
    else f"\\u{start:04X}-\\u{end:04X}"
    for start, end in PAGE_TITLE_NON_BASE_BMP_RANGES
)
# Keep astral code points as exact literal alternatives instead of ranges in a
# character class.  This compiles with and without ECMAScript's Unicode flag:
# no-u engines see exact surrogate pairs, while u engines see exact code points.
PAGE_TITLE_NON_BASE_ASTRAL_SCHEMA_ALTERNATION = "|".join(
    chr(codepoint)
    for codepoint in sorted(PAGE_TITLE_NON_BASE_CODEPOINTS)
    if codepoint > 0xFFFF
)
PAGE_TITLE_SCHEMA_NON_BASE_TOKEN = (
    f"(?:[{PAGE_TITLE_NON_BASE_BMP_SCHEMA_CLASS}]|"
    f"(?:{PAGE_TITLE_NON_BASE_ASTRAL_SCHEMA_ALTERNATION}))"
)
PAGE_TITLE_CONTROL_BMP_SCHEMA_CLASS = "".join(
    f"\\u{start:04X}"
    if start == end
    else f"\\u{start:04X}-\\u{end:04X}"
    for start, end in PAGE_TITLE_CONTROL_RANGES
)
# In non-Unicode ECMAScript mode, a valid astral scalar is represented by a
# high/low surrogate pair.  These forward-only gates reject a low surrogate at
# the start, a high surrogate without a following low surrogate, or a low
# surrogate whose predecessor is not high.  Avoiding lookbehind keeps the
# public JSON Schema portable while preserving no-u/u parity.
PAGE_TITLE_SCHEMA_UNPAIRED_SURROGATE_GATES = (
    r"(?![\uDC00-\uDFFF])"
    r"(?!.*[\uD800-\uDBFF](?![\uDC00-\uDFFF]))"
    r"(?!.*[^\uD800-\uDBFF][\uDC00-\uDFFF])"
)
PAGE_TITLE_SCHEMA_PATTERN = (
    f"^{PAGE_TITLE_SCHEMA_UNPAIRED_SURROGATE_GATES}"
    f"(?!(?:{PAGE_TITLE_SCHEMA_NON_BASE_TOKEN})+$)"
    f"[^{PAGE_TITLE_CONTROL_BMP_SCHEMA_CLASS}<>\\r\\n\\u2028\\u2029]+$"
)
PAGE_TITLE_HTML_DELIMITER_RE = re.compile(r"[<>]")
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
        if not isinstance(title, str) or not title or all(
            ord(character) in PAGE_TITLE_WHITESPACE_CODEPOINTS
            for character in title
        ):
            raise SitePageRegistryError(
                f"pages[{index}].title must contain a non-whitespace character"
            )
        if LINE_TERMINATOR_RE.search(title):
            raise SitePageRegistryError(
                f"pages[{index}].title must not contain CR, LF, U+2028, or U+2029"
            )
        if any(
            ord(character) in PAGE_TITLE_FORBIDDEN_ANYWHERE_CODEPOINTS
            for character in title
        ):
            raise SitePageRegistryError(
                f"pages[{index}].title must not contain Unicode 15.0 Cc controls "
                "or Cs surrogate code points"
            )
        try:
            title.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise SitePageRegistryError(
                f"pages[{index}].title must be encodable as strict UTF-8"
            ) from exc
        if not any(
            ord(character) not in PAGE_TITLE_NON_BASE_CODEPOINTS
            for character in title
        ):
            raise SitePageRegistryError(
                f"pages[{index}].title must contain a base reader-visible character"
            )
        if PAGE_TITLE_HTML_DELIMITER_RE.search(title):
            raise SitePageRegistryError(
                f"pages[{index}].title must not contain raw HTML delimiters"
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


def ecmascript_title_pattern_results(
    pattern: str,
    samples: tuple[str, ...],
) -> dict[str, dict[str, object]]:
    """Compile/test the public JSON-Schema regex in both ECMAScript modes."""

    probe = r"""
const fs = require("fs");
const payload = JSON.parse(fs.readFileSync(0, "utf8"));
const results = {};
for (const [name, flags] of [["no-u", ""], ["u", "u"]]) {
  try {
    const expression = new RegExp(payload.pattern, flags);
    results[name] = {
      compiled: true,
      matches: payload.samples.map((sample) => expression.test(sample)),
    };
  } catch (error) {
    results[name] = {compiled: false, error: String(error)};
  }
}
process.stdout.write(JSON.stringify(results));
"""
    completed = subprocess.run(
        ["node", "-e", probe],
        input=json.dumps({"pattern": pattern, "samples": samples}),
        text=True,
        capture_output=True,
        check=False,
        timeout=15,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Node ECMAScript title-pattern probe failed: "
            f"exit={completed.returncode}, stderr={completed.stderr.strip()!r}"
        )
    result = json.loads(completed.stdout)
    if not isinstance(result, dict):
        raise RuntimeError("Node ECMAScript title-pattern probe returned a non-object")
    return result


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

    for name, title in (
        ("empty published page title", ""),
        ("space-only published page title", "   "),
        ("tab-only published page title", "\t\t"),
        ("Unicode-space-only published page title", "\u3000\u00a0"),
        ("C0-separator-whitespace-only published page title", "\u001c\u001d\u001e\u001f"),
        ("NEXT-LINE-whitespace-only published page title", "\u0085"),
        ("NUL-only published page title", "\u0000"),
        ("BELL-only published page title", "\u0007"),
        ("DELETE-only published page title", "\u007f"),
        ("APPLICATION-PROGRAM-COMMAND-only published page title", "\u009f"),
        ("mixed Cc published page title", "Visible\u0007 title"),
        ("unpaired high-surrogate published page title", "\ud800"),
        ("mixed unpaired-surrogate published page title", "Visible\ud800 title"),
        ("zero-width-only published page title", "\u200b"),
        ("word-joiner-only published page title", "\u2060"),
        ("BOM-only published page title", "\ufeff"),
        ("format-control-only published page title", "\u200e\u202e"),
        ("variation-selector-only published page title", "\ufe0f"),
        ("combining-grapheme-joiner-only published page title", "\u034f"),
        ("combining-acute-only published page title", "\u0301"),
        ("Mongolian-variation-selector-only published page title", "\u180b"),
        ("BRAILLE-PATTERN-BLANK-only published page title", "\u2800"),
        ("HANGUL-CHOSEONG-FILLER-only published page title", "\u115f"),
        ("HANGUL-FILLER-only published page title", "\u3164"),
        ("HALFWIDTH-HANGUL-FILLER-only published page title", "\uffa0"),
        ("raw HTML published page title", "<span>Visible title</span>"),
        (
            "raw script-element published page title",
            "</span><script>test</script><span>",
        ),
    ):
        expect_invalid_registry(failures, name, page_title_fixture(title))

    schema_safe_titles = (
        "e\u0301vidence title",
        "क\u093f",
        "か\u3099",
        "𐀀\U000101fd",
        "😀\ufe0f",
        "Visible\u2800title",
        "Visible\u115ftitle",
        "Visible\u3164title",
        "Visible\uffa0title",
    )

    try:
        raw_schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        title_schema = raw_schema["properties"]["pages"]["items"]["properties"]["title"]
        if title_schema.get("pattern") != PAGE_TITLE_SCHEMA_PATTERN:
            failures.append(
                "site-pages schema title pattern is not synchronized with the "
                "frozen whitespace/Cc/Cs/Cf/Mark/invisible-base parser contract"
            )
        title_pattern = re.compile(PAGE_TITLE_SCHEMA_PATTERN)
        for name, title in (
            ("spaces", "   "),
            ("tabs", "\t\t"),
            ("Unicode spaces", "\u3000\u00a0"),
            ("C0 separator whitespace", "\u001c\u001d\u001e\u001f"),
            ("NEXT LINE whitespace", "\u0085"),
            ("NUL control", "\u0000"),
            ("BELL control", "\u0007"),
            ("DELETE control", "\u007f"),
            ("APPLICATION PROGRAM COMMAND control", "\u009f"),
            ("mixed Cc control", "Visible\u0007 title"),
            ("unpaired high surrogate", "\ud800"),
            ("mixed unpaired high surrogate", "Visible\ud800 title"),
            ("zero width", "\u200b"),
            ("word joiner", "\u2060"),
            ("BOM", "\ufeff"),
            ("variation selector", "\ufe0f"),
            ("combining grapheme joiner", "\u034f"),
            ("combining acute", "\u0301"),
            ("Mongolian variation selector", "\u180b"),
            ("BRAILLE PATTERN BLANK", "\u2800"),
            ("HANGUL CHOSEONG FILLER", "\u115f"),
            ("HANGUL FILLER", "\u3164"),
            ("HALFWIDTH HANGUL FILLER", "\uffa0"),
            ("raw HTML", "<span>Visible title</span>"),
        ):
            if title_pattern.fullmatch(title):
                failures.append(
                    f"site-pages schema title pattern accepted {name}-only/unsafe title"
                )
        for title in schema_safe_titles:
            if not title_pattern.fullmatch(title):
                failures.append(
                    "site-pages schema title pattern rejected safe base/Mark title "
                    f"{title!r}"
                )
        if (
            PAGE_TITLE_WHITESPACE_UNICODE_VERSION != "15.0.0"
            or len(PAGE_TITLE_WHITESPACE_RANGES) != 10
            or len(PAGE_TITLE_WHITESPACE_CODEPOINTS) != 29
        ):
            failures.append(
                "site-pages title whitespace table drifted from the frozen "
                "Unicode 15.0/Python-compatible contract (10 ranges / 29 code points)"
            )
        if (
            PAGE_TITLE_CONTROL_UNICODE_VERSION != "15.0.0"
            or len(PAGE_TITLE_CONTROL_RANGES) != 2
            or len(PAGE_TITLE_CONTROL_CODEPOINTS) != 65
        ):
            failures.append(
                "site-pages title Cc table drifted from the frozen Unicode 15.0 "
                "contract (2 ranges / 65 code points)"
            )
        if (
            PAGE_TITLE_SURROGATE_UNICODE_VERSION != "15.0.0"
            or len(PAGE_TITLE_SURROGATE_RANGES) != 1
            or len(PAGE_TITLE_SURROGATE_CODEPOINTS) != 2048
        ):
            failures.append(
                "site-pages title Cs table drifted from the frozen Unicode 15.0 "
                "contract (1 range / 2048 code points)"
            )
        if (
            PAGE_TITLE_FORMAT_CONTROL_UNICODE_VERSION != "15.0.0"
            or len(PAGE_TITLE_FORMAT_CONTROL_RANGES) != 21
            or len(PAGE_TITLE_FORMAT_CONTROL_CODEPOINTS) != 170
        ):
            failures.append(
                "site-pages title format-control table drifted from the frozen "
                "Unicode 15.0 contract (21 ranges / 170 code points)"
            )
        if (
            PAGE_TITLE_MARK_UNICODE_VERSION != "15.0.0"
            or len(PAGE_TITLE_MARK_RANGES) != 310
            or len(PAGE_TITLE_MARK_CODEPOINTS) != 2450
        ):
            failures.append(
                "site-pages title Mark table drifted from the frozen "
                "Unicode 15.0 contract (310 ranges / 2450 code points)"
            )
        if (
            PAGE_TITLE_INVISIBLE_BASE_UNICODE_VERSION != "15.0.0"
            or len(PAGE_TITLE_INVISIBLE_BASE_RANGES) != 4
            or len(PAGE_TITLE_INVISIBLE_BASE_CODEPOINTS) != 4
        ):
            failures.append(
                "site-pages title invisible-base corpus drifted from the frozen "
                "Unicode 15.0 finite contract (4 ranges / 4 code points)"
            )
        all_format_controls = "".join(
            chr(codepoint) for codepoint in sorted(PAGE_TITLE_FORMAT_CONTROL_CODEPOINTS)
        )
        if title_pattern.fullmatch(all_format_controls):
            failures.append(
                "site-pages schema title pattern accepted the complete format-control corpus"
            )
        try:
            parse_registry_data(
                page_title_fixture(all_format_controls),
                "complete format-control title corpus",
            )
        except SitePageRegistryError:
            pass
        else:
            failures.append(
                "site-pages parser accepted the complete format-control title corpus"
            )
        all_controls = "".join(
            chr(codepoint) for codepoint in sorted(PAGE_TITLE_CONTROL_CODEPOINTS)
        )
        if title_pattern.fullmatch(all_controls):
            failures.append(
                "site-pages schema title pattern accepted the complete Cc corpus"
            )
        try:
            parse_registry_data(page_title_fixture(all_controls), "complete Cc title corpus")
        except SitePageRegistryError:
            pass
        else:
            failures.append("site-pages parser accepted the complete Cc title corpus")
        all_surrogates = "".join(
            chr(codepoint) for codepoint in sorted(PAGE_TITLE_SURROGATE_CODEPOINTS)
        )
        if title_pattern.fullmatch(all_surrogates):
            failures.append(
                "site-pages schema title pattern accepted the complete Cs corpus"
            )
        try:
            parse_registry_data(page_title_fixture(all_surrogates), "complete Cs title corpus")
        except SitePageRegistryError:
            pass
        else:
            failures.append("site-pages parser accepted the complete Cs title corpus")
        all_marks = "".join(
            chr(codepoint) for codepoint in sorted(PAGE_TITLE_MARK_CODEPOINTS)
        )
        if title_pattern.fullmatch(all_marks):
            failures.append(
                "site-pages schema title pattern accepted the complete Mark corpus"
            )
        try:
            parse_registry_data(
                page_title_fixture(all_marks),
                "complete Mark title corpus",
            )
        except SitePageRegistryError:
            pass
        else:
            failures.append(
                "site-pages parser accepted the complete Mark title corpus"
            )
        all_invisible_bases = "".join(
            chr(codepoint)
            for codepoint in sorted(PAGE_TITLE_INVISIBLE_BASE_CODEPOINTS)
        )
        if title_pattern.fullmatch(all_invisible_bases):
            failures.append(
                "site-pages schema title pattern accepted the complete "
                "invisible-base corpus"
            )
        try:
            parse_registry_data(
                page_title_fixture(all_invisible_bases),
                "complete invisible-base title corpus",
            )
        except SitePageRegistryError:
            pass
        else:
            failures.append(
                "site-pages parser accepted the complete invisible-base title corpus"
            )
        all_whitespace = "".join(
            chr(codepoint) for codepoint in sorted(PAGE_TITLE_WHITESPACE_CODEPOINTS)
        )
        if title_pattern.fullmatch(all_whitespace):
            failures.append(
                "site-pages schema title pattern accepted the complete whitespace corpus"
            )
        try:
            parse_registry_data(
                page_title_fixture(all_whitespace),
                "complete whitespace title corpus",
            )
        except SitePageRegistryError:
            pass
        else:
            failures.append(
                "site-pages parser accepted the complete whitespace title corpus"
            )

        ecmascript_unsafe_titles = (
            "\u0000",
            "\u0007",
            "\u001c",
            "\u001d",
            "\u001e",
            "\u001f",
            "\u0085",
            "\u009f",
            "Visible\u0007 title",
            "\ud800",
            "Visible\ud800 title",
            "\u0301",
            "\ufe0f",
            "\u180b",
            "\u2800",
            "\u115f",
            "\u3164",
            "\uffa0",
            "\U000101fd",
            "\U000e0100",
            all_whitespace,
            all_controls,
            all_surrogates,
            all_format_controls,
            all_marks,
            all_invisible_bases,
        )
        ecmascript_samples = ecmascript_unsafe_titles + schema_safe_titles
        ecmascript_results = ecmascript_title_pattern_results(
            PAGE_TITLE_SCHEMA_PATTERN,
            ecmascript_samples,
        )
        expected_matches = [False] * len(ecmascript_unsafe_titles) + [True] * len(
            schema_safe_titles
        )
        for mode in ("no-u", "u"):
            mode_result = ecmascript_results.get(mode, {})
            if mode_result.get("compiled") is not True:
                failures.append(
                    f"site-pages schema title pattern did not compile in ECMAScript "
                    f"{mode}: {mode_result.get('error')!r}"
                )
                continue
            if mode_result.get("matches") != expected_matches:
                failures.append(
                    f"site-pages schema title pattern parser parity drifted in "
                    f"ECMAScript {mode}: {mode_result.get('matches')!r}"
                )
        for title in schema_safe_titles:
            try:
                encoded = title.encode("utf-8", errors="strict")
                encoded.decode("utf-8", errors="strict")
            except UnicodeError as exc:
                failures.append(
                    f"safe published title did not round-trip as strict UTF-8: "
                    f"{title!r}: {exc}"
                )
    except (
        OSError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        RuntimeError,
        subprocess.TimeoutExpired,
    ) as exc:
        failures.append(f"site-pages schema title contract cannot be read: {exc}")

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
    ) + schema_safe_titles
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
