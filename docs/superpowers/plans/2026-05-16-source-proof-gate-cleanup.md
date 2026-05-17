# Source Proof Gate Cleanup Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the old training-data workflow with a hard proof gate, move helper-only material into the right lane, and clean the survey files so only directly proven facts remain in the main map.

**Architecture:** First fix the startup rules so every future session sees the right behavior before touching project files. Then add the proof and reference lanes (`evidence/proof/` and `references/`), clean the survey files into smaller proven pieces, and finish with command-based validation that checks the gate is really in place.

**Tech Stack:** Markdown documentation, repository structure files, git, PowerShell, `rg`

---

## File Map

**Modify**
- `D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md` — remove training-data seeding and add the helper-only + proof-gate workflow
- `D:\GitProjects\PalatableAPI\CLAUDE.md` — replace training-data policy with the new gate, layered order, and game-system organization rule
- `D:\GitProjects\PalatableAPI\RULES.md` — add promotion gate and layer gate in startup rules
- `D:\GitProjects\PalatableAPI\NEXT_SESSION.md` — reinforce the gate so future sessions do not skip it
- `D:\GitProjects\PalatableAPI\workflow\PIPELINE.md` — insert the proof-record step and explicit blocked-until gates
- `D:\GitProjects\PalatableAPI\schemas\FINDING_SCHEMA.md` — require proof-backed fields for canonical findings
- `D:\GitProjects\PalatableAPI\evidence\sources-2026.md` — make it clearly helper-only guidance, not proof for internal facts
- `D:\GitProjects\PalatableAPI\survey\SURFACES.md` — remove training-data framing and keep only smaller proven pieces
- `D:\GitProjects\PalatableAPI\survey\GAME_SYSTEMS.md` — same cleanup as `SURFACES.md`

**Create**
- `D:\GitProjects\PalatableAPI\references\README.md` — define the read-only helper-material lane
- `D:\GitProjects\PalatableAPI\evidence\proof\README.md` — define the proof-record contract and storage rule
- `D:\GitProjects\PalatableAPI\unknowns\proof-gate-questions.md` — hold still-useful but unproven questions removed from main files

