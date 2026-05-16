# hooks/confirmed/

Hook paths that have been tested and are working in the current game version.

## Existing confirmed hooks (from pre-migration/hooks.yml)

These need to be formalized into canonical finding files, but are listed here for quick reference:

- `/Script/Engine.PlayerController:ClientRestart` — player possession, client-side init
- `/Script/Engine.PlayerController:ServerAcknowledgePossession` — player possession, server-side init
- `/Script/Pal.PalGameStateInGame:BroadcastChatMessage` — chat message broadcast
- `/Script/Pal.PalMapObjectConcreteModelBase:OnTriggerInteract` — world object interaction
- `/Script/Pal.PalMapObject:OnCloseParameter` — world object UI close
- `/Script/Pal.PalPartnerSkillParameterComponent:GetActiveSkillMainValueByRank` — partner skill value read
- Blueprint: `WBP_PalPlayerInventoryScrollList_C:Construct` — inventory UI open
- Blueprint: `WBP_ItemChest_C:Destruct` — chest UI close
- Blueprint: `BP_OtomoPalHolderComponent_C:ActivateOtomo` — companion Pal switch
- NotifyOnNewObject: `/Script/Pal.PalBaseCampModel` — base camp created
- NotifyOnNewObject: `BP_OtomoPalHolderComponent_C` — Otomo holder created
- StaticFindObject: `/Script/Pal.Default__PalUtility`
- StaticFindObject: `/Script/Pal.Default__PalMasterDataTablesUtility`

All confirmed for game version 0.7.1.
