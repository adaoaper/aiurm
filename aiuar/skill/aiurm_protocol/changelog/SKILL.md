---
name: changelog
description: |
  CHANGELOG – Mutation tracking for AIURM/AIUAR governance and logic artifacts.
  Defines the AI self-registration protocol for changes to definitional artifacts
  (governance/ and session/logic/). Records are written to project_changelog in
  contextspace_environment — resolved by convention, not declared in governance.
  Enables undo, change history, and drift detection.

  ALWAYS activate before modifying any governance/ or session/logic/ artifact.
  This skill must be active whenever the AI writes, edits, or deletes a monitored artifact.

  Also trigger when the user issues a command to modify a logic or governance artifact,
  such as: 'update the logic', 'change the governance', 'edit logic', 'modify this block',
  'update governance', 'edit the governance', 'add this field', 'remove this field',
  'rewrite the logic', 'add this to governance',
  or any instruction that implies writing to governance/ or logic/.

  Also trigger when the user mentions 'changelog', 'change history', 'undo',
  'what did you change', 'who changed it'.

requires: aiurm, aiuar

---

# CHANGELOG v0.2
Mutation tracking for AIURM/AIUAR governance and logic artifacts.

Dependency chain: aiurm → aiuar → changelog
All AIURM and AIUAR rules remain fully operative when CHANGELOG is active.

---

## PURPOSE

The changelog is the AI's self-registration of every change made to definitional
artifacts in a project. It exists to:

- Give the user full visibility of what the AI changed, when, and why
- Enable undo of any registered change
- Detect unregistered changes made directly by the user
- Operate without git, without technical commands, in natural language

The changelog is NOT an execution log. Session execution events are tracked by `project_audit`.
The changelog tracks evolution of the project's definitional layer across sessions,
written to `project_changelog` resolved by convention from the active contextspace environment.

---

## STORAGE

The changelog SKILL resolves its storage address automatically from the active contextspace
environment convention — it does NOT require a field in the business project governance.

All changelog artifacts are written to:
```
{aiuar_root}/contextspace_environment/general/project_changelog/session_1
```

Two result artifact types coexist in this project:

| Type | Pattern | Purpose |
|---|---|---|
| Changelog entry | `result_changelog__{contextspace}__{project}__{session}__{timestamp}` | Change record |
| Snapshot | `result_snapshot__{contextspace}__{project}__{session}__{timestamp}` | Previous version of modified artifact |
| Revert entry | `result_changelog_undo__{contextspace}__{project}__{session}__{timestamp}` | Revert record |

---

## MONITORED ARTIFACTS

| Location | Monitored | Reason |
|---|---|---|
| `governance/` | yes | pipeline definition owned by the user |
| `{session}/logic/` | yes | business logic owned by the user |
| `skill/` | no | protocol maintained externally by the AIURM maintainer |

---

## EVENT RECORD FORMAT

Every change must produce a record with these fields:

```json
{
  "origin_contextspace": "{contextspace}",
  "origin_entity": "{entity}",
  "origin_project": "{project}",
  "origin_session": "{session}",
  "timestamp": "YYYYMMDD_HHMMSS",
  "owner": "AI | HUMAN",
  "event": "FILE_ADDED | FILE_MODIFIED | FILE_DELETED",
  "artifact": "{relative path from project root}",
  "reason": "AI_AUTONOMOUS | HUMAN_REQUESTED",
  "snapshot_ref": "{result_snapshot__ marker of the saved previous version | null}",
  "change_summary": "{brief description of what was changed and why}"
}
```

### Field definitions

**owner** — who registered this event
| Value | Meaning |
|---|---|
| `AI` | AI registered this entry |
| `HUMAN` | user registered this entry manually |

**event** — what happened to the artifact
| Value | Meaning |
|---|---|
| `FILE_ADDED` | new artifact created |
| `FILE_MODIFIED` | existing artifact changed |
| `FILE_DELETED` | artifact removed |

**reason** — why the change occurred
| Value | Meaning |
|---|---|
| `AI_AUTONOMOUS` | AI decided and acted on its own initiative |
| `HUMAN_REQUESTED` | AI acted on explicit user request |

**snapshot_ref** — marker of the saved previous version in project_changelog
- Required for FILE_MODIFIED and FILE_DELETED
- Use `null` for FILE_ADDED (no prior version exists)

---

## READING THE CHANGELOG

The three fields together give the full picture without explanation:

| owner | reason | Human reads as |
|---|---|---|
| `AI` | `AI_AUTONOMOUS` | AI decided on its own |
| `AI` | `HUMAN_REQUESTED` | I asked, AI executed |
| `HUMAN` | `HUMAN_REQUESTED` | I changed and registered manually |

---

## AI OBLIGATIONS

### Before modifying any monitored artifact

1. Save a full copy of the current file to `project_changelog`
   named: `result_snapshot__{contextspace}__{project}__{session}__{timestamp}`
2. Make the modification
3. Immediately write a changelog event record to `project_changelog`
   named: `result_changelog__{contextspace}__{project}__{session}__{timestamp}`

No modification to a monitored artifact is permitted without a prior snapshot.

---

## UNDO PROTOCOL

The user may request to undo any registered change in natural language.

AI steps:
1. Query `project_changelog` and identify the target event record
2. Locate the referenced snapshot in `project_changelog` via `snapshot_ref`
3. Restore the artifact from the snapshot
4. Write a new event record documenting the revert, adding:

```json
{
  "event": "FILE_MODIFIED",
  "reason": "HUMAN_REQUESTED",
  "reverts": "{snapshot_ref of the restored version}"
}
```

The revert itself is a registered event. The state before revert is also snapshotted.

---

# changelog skill v0.2 — part of the AIURM Protocol

Created by Adao Aparecido Ernesto (2025)
aiurm.org | X: @adaoaper | GitHub: github.com/adaoaper/aiurm
Public domain (CC0)
No stability guarantees are provided.
