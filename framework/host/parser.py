"""
Command parser — converts plain-English input to structured command dicts.
Uses the Lark grammar defined in grammar/palworld.lark.
"""

from pathlib import Path
from lark import Lark, Transformer, Token, UnexpectedInput

GRAMMAR_PATH = Path(__file__).parent.parent.parent / "grammar" / "palworld.lark"

_parser = None

def get_parser() -> Lark:
    global _parser
    if _parser is None:
        grammar = GRAMMAR_PATH.read_text(encoding="utf-8")
        _parser = Lark(grammar, parser="earley", ambiguity="resolve")
    return _parser


class CommandTransformer(Transformer):
    """Converts the Lark parse tree into a flat, usable dict."""

    def start(self, items):
        return items[0]

    # ── Commands ──────────────────────────────────────────────────────────────

    def give_cmd(self, items):
        return {
            "verb": "give",
            "amount": float(items[0]),
            "item": str(items[1]),
            "target_type": "player",
            "target_name": str(items[2]),
        }

    def set_cmd(self, items):
        scope = items[0]
        prop = items[1]
        value = items[2]
        return {"verb": "set", **scope, "property": prop, "value": value}

    def add_cmd(self, items):
        scope = items[0]
        prop = items[1]
        value = items[2]
        return {"verb": "add", **scope, "property": prop, "value": value}

    def remove_cmd(self, items):
        return {
            "verb": "remove",
            "amount": float(items[0]),
            "item": str(items[1]),
            "target_type": "player",
            "target_name": str(items[2]),
        }

    def respawn_cmd(self, items):
        return {"verb": "respawn", "target_type": "player", "target_name": str(items[0])}

    def teleport_cmd(self, items):
        return {
            "verb": "teleport",
            "target_type": "player",
            "target_name": str(items[0]),
            "x": float(items[1]),
            "y": float(items[2]),
            "z": float(items[3]),
        }

    def fly_cmd(self, items):
        return {
            "verb": "fly",
            "target_type": "player",
            "target_name": str(items[0]),
            "value": items[1],
        }

    def sort_cmd(self, items):
        return {"verb": "sort", "target_type": "player", "target_name": str(items[0])}

    def revive_cmd(self, items):
        return {"verb": "revive", "target_type": "player", "target_name": str(items[0])}

    def list_cmd(self, items):
        return {"verb": "list", "listable": str(items[0])}

    def status_cmd(self, items):
        return {"verb": "status"}

    # ── Scopes ────────────────────────────────────────────────────────────────

    def global_scope(self, _):
        return {"scope": "global", "target_name": None}

    def player_scope(self, items):
        return {"scope": "player", "target_name": str(items[0])}

    def pal_scope(self, items):
        return {"scope": "pal", "target_name": str(items[0])}

    def pal_species_scope(self, items):
        return {"scope": "pal_species", "target_name": str(items[0])}

    def item_scope(self, items):
        return {"scope": "item", "target_name": str(items[0])}

    def weapon_scope(self, items):
        return {"scope": "weapon", "target_name": str(items[0])}

    def armor_scope(self, items):
        return {"scope": "armor", "target_name": str(items[0])}

    def food_scope(self, items):
        return {"scope": "food", "target_name": str(items[0])}

    def building_scope(self, items):
        return {"scope": "building", "target_name": str(items[0])}

    # ── Values ────────────────────────────────────────────────────────────────

    def number_value(self, items):
        return float(items[0])

    def special_value(self, items):
        return str(items[0])

    def bool_value(self, items):
        return str(items[0]).lower() in ("on", "true", "yes")

    def string_value(self, items):
        return str(items[0])

    def word_seq(self, items):
        return " ".join(str(i) for i in items)

    def string(self, items):
        # Strip surrounding quotes from ESCAPED_STRING
        s = str(items[0])
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        return s

    def onoff(self, items):
        return str(items[0]).lower() in ("on", "true", "yes")

    def NUMBER(self, tok):
        return float(tok)


def parse(text: str) -> dict:
    """
    Parse a plain-English command string into a structured dict.

    Returns a dict with at minimum {"verb": str, ...}.
    Raises ParseError on invalid input.
    """
    try:
        tree = get_parser().parse(text.strip())
        return CommandTransformer().transform(tree)
    except UnexpectedInput as e:
        raise ParseError(f"Could not understand: '{text}'\n{e}") from e


class ParseError(Exception):
    pass
