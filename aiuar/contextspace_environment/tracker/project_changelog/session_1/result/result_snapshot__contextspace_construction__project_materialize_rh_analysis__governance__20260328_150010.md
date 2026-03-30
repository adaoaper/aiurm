# AIURM Protocol
AIURM/AIUAR Context Space Workflow Specification
DLR Methodology

# Workflow
Materialize project_rh_analysis_example (v0.1)

# Purpose
Materialize ***project_rh_analysis_example into a portable self-contained JSON file.

---

# Governance
as_of                  = 2026-03-28
memory_policy            = IGNORE
substrate_type           = FILESYSTEM
aiuar_root             = ...\aiuar\
aiuar                  = *****contextspace_construction****materializer***project_materialize_rh_analysis**session_1
aiuar_data_source      = aiuar
aiuar_logic_source     = aiuar
aiuar_result_output    = *****contextspace_example
[*aiurm_governance_materialize_rh_analysis] #0

---

# Data

*data_source_node

---

# Logic

*logic_project_materialization

---

# Result

R1. Materialize project_rh_analysis_example
apply *logic_project_materialization to *data_source_node
[*result_materialized] #3

---

# End of pipeline definition
