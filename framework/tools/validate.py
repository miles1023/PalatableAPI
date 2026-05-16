"""
validate.py — startup validator that checks stored byte signatures against live memory.

Run before a session to detect which entity offsets have changed since last verification.
Requires CheatEngine or x64dbg to be running with Palworld attached.

Uses the CheatEngine MCP bridge (already configured in this workspace).
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).parent.parent.parent
KNOWLEDGE = ROOT / "knowledge"


def validate_all(game_version: str | None = None) -> dict:
    """
    Scan all entity YAML files with access: direct entries.
    For each, attempt to verify the stored byte signature against live memory.

    Returns a dict of {entity_name: {field_name: "ok" | "changed" | "not_found" | "skipped"}}
    """
    results = {}
    entity_files = list((KNOWLEDGE / "entities").rglob("*.yml"))
    entity_files = [f for f in entity_files if not f.name.startswith("_")]

    for path in sorted(entity_files):
        yml = yaml.safe_load(path.read_text(encoding="utf-8"))
        name = yml.get("name", path.stem)
        props = yml.get("properties", {})

        direct_props = {k: v for k, v in props.items() if v.get("access") == "direct"}
        if not direct_props:
            continue

        results[name] = {}

        for field_name, field_def in direct_props.items():
            sig = field_def.get("signature")
            if not sig:
                results[name][field_name] = "skipped (no signature)"
                continue

            broken_since = field_def.get("broken_since")
            if broken_since:
                results[name][field_name] = f"skipped (broken since {broken_since})"
                continue

            # Check if this version is in verified_versions
            verified = field_def.get("verified_versions", [])
            if game_version and game_version not in verified:
                results[name][field_name] = f"not verified for version {game_version}"
                continue

            # Attempt signature scan via CheatEngine MCP
            status = _scan_signature(sig)
            results[name][field_name] = status

    return results


def _scan_signature(signature: str) -> str:
    """
    Use CheatEngine MCP to scan for a byte signature in Palworld's process.
    Returns "ok", "changed", or "not_found".
    """
    # CheatEngine MCP is connected via the mcp__cheatengine__ tools.
    # This function is a placeholder — actual MCP calls happen at the Claude session level.
    # In a live session: use mcp__cheatengine__aob_scan_module_unique to scan Palworld-Win64-Shipping.exe
    return "scan_not_run (run from Claude session with CheatEngine MCP)"


def print_report(results: dict):
    print("\n=== Signature Validation Report ===\n")
    all_ok = True
    for entity, fields in results.items():
        for field, status in fields.items():
            icon = "OK" if status == "ok" else "!!"
            if status != "ok":
                all_ok = False
            print(f"  [{icon}] {entity}.{field}: {status}")
    if all_ok:
        print("\nAll direct-access signatures verified.")
    else:
        print("\nSome signatures need re-verification. Run a RE session to update them.")


def main():
    print("Running startup validation against live Palworld process...")
    results = validate_all()
    print_report(results)


if __name__ == "__main__":
    main()
