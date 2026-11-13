---
name: governance
description: |
  GOVERNANCE – Contractual standard for AIURM/AIUAR governance files.
  Defines mandatory sections, required fields, format rules, and naming
  conventions for governance files in any contextspace project.
  Read this before creating or validating a governance file.

  Also trigger when the user mentions 'aiurm', 'aiurm protocol', 'aiuar', 'contextspace', 'aiurm project'

requires: aiurm, aiuar

---

# GOVERNANCE v0.3
Contractual standard for AIURM/AIUAR governance files.

Dependency chain: aiurm → aiuar → governance

---

## PURPOSE

The governance file is the authoritative pipeline definition for a project.

- what the project is
- what data it consumes
- what logic it applies
- what results it must produce
- under what configuration it runs
- which environment projects handle operational concerns

The governance file is NOT a data or logic file.
It contains references to data and logic, not their content.

---

## FILE LOCATION AND NAMING

```
{aiuar_root}/{contextspace}/{entity}/{project}/governance/aiurm_governance_{project}.txt
```

Rules:
- One governance file per project.
- File name must follow the pattern: `aiurm_governance_{project}.txt`
- Stored in `{project}/governance/` — never inside a session folder.
- The `governance/` folder is read-only during session execution.

---

## MANDATORY STRUCTURE

A governance file must contain all five sections in this exact order:

```
1. Header
2. Governance block
3. Data section
4. Logic section
5. Result section
```

Missing any section is a contract violation.

---

## SECTION 1 — HEADER

```
# AIURM Protocol
AIURM/AIUAR Context Space Workflow Specification
DLR Methodology

# Workflow
{workflow name and version}

# Purpose
{one or more lines describing the pipeline purpose and stage sequence}

---
```

Rules:
- The three header lines (`# AIURM Protocol`, spec line, methodology line) are fixed and must not be altered.
- `# Workflow` must identify the pipeline by name and version.
- `# Purpose` must describe the end-to-end flow.

---

## SECTION 2 — GOVERNANCE BLOCK

```
# Governance
{field} = {value}
...

[*aiurm_governance_{project}] #0

---
```

### Field value conventions

