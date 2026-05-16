# FINDING_SCHEMA.md — Canonical Data Model for RE Findings
# This is the contract. Every finding stored in this project must conform to it.
# Last updated: 2026-05-15

---

## Purpose

Every piece of knowledge produced by reverse engineering Palworld must be stored in a
traceable, consistent format. This schema defines that format.

A finding is anything learned about the game's internals: a memory offset, a class
property, a function address, a hook path, a struct layout, an event, a constraint, or
an unknown observation. If it came from a tool session and tells us something about how
Palworld works internally, it is a finding.

---

## Required Fields

Every finding must have all of the following:

```
type:        <see TYPE VALUES below>
name:        <canonical name for this finding>
description: <plain description of what this is or does>
game_system: <folder name from systems/ — which system this belongs to>
surface:     <folder name from surfaces/ — which surface revealed this>
source:
  tool:    <tool name: CheatEngine | x64dbg | Ghidra | UHT | FModel | save-tools | RCON | REST-API | community-research>
  session: <YYYY-MM-DD>
  detail:  <specific file, address, function name, or other locator>
confidence:  <confirmed | inferred | speculated>
status:      <raw | parsed | mapped | reviewed | complete>
```

---

## Optional Fields (include when applicable)

```
aliases:          [list of other names this is known by]
game_version:     <"0.7.1" — version when this was found or last verified>
broken_since:     <version where this stopped working, or null>

# For memory offsets and struct fields:
technical:
  type:           <float | int32 | int64 | bool | FName | FString | FFixedPoint | FVector | TArray | TMap | UObject* | other>
  offset:         <hex offset from object base, e.g. "0x018">
  size:           <byte count>
  signature:      <AOB byte signature for re-resolution after updates>
  addresses:
    "0.7.1":
      client: <hex address or null>
      server: <hex address or null>
  pointer_chain:  [list of derefs from a base pointer to reach this field]
  range:          [min, max]  # if value has a valid range
  default:        <default value if known>
  writable:       <true | false>
  authority:      <client | server | either>  # server = writes from client get overridden
  persistence:    <session | permanent | unknown>
  side_effects:   <describe anything that breaks if you set this naively>

# For UE4SS reflected properties:
technical:
  type:           <UE property type>
  ue_property:    <exact property name in UE reflection>
  component:      <component class name if property lives on a sub-component>
  component_chain: [ordered chain of component names to traverse]

# For functions and hook points:
technical:
  ue_path:        <full UE4SS hook path, e.g. "/Script/Pal.ClassName:FunctionName">
  hook_type:      <pre | post | both>
  authority:      <client | server | either>
  args:           [{name: <name>, type: <type>, position: <0-based index>}]
  returns:        <return type or null>

# For struct layouts:
technical:
  total_size:     <total struct size in bytes>
  fields:         [{offset: <hex>, size: <bytes>, type: <type>, name: <name>, notes: <optional>}]

# Relationships to other findings:
relationships:
  - finding: <name of related finding>
    relation: <"part of" | "references" | "depends on" | "conflicts with" | "same as" | "parent of" | "child of">
    notes:    <optional explanation>

# Open questions about this finding:
open_questions:
  - <question text>
```

---

## TYPE VALUES

| Type | Use for |
|------|---------|
| `memory-offset` | A specific field at a specific byte offset in a struct |
| `ue-property` | A field accessible via UE4SS reflection by name |
| `function` | A callable function (reflected UFunction or binary function) |
| `hook-point` | A RegisterHook or NotifyOnNewObject path |
| `struct` | A complete struct or class layout |
| `event` | Something that fires in the game (may or may not have a hook yet) |
| `system` | A high-level game system entry (links to a systems/ folder) |
| `datatable-column` | A column in a game DataTable |
| `datatable-row` | A specific row in a game DataTable |
| `enum` | An enum type and its values |
| `enum-value` | A single value within an enum |
| `interface` | An external interface (REST endpoint, RCON command, save field) |
| `constraint` | A rule or limit that governs how another finding behaves |
| `unknown` | A finding that does not fit a known type yet |

---

## CONFIDENCE VALUES

| Value | Meaning |
|-------|---------|
| `confirmed` | Verified directly by a tool. CE returned the expected value; the hook fired; FModel showed the column. No ambiguity. |
| `inferred` | Deduced from surrounding evidence. The class name strongly implies the purpose; adjacent confirmed field; community documentation. Could be wrong. |
| `speculated` | Reasonable guess with no direct evidence. Mark clearly. Do not act on speculated findings without upgrading them first. |

---

## STATUS VALUES

| Value | Meaning |
|-------|---------|
| `raw` | Just found, not yet normalized or assigned |
| `parsed` | Normalized to schema format, not yet assigned to system/surface |
| `mapped` | Assigned to game system and surface |
| `reviewed` | Verified for completeness and cross-references |
| `complete` | No open questions; confidence is confirmed; all fields populated |

---

## File Format

Each finding is stored as a Markdown file with YAML front matter.

```markdown
---
type: <value>
name: <value>
game_system: <value>
surface: <value>
confidence: <value>
status: <value>
source:
  tool: <value>
  session: YYYY-MM-DD
  detail: <value>
---

## Description

<plain-language description of what this finding is and why it matters>

## Technical Details

<technical content — offsets, signatures, paths, etc.>

## Open Questions

- <question 1>

## Relationships

- <related finding name> — <relation type>
```

---

## What This Schema Does NOT Contain

The following fields do not belong in the RE finding schema. They belong to the API design phase, which has not started:

- Plain-English command syntax
- Command aliases or verb mappings
- Error codes for user-facing commands
- Backend routing (runtime vs. DataTable)
- Any "what the modder types" framing

If you find yourself wanting to add these fields, stop. They go in `future-api/` when that phase begins.

---

## Example Finding (memory offset)

```markdown
---
type: memory-offset
name: UPalIndividualCharacterParameter.Hp
aliases: [player-hp, pal-hp, current-health]
game_system: player-character
surface: memory-raw
confidence: inferred
status: mapped
game_version: "0.7.1"
source:
  tool: community-research
  session: 2026-05-15
  detail: NightFyre/Palworld-Internal SDK, cross-referenced with UHT dump
---

## Description

The HP field on UPalIndividualCharacterParameter. This is the current hit points for
both players and Pals (both use the same component class).

## Technical Details

- type: FFixedPoint
- component_chain: [CharacterParameterComponent, IndividualParameter]
- writable: true
- authority: server
- side_effects: Setting to 0 triggers death sequence. Setting above MaxHP has unknown behavior.

## Open Questions

- FFixedPoint inner field: is the actual float at .Value or .RawValue? This blocks modification. Confirm via x64dbg breakpoint on HP read.

## Relationships

- UPalIndividualCharacterParameter.MaxHP — related field (maximum HP cap)
- UPalCharacterParameterComponent — parent component that owns this parameter
```
