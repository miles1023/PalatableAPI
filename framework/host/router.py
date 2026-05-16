"""
Router — sends resolved commands to the correct execution backend.

Backend 1: runtime  — sends to the UE4SS Lua mod via named pipe (bridge.py)
Backend 2: datatables — generates a PalSchema-compatible JSON patch file
"""

from pathlib import Path
from typing import Any
import json

from . import bridge
from .resolver import _SENTINEL_READ_MAX, ResolveError


OUTPUT_DIR = Path(__file__).parent.parent.parent / "output" / "patches"


def route(verb: str, parsed: dict, binding: dict, value: Any) -> str:
    """
    Execute a resolved command. Returns a plain-English result message.

    parsed  — the full parsed command dict from parser.py
    binding — the resolved property binding from resolver.py
    value   — the resolved concrete value from resolver.resolve_value()
    """
    backend = binding["backend"]

    if backend == "runtime":
        return _route_runtime(verb, parsed, binding, value)
    elif backend == "datatables":
        return _route_datatables(verb, parsed, binding, value)
    else:
        raise RouterError(f"Unknown backend: {backend}")


def route_builtin(verb: str, parsed: dict) -> str:
    """Handle built-in verbs that don't go through the property resolver."""
    if verb == "give":
        return _route_give(parsed)
    if verb == "respawn":
        return _route_respawn(parsed)
    if verb == "teleport":
        return _route_teleport(parsed)
    if verb == "fly":
        return _route_fly(parsed)
    if verb == "sort":
        return _route_sort(parsed)
    if verb == "revive":
        return _route_revive(parsed)
    if verb == "list":
        return _route_list(parsed)
    if verb == "status":
        return _route_status()
    raise RouterError(f"No built-in handler for verb '{verb}'")


# ── Runtime Backend ───────────────────────────────────────────────────────────

def _route_runtime(verb: str, parsed: dict, binding: dict, value: Any) -> str:
    scope = parsed.get("scope")
    target = parsed.get("target_name")
    field = binding["field"]
    entity = binding["entity"]
    access_chain = binding.get("access_chain", [])
    value_field = binding.get("value_field")  # for FFixedPoint

    if value is _SENTINEL_READ_MAX:
        raise RouterError("'max' value requires a runtime read — not yet implemented for this property")

    cmd_key = f"{verb}_{scope}_{field.lower()}"

    payload = {
        "cmd": cmd_key,
        "args": {
            f"{scope}_name": target,
            "value": value,
            "entity": entity,
            "access_chain": access_chain,
            "value_field": value_field,
        }
    }

    result = bridge.send(payload)

    if result.get("ok"):
        return result.get("message", "Done.")
    else:
        raise RouterError(result.get("message", "Unknown runtime error"))


# ── DataTable Backend ─────────────────────────────────────────────────────────

def _route_datatables(verb: str, parsed: dict, binding: dict, value: Any) -> str:
    datatable = binding["datatable"]
    column = binding["column"]
    target = parsed.get("target_name")
    value_type = binding.get("value_type", "float")

    # Resolve value type
    if value_type == "bool":
        typed_value = bool(value)
    elif value_type in ("int", "int32"):
        typed_value = int(value)
    elif value_type == "float":
        typed_value = float(value)
    else:
        typed_value = value  # FName, string — leave as-is

    # Resolve the row key (plain-English name -> internal ID)
    row_key = _resolve_row_key(datatable, target)

    # Generate PalSchema raw/ patch
    patch = {
        row_key: {
            column: typed_value
        }
    }

    # Write to output/patches/<datatable>.json
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    patch_path = OUTPUT_DIR / f"{datatable}.json"

    # Merge with existing patch if present
    existing = {}
    if patch_path.exists():
        existing = json.loads(patch_path.read_text(encoding="utf-8"))

    existing.setdefault(row_key, {}).update(patch[row_key])
    patch_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    return (
        f"Patch written: {datatable} / {row_key} / {column} = {typed_value}\n"
        f"File: {patch_path}\n"
        f"Deploy with: copy output\\patches\\{datatable}.json "
        f"<PalworldInstall>\\Pal\\Content\\Paks\\~mods\\PalatableAPI\\raw\\"
    )


def _resolve_row_key(datatable: str, plain_name: str) -> str:
    """Convert plain-English name to internal DataTable row key."""
    # TODO: load name maps from knowledge/enums/enums.yml and datatable files
    # For now, return the name as-is and let the user supply internal IDs
    return plain_name


# ── Built-in Command Routes ───────────────────────────────────────────────────

def _route_give(parsed: dict) -> str:
    payload = {
        "cmd": "give_item",
        "args": {
            "player_name": parsed["target_name"],
            "item_id": parsed["item"],  # TODO: resolve to internal FName
            "amount": int(parsed["amount"]),
        }
    }
    result = bridge.send(payload)
    if result.get("ok"):
        return result.get("message", "Done.")
    raise RouterError(result.get("message", "Give failed"))


def _route_respawn(parsed: dict) -> str:
    payload = {"cmd": "respawn_player", "args": {"player_name": parsed["target_name"]}}
    result = bridge.send(payload)
    if result.get("ok"):
        return result.get("message", "Done.")
    raise RouterError(result.get("message", "Respawn failed"))


def _route_teleport(parsed: dict) -> str:
    payload = {
        "cmd": "teleport_player",
        "args": {
            "player_name": parsed["target_name"],
            "x": parsed["x"], "y": parsed["y"], "z": parsed["z"],
        }
    }
    result = bridge.send(payload)
    if result.get("ok"):
        return result.get("message", "Done.")
    raise RouterError(result.get("message", "Teleport failed"))


def _route_fly(parsed: dict) -> str:
    payload = {
        "cmd": "fly_player",
        "args": {"player_name": parsed["target_name"], "value": parsed["value"]}
    }
    result = bridge.send(payload)
    if result.get("ok"):
        return result.get("message", "Done.")
    raise RouterError(result.get("message", "Fly failed"))


def _route_sort(parsed: dict) -> str:
    payload = {"cmd": "sort_inventory", "args": {"player_name": parsed["target_name"]}}
    result = bridge.send(payload)
    if result.get("ok"):
        return result.get("message", "Done.")
    raise RouterError(result.get("message", "Sort failed"))


def _route_revive(parsed: dict) -> str:
    payload = {"cmd": "revive_player", "args": {"player_name": parsed["target_name"]}}
    result = bridge.send(payload)
    if result.get("ok"):
        return result.get("message", "Done.")
    raise RouterError(result.get("message", "Revive failed"))


def _route_list(parsed: dict) -> str:
    listable = parsed.get("listable", "")
    payload = {"cmd": "list", "args": {"listable": listable}}
    result = bridge.send(payload)
    if result.get("ok"):
        items = result.get("items", [])
        return "\n".join(items) if items else f"No {listable} found."
    raise RouterError(result.get("message", "List failed"))


def _route_status() -> str:
    if bridge.is_connected():
        return "Connected to Palworld. UE4SS mod active."
    return "Not connected. Start Palworld with UE4SS and the PalatableAPI mod loaded."


class RouterError(Exception):
    pass