**Move**
- `D:\GitProjects\PalatableAPI\unknowns\UE4SSforCONTEXTonly\` -> `D:\GitProjects\PalatableAPI\references\UE4SSforCONTEXTonly\`

**Verification commands**
- `rg "UNVERIFIED - training data|UNVERIFIED — training data|may be outdated|seeded from AI training data|survey from training data" D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow D:\GitProjects\PalatableAPI\survey D:\GitProjects\PalatableAPI\schemas D:\GitProjects\PalatableAPI\evidence -n`
- `rg "PROMOTION GATE|LAYER GATE|layered enumeration|game system, not by tool" D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow -n`
- `rg "Proof source:|Proof record:|Verified on:" D:\GitProjects\PalatableAPI\survey -n`

---

## Chunk 1: Startup Rules And Proof Lanes

### Task 1: Replace the old source policy in the files future sessions read first

**Files:**
- Modify: `D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md`
- Modify: `D:\GitProjects\PalatableAPI\CLAUDE.md`
- Modify: `D:\GitProjects\PalatableAPI\RULES.md`
- Modify: `D:\GitProjects\PalatableAPI\NEXT_SESSION.md`
- Modify: `D:\GitProjects\PalatableAPI\workflow\PIPELINE.md`

- [ ] **Step 1: Run the policy audit to show the old wording still exists**

Run:
```powershell
rg "UNVERIFIED - training data|UNVERIFIED — training data|may be outdated|seeded from AI training data|survey from training data" D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow -n
```

Expected: matches showing the old source-policy wording that must be removed or rewritten.

- [ ] **Step 2: Rewrite `Project-PreReverseEngineering.md` Phase 0**

Replace the training-data survey instruction with text that says:
- use only current 2026 helper sources
- helper sources only point the search in the right direction
- layered enumeration is required in order
- findings are organized by game system, not by tool
- nothing enters main files until the proof gate is satisfied

- [ ] **Step 3: Rewrite `CLAUDE.md` with the hard gate language**

Add or replace sections so `CLAUDE.md` clearly states:
- training data is not an allowed source
- 2026 sources are helper-only guidance
- reference-only material is not proof
- main files require direct confirmation
- official docs may only prove the public-facing surface itself
- the dropped UE4SS tree is reference-only guidance
- `PROMOTION GATE` blocks promotion until proof is captured
- `LAYER GATE` blocks deeper work until earlier layers are exhausted
- discoveries are filed by game system, not by tool

- [ ] **Step 4: Rewrite `RULES.md` with the same gate and exception language**

Make sure `RULES.md` repeats:
- helper-only 2026 sources
- reference-only is not proof
- public-surface-docs exception
- UE4SS reference-only exception
- promotion gate
- layer gate
- layered enumeration order
- organize by game system, not by tool

- [ ] **Step 5: Rewrite `NEXT_SESSION.md` so it reinforces the gate**

Add a short reminder that:
- helper sources can generate leads
- the next task still cannot promote facts without proof
- layered enumeration stays in force
- public-surface docs may prove the public surface itself
- the dropped UE4SS tree is reference-only guidance only

- [ ] **Step 6: Rewrite `workflow\\PIPELINE.md` with the exact blocked-until sequence**

Make sure the workflow explicitly shows:
- helper lead
- layered enumeration before deeper live tool work
- direct check
- saved proof record
- promotion

and clearly says the flow is blocked until the earlier step is complete.

- [ ] **Step 7: Run the gate-presence check**

Run:
```powershell
rg "PROMOTION GATE|LAYER GATE|layered enumeration|game system, not by tool|helper-only|reference-only|public-facing surface|UE4SS" D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow -n
```

Expected: each startup file and the workflow file show the gate language plus the exception language.

- [ ] **Step 8: Re-run the banned-phrase check for these files**

Run:
```powershell
rg "UNVERIFIED - training data|UNVERIFIED — training data|may be outdated|seeded from AI training data|survey from training data" D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow -n
```

Expected: no matches that preserve the old behavior as an allowed path in the startup-rule files.

- [ ] **Step 9: Commit the startup-rule changes**

Run:
```powershell
git add D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow\PIPELINE.md
git commit -m "docs: add source proof gates to startup rules"
```

Expected: one commit containing only the startup-rule and workflow updates.

### Task 2: Create the proof lane and the reference-only lane

**Files:**
- Create: `D:\GitProjects\PalatableAPI\references\README.md`
- Create: `D:\GitProjects\PalatableAPI\evidence\proof\README.md`
- Move: `D:\GitProjects\PalatableAPI\unknowns\UE4SSforCONTEXTonly\` -> `D:\GitProjects\PalatableAPI\references\UE4SSforCONTEXTonly\`
- Modify: `D:\GitProjects\PalatableAPI\CLAUDE.md`
- Modify: `D:\GitProjects\PalatableAPI\RULES.md`

- [ ] **Step 1: Create the new directories**

Run:
```powershell
New-Item -ItemType Directory -Path D:\GitProjects\PalatableAPI\references -Force
New-Item -ItemType Directory -Path D:\GitProjects\PalatableAPI\evidence\proof -Force
```

Expected: both directories exist.

- [ ] **Step 2: Write `references\README.md`**

Document:
- this area is read-only helper material
- it is not part of startup reading
- it must not become a catch-all bucket
- large helper artifacts go here only when they are not proof
- nothing from `references/` may enter main files without direct proof
- it may help when progress is slow or a session is stuck

- [ ] **Step 3: Write `evidence\proof\README.md`**

Document the exact proof-record contract:
- fact name
- one proof record per proven fact
- path shape: `evidence/proof/YYYY-MM-DD/<fact-slug>.md`
- required fields: fact confirmed, proved by, verified on, game version, raw artifact path, short verification note
- canonical finding proof fields and survey proof notes both point here

- [ ] **Step 4: Move the dropped UE4SS tree into `references\`**

Run:
```powershell
Move-Item D:\GitProjects\PalatableAPI\unknowns\UE4SSforCONTEXTonly D:\GitProjects\PalatableAPI\references\UE4SSforCONTEXTonly
```

Expected: the helper artifact now sits under `references\` and no longer looks like an unresolved project fact.

- [ ] **Step 5: Update the structure summaries that mention top-level folders**

Make sure `CLAUDE.md` and `RULES.md` both describe:
- `references/`
- `evidence/proof/`
- `unknowns/` as open questions
- `backlog/` as planned follow-up work
- `findings/pre-migration/` as legacy material awaiting re-check

- [ ] **Step 6: Verify the new lanes are visible and the old UE4SS location is gone**

Run:
```powershell
Test-Path D:\GitProjects\PalatableAPI\references\UE4SSforCONTEXTonly
Test-Path D:\GitProjects\PalatableAPI\unknowns\UE4SSforCONTEXTonly
rg "references/|evidence/proof/" D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\references\README.md D:\GitProjects\PalatableAPI\evidence\proof\README.md -n
rg "unknowns/|backlog/|findings/pre-migration/" D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md -n
rg "fact name|fact confirmed|proved by|verified on|game version|raw artifact path|short verification note" D:\GitProjects\PalatableAPI\evidence\proof\README.md -n
```

Expected:
- first command returns `True`
- second command returns `False`
- the `rg` command shows the new lane descriptions in the startup files and README files
- the second `rg` command shows the intended meanings for `unknowns/`, `backlog/`, and `findings/pre-migration/`
- the final `rg` command shows the required proof-record fields in `evidence\proof\README.md`

- [ ] **Step 7: Commit the new lanes**

Run:
```powershell
git add D:\GitProjects\PalatableAPI\references D:\GitProjects\PalatableAPI\evidence\proof D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md
git commit -m "docs: add proof and reference lanes"
```

Expected: one commit containing the new directory structure and README guidance.

---

## Chunk 2: Canonical Proof Rules And Survey Cleanup

### Task 3: Make canonical findings require proof-backed fields

**Files:**
- Modify: `D:\GitProjects\PalatableAPI\schemas\FINDING_SCHEMA.md`
- Modify: `D:\GitProjects\PalatableAPI\evidence\sources-2026.md`
- Verify: `D:\GitProjects\PalatableAPI\systems\`
- Verify: `D:\GitProjects\PalatableAPI\surfaces\`
- Verify: `D:\GitProjects\PalatableAPI\memory\`
- Verify: `D:\GitProjects\PalatableAPI\relationships\`
- Verify: `D:\GitProjects\PalatableAPI\hooks\confirmed\`

- [ ] **Step 1: Read the current schema and evidence guidance**

Run:
```powershell
rg "confidence|source|proof|verified|training data" D:\GitProjects\PalatableAPI\schemas\FINDING_SCHEMA.md D:\GitProjects\PalatableAPI\evidence\sources-2026.md -n
```

Expected: current schema and source guidance lines are visible for rewrite.

- [ ] **Step 2: Update `FINDING_SCHEMA.md`**

Make the file clearly say:
- it defines canonical proof-backed findings
- lead-tracking material in `unknowns/`, `backlog/`, `hooks/candidates/`, `references/`, and `findings/pre-migration/` is not a canonical finding
- proof-backed entries require `proof.produced_by`, `proof.location`, `proof.verified_on`, and `proof.fact_confirmed`
- `proof.location` points to a record under `evidence/proof/`
- canonical proof-backed findings in the main lane use `confirmed`

- [ ] **Step 3: Update `sources-2026.md`**

Rewrite the usage notes so the file says:
- these sources help find targets
- they do not prove internal facts by themselves
- official docs can only prove the public-facing surface itself
- this file does not bypass the proof gate

- [ ] **Step 4: Audit other proof-backed main-lane folders for seeded carryover**

Run:
```powershell
rg "UNVERIFIED - training data|UNVERIFIED — training data|may be outdated|seeded from AI training data" D:\GitProjects\PalatableAPI\systems D:\GitProjects\PalatableAPI\surfaces D:\GitProjects\PalatableAPI\memory D:\GitProjects\PalatableAPI\relationships D:\GitProjects\PalatableAPI\hooks\confirmed -n
```

Expected: either no matches, or a short list of files that must be cleaned or downgraded out of the main lane during implementation.

- [ ] **Step 5: If the audit finds seeded main-lane entries, clean or downgrade them immediately**

If Step 4 returns matches:
- remove the unsupported claim from the main-lane file, or
- move the still-useful lead into `unknowns\proof-gate-questions.md`

Do not leave a matched seeded claim in the main truth lane.

- [ ] **Step 6: Verify the schema and evidence wording**

Run:
```powershell
rg "proof\.produced_by|proof\.location|proof\.verified_on|proof\.fact_confirmed|helper map|does not bypass the proof gate" D:\GitProjects\PalatableAPI\schemas\FINDING_SCHEMA.md D:\GitProjects\PalatableAPI\evidence\sources-2026.md -n
```

Expected: the new proof contract and helper-only wording are present.

- [ ] **Step 7: Commit the schema and evidence updates**

Run:
```powershell
git add D:\GitProjects\PalatableAPI\schemas\FINDING_SCHEMA.md D:\GitProjects\PalatableAPI\evidence\sources-2026.md
git commit -m "docs: require proof-backed canonical findings"
```

Expected: one commit containing only the proof contract and helper-source guidance changes.

### Task 4: Clean `survey/SURFACES.md` into smaller proven pieces

**Files:**
- Modify: `D:\GitProjects\PalatableAPI\survey\SURFACES.md`
- Create: `D:\GitProjects\PalatableAPI\unknowns\proof-gate-questions.md`
- Create: `D:\GitProjects\PalatableAPI\evidence\proof\<run-date>\*.md`

- [ ] **Step 1: Run the audit for old survey wording**

Run:
```powershell
rg "training data|UNVERIFIED - training data|UNVERIFIED — training data|may be outdated|seeded from AI training data" D:\GitProjects\PalatableAPI\survey\SURFACES.md -n
```

Expected: matches showing the old framing and labels that must leave the main survey.

- [ ] **Step 2: Rewrite the file introduction**

Remove the training-data-seeded framing and replace it with:
- only directly proven facts stay here
- helper material may guide the search but cannot satisfy the proof gate
- entries are organized by surface, but proof still points back to the real surface or live tool

- [ ] **Step 3: Create `unknowns\\proof-gate-questions.md` with a fixed structure**

Start the file with:
- `# Proof Gate Questions`
- `## Surface questions`
- `## Game system questions`

