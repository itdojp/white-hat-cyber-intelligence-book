#!/usr/bin/env python3
"""Finite reader-visible text projection shared by publication consumers.

This module does not parse Markdown or implement the Content Safety Policy.
It only projects the HTML character references that browsers render as
collapsible ASCII whitespace before a bounded reader-visible field is scanned.
"""

from __future__ import annotations

import re


HTML_COLLAPSIBLE_WHITESPACE_CODEPOINTS = frozenset(
    {
        0x0009,  # CHARACTER TABULATION
        0x000A,  # LINE FEED
        0x000C,  # FORM FEED
        0x000D,  # CARRIAGE RETURN
        0x0020,  # SPACE
    }
)
HTML_COLLAPSIBLE_WHITESPACE_NAMED_ENTITIES = (
    "NewLine",
    "Tab",
)

# Named HTML5 references in this finite corpus require their semicolon.
# Numeric references follow the browser grammar and may omit it, but a
# semicolonless match stops before the next decimal/hex digit.  The expression
# intentionally excludes non-collapsible references such as ``&nbsp;``.
_HTML_COLLAPSIBLE_WHITESPACE_ENTITY = re.compile(
    r"&(?:"
    r"(?:NewLine|Tab);"
    r"|#0*(?:9|1[023]|32)(?:;|(?![0-9]))"
    r"|#[xX]0*(?:9|[aA]|[cC]|[dD]|20)(?:;|(?![0-9A-Fa-f]))"
    r")"
)


def normalize_html_collapsible_whitespace_entities(text: str) -> str:
    """Replace one direct finite whitespace-reference layer with ASCII space.

    Literal source newlines are preserved.  Double-encoded references such as
    ``&amp;NewLine;`` are also preserved because a browser decodes them to the
    literal text ``&NewLine;`` rather than to a newline in one rendering pass.
    """

    if not isinstance(text, str):
        raise TypeError("text must be str")
    return _HTML_COLLAPSIBLE_WHITESPACE_ENTITY.sub(" ", text)


def protect_html_collapsible_whitespace_entities(text: str) -> str:
    """Protect a once-decoded literal before one downstream entity decode.

    Some bounded Markdown projections decode one renderer layer before sending
    the result to the shared Policy, whose normalizer performs its own single
    decode.  A whitespace reference still present after the first decode came
    from encoded literal text; re-encode only its ampersand so the downstream
    pass cannot turn that literal into a clause boundary.
    """

    if not isinstance(text, str):
        raise TypeError("text must be str")
    return _HTML_COLLAPSIBLE_WHITESPACE_ENTITY.sub(
        lambda match: "&amp;" + match.group(0)[1:],
        text,
    )
