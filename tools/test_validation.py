"""Focused checks for applicability, legacy compatibility and explicit missing evidence."""

from copy import deepcopy
import json
import unittest

from validate import ROOT, SCHEMA_PATH, validate_record


class RecordSemantics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8-sig"))
        cls.author = json.loads((ROOT / "examples/brorsson-2026-author-record.json").read_text(encoding="utf-8-sig"))
        cls.legacy = json.loads((ROOT / "examples/hessmann-2025.json").read_text(encoding="utf-8-sig"))

    def test_current_and_legacy_sources_validate(self):
        self.assertEqual(validate_record(self.author, self.schema), [])
        self.assertEqual(validate_record(self.legacy, self.schema), [])

    def test_new_core_inapplicability_requires_a_reason(self):
        record = deepcopy(self.author)
        record["items"][1]["status"] = "not_applicable"
        self.assertTrue(any("applicability_reason" in e for e in validate_record(record, self.schema)))
        record["items"][1]["applicability_reason"] = "No data partition or model-selection operation forms part of the declared workflow."
        self.assertEqual(validate_record(record, self.schema), [])

    def test_legacy_core_inapplicability_is_not_reinterpreted(self):
        record = deepcopy(self.legacy)
        record["items"][1]["status"] = "not_applicable"
        self.assertTrue(any("cannot be not_applicable" in e for e in validate_record(record, self.schema)))

    def test_unavailable_detail_cannot_be_converted_to_zero(self):
        record = deepcopy(self.author)
        record["items"][4]["details"]["cumulative_attempts_and_unique_candidates"]["value"] = 0
        self.assertTrue(any("must be null" in e for e in validate_record(record, self.schema)))

    def test_reported_detail_requires_an_evidence_location(self):
        record = deepcopy(self.author)
        record["items"][2]["details"]["architecture"].pop("source_locations")
        self.assertTrue(any("source_locations" in e for e in validate_record(record, self.schema)))

    def test_not_performed_is_distinct_from_an_evidence_gap(self):
        record = deepcopy(self.author)
        entry = record["items"][7]["details"]["new_prospective_synthesis"]
        self.assertEqual(entry["status"], "not_performed")
        entry.pop("rationale")
        self.assertTrue(any("rationale" in e for e in validate_record(record, self.schema)))

    def test_author_response_requires_more_than_a_state(self):
        record = deepcopy(self.author)
        record["items"][0].pop("details")
        self.assertTrue(any("operational author response" in e for e in validate_record(record, self.schema)))

    def test_schema_uses_the_same_missing_value_semantics(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("Optional independent JSON Schema engine is unavailable")
        Draft202012Validator.check_schema(self.schema)
        engine = Draft202012Validator(self.schema)
        self.assertEqual(list(engine.iter_errors(self.author)), [])
        self.assertEqual(list(engine.iter_errors(self.legacy)), [])
        record = deepcopy(self.author)
        record["items"][4]["details"]["cumulative_attempts_and_unique_candidates"]["value"] = 0
        self.assertTrue(list(engine.iter_errors(record)))
        record = deepcopy(self.legacy)
        record["items"][1]["status"] = "not_applicable"
        self.assertTrue(list(engine.iter_errors(record)))


if __name__ == "__main__":
    unittest.main()
