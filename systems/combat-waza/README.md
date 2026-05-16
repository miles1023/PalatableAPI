# systems/combat-waza/

The Pal attack and skill system. "Waza" is the internal term for moves/attacks.

## DataTables

- **DT_WazaDataTable** — individual skill definitions (damage, type, cooldown, etc.)
  Status: PARTIAL — column names NOT YET CONFIRMED. Needs FModel export with current Mappings.usmap.
- **DT_WazaMasterLevel** — maps Pal species + level → skill learned at that level

## Known data

DT_WazaDataTable (confirmed columns):
- WazaID — unique identifier
- WazaType — element type (EPalElementType)
- Power — base damage
- (Other columns unknown until FModel export)

## Open questions

- Full DT_WazaDataTable column list — THIS IS THE TOP RE PRIORITY for DataTables
- Damage calculation formula (how Power + attacker stats + defender stats combine)
- Cooldown and animation timing fields
- Status effect application columns

## Access surfaces

- FModel + Mappings.usmap (requires current Mappings.usmap — do this first)
- PalSchema / PAK mod (modify)

## Pre-migration data

See `findings/pre-migration/datatables/DT_WazaDataTable.yml` (stub only — most fields unknown),
`DT_WazaMasterLevel.yml`
