#!/usr/bin/env python3
"""Validate machine-readable records under the reporting protocol.

This intentionally small validator checks completeness, allowed values, and basic
types. It does not assess the scientific adequacy of a reported method or claim.
Records with checklist_version 0.2.0 are checked with the archived validator in
legacy/v0.2.0.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "reporting-checklist.schema.json"
LEGACY_DIR = ROOT / "legacy" / "v0.2.0"


def load_json(path: Path) -> tuple[Any | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")), []
    except OSError as exc:
        return None, [f"could not read file: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_string_list(value: Any, location: str, errors: list[str], *, nonempty: bool) -> None:
    if not isinstance(value, list):
        errors.append(f"{location} must be an array")
        return
    if nonempty and not value:
        errors.append(f"{location} must contain at least one entry")
    for index, entry in enumerate(value):
        if not nonempty_string(entry):
            errors.append(f"{location}[{index}] must be a non-empty string")


def validate_study(study: Any, schema: dict[str, Any], errors: list[str]) -> None:
    study_schema = schema["$defs"]["study"]
    if not isinstance(study, dict):
        errors.append("study must be an object")
        return
    for field in study_schema["required"]:
        if field not in study:
            errors.append(f"study.{field} is required")
    for field, value in study.items():
        if field not in study_schema["properties"]:
            errors.append(f"unknown study field '{field}'")
        elif not nonempty_string(value):
            errors.append(f"study.{field} must be a non-empty string")
    record_date = study.get("record_date")
    if nonempty_string(record_date):
        try:
            date.fromisoformat(record_date)
        except ValueError:
            errors.append("study.record_date must use YYYY-MM-DD")


def validate_record_item(item: dict[str, Any], location: str, record_type: str,
                         schema: dict[str, Any], errors: list[str]) -> None:
    item_schema = schema["$defs"]["record_item"]
    for field in item_schema["required"]:
        if field not in item:
            errors.append(f"{location}.{field} is required")
    for field in item:
        if field not in item_schema["properties"]:
            errors.append(f"unknown field '{location}.{field}'")
    answer = item.get("answer")
    answers = set(item_schema["properties"]["answer"]["enum"])
    if answer not in answers:
        errors.append(f"{location}.answer must be one of {sorted(answers)}")
    if record_type == "author_record":
        if answer == "not_stated":
            errors.append(f"{location}.answer 'not_stated' is only permitted in publication records")
        if "not_stated" in item:
            errors.append(f"{location}.not_stated is only permitted in publication records")
    if not nonempty_string(item.get("entry")):
        errors.append(f"{location}.entry must be a non-empty string")
    if "not_stated" in item:
        validate_string_list(item["not_stated"], f"{location}.not_stated", errors, nonempty=True)
    # A not-applicable answer needs a reason in the entry, but not necessarily a source.
    validate_string_list(
        item.get("source_locations"),
        f"{location}.source_locations",
        errors,
        nonempty=answer not in ("not_applicable", "not_stated"),
    )


def validate_audit_item(item: dict[str, Any], location: str,
                        schema: dict[str, Any], errors: list[str]) -> None:
    item_schema = schema["$defs"]["audit_item"]
    for field in item_schema["required"]:
        if field not in item:
            errors.append(f"{location}.{field} is required")
    for field in item:
        if field not in item_schema["properties"]:
            errors.append(f"unknown field '{location}.{field}'")
    statuses = set(item_schema["properties"]["status"]["enum"])
    if item.get("status") not in statuses:
        errors.append(f"{location}.status must be one of {sorted(statuses)}")
    if not nonempty_string(item.get("summary")):
        errors.append(f"{location}.summary must be a non-empty string")
    validate_string_list(item.get("source_locations"), f"{location}.source_locations", errors, nonempty=True)


def validate_ledger(ledger: Any, schema: dict[str, Any], errors: list[str]) -> None:
    row_schema = schema["$defs"]["ledger_row"]
    if not isinstance(ledger, list):
        errors.append("stage_ledger must be an array")
        return
    for index, row in enumerate(ledger):
        location = f"stage_ledger[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{location} must be an object")
            continue
        for field in row_schema["required"]:
            if field not in row:
                errors.append(f"{location}.{field} is required")
        for field, value in row.items():
            if field not in row_schema["properties"]:
                errors.append(f"unknown field '{location}.{field}'")
            elif field in ("n_in", "n_out", "evaluator_calls"):
                if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                    errors.append(f"{location}.{field} must be a non-negative integer or null")
            elif field in ("stage", "rule") and not nonempty_string(value):
                errors.append(f"{location}.{field} must be a non-empty string")


def validate_record(record: Any, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["top-level value must be an object"]

    for field in schema["required"]:
        if field not in record:
            errors.append(f"missing top-level field '{field}'")
    for field in record:
        if field not in schema["properties"]:
            errors.append(f"unknown top-level field '{field}'")

    record_types = set(schema["properties"]["record_type"]["enum"])
    record_type = record.get("record_type")
    if record_type not in record_types:
        errors.append(f"record_type must be one of {sorted(record_types)}")
        return errors

    validate_study(record.get("study"), schema, errors)

    items = record.get("items")
    if not isinstance(items, list):
        errors.append("items must be an array")
        return errors

    allowed_ids = set(schema["$defs"]["item_id"]["enum"])
    seen: list[str] = []
    for index, item in enumerate(items):
        location = f"items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{location} must be an object")
            continue
        item_id = item.get("id")
        if item_id not in allowed_ids:
            errors.append(f"{location}.id must be one of {sorted(allowed_ids)}")
            continue
        if item_id in seen:
            errors.append(f"duplicate item '{item_id}'")
            continue
        seen.append(item_id)
        if record_type == "retrospective_audit":
            validate_audit_item(item, location, schema, errors)
        else:
            validate_record_item(item, location, record_type, schema, errors)

    required = schema["x-required-ids-by-record-type"][record_type]
    missing = [item_id for item_id in required if item_id not in seen]
    if missing:
        errors.append(f"missing items: {', '.join(missing)}")
    expected_order = [item_id for item_id in schema["x-checklist-order"] if item_id in seen]
    if seen != expected_order:
        errors.append("items must follow the order of the eight steps")

    if "stage_ledger" in record:
        validate_ledger(record["stage_ledger"], schema, errors)
    if "notes" in record and not isinstance(record["notes"], str):
        errors.append("notes must be a string")
    return errors


def legacy_validator():
    """Load the archived version 0.2.0 validator and its schema."""
    spec = importlib.util.spec_from_file_location("legacy_validate", LEGACY_DIR / "tools" / "validate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    schema, errors = load_json(LEGACY_DIR / "schema" / "reporting-checklist.schema.json")
    return module, schema, errors


def discover_json_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.glob("*.json")))
        else:
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check reporting-protocol JSON records for completeness and basic types."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="JSON file or directory")
    args = parser.parse_args()

    schema, schema_errors = load_json(SCHEMA_PATH)
    if schema_errors or not isinstance(schema, dict):
        for error in schema_errors or ["schema must contain a JSON object"]:
            print(f"ERROR {SCHEMA_PATH}: {error}", file=sys.stderr)
        return 2

    files = discover_json_files(args.paths)
    if not files:
        print("ERROR: no JSON files found", file=sys.stderr)
        return 2

    failed = 0
    for path in files:
        record, errors = load_json(path)
        if not errors:
            version = record.get("checklist_version") if isinstance(record, dict) else None
            if version == schema["properties"]["checklist_version"]["const"]:
                errors = validate_record(record, schema)
            elif version == "0.2.0":
                module, legacy_schema, legacy_errors = legacy_validator()
                errors = legacy_errors or module.validate_record(record, legacy_schema)
            else:
                errors = [f"unsupported checklist_version {version!r}"]
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {path}")

    if failed:
        print(f"\n{failed} of {len(files)} file(s) failed validation.")
        return 1
    print(f"\nValidated {len(files)} file(s); no structural errors found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
