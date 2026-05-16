 ## What this project is
 
 We are reverse engineering Palworld to produce a complete, accurate map of its
 internal systems — memory, functions, entities, events, hooks, server interfaces,
 and any other surface that can be observed or controlled externally.
 
 That map will be used later, in a separate phase, to design a plain English API.
 That API phase does not exist yet. Do not think about it. Do not shape anything
 around it. Your only job is to build a system that captures everything about how
 the game works internally, organized so well that nothing is ever lost or missed.
 
 I am non-technical. Work methodically and produce durable files, not chat explanations.
 Work in sweeps, not hops. Do not skip ahead.
 
 ---
 
 ## Phase 0: Ecosystem survey (do this before touching folders or schemas)
 
 Survey what is already publicly known about Palworld modding from your training data.
 The goal is to identify every modding SURFACE that has been used by existing mods,
 so our capture system does not miss any of them.
 
 Look for:
 - Mod frameworks and tools already used (UE4SS, PAK mods, blueprint mods, etc.)
 - What game systems existing mods interact with
 - What data is readable vs writable vs event-driven
 - Any scripting or RCON interfaces
 - Any memory structures or offsets already documented by the community
 - Save file structure if relevant
 - Dedicated server interfaces
 - Any other external access points the community has found
 
 From this survey, produce two seed files:
   1. SURFACES.md — every modding surface found, what it exposes, how it is accessed
   2. GAME_SYSTEMS.md — every internal game system found (entities, stats, inventory,
      world state, AI, server, save data, etc.)
 
 Mark each entry with its source and confidence level (known / inferred / unknown).
 
 ## Phase 0 completion gate — REQUIRED before proceeding
 
 Before creating any folders or schemas, present the complete surface list to the user.
 
 Format it clearly:
 - Every modding surface found
 - What it exposes and how it is accessed
 - What game systems it touches
 - Your confidence that the list is complete
 - Any surfaces you are uncertain about or could not verify
 
 Then explicitly ask:
 
   "Does this surface list look complete to you? Are there any surfaces,
    tools, or interfaces you know exist that are not on this list?
    I will not build the scaffolding until you confirm this list is complete."
 
 Do not proceed to Phase 1 until the user confirms the surface list is complete.
 If the user adds surfaces, update the seed files and re-present the list.
 Repeat until the user confirms completeness.
 
 This gate exists because a missed surface means re-doing all reverse engineering work.
 It is worth taking extra time here.
 
 ---
 
 ## Phase 1: Audit current project state
 
 Inspect what already exists in the project.
 Summarize it briefly. Identify what to keep, discard, or reorganize.
 Establish a clean base to build on.
 
 ---
 
 ## Phase 2: Create the full folder and file scaffolding
 
 Create every folder and every placeholder file needed.
 Structure it around the surfaces and game systems identified in Phase 0.
 Every folder must have a README.md explaining what goes in it and why.
 
 Required areas (design the exact names yourself based on what makes sense):
 
 - Ecosystem survey outputs (from Phase 0)
 - Raw reverse engineering tool output intake
 - Parsed and normalized findings
 - Game system registry (one area per major system found in Phase 0)
 - Surface registry (one area per modding surface found in Phase 0)
 - Cross-system relationships and dependencies
 - Memory structures and offsets
 - Functions, hooks, and events
 - Unknowns and unresolved findings
 - Confidence and evidence tracking
 - Session handoff notes
 - Future API workspace (empty, no structure yet — just a placeholder folder)
 - Schemas and data model definitions
 - Ingestion workflow definitions
 - Backlog and triage area
 
 The future API workspace must remain completely empty. No structure, no assumptions.
 It exists only so there is a place for it later.
 
 ---
 
 ## Phase 3: Define the canonical data model
 
 Design a schema for storing reverse engineering discoveries.
 Every discovery must be traceable: what was found, where, how confident, from what source.
 
 Each finding should be able to record:
 - Type (memory offset / function / class / struct / event / hook / system / entity /
   constraint / interface / unknown)
 - Name and aliases
 - Description of what it does or represents
 - Technical detail (offset, signature, syntax, range, type, etc.)
 - Which game system it belongs to
 - Which modding surface it was found through
 - Source (tool name, session date, file, address)
 - Confidence level (confirmed / inferred / speculated)
 - Relationships to other findings
 - Status (raw / parsed / mapped / reviewed / complete)
 
 Save this schema as a file. It is the contract everything else follows.
 Do not add any API-layer fields. Those come later.
 
 ---
 
 ## Phase 4: Define the ingestion workflow
 
 Write out the step-by-step process a finding travels from raw tool output to
 fully stored knowledge. Make it a file, not prose in chat.
 
 The pipeline is:
   raw tool output → intake → parse → normalize → deduplicate →
   assign to game system → assign to surface → link relationships →
   mark confidence → review and triage → promote to canonical
 
 ---
 
 ## Phase 5: Write the session continuation rules
 
 Create a RULES.md that any future AI session can read cold and immediately understand:
 - How the project is structured and why
 - Where new findings go
 - How to process them through the pipeline
 - How to avoid duplication
 - How to handle uncertainty and unknowns
 - How to hand off cleanly to the next session
 - What is explicitly out of scope until the map is complete
 
 This file is the most important deliverable. It prevents knowledge loss between sessions.
 
 ---
 
 ## Required deliverables before finishing
 
 Do not end the session until all of these exist as actual files:
 1. SURFACES.md (from Phase 0)
 2. GAME_SYSTEMS.md (from Phase 0)
 3. Full folder structure with README.md in each folder
 4. Schema definition file
 5. Ingestion pipeline file
 6. RULES.md
 7. NEXT_SESSION.md — what the reverse engineering tools session should do first,
    in what order, and what output to expect
 
 ---
 
 ## Working rules
 
 - Produce files. Do not put important information only in chat.
 - One phase at a time. Finish each phase before starting the next.
 - If something is unknown, create a placeholder and mark it unknown.
 - Do not start reverse engineering yet.
 - Do not design or hint at the API layer yet.
 - Ask me if you need a decision. Do not guess on things that affect structure.
