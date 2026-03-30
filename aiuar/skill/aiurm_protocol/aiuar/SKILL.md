---
name: aiuar
description: |
  AIUAR Extension – Artificial Intelligence Universal Address Reference.
  Contextual addressing layer for the AIURM protocol.
  Activates automatically whenever AIURM is active.

  Use this skill whenever the user:
  - Uses AIUAR path addressing (contextspace/entity/project/session)
  - References cross-session or cross-project context
  - Uses reference mode in DLR blocks
  - Defines or resolves a contextspace structure

  Also trigger when the user mentions 'aiurm', 'aiurm protocol', 'aiuar', 'contextspace'

requires: aiurm

---

AIUAR extends AIURM with a hierarchical addressing system that resolves any DLR artifact
across any substrate — filesystem, JSON, or key-value store.
While AIURM defines *what* a block of information is (marker), AIUAR defines *where* it lives
in the full space of interactions.

Dependency: This extension requires AIURM Protocol v0.1 or later.

---

## ADDRESSING HIERARCHY

AIUAR defines an agnostic node hierarchy. Every node receives a unique asterisk identifier by depth.
The physical representation depends on the substrate (filesystem, JSON, or key-value store).
The diagram below uses tree notation for readability only.

```
aiuar_root/aiuar/
└── *****contextspace_environment/
    └── ****entity/
        ├── governance/   ← pipeline definition (read-only during execution)
        └── ***project_1/
            └── **session_1/
                ├── data/     ← *data_x markers
                ├── logic/    ← *logic_x markers
                └── result/   ← *result_x markers
```
*(tree notation representation — resolves identically on any hierarchical substrate)*

