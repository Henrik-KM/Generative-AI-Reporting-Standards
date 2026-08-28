#!/usr/bin/env python3
"""Validate machine-readable reporting-checklist responses.

This intentionally small validator checks completeness, allowed values, and basic
types. It does not assess the scientific adequacy of a reported method or claim.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "reporting-checklist.schema.json"


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


def validate_record(record: Any, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["top-level value must be an object"]

    top_required = schema["required"]
    top_properties = schema["properties"]
    for field in top_required:
        if field not in record:
            errors.append(f"missing top-level field '{field}'")
    for field in record:
        if field not in top_properties:
            errors.append(f"unknown top-level field '{field}'")

    if record.get("checklist_version") != top_properties["checklist_version"]["const"]:
        errors.append(
            "checklist_version must be "
            f"'{top_properties['checklist_version']['const']}'"
        )

    record_types = set(top_properties["record_type"]["enum"])
    record_type = record.get("record_type")
    if not isinstance(record_type, str):
        errors.append("record_type must be a string")
    elif record_type not in record_types:
        errors.append(f"record_type must be one of {sorted(record_types)}")

    study = record.get("study")
    study_schema = schema["$defs"]["study"]
    if not isinstance(study, dict):
        errors.append("study must be an object")
    else:
        for field in study_schema["required"]:
            if field not in study:
                errors.append(f"study.{field} is required")
        for field, value in study.items():
            if field not in study_schema["properties"]:
                errors.append(f"unknown study field '{field}'")
            elif not nonempty_string(value):
                errors.append(f"study.{field} must be a non-empty string")
        audit_date = study.get("audit_date")
        if nonempty_string(audit_date):
            try:
                date.fromisoformat(audit_date)
            except ValueError:
                errors.append("study.audit_date must use YYYY-MM-DD")

    items = record.get("items")
    if not isinstance(items, list):
        errors.append("items must be an array")
        return errors

    item_schema = schema["$defs"]["item"]
    allowed_ids = set(item_schema["properties"]["id"]["enum"])
    allowed_statuses = set(item_schema["properties"]["status"]["enum"])
    category_by_id = schema["x-category-by-id"]
    required_record_ids = set(schema["x-required-record-ids"])
    seen: set[str] = set()

    for index, item in enumerate(items):
        location = f"items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{location} must be an object")
            continue
        for field in item_schema["required"]:
            if field not in item:
                errors.append(f"{location}.{field} is required")
        for field in item:
            if field not in item_schema["properties"]:
                errors.append(f"unknown field '{location}.{field}'")

        item_id = item.get("id")
        if not isinstance(item_id, str):
            errors.append(f"{location}.id must be a string")
        elif item_id not in allowed_ids:
            errors.append(f"{location}.id must be one of {sorted(allowed_ids)}")
        elif item_id in seen:
            errors.append(f"duplicate checklist item '{item_id}'")
        else:
            seen.add(item_id)
            expected_category = category_by_id[item_id]
            if item.get("category") != expected_category:
                errors.append(
                    f"{location}.category must be '{expected_category}' for {item_id}"
                )
            if item.get("status") == "not_applicable" and expected_category == "required":
                errors.append(f"{location}.status cannot be not_applicable for required item {item_id}")

        status = item.get("status")
        if not isinstance(status, str):
            errors.append(f"{location}.status must be a string")
        elif status not in allowed_statuses:
            errors.append(f"{location}.status must be one of {sorted(allowed_statuses)}")
        if not nonempty_string(item.get("summary")):
            errors.append(f"{location}.summary must be a non-empty string")
        validate_string_list(
            item.get("source_locations"),
            f"{location}.source_locations",
            errors,
            nonempty=True,
        )
        if "artifacts" in item:
            validate_string_list(
                item["artifacts"], f"{location}.artifacts", errors, nonempty=False
            )
        if "notes" in item and not isinstance(item["notes"], str):
            errors.append(f"{location}.notes must be a string")

    missing = [item_id for item_id in schema["x-checklist-order"] if item_id in required_record_ids and item_id not in seen]
    if missing:
        errors.append(f"missing checklist items: {', '.join(missing)}")

    order = [
        item_id
        for item in items
        if isinstance(item, dict)
        for item_id in [item.get("id")]
        if isinstance(item_id, str) and item_id in allowed_ids
    ]
    expected_order = [item_id for item_id in schema["x-checklist-order"] if item_id in seen]
    if order != expected_order:
        errors.append("items must follow the canonical checklist order")

    if "notes" in record and not isinstance(record["notes"], str):
        errors.append("notes must be a string")
    return errors


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
        description="Check reporting-checklist JSON files for completeness and basic types."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="JSON file or directory")
    args = parser.parse_args()

    schema_data, schema_errors = load_json(SCHEMA_PATH)
    if schema_errors or not isinstance(schema_data, dict):
        for error in schema_errors or ["schema must contain a JSON object"]:
            print(f"ERROR {SCHEMA_PATH}: {error}", file=sys.stderr)
        return 2

    files = discover_json_files(args.paths)
    if not files:
        print("ERROR: no JSON files found", file=sys.stderr)
        return 2

    failed = 0
    for path in files:
        record, parse_errors = load_json(path)
        errors = parse_errors or validate_record(record, schema_data)
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