| Value type | Format | Examples |
|---|---|---|
| Numeric | no quotes | `table_max_rows = 50` |
| Path | no quotes | `aiuar_root = ...\aiuar\` |
| AIUAR address | no quotes | `aiuar = *****contextspace****entity***project**session` |
| Keyword / enum | no quotes | `output_result_format = JSON` |
| Explicit string | quotes | `as_of = "2026-03-25"`, `policy_version = "HRPOL_V1"` |
| String with spaces | quotes | `description = "HR analysis pipeline"` |

### Mandatory AIUAR fields

| Field | Description |
|---|---|
| `as_of` | Reference date of the governance definition |
| `substrate_type` | Physical substrate where this governance lives. e.g. `FILESYSTEM`, `JSON_FILE`, `MARKDOWN_FILE` |
| `aiuar_root` | Physical anchor — resolved by the executor from the active working directory. Convention: `...\aiuar\` |
| `aiuar` | Full AIUAR address of the active session in asterisk notation |
| `aiuar_data_source` | Session address for data resolution. Default: `aiuar` |
| `aiuar_logic_source` | Session address for logic resolution. Default: `aiuar` |
| `aiuar_result_output` | Session address for result output. Default: `aiuar`. Can use `**session_{n}+1` to auto-increment session per execution run. |
| `execution_id` | Random identifier generated per execution (e.g. `20260327_a3f7b2`). Forces fresh execution — an unknown `execution_id` in logs means the executor must run, not skip |

`aiuar` encodes the complete address in a single field using AIUAR notation:
```
aiuar = *****contextspace****entity***project**session
```

Example:
```
aiuar_root     = ...\aiuar\
substrate_type = FILESYSTEM
aiuar          = *****contextspace_environment****tracker***project_audit**session_1
```

### Optional fields (common)

| Field | Description |
|---|---|
| `policy_version` | Policy set identifier | e.g. `"HRPOL_V1"` |
| `response_contract` | e.g. `STRUCTURED_OUTPUT_REQUIRED` |
| `output_result_format` | e.g. `JSON`, `TEXT` |
| `runtime` | e.g. `python`, `native` |
| `execution_trigger` | e.g. `python_runtime`, `manual` |
| `audit_level` | e.g. `FULL`, `MINIMAL` |
| `audit_policy` | e.g. `LOG_EACH_RESULT_STEP` |
| `language_policy_default` | e.g. `EN`, `PT` |
| `schema_mode` | e.g. `restrict`, `permissive` |
| `aiurm_markers_location` | e.g. `IN_JSON_BODY`, `INLINE` |

### Resolution mode field (optional)

| Field | Values | Description |
|---|---|---|
| `resolution_mode_default` | `INFERENCE` \| `HYBRID` \| `DETERMINISTIC` \| `AUTO` | Project-wide resolution mode, applied to every Result step that carries no mode suffix |

If the field is absent, steps without a mode suffix are resolved as `AUTO`.

The modes, the per-step mode suffix, and what the executor is expected to do in each
are defined in RESOLUTION MODE.

### Result artifact format rule

`output_result_format = JSON` + `aiurm_markers_location = IN_JSON_BODY` together form a mandatory contract. When both are declared, every result artifact MUST include as its first two fields:

```json
{
  "aiurm_marker": "[*result_x]",
  "aiuar_address": "*****contextspace****entity***project**session*result_x",
  ...
}
```

| Field | Value | Purpose |
|---|---|---|
| `aiurm_marker` | `"[*result_x]"` | Artifact identity — marker as defined in AIURM SKILL |
| `aiuar_address` | full AIUAR address | Artifact location — enables cross-session reference |
| `aiurm_custom_marker` | Marker format declaration |
| `aiurm_automatic_marker` | Auto-marker format declaration |
| `synthetic_data_expansion_policy` | Instructions for data expansion during execution |
| `inheritance_mode` | e.g. `full_reprocess`, `delta_reprocess` |

### Operational concerns

Audit, log, exception, and code artifacts are not stored inside the session.
To register an event, the executor must execute the corresponding environment project.
The environment projects are addressed in governance:

| Concern   | Governance field    | Handled by        |
|-----------|---------------------|-------------------|
| Audit     | `project_audit`     | project_audit     |
| Log       | `project_log`       | project_log       |
| Exception | `project_exception` | project_exception |
| Code      | `project_code`      | project_code      |

If an environment field is absent or empty, the executing agent handles
the concern directly without external delegation.

### Environment fields (optional)

Declare the AIUAR session addresses of the operational environment projects.
All values are relative to `aiuar_root`. If absent, the executing agent handles
operational concerns directly without external delegation.

| Field | Value format | Description |
|---|---|---|
| `project_audit` | `*****{contextspace}****{entity}***{project}*aiurm_governance_{project}` | Audit project — resolved via governance indirection |
| `project_log` | `*****{contextspace}****{entity}***{project}*aiurm_governance_{project}` | Log project — resolved via governance indirection |
| `project_exception` | `*****{contextspace}****{entity}***{project}*aiurm_governance_{project}` | Exception project — resolved via governance indirection |
| `project_code` | `*****{contextspace}****{entity}***{project}*aiurm_governance_{project}` | Code project — resolved via governance indirection |

### Governance indirection rule

When an environment field value ends with `*aiurm_governance_{project}`, the executor must:

1. Locate the governance file of the referenced project
2. Read its `aiuar` field to determine the active session
3. Use that session as the write target

This is late binding — the active session is resolved at runtime from the target project's governance, not hardcoded in the caller's governance. If the target project migrates to a new session, no caller governance needs to change.

Example:
```
project_audit     = *****contextspace_environment****tracker***project_audit*aiurm_governance_project_audit
project_log       = *****contextspace_environment****tracker***project_log*aiurm_governance_project_log
project_exception = *****contextspace_environment****tracker***project_exception*aiurm_governance_project_exception
project_code      = *****contextspace_environment****tracker***project_code*aiurm_governance_project_code
```

### Field extensibility

Governance is an extensible control structure. Some projects may implement
specific fields without necessarily being cited in this SKILL — for example,
`aiuar_review_target`, `claim_strategy`, `human_readability_mode`,
`synthetic_data_expansion_policy`.

Such fields are valid as project-specific contract and must be preserved on
read and rewrite. The SKILL documents the core; project governance carries the rest.

---

## EXECUTOR OBLIGATION — ENVIRONMENT WRITES IN AIURM PIPELINE EXECUTIONS

This section defines mandatory executor behavior for environment writes triggered by pipeline execution.
It is not a field description — it is a pipeline obligation.

When an environment field is declared in governance, the executor MUST write to the resolved target according to the rules below.

1. `*aiurm_governance_{project}.project_audit`
   The executor MUST execute it and write audit records for completed Result steps.

2. `*aiurm_governance_{project}.project_log`
   The executor MUST execute it and write one log record per Result step, including `completed`, `failed`, `aborted`, or `skipped` status.

3. `*aiurm_governance_{project}.project_exception`
   The executor MUST execute it for any failed, aborted, validation-failed, or unresolvable-marker step.

4. `*aiurm_governance_{project}.project_code`
   The executor MUST execute it for every generated or modified code artifact produced in the scope of execution, including executors, resolvers, transformers, helper scripts, and test files.

### Mandatory timing rule

Environment writes do NOT depend on successful completion of all Result steps.

- `project_audit` applies after successful completion of the relevant Result steps.
- `project_log` applies whenever step status is materialized.
- `project_exception` applies immediately when an exception condition is detected.
- `project_code` applies immediately when a code artifact is generated or modified.

### Mandatory project_code rule

When `project_code` is declared, it designates the location where the AI must place any artifacts it generates during governance execution — scripts, temporary files, tests, intermediate outputs, or any other execution support material.

The AI MUST create a node named:

```
result_code__{contextspace}__{project}__{execution_id}/
```

inside the active `project_code` session result path, whenever it needs to write such artifacts.

Rules:
- The AI follows the `project_code` governance declared by the calling project. That governance may instruct the use of specific, previously generated code.
- The folder or node is created only when the AI has artifacts to store — if nothing was generated, no node is created.
- The internal structure and naming of the node's contents are entirely free — the protocol does not prescribe them.
- The AI MUST NOT create execution artifacts at `aiuar_root` or outside this node.
- Whether a step is resolved by code is decided by its resolution mode (see RESOLUTION MODE): code is the resolver in `DETERMINISTIC` steps, computes under the model's direction in `HYBRID` steps, and is limited to input and output in `INFERENCE` steps. Beyond what the mode calls for, the AI SHOULD avoid unnecessary code generation.

---

### Governance marker rule

The governance block must end with its own marker, immediately before the closing `---`:

```
[*aiurm_governance_{project}] #0
```

- The marker name must match the project name.
- Intention suffix `#0` is mandatory — governance registration emits no output.