Use it only for short plain-language follow-up questions removed from the main surveys.

- [ ] **Step 4: Add a `### Fact:` subheading format for retained surface facts**

Use one `### Fact:` subheading per retained proven fact so proof coverage can be counted.

- [ ] **Step 5: Clean SURFACE 1 and SURFACE 2 and create proof records**
- [ ] **Step 5: Clean SURFACE 1 and SURFACE 2**

Work through:
- `SURFACE 1: UE4SS`
- `SURFACE 2: PAK Mod System`

For each heading:
- keep only the proven fact statements
- split multi-fact blocks so one kept fact maps to one proof record
- remove unsupported claims from the main file

- [ ] **Step 6: Create proof record files for the facts kept from SURFACE 1 and SURFACE 2**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 5.

- [ ] **Step 7: Clean SURFACE 3 and SURFACE 4**

Work through:
- `SURFACE 3: PalSchema`
- `SURFACE 4: Raw Memory Access`

For each heading:
- keep only the proven fact statements
- split multi-fact blocks so one kept fact maps to one proof record
- remove unsupported claims from the main file

- [ ] **Step 8: Create proof record files for the facts kept from SURFACE 3 and SURFACE 4**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 7.

- [ ] **Step 9: Clean SURFACE 5 and SURFACE 6**

