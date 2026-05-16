"""
Resolver — translates a parsed command dict into an executable action spec.

Walks the inheritance chain for entity properties.
Resolves property aliases via commands.yml.
Handles special values (infinite, max, default).
"""

from pathlib import Path
from functools import lru_cache
import yaml

COMMANDS_YML = Path(__file__).parent.parent.parent / "grammar" / "commands.yml"
KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"


@lru_cache(maxsize=1)
def load_commands() -> dict:
    return yaml.safe_load(COMMANDS_YML.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def load_entity(name: str) -> dict | None:
    for path in (KNOWLEDGE_DIR / "entities").rglob(f"{name}.yml"):
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    return None


@lru_cache(maxsize=None)
def load_datatable(name: str) -> dict | None:
    for path in (KNOWLEDGE_DIR / "datatables").rglob(f"{name}.yml"):
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    return None


def resolve_property(scope: str, property_name: str) -> dict:
    """
    Given a scope (player/pal/pal_species/item/global/etc.) and a
    plain-English property name, return the binding spec.

    Returns a dict with keys:
      backend: "runtime" | "datatables"
      For runtime: entity, field, access_chain, value_type
      For datatables: datatable, column, value_type

    Raises ResolveError if the property or scope is not found.
    """
    commands = load_commands()
    props = commands.get("properties", {})
    work_suits = commands.get("work_suitabilities", {})

    # Normalize property name — check aliases
    canonical = _find_canonical(property_name, props)
    if canonical is None:
        # Check work suitability sub-property ("work mining" -> "work mining")
        if property_name.startswith("work "):
            work_type = property_name[5:].strip()
            return _resolve_work_suitability(work_type, scope, work_suits)
        raise ResolveError(
            f"Unknown property '{property_name}'. Run 'list commands' to see valid properties."
        )

    prop_def = props[canonical]
    scopes = prop_def.get("scopes", {})

    if scope not in scopes:
        valid = ", ".join(scopes.keys())
        raise ResolveError(
            f"Property '{property_name}' does not apply to scope '{scope}'. "
            f"Valid scopes: {valid}"
        )

    binding = scopes[scope]

    if "entity" in binding:
        return {
            "backend": "runtime",
            "entity": binding["entity"],
            "field": binding["field"],
            "access_chain": binding.get("access_chain", []),
            "value_type": binding.get("value_type", "float"),
            "value_field": binding.get("value_field"),  # for FFixedPoint
            "range": binding.get("range"),
            "default": binding.get("default"),
        }
    elif "datatable" in binding:
        return {
            "backend": "datatables",
            "datatable": binding["datatable"],
            "column": binding["column"],
            "value_type": binding.get("value_type", "float"),
            "enum": binding.get("enum"),
            "valid_values": binding.get("valid_values"),
        }
    else:
        status = binding.get("status", "unknown")
        raise ResolveError(
            f"Property '{property_name}' for scope '{scope}' is not yet implemented (status: {status})."
        )


def resolve_value(value, binding: dict) -> object:
    """
    Convert a parsed value (float, str special keyword, or bool) to the
    concrete value to write, accounting for the property's value_type.
    """
    commands = load_commands()
    special_map = commands.get("special_values", {})

    if isinstance(value, str):
        if value in special_map:
            mapped = special_map[value]
            if mapped == "<<read_field_max>>":
                return _SENTINEL_READ_MAX
            if mapped == "<<lookup_default>>":
                return binding.get("default")
            return mapped
        # Enum value — normalize to proper case if needed
        if binding.get("valid_values") and value.lower() not in binding["valid_values"]:
            raise ResolveError(
                f"Invalid value '{value}'. Valid values: {', '.join(binding['valid_values'])}"
            )
        return value

    # Numeric value range check
    if isinstance(value, (int, float)) and binding.get("range"):
        lo, hi = binding["range"]
        if not (lo <= value <= hi):
            raise ResolveError(
                f"Value {value} is out of range. Must be between {lo} and {hi}."
            )

    return value


def _find_canonical(name: str, props: dict) -> str | None:
    name = name.lower().replace("-", "_").replace(" ", "_")
    if name in props:
        return name
    for canonical, defn in props.items():
        aliases = [a.lower().replace("-", "_") for a in defn.get("aliases", [])]
        if name in aliases:
            return canonical
    return None


def _resolve_work_suitability(work_type: str, scope: str, work_suits: dict) -> dict:
    if scope != "pal_species":
        raise ResolveError(
            f"Work suitability can only be set on 'pal-species', not '{scope}'"
        )
    normalized = work_type.lower().replace("-", "_")
    for key, defn in work_suits.items():
        aliases = [a.lower().replace("-", "_") for a in defn.get("aliases", [])]
        if normalized == key or normalized in aliases:
            return {
                "backend": "datatables",
                "datatable": "DT_PalMonsterParameter",
                "column": defn["column"],
                "value_type": "int",
                "range": [0, 4],
            }
    valid = ", ".join(work_suits.keys())
    raise ResolveError(f"Unknown work type '{work_type}'. Valid types: {valid}")


class _ReadMaxSentinel:
    """Sentinel: runtime must read the max field and use that as the value."""
    def __repr__(self): return "<<max>>"

_SENTINEL_READ_MAX = _ReadMaxSentinel()


class ResolveError(Exception):
    pass