---

## SECTION 3 — DATA SECTION

```
# Data

*{data_marker_x}
*{data_marker_y}
...

```

Rules:
- Lists only marker references — one per line, in `*marker` format (no brackets).
- No data content inline. Content lives in `{session}/data/`.
- Optional subtypes may be used in Data markers, e.g. `data_param_...`, `data_table_...`, `data_profile_...`.
- The intention suffix (`#0`) is strongly recommended for Data blocks.

---

## SECTION 4 — LOGIC SECTION

```
# Logic

*{logic_marker_x}
*{logic_marker_y}

...

---
```

Rules:
- Lists only marker references — one per line, in `*marker` format (no brackets).
- No logic content inline. Content lives in `{session}/logic/`.
- The intention suffix (`#0`) is strongly recommended for Logic blocks.

---

## SECTION 5 — RESULT SECTION

```
# Result

R{n}. {Title}
apply *{logic_marker} to *{data_marker_x} and *{data_marker_y}...
[*{result_marker}] #{intention_suffix} {MODE}
...

```

Rules:
- Every result step must have: a numbered title, an Apply block, and a marker assignment.
- The intention suffix (`#0`) is strongly discouraged for Result blocks.
- The intention suffixes (`#1`, `#2`, `#3`) are strongly recommended, but not mandatory, for Result blocks.
- A mode suffix (`INFERENCE`, `HYBRID`, `DETERMINISTIC`, `AUTO`) may follow the intention suffix on the marker line. It is optional and declares how that step must be resolved — see RESOLUTION MODE.
- `R1.`, `R2.`, `R3.`, etc. are human-readable identifiers only. They do not define execution order by themselves.
- Execution follows the logical order of result blocks in the governance file, unless an explicit rule states otherwise.
- **The result marker is the primary identifier of a step — never `Rn`.** The AI must always reference a step by its marker (e.g., `*result_x`), not by its numeric label.
- When a step title is needed (e.g., in audit or exception records), always use the full title including both label and name (e.g., `"R1. Store code artifact"`), never the label alone (`"R1"`).