Work through:
- `SURFACE 5: DLL Injection`
- `SURFACE 6: RCON`

For each heading:
- keep only the proven fact statements
- split multi-fact blocks so one kept fact maps to one proof record
- remove unsupported claims from the main file

- [ ] **Step 10: Create proof record files for the facts kept from SURFACE 5 and SURFACE 6**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 9.

- [ ] **Step 11: Clean SURFACE 7 and SURFACE 8**

Work through:
- `SURFACE 7: REST API`
- `SURFACE 8: Save File Parsing`

For each heading:
- keep only the proven fact statements
- split multi-fact blocks so one kept fact maps to one proof record
- remove unsupported claims from the main file

- [ ] **Step 12: Create proof record files for the facts kept from SURFACE 7 and SURFACE 8**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 11.

- [ ] **Step 13: Clean SURFACE 9 and SURFACE 10**

Work through:
- `SURFACE 9: Config / INI Files`
- `SURFACE 10: UHT Dump via UE4SS`

For each heading:
- keep only the proven fact statements
- split multi-fact blocks so one kept fact maps to one proof record
- remove unsupported claims from the main file

- [ ] **Step 14: Create proof record files for the facts kept from SURFACE 9 and SURFACE 10**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 13.

- [ ] **Step 15: Clean SURFACE 11 and SURFACE 12**

Work through:
- `SURFACE 11: FModel`
- `SURFACE 12: Ghidra / IDA Pro`

For each heading:
- keep only the proven fact statements
- split multi-fact blocks so one kept fact maps to one proof record
- remove unsupported claims from the main file

