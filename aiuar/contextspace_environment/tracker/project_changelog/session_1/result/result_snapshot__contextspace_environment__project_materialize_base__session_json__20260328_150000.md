Materialize a contextspace AIUAR address into a portable JSON file.

target format:
{
  "<contextspace_name>": {
    "<entity_name>": {
      "<project_name>": {
        "governance": "...(string — full content of aiurm_governance_{project}.txt)",
        "<session_n>": {
          "data":   { "<artifact_name>": "...(string — file content verbatim)" },
          "logic":  { "<artifact_name>": "...(string — file content verbatim)" },
          "result": { "<artifact_name>": "...(string — file content verbatim)" }
        }
      }
    }
  }
}

rules:
- folders become JSON object keys
- files (markers) become string values with content preserved verbatim
- no decomposition of content into nested JSON objects
- governance/ folder maps to "governance" key — content as single string
- each session folder maps to a session key (session_1, session_2, ...)
- node_d = "none" → omit data key from output
- node_l = "none" → omit logic key from output
- node_r = "none" → include result key as empty object: "result": {}
- "none" is explicit exclusion — not omission
- AIUAR hierarchy maintained as keys at every level: contextspace → entity → project → session → DLR
- file names without extension become the artifact key name
- output file name = {node_contextspace}.json — appended to aiuar_result_output address
- session DLR key order must be: data → logic → result (never reorder)
- replace substrate_type = FILESYSTEM with substrate_type = JSON_FILE in the governance string
- always add execution_id = {YYYYMMDD}_{6-char random alphanumeric} to the governance string

[*logic_project_materialization]