---

## RESOLUTION MODE

### Why it exists

The model's attention is the scarce resource of a governed execution.

A capable executor can resolve almost any step by writing code. The numbers come out
right, and nobody has looked at the data. What humans want from an AI is not only the
result but its presence at the points that matter.

The resolution mode is how the governance author declares, step by step, where the
model's own look is required and where calculation is enough. The author answers one
question per step: does this step need the model's eyes, is calculation enough, or both?

This section explains the intent so that the executor can act on it, including in
situations the text does not enumerate.

### The modes

Each mode is defined by what the model's attention must pass over.

| Mode | The model's attention passes over |
|---|---|
| `INFERENCE` | the rule, the data, and the result |
| `HYBRID` | the rule, plus the inputs and outputs of the delegated computation |
| `DETERMINISTIC` | the rule only |

**INFERENCE** — the model's look is required on everything.

Expected of the executor:
- Read the data itself; do not hand it to a parser.
- Interpret the rule and resolve the step by its own reasoning.
- Notice what a calculation would not notice, and record it.
- Use code only for input and output (reading and writing artifacts), never to produce the step's answer.

**HYBRID** — code guarantees the number; the contract guarantees the look.

Expected of the executor:
- Keep the judgment (interpreting the rule, classifying, choosing) and delegate the arithmetic to code.
- Read what goes into the computation and what comes out of it.
- Record what it observes: anomalies, surprises, values that are well-formed but look wrong.

Two shapes are valid and may be combined in one step: the model judges and code computes
from that judgment; or code computes and the model examines the outcome. The model is not
expected to re-check the arithmetic. A step in which the model only forwards the code's
output has not been resolved in `HYBRID` mode.

**DETERMINISTIC** — calculation is enough.

Expected of the executor:
- Read the rule and translate it faithfully into code.
- Run the code and report the result.

The data does not need to enter the model's context, and no observation is contracted.

**AUTO** — the choice is delegated to the executor.

`AUTO` is not a fourth way of resolving a step. It asks the executor to choose one of the
three modes above for that step and to record the choice.

Expected of the executor:
- Choose by the intent of this section, not by cost alone: ask where a look would notice something a calculation would not.
- Do not resolve every step by code by default; that defeats the purpose of the contract.
- Fulfil the expectations of the mode it chose.

### Where the mode is declared

Per step — a mode suffix on the marker line of a Result step, after the intention suffix:

```
R8. Generate Stress Test Results
apply *logic_stress_tests to *result_portfolio_data_normalized
[*result_stress_test_results] #3 DETERMINISTIC
```

Rules:
- Canonical spelling is uppercase: `INFERENCE`, `HYBRID`, `DETERMINISTIC`, `AUTO`.
- The order is fixed: `[*marker] #n MODE`.
- The intention suffix and the mode suffix are optional and independent: `[*marker] HYBRID` is valid.
- The mode suffix is valid only on the marker line of a Result step. It has no meaning on the governance marker or in the Data and Logic sections.

The marker line carries both sides of the attention contract: `#n` declares how much
the human will read; the mode declares where the model must look.

Per project — one governance field:

```
resolution_mode_default = INFERENCE
```

Precedence:

1. The mode suffix on the step.
2. `resolution_mode_default`.
3. Neither is present: `AUTO`.

Code used in `HYBRID` and `DETERMINISTIC` steps runs under the project-wide `runtime` and
`execution_trigger` fields and is stored according to the Mandatory project_code rule.

### What is recorded

Declared where it matters; recorded where delegated.

The audit record of every completed Result step must carry:

| Field | Rule |
|---|---|
| `resolution_applied` | Mandatory. The mode actually used: `INFERENCE`, `HYBRID`, or `DETERMINISTIC`. Never `AUTO`. |
| `ai_observation` | Mandatory when the applied mode is `INFERENCE` or `HYBRID`: what the model noticed while looking. When there is nothing to report, say so explicitly — this distinguishes "looked and saw nothing" from "did not look". Also mandatory, in any mode, when the applied mode differs from the declared one: state the deviation and its reason. |