- [ ] **Step 16: Create proof record files for the facts kept from SURFACE 11 and SURFACE 12**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 15.

- [ ] **Step 17: Clean SURFACE 13, SURFACE 14, and the completeness section**

Work through:
- `SURFACE 13: x64dbg`
- `SURFACE 14: Steam Workshop`
- `Surface Completeness Assessment`

For each heading:
- keep only the proven fact statements
- split multi-fact blocks so one kept fact maps to one proof record
- remove unsupported claims from the main file

- [ ] **Step 18: Create proof record files for the facts kept from SURFACE 13, SURFACE 14, and the completeness section**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 17.

- [ ] **Step 19: Record still-useful open questions**

Append removed but still-useful questions to `D:\GitProjects\PalatableAPI\unknowns\proof-gate-questions.md` as short plain-language items.

- [ ] **Step 20: Add proof notes to retained survey facts**

Use this exact format under each retained fact block:
```text
Proof source: <tool or real surface>
Proof record: evidence/proof/<path>
Verified on: YYYY-MM-DD
```

- [ ] **Step 21: Verify the surface-fact structure, proof-note counts, proof-file existence, and proof-file contents**

Run:
```powershell
rg "^### Fact:" D:\GitProjects\PalatableAPI\survey\SURFACES.md -n
rg "^Proof record:" D:\GitProjects\PalatableAPI\survey\SURFACES.md -n
Select-String -Path D:\GitProjects\PalatableAPI\survey\SURFACES.md -Pattern '^Proof record:\s+(.+)$' | ForEach-Object { $p = $_.Matches[0].Groups[1].Value; if (-not (Test-Path (Join-Path D:\GitProjects\PalatableAPI $p))) { Write-Host "MISSING $p" } }
rg "Fact confirmed:|Proved by:|Verified on:|Game version:|Raw artifact:|Verification note:" D:\GitProjects\PalatableAPI\evidence\proof -n
```

Expected:
- the number of `### Fact:` headings matches the number of `Proof record:` lines
- the PowerShell check prints nothing because every proof record file exists
- the `rg` command shows the required proof-record fields in the created proof files

- [ ] **Step 22: Commit the surface cleanup**

Run:
```powershell
git add D:\GitProjects\PalatableAPI\survey\SURFACES.md D:\GitProjects\PalatableAPI\unknowns\proof-gate-questions.md D:\GitProjects\PalatableAPI\evidence\proof
git commit -m "docs: clean surfaces survey behind proof gate"
```

Expected: one commit containing the cleaned surface survey and the follow-up question file.

### Task 5: Clean `survey/GAME_SYSTEMS.md` into smaller proven pieces

**Files:**
- Modify: `D:\GitProjects\PalatableAPI\survey\GAME_SYSTEMS.md`
- Modify: `D:\GitProjects\PalatableAPI\unknowns\proof-gate-questions.md`
- Create: `D:\GitProjects\PalatableAPI\evidence\proof\<run-date>\*.md`

- [ ] **Step 1: Run the audit for old game-system wording**

Run:
```powershell
rg "training data|UNVERIFIED - training data|UNVERIFIED — training data|may be outdated|seeded from AI training data" D:\GitProjects\PalatableAPI\survey\GAME_SYSTEMS.md -n
```

Expected: matches showing the old framing and labels that must leave the main survey.

- [ ] **Step 2: Rewrite the file introduction**

Replace the seeded-language intro with text that says:
- this file contains only directly proven system facts
- the structure follows game systems, not tools
- unsupported system claims belong in `unknowns/` or `backlog/`, not in the main survey

- [ ] **Step 3: Add a `### Fact:` subheading format for retained system facts**

Use one `### Fact:` subheading per retained proven fact so proof coverage can be counted.

- [ ] **Step 4: Clean SYSTEM 1 through SYSTEM 3 and create proof records**

Work through:
- `SYSTEM 1: Player Character`
- `SYSTEM 2: Player Inventory`
- `SYSTEM 3: Pal Character`

For each heading:
- keep only the fact statements that can be directly proven
- split multi-fact blocks so each retained fact can point to one proof record
- move still-useful but unproven questions out of the main file

- [ ] **Step 5: Create proof record files for the facts kept from SYSTEM 1 through SYSTEM 3**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 4.

- [ ] **Step 6: Clean SYSTEM 4 through SYSTEM 6**

