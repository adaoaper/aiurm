Materialize a ***project AIUAR address into a portable Markdown file.

target format:
# {project_name}

## governance
{full content of aiurm_governance_{project}.txt}

## {session_n}

### data
#### {artifact_name}
{file content verbatim}

### logic
#### {artifact_name}
{file content verbatim}

### result
#### {artifact_name}
{file content verbatim}

rules:
- folders become markdown headings at the appropriate level
- files (markers) become content blocks under their heading
- content preserved verbatim under each heading
- governance/ folder maps to "## governance" — content as plain text block
- each session folder maps to "## session_n"
- data_source_d = "none" → omit data section from output
- data_source_l = "none" → omit logic section from output
- node_r = "none" → include result section as empty: ### result (no artifacts)
- "none" is explicit exclusion — not omission
- AIUAR hierarchy maintained as heading levels
- file names without extension become the artifact heading name
- section order must be: data → logic → result (never reorder)
- output file extension must be .md — if aiuar_result_output declares .json, replace with .md
- replace substrate_type = FILESYSTEM with substrate_type = MARKDOWN_FILE in the governance block
- always add execution_id = {YYYYMMDD}_{6-char random alphanumeric} to the governance block, immediately after aiuar_local_resolve_priority

[*logic_project_materialization]