The human reads in the audit where the model looked and where it calculated, and adjusts
the suffixes for the next execution.

### When the declared mode cannot be followed

The executor follows the declared mode as far as it honestly can. This is new ground and
no execution is perfect: what the contract forbids is silence, not deviation.

- If a step is resolved differently from what was declared, in whole or in part, the executor records the mode it actually used in `resolution_applied` and states the deviation and its reason in `ai_observation`.
- Replacing a required look with code is the deviation this contract most wants to avoid. When it happens, it must be visible in the audit.
- A step that cannot be resolved in any mode follows the existing failure path: it is recorded as failed or aborted, and subsequent steps that do not depend on it may continue.

### Legacy resolution fields (v0.2)

Governance files written for v0.2 may still carry the six resolution fields.

- `resolution_mode = X` is read as `resolution_mode_default = X`.
- `primary_resolver`, `requires_llm_reasoning`, `primary_resolution_by_code`, `instrumental_code_role`, and `resolution_scope` are no longer part of the contract. They have no effect, do not count as project-specific fields under the Field extensibility rule, and should be removed when the file is next edited.

---

## RECOMMENDED GOVERNANCE STRUCTURE

This list is a guide for whoever writes or reviews a governance file.

- Follow strict AIURM, AIUAR, and governance definitions.
- File naming and location follow the convention: `governance/aiurm_governance_{project}.txt`.
- All mandatory governance fields are present.
- Governance marker `[*aiurm_governance_{project}] #0` is present and correctly named.
- Data section contains only `*marker` references (no content).
- Logic section contains only `*marker` references (no content).
- Every Result step has a title, an Apply block, and a result marker assignment.
- Result steps are numbered for human reference only.
- Execution follows the logical order of Result blocks, not necessarily their numeric labels.
- File ends with `# End of pipeline definition`.
- Every Logic marker referenced in any Result Apply block is declared in the Logic section.
- Every Data marker referenced in any Result Apply block is declared in the Data section.
- Every referenced Data and Logic marker has a corresponding artifact in the contextspace.

---

## GOVERNED EXECUTION PREMISES — MARKER RESOLUTION

Markers referenced in an Apply block are resolved during execution of the corresponding Result step.

Good practice: the executor persists the result of each Apply as soon as it is available.
Work already done stays recorded if the execution is interrupted, and later steps start
from the written result.

Resolution requires:

1. The marker is declared in the appropriate governance section (`Data` or `Logic`).
2. A corresponding artifact with the same name exists in the active contextspace.

Declaration without artifact, or artifact without declaration, is a resolution failure for that step.

### Unresolvable marker → exception + abort

If any marker referenced in an Apply block cannot be resolved, the executor must:

1. Write an exception record to the `project_exception` address (from governance) using this format:

```json
{
  "origin_contextspace": "{contextspace}",
  "origin_entity": "{entity}",
  "origin_project": "{project}",
  "origin_session": "{session}",
  "timestamp": "YYYYMMDD_HHMMSS",
  "step": "R{n}",
  "title": "{step title}",
  "exception_type": "UNRESOLVABLE_MARKER",
  "marker": "*{marker_name}",
  "expected_in_governance_section": "Logic | Data",
  "governance_declared": true,
  "artifact_found": false,
  "action": "ABORTED",
  "executor_insight": "{optional diagnostic insight}"
}
```

2. Name the exception result artifact:
   `result_exception__{contextspace}__{project}__{session}__{timestamp}`

3. Abort execution of the current step. Subsequent steps that do not depend on the failed marker may continue.

---

## CRITICAL RULE — GOVERNANCE IS AN INDEX, NOT A STORE

The governance file defines *what* the pipeline does and *where* to find inputs and outputs.
It must never contain data payloads, logic instructions, or result content inline.

Violations:
- Embedding JSON data in the Data section → move to `session/data/`
- Embedding logic text in the Logic section → move to `session/logic/`
- Omitting the Result section → contract is incomplete, pipeline is unexecutable

---

# governance skill v0.3 — part of the AIURM Protocol

Created by Adao Aparecido Ernesto (2025)
aiurm.org | X: @adaoaper | GitHub: github.com/adaoaper/aiurm
Public domain (CC0)
No stability guarantees are provided.