Work through:
- `SYSTEM 4: Pal Storage / Container`
- `SYSTEM 5: Static Pal Data`
- `SYSTEM 6: Item System`

For each heading:
- keep only the fact statements that can be directly proven
- split multi-fact blocks so each retained fact can point to one proof record
- move still-useful but unproven questions out of the main file

- [ ] **Step 7: Create proof record files for the facts kept from SYSTEM 4 through SYSTEM 6**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 6.

- [ ] **Step 8: Clean SYSTEM 7 through SYSTEM 9**

Work through:
- `SYSTEM 7: Building System`
- `SYSTEM 8: Combat / Skill System`
- `SYSTEM 9: Technology Tree / Research System`

For each heading:
- keep only the fact statements that can be directly proven
- split multi-fact blocks so each retained fact can point to one proof record
- move still-useful but unproven questions out of the main file

- [ ] **Step 9: Create proof record files for the facts kept from SYSTEM 7 through SYSTEM 9**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 8.

- [ ] **Step 10: Clean SYSTEM 10 through SYSTEM 12**

Work through:
- `SYSTEM 10: Guild System`
- `SYSTEM 11: Base Camp System`
- `SYSTEM 12: World State / Map`

For each heading:
- keep only the fact statements that can be directly proven
- split multi-fact blocks so each retained fact can point to one proof record
- move still-useful but unproven questions out of the main file

- [ ] **Step 11: Create proof record files for the facts kept from SYSTEM 10 through SYSTEM 12**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 10.

- [ ] **Step 12: Clean SYSTEM 13 through SYSTEM 15**

Work through:
- `SYSTEM 13: Time / Weather System`
- `SYSTEM 14: AI / Behavior System`
- `SYSTEM 15: Server / Multiplayer Session`

For each heading:
- keep only the fact statements that can be directly proven
- split multi-fact blocks so each retained fact can point to one proof record
- move still-useful but unproven questions out of the main file

- [ ] **Step 13: Create proof record files for the facts kept from SYSTEM 13 through SYSTEM 15**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 12.

- [ ] **Step 14: Clean SYSTEM 16 through SYSTEM 18**

Work through:
- `SYSTEM 16: Crafting / Production System`
- `SYSTEM 17: Player Progression`
- `SYSTEM 18: Event System`

For each heading:
- keep only the fact statements that can be directly proven
- split multi-fact blocks so each retained fact can point to one proof record
- move still-useful but unproven questions out of the main file

- [ ] **Step 15: Create proof record files for the facts kept from SYSTEM 16 through SYSTEM 18**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 14.

- [ ] **Step 16: Clean SYSTEM 19 through SYSTEM 21 plus the completeness section**

Work through:
- `SYSTEM 19: Pal Capture System`
- `SYSTEM 20: Pal Breeding System`
- `SYSTEM 21: Audio / Visual`
- `Game Systems Completeness Assessment`

For each heading:
- keep only the fact statements that can be directly proven
- split multi-fact blocks so each retained fact can point to one proof record
- move still-useful but unproven questions out of the main file

- [ ] **Step 17: Create proof record files for the facts kept from SYSTEM 19 through SYSTEM 21 plus the completeness section**

Create one proof record file under the run-date folder in `evidence/proof/` for each retained fact from Step 16.

- [ ] **Step 18: Add or extend proof notes**

Use the same three-line proof-note format as `SURFACES.md`.

- [ ] **Step 19: Append any removed but useful questions**

Add any removed system questions to `D:\GitProjects\PalatableAPI\unknowns\proof-gate-questions.md`.

- [ ] **Step 20: Verify the system-fact structure, proof-note counts, proof-file existence, and proof-file contents**

Run:
```powershell
rg "^### Fact:" D:\GitProjects\PalatableAPI\survey\GAME_SYSTEMS.md -n
rg "^Proof record:" D:\GitProjects\PalatableAPI\survey\GAME_SYSTEMS.md -n
Select-String -Path D:\GitProjects\PalatableAPI\survey\GAME_SYSTEMS.md -Pattern '^Proof record:\s+(.+)$' | ForEach-Object { $p = $_.Matches[0].Groups[1].Value; if (-not (Test-Path (Join-Path D:\GitProjects\PalatableAPI $p))) { Write-Host "MISSING $p" } }
rg "Fact confirmed:|Proved by:|Verified on:|Game version:|Raw artifact:|Verification note:" D:\GitProjects\PalatableAPI\evidence\proof -n
```