| Level | Identifier | Convention name | Example | Status |
|---|---|---|---|---|
| aiuar_root |  | Physical anchor — declared in governance | `...\aiuar\` | Implemented |
| 5 | `*****` | contextspace | `*****contextspace_environment`    | Implemented |
| 4 | `****`  | entity       | `****entity`                       | Implemented |
| 3 | `***`   | project      | `***project_1`                     | Implemented |
| 2 | `**`    | session      | `**session_1`                      | Implemented |
| 1 | `*`     | marker       | `*data_x`, `*logic_x`, `*result_x` | Implemented |

The hierarchy reads from broadest to narrowest:
`aiuar_root / *****contextspace / ****entity / ***project / **session / *marker`

Full address notation:
`*****contextspace_1****entity_1***project_1**session_1*marker`

`aiuar_root` is the only level defined outside the address — declared in governance,
resolved by the executor before any address is parsed.

---

## THE TERMINAL NODE: DLR

At the end of every AIUAR address, the AI finds the atom of execution — the DLR node.

| Type   | Node   | Marker prefix   | Meaning                     |
|--------|--------|-----------------|-----------------------------|
| Data   | data   | *data_x         | Raw input — the fact        |
| Logic  | logic  | *logic_x        | Rule — what to do           |
| Result | result | *result_x       | Materialized output          |

The instruction to the AI is: **"Resolve the DLR of address X."**
The AI consumes Data, applies Logic, and deposits the Result — without ambiguity about where each lives.

The `*data_x` marker is not restricted to structured facts or tabular data. It can reference any content the executor is capable of resolving — text, JSON, binary, image, a file, a query result, or any artifact addressable in the active substrate. The marker names the input; the substrate and executor determine what is loaded.

`*marker` notation (single asterisk) continues to identify DLR artifacts as defined in AIURM.
AIUAR adds the path above the marker — it does not change marker behavior.

---

## SUBSTRATE AGNOSTICISM

The greatest strength of AIUAR is physical abstraction.
The AI only needs to know the address. How the structure is stored is irrelevant.

AIUAR resolves across:

| Substrate             | `substrate_type`    | Representation                              |
|-----------------------|---------------------|---------------------------------------------|
| Filesystem            | `FILESYSTEM`        | folders and files on disk                   |
| JSON file             | `JSON_FILE`         | nested keys in a single `.json` document    |
| Markdown file         | `MARKDOWN_FILE`     | headings and content blocks in a `.md` file |
| Any structured format | `{FORMAT}_FILE`     | any single-file format following this pattern |

The address notation is the same across all substrates.
Resolution depends on the executor's capability to navigate the declared substrate.
If the executor cannot resolve the substrate, execution must abort with an exception.

### Substrate inference

The executor resolves the substrate type from the `substrate_type` field declared in governance.
This field is mandatory — execution without `substrate_type` is a protocol violation.

### File-based substrate resolution (JSON_FILE, MARKDOWN_FILE)

When `substrate_type` is `JSON_FILE` or `MARKDOWN_FILE`, all artifacts — governance, data, logic,
and result — are resolved from a single file. The executor must NOT access the filesystem for
individual artifact files.

Resolution rules:
- The substrate file is declared explicitly in the execute command using `in {filename}`
- All artifact content is read from within that single file
- The AIUAR hierarchy is represented as nested keys (JSON) or heading levels (Markdown)
- Writing results back to the substrate file follows the same single-file discipline

### Cross-substrate resolution

The active contextspace substrate is immutable. References to other contextspaces resolve using the substrate declared in the target governance — this is cross-substrate resolution.

To resolve a cross-contextspace reference:
1. Locate the target governance via the AIUAR address
2. Read its `substrate_type`
3. Resolve the target artifacts using that substrate

### Substrate discipline

The AI must never write artifacts outside the active session's DLR scope.

- `aiuar_root`, contextspace, entity, and project root are read-only during execution
- All AI-generated artifacts must be placed in `data/`, `logic/`, or `result/` within the active session
- Operational artifacts (audit, log, exception, code) are written to the addresses
  declared in governance environment fields — never as local folders inside the session
- Writing artifacts at project root, contextspace root, or aiuar_root is a protocol violation

---

## GENERAL RULES FOR AIUAR

### Address composition

- A full AIUAR address names all levels from contextspace to marker:
  `*****contextspace****entity***project**session*marker`
- `aiuar_root` is resolved from governance — it is never written inline in an address.
- Within the active governance context, the marker alone is a valid local reference: `*data_x`
- Any cross-scope reference must use the full address — no partial paths.

### AIUAR notation rule

Any reference to an AIUAR artifact must use AIUAR notation — never a literal substrate path.
The asterisk count identifies the level unambiguously.

| Correct | Incorrect |
|---|---|
| `*data_x` (local, active context implied) | `data/data_x.txt` |
| `*****contextspace_1****entity_1***project_1**session_1*data_x` | `session_1/data/data_x` |

### Scope inference

- `*marker` — marker artifact in the active context (1 asterisk)
- `**session` — session node (2 asterisks)
- `***project` — project node (3 asterisks)
- `****entity` — entity node (4 asterisks)
- `*****contextspace` — contextspace node (5 asterisks)

The asterisk count makes any address self-describing — the depth is always explicit.

### Level prefix rule

The level prefix is mandatory. The asterisk count encodes the depth; the prefix names the level explicitly.

### Active context resolution in contextspace execution

When operating within a contextspace, the active context is determined
by the governance fields of the active project:

```
aiuar_root   → physical anchor for all resolution
contextspace → resolves contextspace level
entity       → resolves entity level
project      → resolves project level
session      → resolves session level
```

Governance is mandatory. The executor must load governance before any
address resolution. Execution without governance is a protocol violation.

---

## GOVERNANCE FIELDS

AIUAR resolution depends on governance fields — see the governance skill for full specification.

`aiuar_root` is the only field that carries the `aiuar_` prefix — it is the namespace anchor.
All other AIUAR hierarchy fields are implicitly scoped under it.

---

## ADDRESS USAGE PATTERNS

Every artifact stored under `aiuar_root` is addressable via AIUAR notation from any project.
A full address gives any executor unambiguous access to any artifact across the entire contextspace.

Local reference — marker only, all levels resolved from active governance context:
```
apply *logic_x to *data_x
```

Cross-session reference — same project, different session:
```
*****contextspace_1****entity_1***project_1**session_1*result_x
*****contextspace_1****entity_1***project_1**session_2*result_x
```

Cross-project reference — same entity, different project:
```
*****contextspace_1****entity_1***project_1**session_1*result_x
*****contextspace_1****entity_1***project_2**session_1*data_x
```

Cross-entity reference — same contextspace, different entity:
```
*****contextspace_1****entity_1***project_1**session_1*data_x
*****contextspace_1****entity_2***project_1**session_1*data_x
```

Cross-contextspace reference — full address, all levels explicit:
```
*****contextspace_1****entity_1***project_1**session_1*data_x
*****contextspace_2****entity_1***project_1**session_1*data_x
```

---


## EXECUTE COMMAND

`execute` targets the governance file `aiurm_governance_{project}` of a project and runs its pipeline linearly — loading governance fields, resolving Data and Logic markers, and executing Result steps in order.

Valid forms:

- Filesystem path: `execute path/to/governance/aiurm_governance_{project}`
- AIUAR short (development): `execute ***{project}*governance`
- AIUAR full (production): `execute *****{contextspace}****{entity}***{project}*governance`
- File substrate: `execute in {filename} ***{project}*aiurm_governance_{project}`

### File substrate execute

Used when the project lives in a `JSON_FILE` or `MARKDOWN_FILE` substrate.

```
execute in contextspace_example.md ***project_rh_analysis_example*aiurm_governance_rh_analysis_example
```

- `in {filename}` — declares the substrate file (relative to `aiuar_root` or working directory)
- `***{project}*{governance_marker}` — locates the project within the file
- The governance marker is mandatory — a single file may contain multiple projects
- Once the executor enters the file, ALL artifact resolution happens within that file only

---

## BEST PRACTICES FOR AIUAR

- Naming: Use descriptive, lowercase, underscore_separated names at every level (e.g., `drug_discovery_q1`, `exploration_run_04`).
- Partial Addresses: Prefer partial addresses within a known context. Use full addresses only for cross-scope references.
- Separation of Concerns: The address names meaning. The resolver finds storage. The pipeline describes relationships. Keep these layers independent.

---

## INHERITANCE PATTERN

A child project inherits from a parent by referencing the parent's logic artifacts
via AIUAR addressing in its own Logic blocks.

### Example — cross-session logic reference

```
# Logic

**session_x*logic_scoring

# Child logic delta

L1. Scoring policy
- Inherit from parent. Increase all thresholds by 10%.
[*logic_scoring] #0
```

### Example — cross-project logic reference

```
# Logic

***project_x**session_y*logic_audit_2
```

---

# aiuar skill v0.1 — part of the AIURM Protocol

Created by Adao Aparecido Ernesto (2025)
aiurm.org | X: @adaoaper | GitHub: github.com/adaoaper/aiurm
Public domain (CC0)
No stability guarantees are provided.
