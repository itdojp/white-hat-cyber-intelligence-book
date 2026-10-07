"""Source review dates may advance without erasing a chapter's audit baseline."""

from datetime import date


def meets_audit_baseline(value: object, baseline: str) -> bool:
    """Accept only canonical full dates at or after the retained audit date.

    Source meaning, version, scope and freshness still need their owning checks
    and review. A newer date alone is never evidence of editorial correctness.
    """
    if not isinstance(value, str):
        return False
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    return parsed.isoformat() == value and parsed >= date.fromisoformat(baseline)