Expected:
- the number of `### Fact:` headings matches the number of `Proof record:` lines
- the PowerShell check prints nothing because every proof record file exists
- the `rg` command shows the required proof-record fields in the created proof files

- [ ] **Step 21: Commit the system cleanup**

Run:
```powershell
git add D:\GitProjects\PalatableAPI\survey\GAME_SYSTEMS.md D:\GitProjects\PalatableAPI\unknowns\proof-gate-questions.md D:\GitProjects\PalatableAPI\evidence\proof
git commit -m "docs: clean game systems survey behind proof gate"
```

Expected: one commit containing the cleaned game-system survey and updated follow-up questions.

### Task 6: Run the final repo validation

**Files:**
- Verify: `D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md`
- Verify: `D:\GitProjects\PalatableAPI\CLAUDE.md`
- Verify: `D:\GitProjects\PalatableAPI\RULES.md`
- Verify: `D:\GitProjects\PalatableAPI\NEXT_SESSION.md`
- Verify: `D:\GitProjects\PalatableAPI\workflow\PIPELINE.md`
- Verify: `D:\GitProjects\PalatableAPI\schemas\FINDING_SCHEMA.md`
- Verify: `D:\GitProjects\PalatableAPI\evidence\sources-2026.md`
- Verify: `D:\GitProjects\PalatableAPI\survey\SURFACES.md`
- Verify: `D:\GitProjects\PalatableAPI\survey\GAME_SYSTEMS.md`
- Verify: `D:\GitProjects\PalatableAPI\references\README.md`
- Verify: `D:\GitProjects\PalatableAPI\evidence\proof\README.md`

- [ ] **Step 1: Run the repo-wide banned-phrase sweep**

Run:
```powershell
rg "UNVERIFIED - training data|UNVERIFIED — training data|may be outdated|seeded from AI training data|survey from training data" D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow D:\GitProjects\PalatableAPI\survey D:\GitProjects\PalatableAPI\schemas D:\GitProjects\PalatableAPI\evidence -n
rg "training data" D:\GitProjects\PalatableAPI\Project-PreReverseEngineering.md D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow D:\GitProjects\PalatableAPI\survey D:\GitProjects\PalatableAPI\schemas D:\GitProjects\PalatableAPI\evidence -n
```

Expected:
- the first command finds no banned carryover wording
- the second command only shows allowed prohibition wording such as training data being disallowed

- [ ] **Step 2: Run the gate-presence sweep**

Run:
```powershell
rg "PROMOTION GATE|LAYER GATE|layered enumeration|game system, not by tool" D:\GitProjects\PalatableAPI\CLAUDE.md D:\GitProjects\PalatableAPI\RULES.md D:\GitProjects\PalatableAPI\NEXT_SESSION.md D:\GitProjects\PalatableAPI\workflow -n
```

Expected: the required gate language appears in the startup and workflow files.

- [ ] **Step 3: Run the survey proof-note sweep**

Run:
```powershell
rg "Proof source:|Proof record:|Verified on:" D:\GitProjects\PalatableAPI\survey -n
```

Expected: the cleaned surveys show proof notes for retained facts.

- [ ] **Step 4: Verify schema proof fields still exist**

Run:
```powershell
rg "proof\.produced_by|proof\.location|proof\.verified_on|proof\.fact_confirmed|confirmed" D:\GitProjects\PalatableAPI\schemas\FINDING_SCHEMA.md -n
```

Expected: the schema still shows the required proof fields and the `confirmed` rule for canonical findings.

- [ ] **Step 5: Verify the UE4SS reference tree moved correctly**

Run:
```powershell
Test-Path D:\GitProjects\PalatableAPI\references\UE4SSforCONTEXTonly
Test-Path D:\GitProjects\PalatableAPI\unknowns\UE4SSforCONTEXTonly
```

Expected:
- first command returns `True`
- second command returns `False`

- [ ] **Step 6: Review `git diff --stat` to confirm only intended files changed**

Run:
```powershell
git --no-pager diff --stat HEAD~5..HEAD
```

Expected: only the planned rule files, survey files, proof/reference lane files, schema/evidence files, and follow-up question file changed across the task commits.

- [ ] **Step 7: Confirm there is no extra work left uncommitted**

Run:
```powershell
git status --short
```

Expected: no unexpected files are left unstaged or uncommitted after the task-level commits above.
