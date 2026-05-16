-- PalatableAPI UE4SS Mod
-- Runs inside Palworld via UE4SS injection.
-- Receives commands from the Python host via named pipe and executes them in-game.
-- Sends results back to the Python host.

local PIPE_NAME = "\\\\.\\pipe\\PalatableAPI"
local VERSION = "0.1.0"

-- ─── State ────────────────────────────────────────────────────────────────────

local initialized = false
local player_controller = nil
local player_character = nil

-- ─── Initialization ───────────────────────────────────────────────────────────

-- Hook ClientRestart as the safe init point (fires when player possesses a controller)
RegisterHook("/Script/Engine.PlayerController:ClientRestart", function(context)
    player_controller = context:get()
    player_character = UEHelpers.GetPlayerCharacter()
    initialized = true
    print("[PalatableAPI] Initialized. Player controller acquired.")
    -- TODO: Open named pipe listener after init
end)

-- ─── Utility Helpers ──────────────────────────────────────────────────────────

local function get_player_by_name(name)
    -- FindAllOf returns all instances of a class
    -- TODO: iterate and match display name or player state name
    local controllers = FindAllOf("PalPlayerController")
    if not controllers then return nil, "No players found" end
    for _, ctrl in ipairs(controllers) do
        -- TODO: get player name from PlayerState and compare
        -- Placeholder: return first player if name is "*"
        if name == "*" then return ctrl, nil end
    end
    return nil, string.format("No player named '%s' found", name)
end

local function get_character_param_component(character)
    if not character then return nil, "No character" end
    local comp = character.CharacterParameterComponent
    if not comp or comp:IsNull() then
        return nil, "CharacterParameterComponent not found"
    end
    return comp, nil
end

local function get_individual_param(character)
    local comp, err = get_character_param_component(character)
    if err then return nil, err end
    local param = comp.IndividualParameter
    if not param or param:IsNull() then
        return nil, "IndividualParameter not found"
    end
    return param, nil
end

local function get_inventory_data(controller)
    if not controller then return nil, "No controller" end
    local state = controller.PlayerState
    if not state or state:IsNull() then return nil, "PlayerState not found" end
    local inventory = state:GetInventoryData()
    if not inventory or inventory:IsNull() then return nil, "InventoryData not found" end
    return inventory, nil
end

-- ─── Command Handlers ─────────────────────────────────────────────────────────

local commands = {}

-- set player health
commands["set_player_health"] = function(args)
    -- args: { player_name, value }
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local character = controller.Pawn
    local param, perr = get_individual_param(character)
    if perr then return false, perr end
    local max_hp = param.MaxHP.Value
    local new_hp = math.min(args.value, max_hp)
    param.Hp.Value = new_hp
    return true, string.format("Player %s health set to %.1f", args.player_name, new_hp)
end

-- set player max_health
commands["set_player_max_health"] = function(args)
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local character = controller.Pawn
    local param, perr = get_individual_param(character)
    if perr then return false, perr end
    param.MaxHP.Value = args.value
    return true, string.format("Player %s max health set to %.1f", args.player_name, args.value)
end

-- set player hunger
commands["set_player_hunger"] = function(args)
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local character = controller.Pawn
    local param, perr = get_individual_param(character)
    if perr then return false, perr end
    local max_hunger = param.MaxFullStomach
    local new_hunger = math.min(args.value, max_hunger)
    param.FullStomach = new_hunger
    return true, string.format("Player %s hunger set to %.1f", args.player_name, new_hunger)
end

-- set player sanity
commands["set_player_sanity"] = function(args)
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local character = controller.Pawn
    local param, perr = get_individual_param(character)
    if perr then return false, perr end
    local clamped = math.max(0.0, math.min(100.0, args.value))
    param.SanityValue = clamped
    return true, string.format("Player %s sanity set to %.1f", args.player_name, clamped)
end

-- set player invincible
commands["set_player_invincible"] = function(args)
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local character = controller.Pawn
    local comp, cerr = get_character_param_component(character)
    if cerr then return false, cerr end
    comp.bIsEnableMuteki = args.value
    local state = args.value and "enabled" or "disabled"
    return true, string.format("Player %s invincibility %s", args.player_name, state)
end

-- set player walkspeed
commands["set_player_walkspeed"] = function(args)
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local character = controller.Pawn
    if not character or character:IsNull() then return false, "Character not found" end
    local movement = character.CharacterMovement
    if not movement or movement:IsNull() then return false, "MovementComponent not found" end
    movement.MaxWalkSpeed = args.value
    return true, string.format("Player %s walk speed set to %.1f", args.player_name, args.value)
end

-- set player carryweight
commands["set_player_carryweight"] = function(args)
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local inventory, ierr = get_inventory_data(controller)
    if ierr then return false, ierr end
    inventory.MaxInventoryWeight = args.value
    return true, string.format("Player %s carry weight set to %.1f", args.player_name, args.value)
end

-- give item to player
commands["give_item"] = function(args)
    -- args: { player_name, item_id, amount }
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local inventory, ierr = get_inventory_data(controller)
    if ierr then return false, ierr end
    -- RequestAddItem(StaticId, count, bool)
    local item_name = CreateFName(args.item_id)
    inventory:RequestAddItem(item_name, args.amount, true)
    return true, string.format("Gave %d x %s to %s", args.amount, args.item_id, args.player_name)
end

-- respawn player
commands["respawn_player"] = function(args)
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    local state = controller.PlayerState
    if not state or state:IsNull() then return false, "PlayerState not found" end
    state:RequestRespawn()
    return true, string.format("Respawned %s", args.player_name)
end

-- fly player
commands["fly_player"] = function(args)
    local controller, err = get_player_by_name(args.player_name)
    if err then return false, err end
    if args.value then
        controller:StartFlyToServer()
        return true, string.format("Fly enabled for %s", args.player_name)
    else
        controller:EndFlyToServer()
        return true, string.format("Fly disabled for %s", args.player_name)
    end
end

-- ─── Command Dispatcher ───────────────────────────────────────────────────────

local function dispatch(command_key, args)
    if not initialized then
        return false, "PalatableAPI not initialized — is Palworld running with a player loaded?"
    end
    local handler = commands[command_key]
    if not handler then
        return false, string.format("Unknown command key: %s", command_key)
    end
    local ok, msg = pcall(handler, args)
    if not ok then
        return false, string.format("Error executing %s: %s", command_key, msg)
    end
    return msg  -- msg is {success, message} from handler
end

-- ─── IPC Listener ─────────────────────────────────────────────────────────────
-- TODO: Implement named pipe server to receive JSON commands from Python host
-- Each message format: { "cmd": "set_player_health", "args": { ... } }
-- Response format: { "ok": true/false, "message": "..." }
-- UE4SS does not have built-in socket/pipe support — will use ExecuteInGameThread
-- and polling mechanism or UE4SS HTTP server plugin if available.

print(string.format("[PalatableAPI] v%s loaded. Waiting for player init...", VERSION))
