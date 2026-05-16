# hooks/candidates/

Suspected hook paths that have NOT yet been tested.

Add entries here when you have a reasonable hypothesis about a hook path but have not confirmed it works. Include why you think it exists and how you found it.

## Open hook candidates (needed but not yet found)

These are missing hooks that block important parts of the RE map:

- Player death event — how? (search Ghidra for "OnDeath", "Die", "Kill" in Pal namespace)
- Pal capture event — how? (search for "Capture", "Catch", "PalSphere" in Pal namespace)
- Player level-up event — how? (search for "LevelUp", "GainLevel" in Pal namespace)
- Base camp raid / attack event — how? (search for "Raid", "Attack", "BaseCamp" in Pal namespace)
- Item pickup event — how? (search for "PickUp", "Collect", "AddItem" in Pal namespace)
- Crafting complete event — how? (search for "Craft", "Complete", "Product" in Pal namespace)
- Fast travel event — how? (search for "FastTravel", "Teleport", "Warp" in Pal namespace)

## How to test a candidate

1. Add it to RegisterHook in a test Lua script
2. Trigger the event in-game
3. If the hook fires: move to confirmed/
4. If it does not fire: note why and keep or discard the candidate
