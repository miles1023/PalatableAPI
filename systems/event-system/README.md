# systems/event-system/

All observable game events — places where external code can hook in and respond.

## Confirmed hook paths (from hooks.yml)

### Engine-level (use as mod init points)
- `/Script/Engine.PlayerController:ClientRestart` — player possession, client-side init
- `/Script/Engine.PlayerController:ServerAcknowledgePossession` — player possession, server-side init

### Game events
- `/Script/Pal.PalGameStateInGame:BroadcastChatMessage` — any chat message broadcast
- `/Script/Pal.PalMapObjectConcreteModelBase:OnTriggerInteract` — player interacts with world object
- `/Script/Pal.PalMapObject:OnCloseParameter` — world object UI closed
- `/Script/Pal.PalPartnerSkillParameterComponent:GetActiveSkillMainValueByRank` — partner skill value read

### Blueprint events
- `WBP_PalPlayerInventoryScrollList_C:Construct` — inventory UI opened
- `WBP_ItemChest_C:Destruct` — chest UI closed
- `BP_OtomoPalHolderComponent_C:ActivateOtomo` — companion Pal activated/switched

### NotifyOnNewObject (fires when instance created)
- `/Script/Pal.PalBaseCampModel` — base camp created or loaded
- `/Game/Pal/Blueprint/Component/OtomoHolder/BP_OtomoPalHolderComponent_C` — Otomo holder created

## MISSING hook paths (open TODOs — high priority)

- Player death event
- Pal capture event
- Player level-up event
- Base camp raid / attack event
- Item pickup event
- Crafting complete event
- Fast travel event

## Access surface

All hooks via UE4SS RegisterHook and NotifyOnNewObject.

## Pre-migration data

See `findings/pre-migration/hooks.yml`
