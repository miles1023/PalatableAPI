"""
PalatableAPI REPL — the interactive plain-English command shell.

Usage:
    python -m framework.host.repl          # interactive shell
    python -m framework.host.repl "give 10 Stone to PlayerName"   # single command
    python -m framework.host.repl --file commands.txt              # batch file
"""

import sys
import readline  # noqa: F401 — enables arrow-key history on Unix/Windows
from pathlib import Path

from .parser import parse, ParseError
from .resolver import resolve_property, resolve_value, ResolveError
from .router import route, route_builtin, RouterError
from .bridge import BridgeError

BANNER = """
PalatableAPI v0.1.0
Type a command or 'help' to see what's available. Ctrl+C or 'exit' to quit.
"""

BUILTIN_VERBS = {"give", "respawn", "teleport", "fly", "sort", "revive", "list", "status"}

HELP_TEXT = """
Available commands (plain English — quotes around names with spaces):

  PLAYER
    set player "Name" health 100          set current health
    set player "Name" max_health 500      set maximum health
    set player "Name" hunger 100          set hunger (0=starving, max=full)
    set player "Name" sanity 100          set sanity (0-100)
    set player "Name" invincible on|off   toggle invincibility
    set player "Name" walkspeed 1200      set movement speed (default 600)
    set player "Name" carryweight infinite set carry weight (infinite = unlimited)
    give 10 "Stone" to "Name"            give items
    respawn player "Name"                 respawn a player
    teleport player "Name" to X Y Z       teleport to coordinates
    fly player "Name" on|off             toggle fly mode
    revive player "Name"                  revive dying player
    sort player "Name" inventory          sort inventory

  PAL (live instance)
    set pal "Name" health 200            set a spawned Pal's health

  PAL SPECIES (affects all Pals of that type)
    set pal-species "Lamball" capture_rate 2.0
    set pal-species "Lamball" base_hp 200
    set pal-species "Lamball" melee_attack 150
    set pal-species "Lamball" defense 80
    set pal-species "Lamball" run_speed 400
    set pal-species "Lamball" mount_speed 600
    set pal-species "Lamball" work mining 4
    set pal-species "Lamball" nocturnal on
    set pal-species "Lamball" ai_behavior ignore

  ITEMS
    set item "Stone" max_stack 9999
    set item "Stone" weight 0.1
    set item "Stone" price 1
    set weapon "Handgun" attack 500
    set weapon "Handgun" magazine_size 30
    set food "Berries" restore_hunger 50
    set food "Berries" restore_hp 20

  BUILDINGS
    set building "WorkBench" hp 99999
    set building "WorkBench" build_cost free

  UTILITIES
    list players                          show all connected players
    list pals                             show all spawned Pals
    list commands                         show all available commands
    status                                show connection status
    help                                  show this message
    exit                                  quit

Special values: infinite, max, min, default, free, on, off
"""


def run_command(text: str) -> str:
    """Parse and execute one command. Returns the result message."""
    text = text.strip()

    if not text or text.startswith("#"):
        return ""

    if text.lower() in ("help", "?", "h"):
        return HELP_TEXT

    if text.lower() in ("exit", "quit", "q"):
        sys.exit(0)

    try:
        parsed = parse(text)
    except ParseError as e:
        return f"Parse error: {e}"

    verb = parsed.get("verb")

    # Built-in verbs go directly to router
    if verb in BUILTIN_VERBS:
        try:
            return route_builtin(verb, parsed)
        except (RouterError, BridgeError) as e:
            return f"Error: {e}"

    # Property-modifying verbs (set, add) go through resolver first
    scope = parsed.get("scope")
    prop = parsed.get("property")
    raw_value = parsed.get("value")

    try:
        binding = resolve_property(scope, prop)
        value = resolve_value(raw_value, binding)
        return route(verb, parsed, binding, value)
    except ResolveError as e:
        return f"Error: {e}"
    except (RouterError, BridgeError) as e:
        return f"Error: {e}"


def run_interactive():
    print(BANNER)

    # Show connection status on launch
    from .bridge import is_connected
    if is_connected():
        print("Status: Connected to Palworld.\n")
    else:
        print("Status: Not connected. Start Palworld with UE4SS to enable runtime commands.\n"
              "        DataTable patch commands will still work offline.\n")

    while True:
        try:
            text = input("pal> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not text:
            continue

        result = run_command(text)
        if result:
            print(result)


def run_file(path: str):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines, 1):
        if not line.strip() or line.strip().startswith("#"):
            continue
        print(f"pal> {line}")
        result = run_command(line)
        if result:
            print(result)


def main():
    args = sys.argv[1:]

    if not args:
        run_interactive()
    elif args[0] == "--file" and len(args) >= 2:
        run_file(args[1])
    else:
        # Single command from CLI
        result = run_command(" ".join(args))
        print(result)


if __name__ == "__main__":
    main()
