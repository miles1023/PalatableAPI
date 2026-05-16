# PalatableAPI Reference

A plain-English command interface for modding Palworld.
Commands work in the interactive shell (`pal>`), as single CLI calls, or in batch script files.

## Quick Start

```
python -m framework.host.repl
```

Then type commands at the `pal>` prompt.

## Command Reference

### Give Items

```
give 10 "Stone" to "PlayerName"
give 1 "HandgunBullet_Blank" to "PlayerName"
```

---

### Player Commands

```
set player "PlayerName" health 100
set player "PlayerName" health max
set player "PlayerName" max_health 1000
set player "PlayerName" hunger infinite
set player "PlayerName" sanity 100
set player "PlayerName" invincible on
set player "PlayerName" invincible off
set player "PlayerName" walkspeed 1200
set player "PlayerName" walkspeed default
set player "PlayerName" carryweight infinite
set player "PlayerName" carryweight 5000

respawn player "PlayerName"
revive player "PlayerName"
teleport player "PlayerName" to 12500 -8000 200
fly player "PlayerName" on
fly player "PlayerName" off
sort player "PlayerName" inventory
```

---

### Pal Commands (live spawned Pal)

```
set pal "LambballName" health max
set pal "LambballName" health 500
set pal "LambballName" hunger infinite
```

---

### Pal Species Commands (affects all Pals of that type)

> These generate DataTable patch files. Deploy them via the output/ folder.

```
set pal-species "Lamball" capture_rate 2.0
set pal-species "Lamball" base_hp 500
set pal-species "Lamball" melee_attack 200
set pal-species "Lamball" defense 150
set pal-species "Lamball" run_speed 600
set pal-species "Lamball" mount_speed 900
set pal-species "Lamball" nocturnal on
set pal-species "Lamball" ai_behavior ignore

set pal-species "Lamball" work mining 4
set pal-species "Lamball" work fire 3
set pal-species "Lamball" work watering 2
```

Work types: `fire`, `watering`, `planting`, `electricity`, `crafting`, `gathering`,
`lumbering`, `mining`, `oil`, `medicine`, `cooling`, `transport`, `farming`

Work levels: `0` (none) through `4` (max)

---

### Item Commands

```
set item "Stone" max_stack 9999
set item "Stone" weight 0.01
set item "Stone" price 1

set weapon "OldBow" attack 999
set weapon "Handgun" magazine_size 100
set weapon "Handgun" attack 500

set food "Berries" restore_hunger 100
set food "Berries" restore_hp 50
```

---

### Building Commands

```
set building "WorkBench" hp 99999
set building "WorkBench" build_cost free
```

---

### Utility Commands

```
list players          show all connected players
list pals             show all spawned Pals in the world
list commands         show all available commands
status                show connection status
help                  show help
exit                  quit the shell
```

---

### Special Values

| Value     | Meaning                              |
|-----------|--------------------------------------|
| `infinite` | Maximum numeric value (99999999)     |
| `max`      | Read the property's own max field    |
| `min`      | 0 or minimum allowed value           |
| `default`  | Restore the game's default value     |
| `free`     | Set a cost to 0                      |
| `on`       | Boolean true                         |
| `off`      | Boolean false                        |

---

### Batch Script Files

Create a `.txt` file with one command per line. Lines starting with `#` are comments.

```
# My server setup script
set player "Admin" carryweight infinite
set player "Admin" invincible on
set pal-species "Lamball" capture_rate 1.5
```

Run it:
```
python -m framework.host.repl --file my_script.txt
```

---

### Runtime vs DataTable Commands

| Type | Commands | Requires game running |
|------|----------|----------------------|
| Runtime | Player health, hunger, speed, invincibility, fly, teleport, give | Yes |
| DataTable | Pal species stats, item properties, building stats | No (generates patch file) |

DataTable patches are written to `output/patches/` and must be deployed to your
PalSchema mod folder to take effect.

---

### Item Name Reference

Use the item's internal name (FName). Common examples:

| Plain Name | Internal ID |
|------------|-------------|
| Stone | `Stone` |
| Iron Ore | `IronOre` |
| Handgun Bullets | `HandgunBullet_Blank` |
| Old Bow | `OldBow` |

> Full item name list: run FModel on `Pal-Windows.pak` and export `DA_StaticItemDataAsset`.

---

### Pal Species Name Reference

Use the plain-English Pal name (e.g. `Lamball`). The API maps it to the internal `EPalTribeID`.

> See `knowledge/enums/enums.yml` for the full EPalTribeID to plain-English name map.
