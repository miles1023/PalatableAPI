#!/usr/bin/env python3
"""
validate_findings.py — Schema validation for PalatableAPI finding files.

Scans all Markdown files under findings/, systems/, memory/, and hooks/ that
contain YAML front matter, and checks that every required field defined in
schemas/FINDING_SCHEMA.md is present.

Required fields (per FINDING_SCHEMA.md):
  type, name, description, game_system, surface, source.tool,
  source.session, source.detail, confidence, status

Exit code 0 = all findings valid.
Exit code 1 = one or more findings are missing required fields.
"""

import os
import sys
import yaml

REQUIRED_TOP_LEVEL = ["type", "name", "description", "game_system", "surface", "confidence", "status"]
REQUIRED_SOURCE_KEYS = ["tool", "session", "detail"]

# Directories that may contain canonical finding files with YAML front matter.
SCAN_DIRS = ["findings", "systems", "memory", "hooks"]

# Files under these prefixes are pre-migration originals in old YAML format —
# they do not use the canonical schema front-matter and are excluded from
# schema validation.
EXCLUDE_PREFIXES = [os.path.join("findings", "pre-migration")]


def parse_front_matter(path):
    """
    Extract YAML front matter from a Markdown file.
    Returns a dict on success, None if no front matter is present.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    if not lines or lines[0].strip() != "---":
        return None

    end_index = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = i
            break

    if end_index is None:
        return None

    front_matter = "".join(lines[1:end_index])
    try:
        return yaml.safe_load(front_matter) or {}
    except yaml.YAMLError:
        return None


def validate_finding(path, data):
    """Return a list of error strings for this finding."""
    errors = []

    for field in REQUIRED_TOP_LEVEL:
        if field not in data or data[field] is None or str(data[field]).strip() == "":
            errors.append(f"  Missing required field: '{field}'")

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("  Missing required field: 'source' (must be a mapping)")
    else:
        for key in REQUIRED_SOURCE_KEYS:
            if key not in source or source[key] is None or str(source[key]).strip() == "":
                errors.append(f"  Missing required source sub-field: 'source.{key}'")

    valid_confidence = {"confirmed", "inferred", "speculated"}
    if data.get("confidence") and data["confidence"] not in valid_confidence:
        errors.append(
            f"  Invalid confidence value '{data['confidence']}': "
            f"must be one of {sorted(valid_confidence)}"
        )

    valid_status = {"raw", "parsed", "mapped", "reviewed", "complete"}
    if data.get("status") and data["status"] not in valid_status:
        errors.append(
            f"  Invalid status value '{data['status']}': "
            f"must be one of {sorted(valid_status)}"
        )

    return errors


def should_exclude(path):
    normalized = os.path.normpath(path)
    for prefix in EXCLUDE_PREFIXES:
        if normalized.startswith(os.path.normpath(prefix)):
            return True
    return False


def main():
    failures = 0
    checked = 0

    for scan_dir in SCAN_DIRS:
        if not os.path.isdir(scan_dir):
            continue
        for dirpath, _dirnames, filenames in os.walk(scan_dir):
            for filename in filenames:
                if not filename.endswith(".md"):
                    continue
                filepath = os.path.join(dirpath, filename)
                if should_exclude(filepath):
                    continue

                data = parse_front_matter(filepath)
                if data is None:
                    # No YAML front matter — not a canonical finding file, skip.
                    continue

                checked += 1
                errors = validate_finding(filepath, data)
                if errors:
                    failures += 1
                    print(f"FAIL: {filepath}")
                    for err in errors:
                        print(err)

    if checked == 0:
        print("No canonical finding files found to validate.")
    else:
        print(f"\nValidated {checked} finding file(s). Failures: {failures}.")

    sys.exit(1 if failures > 0 else 0)


if __name__ == "__main__":
    main()
