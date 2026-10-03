"""Issue189: finite Source identity migration; no legal/renderer emulation."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
# Match the CLI entrypoint: the shared site module imports its sibling assets.
sys.path.insert(0, str(ROOT / "scripts"))
from scripts.check_chapter02_contract import chapter02_source_metadata_errors  # noqa: E402

SOURCE_ID = "SRC-IPA-VDP-001"


class SourceEditionTests(unittest.TestCase):
    def setUp(self):
        sources = json.loads((ROOT / "references/sources.json").read_text(encoding="utf-8"))
        self.entries = {s["id"]: s for s in sources["sources"]}

    def test_audited_current_edition_and_retained_law_pass(self):
        self.assertEqual(chapter02_source_metadata_errors(self.entries), [])

    def test_old_edition_or_date_only_update_is_not_accepted(self):
        for checked in ("2026-09-17", "2026-10-03"):
            with self.subTest(checked=checked):
                mutated = copy.deepcopy(self.entries)
                mutated[SOURCE_ID].update(version="2024 edition", checkedAt=checked)
                self.assertTrue(any("version" in e for e in chapter02_source_metadata_errors(mutated)))

    def test_release_day_and_guidance_status_are_exact(self):
        for field, value in (("publishedAt", None), ("publishedAt", "2026-10-03"), ("status", "draft")):
            with self.subTest(field=field, value=value):
                mutated = copy.deepcopy(self.entries)
                mutated[SOURCE_ID][field] = value
                self.assertTrue(any(field in e for e in chapter02_source_metadata_errors(mutated)))

    def test_stale_audit_or_review_baseline_is_rejected(self):
        for field, value in (("checkedAt", "2026-09-17"), ("nextReviewAt", "2026-12-17")):
            with self.subTest(field=field):
                mutated = copy.deepcopy(self.entries)
                mutated[SOURCE_ID][field] = value
                self.assertTrue(any(field in e for e in chapter02_source_metadata_errors(mutated)))

    def test_current_and_historical_provenance_are_required(self):
        for marker in ("2026-10-03 limited edition migration (Issue #189)",
                       "official IPA page and linked 2024 edition guideline were rechecked on 2026-08-05"):
            with self.subTest(marker=marker):
                mutated = copy.deepcopy(self.entries)
                mutated[SOURCE_ID]["notes"] = mutated[SOURCE_ID]["notes"].replace(marker, "", 1)
                self.assertTrue(any("notes missing marker" in e for e in chapter02_source_metadata_errors(mutated)))

    def test_missing_source_and_nontext_notes_fail_closed(self):
        mutated = copy.deepcopy(self.entries)
        del mutated[SOURCE_ID]
        self.assertTrue(any("missing " + SOURCE_ID in e for e in chapter02_source_metadata_errors(mutated)))
        mutated = copy.deepcopy(self.entries)
        mutated[SOURCE_ID]["notes"] = None
        self.assertTrue(any("notes must be a string" in e for e in chapter02_source_metadata_errors(mutated)))

    def test_later_audit_does_not_require_history_rewrite(self):
        mutated = copy.deepcopy(self.entries)
        mutated[SOURCE_ID].update(checkedAt="2026-10-04", nextReviewAt="2027-01-04")
        self.assertEqual(chapter02_source_metadata_errors(mutated), [])


if __name__ == "__main__":
    unittest.main()
