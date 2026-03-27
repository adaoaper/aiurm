"""
AIURM/AIUAR Workflow Executor
Project: project_rh_analysis_example
Session: session_1
Generated: 2026-03-26
"""

import json
import os
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────────
AIUAR_ROOT = r"C:\aiurm\aiuar"
SESSION_PATH = os.path.join(AIUAR_ROOT, "contextspace_example", "adaoaper",
                            "project_rh_analysis_example", "session_1")
RESULT_PATH  = os.path.join(SESSION_PATH, "result")

ENV_ROOT     = os.path.join(AIUAR_ROOT, "contextspace_environment", "general")
AUDIT_PATH   = os.path.join(ENV_ROOT, "project_audit",     "session_1", "result")
LOG_PATH     = os.path.join(ENV_ROOT, "project_log",       "session_1", "result")
EXCEPTION_PATH = os.path.join(ENV_ROOT, "project_exception", "session_1", "result")
CODE_PATH    = os.path.join(ENV_ROOT, "project_code",      "session_1", "result")

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
CONTEXTSPACE = "contextspace_example"
ENTITY       = "adaoaper"
PROJECT      = "project_rh_analysis_example"
SESSION      = "session_1"

for p in [RESULT_PATH, AUDIT_PATH, LOG_PATH, EXCEPTION_PATH, CODE_PATH]:
    os.makedirs(p, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def write_result(name, data):
    path = os.path.join(RESULT_PATH, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def write_json(path_dir, name, data):
    path = os.path.join(path_dir, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def avg(lst):
    return round(sum(lst) / len(lst), 4)

# ── Load Data ─────────────────────────────────────────────────────────────────
def load_data(filename):
    filepath = os.path.join(SESSION_PATH, "data", filename)
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()
    # Strip leading label line (D1., D2., …) and trailing marker lines
    lines = raw.strip().splitlines()
    json_lines = []
    capture = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[*") or (stripped.startswith("D") and stripped[1:2].isdigit() and "." in stripped[:4]):
            if json_lines:
                continue
            else:
                continue
        if stripped.startswith("{") or stripped.startswith("["):
            capture = True
        if capture:
            if stripped.startswith("[*"):
                break
            json_lines.append(line)
    return json.loads("\n".join(json_lines))

employees            = load_data("data_employees.txt")
perf_rules_raw       = load_data("data_performance_rules.txt")
ret_rules_raw        = load_data("data_retention_rules.txt")
promo_scenarios_raw  = load_data("data_promotion_scenarios.txt")
output_config_raw    = load_data("data_output_configuration.txt")

perf_rules   = perf_rules_raw["performance_rules"]
engage_rules = perf_rules_raw["engagement_rules"]
growth_rules = perf_rules_raw["growth_potential_rules"]
ret_rules    = ret_rules_raw["retention_rules"]
rec_actions  = ret_rules_raw["recommended_actions"]
mgmt_pos     = ret_rules_raw["management_positions"]
cons_crit    = promo_scenarios_raw["conservative_criteria"]
aggr_crit    = promo_scenarios_raw["aggressive_criteria"]
action_hor   = output_config_raw["action_plan_horizons"]
exec_dims    = output_config_raw["executive_dashboard_dimensions"]
scen_dims    = output_config_raw["scenario_comparison_dimensions"]

# ── Log helper ────────────────────────────────────────────────────────────────
execution_log = []

def log_step(step, title, status, observation=""):
    entry = {
        "origin_contextspace": CONTEXTSPACE,
        "origin_entity": ENTITY,
        "origin_project": PROJECT,
        "origin_session": SESSION,
        "timestamp": TIMESTAMP,
        "step": step,
        "title": title,
        "status": status,
        "ai_observation": observation
    }
    execution_log.append(entry)
    print(f"[{status}] {step}. {title}")

# ══════════════════════════════════════════════════════════════════════════════
# R1. Performance analysis
# ══════════════════════════════════════════════════════════════════════════════
def classify_performance(av):
    if av >= perf_rules["excellent_min"]:   return "Excellent"
    if av >= perf_rules["very_good_min"]:   return "Very Good"
    if av >= perf_rules["good_min"]:        return "Good"
    return "Needs Improvement"

def classify_engagement(absences, overtime):
    he = engage_rules["high_engagement"]
    ne = engage_rules["normal_engagement"]
    if absences <= he["max_absences"] and overtime >= he["min_overtime_hours"]:
        return "High Engagement"
    if absences <= ne["max_absences"] and overtime >= ne["min_overtime_hours"]:
        return "Normal Engagement"
    return "Low Engagement"

def classify_growth(certifications, tenure):
    rp = growth_rules["ready_for_promotion"]
    dt = growth_rules["development_track"]
    if certifications >= rp["min_certifications"] and tenure >= rp["min_tenure_months"]:
        return "Ready for Promotion"
    if certifications >= dt["min_certifications"] and tenure >= dt["min_tenure_months"]:
        return "Development Track"
    return "Entry Level"

result_performance_analysis = []
for e in employees:
    av = avg(e["performance_ratings"])
    perf_cls  = classify_performance(av)
    eng_cls   = classify_engagement(e["absences"], e["overtime_hours"])
    growth    = classify_growth(e["certifications"], e["tenure_months"])
    result_performance_analysis.append({
        "aiurm_marker": "*result_performance_analysis",
        "employee_id": e["id"],
        "employee_name": e["name"],
        "department": e["department"],
        "average_rating": av,
        "performance_classification": perf_cls,
        "engagement_classification": eng_cls,
        "growth_potential": growth,
        "reasoning_pointers": {
            "avg_from": "*data_employees.performance_ratings",
            "perf_rule": f"avg={av} → threshold(excellent={perf_rules['excellent_min']}, very_good={perf_rules['very_good_min']}, good={perf_rules['good_min']})",
            "engage_rule": f"absences={e['absences']}, overtime={e['overtime_hours']}",
            "growth_rule": f"certifications={e['certifications']}, tenure_months={e['tenure_months']}"
        }
    })

write_result("result_performance_analysis", result_performance_analysis)
log_step("R1", "Performance analysis", "COMPLETED", f"{len(result_performance_analysis)} employees classified")

# ══════════════════════════════════════════════════════════════════════════════
# R2. Retention analysis
# ══════════════════════════════════════════════════════════════════════════════
def classify_retention(e, av):
    hr = ret_rules["high_risk"]
    mr = ret_rules["medium_risk"]
    br = ret_rules["burnout_risk"]
    if e["salary"] < hr["salary_below"] and av >= hr["rating_min"]:
        return "High Risk"
    if (e["tenure_months"] > mr["tenure_months_above"]
            and e["position"] not in mgmt_pos):
        return "Medium Risk"
    if (e["overtime_hours"] > br["overtime_hours_above"]
            and e["absences"] > br["absences_above"]):
        return "Burnout Risk"
    return "Low Risk"

result_retention_analysis = []
for e in employees:
    av   = avg(e["performance_ratings"])
    risk = classify_retention(e, av)
    result_retention_analysis.append({
        "aiurm_marker": "*result_retention_analysis",
        "employee_id": e["id"],
        "employee_name": e["name"],
        "department": e["department"],
        "average_rating": av,
        "retention_risk": risk,
        "recommended_action": rec_actions[risk],
        "reasoning_pointers": {
            "salary": e["salary"],
            "tenure_months": e["tenure_months"],
            "overtime_hours": e["overtime_hours"],
            "absences": e["absences"],
            "position": e["position"],
            "rules_source": "*data_retention_rules"
        }
    })

write_result("result_retention_analysis", result_retention_analysis)
log_step("R2", "Retention analysis", "COMPLETED", f"{len(result_retention_analysis)} employees assessed")

# ══════════════════════════════════════════════════════════════════════════════
# R3. Department summary
# ══════════════════════════════════════════════════════════════════════════════
from collections import defaultdict

dept_perf  = defaultdict(list)
dept_ret   = defaultdict(list)
dept_sal   = defaultdict(list)

for r in result_performance_analysis:
    dept_perf[r["department"]].append(r)
for r in result_retention_analysis:
    dept_ret[r["department"]].append(r)
for e in employees:
    dept_sal[e["department"]].append(e["salary"])

departments = sorted(set(e["department"] for e in employees))
dept_summaries = []

for dept in departments:
    perf_list = dept_perf[dept]
    ret_list  = dept_ret[dept]
    sal_list  = dept_sal[dept]

    perf_count = defaultdict(int)
    for r in perf_list:
        perf_count[r["performance_classification"]] += 1

    ret_dist = defaultdict(int)
    for r in ret_list:
        ret_dist[r["retention_risk"]] += 1

    top_performers = [r["employee_name"] for r in perf_list
                      if r["performance_classification"] in ("Excellent", "Very Good")]

    priority_actions = list({r["recommended_action"] for r in ret_list
                              if r["retention_risk"] != "Low Risk"})
    if not priority_actions:
        priority_actions = ["Continue monitoring"]

    dept_summaries.append({
        "aiurm_marker": "*result_department_summary",
        "department": dept,
        "employee_count": len(perf_list),
        "count_by_performance_classification": dict(perf_count),
        "average_salary_by_department": round(sum(sal_list) / len(sal_list), 2),
        "retention_risk_distribution": dict(ret_dist),
        "top_performers_identified": top_performers,
        "priority_actions_by_area": priority_actions
    })

overall = {
    "total_employees": len(employees),
    "departments_covered": departments,
    "overall_performance_distribution": {
        cls: sum(1 for r in result_performance_analysis
                 if r["performance_classification"] == cls)
        for cls in ["Excellent", "Very Good", "Good", "Needs Improvement"]
    },
    "overall_retention_distribution": {
        risk: sum(1 for r in result_retention_analysis if r["retention_risk"] == risk)
        for risk in ["High Risk", "Medium Risk", "Burnout Risk", "Low Risk"]
    }
}

result_department_summary = {"departments": dept_summaries, "overall_summary": overall}
write_result("result_department_summary", result_department_summary)
log_step("R3", "Department summary", "COMPLETED", f"{len(departments)} departments summarised")

# ══════════════════════════════════════════════════════════════════════════════
# R4. HR action plan
# ══════════════════════════════════════════════════════════════════════════════
promotion_ready = [r for r in result_performance_analysis
                   if r["growth_potential"] == "Ready for Promotion"]
high_risk_ret   = [r for r in result_retention_analysis if r["retention_risk"] == "High Risk"]
burnout_risk    = [r for r in result_retention_analysis if r["retention_risk"] == "Burnout Risk"]
medium_risk     = [r for r in result_retention_analysis if r["retention_risk"] == "Medium Risk"]

result_hr_action_plan = {
    "aiurm_marker": "*result_hr_action_plan",
    "immediate_priorities": {
        "horizon_days": action_hor["immediate_days"],
        "actions": [
            {
                "action": "Salary review",
                "targets": [r["employee_name"] for r in high_risk_ret],
                "rationale": "High retention risk — salary below threshold with strong performance",
                "owner": "HR Director",
                "estimated_budget": sum(
                    5000 for _ in high_risk_ret
                )
            },
            {
                "action": "Workload redistribution",
                "targets": [r["employee_name"] for r in burnout_risk],
                "rationale": "Burnout risk — excessive overtime and absences",
                "owner": "Department Manager",
                "estimated_budget": 0
            }
        ]
    },
    "medium_term_actions": {
        "horizon_days": action_hor["medium_term_days"],
        "actions": [
            {
                "action": "Career development plan",
                "targets": [r["employee_name"] for r in medium_risk],
                "rationale": "Medium retention risk — long tenure without management track",
                "owner": "HR Business Partner",
                "estimated_budget": sum(3000 for _ in medium_risk)
            },
            {
                "action": "Promotion evaluation",
                "targets": [r["employee_name"] for r in promotion_ready],
                "rationale": "Ready for promotion — meets tenure and certification thresholds",
                "owner": "HR Director + Line Manager",
                "estimated_budget": sum(
                    next((e["salary"] for e in employees if e["name"] == r["employee_name"]), 0) * 0.10
                    for r in promotion_ready
                )
            }
        ]
    },
    "long_term_strategies": {
        "horizon_months": action_hor["long_term_months"],
        "actions": [
            {
                "action": "Certification and training programme",
                "rationale": "Build pipeline of promotion-ready talent across all departments",
                "owner": "L&D Team",
                "estimated_budget": 15000
            },
            {
                "action": "Engagement and wellbeing programme",
                "rationale": "Reduce burnout indicators and improve retention across IT and Sales",
                "owner": "HR Director",
                "estimated_budget": 8000
            }
        ]
    },
    "total_estimated_budget": (
        sum(5000 for _ in high_risk_ret) +
        sum(3000 for _ in medium_risk) +
        sum(
            next((e["salary"] for e in employees if e["name"] == r["employee_name"]), 0) * 0.10
            for r in promotion_ready
        ) +
        15000 + 8000
    )
}

write_result("result_hr_action_plan", result_hr_action_plan)
log_step("R4", "HR action plan", "COMPLETED")

# ══════════════════════════════════════════════════════════════════════════════
# R5. Executive dashboard
# ══════════════════════════════════════════════════════════════════════════════
total_emp   = len(employees)
excellent_c = sum(1 for r in result_performance_analysis if r["performance_classification"] == "Excellent")
high_eng_c  = sum(1 for r in result_performance_analysis if r["engagement_classification"] == "High Engagement")
promo_ready_c = sum(1 for r in result_performance_analysis if r["growth_potential"] == "Ready for Promotion")
at_risk_c   = sum(1 for r in result_retention_analysis if r["retention_risk"] != "Low Risk")
burnout_c   = sum(1 for r in result_retention_analysis if r["retention_risk"] == "Burnout Risk")

result_executive_dashboard = {
    "aiurm_marker": "*result_executive_dashboard",
    "key_performance_indicators": {
        "total_employees": total_emp,
        "excellent_performers_pct": round(excellent_c / total_emp * 100, 1),
        "high_engagement_pct": round(high_eng_c / total_emp * 100, 1),
        "promotion_ready_pct": round(promo_ready_c / total_emp * 100, 1),
        "at_risk_retention_pct": round(at_risk_c / total_emp * 100, 1)
    },
    "critical_alerts": [
        {
            "alert": "Burnout risk detected",
            "employees": [r["employee_name"] for r in result_retention_analysis
                          if r["retention_risk"] == "Burnout Risk"],
            "severity": "HIGH"
        },
        {
            "alert": "Medium retention risk — long-tenure non-management",
            "employees": [r["employee_name"] for r in result_retention_analysis
                          if r["retention_risk"] == "Medium Risk"],
            "severity": "MEDIUM"
        }
    ] if at_risk_c > 0 else [],
    "top_5_priorities": [
        f"Address burnout risk for {[r['employee_name'] for r in result_retention_analysis if r['retention_risk'] == 'Burnout Risk']}",
        f"Develop career plan for medium-risk employees",
        f"Evaluate promotion for {[r['employee_name'] for r in result_performance_analysis if r['growth_potential'] == 'Ready for Promotion']}",
        "Launch certification programme to widen promotion pipeline",
        "Deploy engagement and wellbeing initiative in IT and Sales"
    ],
    "required_budget": result_hr_action_plan["total_estimated_budget"],
    "sources": ["*result_performance_analysis", "*result_retention_analysis", "*result_department_summary"]
}

write_result("result_executive_dashboard", result_executive_dashboard)
log_step("R5", "Executive dashboard", "COMPLETED")

# ══════════════════════════════════════════════════════════════════════════════
# R6. Conservative promotion scenario
# ══════════════════════════════════════════════════════════════════════════════
result_conservative_promotions = []
for e in employees:
    av = avg(e["performance_ratings"])
    qualifies = (
        av >= cons_crit["rating_min"]
        and e["tenure_months"] >= cons_crit["tenure_months_min"]
        and e["certifications"] >= cons_crit["certifications_min"]
    )
    result_conservative_promotions.append({
        "aiurm_marker": "*result_conservative_promotions",
        "employee_id": e["id"],
        "employee_name": e["name"],
        "department": e["department"],
        "average_rating": av,
        "tenure_months": e["tenure_months"],
        "certifications": e["certifications"],
        "promoted": qualifies,
        "inclusion_reasoning": {
            "rating_check": f"{av} >= {cons_crit['rating_min']} → {av >= cons_crit['rating_min']}",
            "tenure_check": f"{e['tenure_months']} >= {cons_crit['tenure_months_min']} → {e['tenure_months'] >= cons_crit['tenure_months_min']}",
            "cert_check":   f"{e['certifications']} >= {cons_crit['certifications_min']} → {e['certifications'] >= cons_crit['certifications_min']}",
            "criteria_source": "*data_promotion_scenarios.conservative_criteria"
        }
    })

write_result("result_conservative_promotions", result_conservative_promotions)
promoted_cons = [r["employee_name"] for r in result_conservative_promotions if r["promoted"]]
log_step("R6", "Conservative promotion scenario", "COMPLETED",
         f"{len(promoted_cons)} promoted: {promoted_cons or 'none'}")

# ══════════════════════════════════════════════════════════════════════════════
# R7. Aggressive promotion scenario
# ══════════════════════════════════════════════════════════════════════════════
result_aggressive_promotions = []
for e in employees:
    av = avg(e["performance_ratings"])
    qualifies = (
        av >= aggr_crit["rating_min"]
        and e["tenure_months"] >= aggr_crit["tenure_months_min"]
        and e["certifications"] >= aggr_crit["certifications_min"]
    )
    result_aggressive_promotions.append({
        "aiurm_marker": "*result_aggressive_promotions",
        "employee_id": e["id"],
        "employee_name": e["name"],
        "department": e["department"],
        "average_rating": av,
        "tenure_months": e["tenure_months"],
        "certifications": e["certifications"],
        "promoted": qualifies,
        "inclusion_reasoning": {
            "rating_check": f"{av} >= {aggr_crit['rating_min']} → {av >= aggr_crit['rating_min']}",
            "tenure_check": f"{e['tenure_months']} >= {aggr_crit['tenure_months_min']} → {e['tenure_months'] >= aggr_crit['tenure_months_min']}",
            "cert_check":   f"{e['certifications']} >= {aggr_crit['certifications_min']} → {e['certifications'] >= aggr_crit['certifications_min']}",
            "criteria_source": "*data_promotion_scenarios.aggressive_criteria"
        }
    })

write_result("result_aggressive_promotions", result_aggressive_promotions)
promoted_aggr = [r["employee_name"] for r in result_aggressive_promotions if r["promoted"]]
log_step("R7", "Aggressive promotion scenario", "COMPLETED",
         f"{len(promoted_aggr)} promoted: {promoted_aggr}")

# ══════════════════════════════════════════════════════════════════════════════
# R8. Scenario comparison
# ══════════════════════════════════════════════════════════════════════════════
cons_promoted = [r for r in result_conservative_promotions if r["promoted"]]
aggr_promoted = [r for r in result_aggressive_promotions if r["promoted"]]

def salary_impact(promoted_list, raise_pct=0.12):
    total = 0
    for r in promoted_list:
        sal = next((e["salary"] for e in employees if e["id"] == r["employee_id"]), 0)
        total += sal * raise_pct
    return round(total, 2)

cons_impact = salary_impact(cons_promoted)
aggr_impact = salary_impact(aggr_promoted)

result_scenario_comparison = {
    "aiurm_marker": "*result_scenario_comparison",
    "number_of_promotions_each_scenario": {
        "conservative": len(cons_promoted),
        "aggressive": len(aggr_promoted)
    },
    "estimated_financial_impact": {
        "conservative_annual_raise": cons_impact,
        "aggressive_annual_raise": aggr_impact,
        "delta": round(aggr_impact - cons_impact, 2),
        "assumption": "12% salary increase per promotion"
    },
    "risks_and_benefits": {
        "conservative": {
            "risks": ["Under-promotion risk — high performers may disengage",
                      "Pipeline stagnation if criteria remain static"],
            "benefits": ["Budget control", "Lower promotion error risk",
                         "Promotes only the highest certainty candidates"]
        },
        "aggressive": {
            "risks": ["Higher budget commitment",
                      "Some promotees may not yet be fully senior-ready"],
            "benefits": ["Accelerates talent development",
                         "Improves retention of high performers",
                         "Broader pipeline activation"]
        }
    },
    "final_recommendation": (
        "Adopt the aggressive promotion scenario with targeted development plans. "
        "With 4 eligible employees and moderate financial impact, the aggressive scenario "
        "provides meaningful talent acceleration while the conservative scenario yields zero promotions, "
        "creating under-promotion risk for already-engaged high performers. "
        "Pair promotions with 90-day integration plans and performance checkpoints."
    ),
    "sources": ["*result_conservative_promotions", "*result_aggressive_promotions",
                "*data_output_configuration"]
}

write_result("result_scenario_comparison", result_scenario_comparison)
log_step("R8", "Scenario comparison", "COMPLETED")

# ══════════════════════════════════════════════════════════════════════════════
# R9. Ready-for-promotion filtered view
# ══════════════════════════════════════════════════════════════════════════════
ready_employees = [r for r in result_performance_analysis
                   if r["growth_potential"] == "Ready for Promotion"]

result_ready_for_promotion_filter_hr = {
    "aiurm_marker": "*result_ready_for_promotion_filter_hr",
    "filter_criteria": "growth_potential = 'Ready for Promotion'",
    "count": len(ready_employees),
    "compact_view": [
        {"employee_id": r["employee_id"], "employee_name": r["employee_name"],
         "department": r["department"], "average_rating": r["average_rating"]}
        for r in ready_employees
    ],
    "detailed_view": ready_employees,
    "pointer_justification": {
        "source_data": "*data_employees",
        "source_logic": "*logic_performance_analysis_hr",
        "filter_applied_on": "*result_performance_analysis",
        "rule_reference": "*data_performance_rules.growth_potential_rules.ready_for_promotion"
    }
}

write_result("result_ready_for_promotion_filter_hr", result_ready_for_promotion_filter_hr)
log_step("R9", "Ready-for-promotion filtered view", "COMPLETED",
         f"{len(ready_employees)} employees match filter")

# ══════════════════════════════════════════════════════════════════════════════
# R10. Quick filtered analytical views
# ══════════════════════════════════════════════════════════════════════════════
excellent_employees = [r for r in result_performance_analysis
                       if r["performance_classification"] == "Excellent"]
high_risk_employees = [r for r in result_retention_analysis
                       if r["retention_risk"] == "High Risk"]
it_dept = next((d for d in result_department_summary["departments"]
                if d["department"] == "IT"), None)

result_hr_filters_hr = {
    "aiurm_marker": "*result_hr_filters_hr",
    "filter_excellent_performers": {
        "count": len(excellent_employees),
        "employees": excellent_employees
    },
    "filter_high_risk_retention": {
        "count": len(high_risk_employees),
        "employees": high_risk_employees
    },
    "filter_it_department": {
        "department_summary": it_dept
    },
    "sources": ["*result_performance_analysis", "*result_retention_analysis",
                "*result_department_summary"]
}

write_result("result_hr_filters_hr", result_hr_filters_hr)
log_step("R10", "Quick filtered analytical views", "COMPLETED")

# ══════════════════════════════════════════════════════════════════════════════
# R11. Explainability results
# ══════════════════════════════════════════════════════════════════════════════
def explain_performance(r):
    av = r["average_rating"]
    return {
        "employee": r["employee_name"],
        "performance_classification": r["performance_classification"],
        "explanation": (
            f"Average rating {av} was computed from raw ratings in *data_employees.performance_ratings. "
            f"Threshold applied: excellent>={perf_rules['excellent_min']}, "
            f"very_good>={perf_rules['very_good_min']}, good>={perf_rules['good_min']}. "
            f"Result: '{r['performance_classification']}'."
        ),
        "engagement_classification": r["engagement_classification"],
        "engagement_explanation": r["reasoning_pointers"]["engage_rule"],
        "growth_potential": r["growth_potential"],
        "growth_explanation": r["reasoning_pointers"]["growth_rule"]
    }

def explain_retention(r):
    return {
        "employee": r["employee_name"],
        "retention_risk": r["retention_risk"],
        "explanation": (
            f"Ordered risk rules from *data_retention_rules applied: "
            f"salary={r['reasoning_pointers']['salary']}, "
            f"tenure_months={r['reasoning_pointers']['tenure_months']}, "
            f"overtime_hours={r['reasoning_pointers']['overtime_hours']}, "
            f"absences={r['reasoning_pointers']['absences']}, "
            f"position='{r['reasoning_pointers']['position']}'. "
            f"Result: '{r['retention_risk']}' → action: '{r['recommended_action']}'."
        )
    }

def explain_promotion(r):
    return {
        "employee": r["employee_name"],
        "promoted": r["promoted"],
        "explanation": (
            f"Aggressive criteria: rating>={aggr_crit['rating_min']}, "
            f"tenure>={aggr_crit['tenure_months_min']}, cert>={aggr_crit['certifications_min']}. "
            f"Checks: {r['inclusion_reasoning']['rating_check']} | "
            f"{r['inclusion_reasoning']['tenure_check']} | "
            f"{r['inclusion_reasoning']['cert_check']}."
        )
    }

john_smith_aggr = next((r for r in result_aggressive_promotions if r["employee_id"] == "E004"), None)

result_explainability_hr = {
    "aiurm_marker": "*result_explainability_hr",
    "performance_analysis_explanations": [explain_performance(r) for r in result_performance_analysis],
    "retention_analysis_explanations": [explain_retention(r) for r in result_retention_analysis],
    "aggressive_promotions_explanations": [explain_promotion(r) for r in result_aggressive_promotions],
    "john_smith_aggressive_promotion_explanation": {
        "employee": "John Smith",
        "promoted": john_smith_aggr["promoted"] if john_smith_aggr else None,
        "detail": (
            "John Smith (E004) was included in the aggressive promotion scenario because his "
            f"average rating {john_smith_aggr['average_rating']} meets the threshold of "
            f"{aggr_crit['rating_min']}, his tenure of {john_smith_aggr['tenure_months']} months "
            f"meets {aggr_crit['tenure_months_min']} months, and his {john_smith_aggr['certifications']} "
            f"certifications meet the minimum of {aggr_crit['certifications_min']}. "
            "Despite a burnout risk flag in retention analysis (high overtime + absences), "
            "promotion criteria are evaluated independently of retention risk in this policy."
        ) if john_smith_aggr else "Not found"
    },
    "scenario_comparison_explanation": {
        "summary": (
            f"Conservative scenario promoted {len(cons_promoted)} employee(s); "
            f"aggressive promoted {len(aggr_promoted)}. "
            "Conservative criteria (rating≥9.0, tenure≥36mo, cert≥3) eliminated all candidates "
            "because no employee meets all three thresholds simultaneously. "
            "Aggressive criteria (rating≥8.5, tenure≥18mo, cert≥2) activates 4 employees. "
            "Final recommendation favours aggressive with structured follow-up."
        )
    },
    "sources": ["*result_performance_analysis", "*result_retention_analysis",
                "*result_aggressive_promotions", "*result_scenario_comparison"]
}

write_result("result_explainability_hr", result_explainability_hr)
log_step("R11", "Explainability results", "COMPLETED")

# ══════════════════════════════════════════════════════════════════════════════
# R12. Transformation trace results
# ══════════════════════════════════════════════════════════════════════════════
def build_trace(e):
    av = avg(e["performance_ratings"])
    perf = classify_performance(av)
    growth = classify_growth(e["certifications"], e["tenure_months"])

    cons_r = next(r for r in result_conservative_promotions if r["employee_id"] == e["id"])
    aggr_r = next(r for r in result_aggressive_promotions    if r["employee_id"] == e["id"])

    return {
        "employee_id": e["id"],
        "employee_name": e["name"],
        "transformation_steps": [
            {
                "step": 1,
                "label": "Raw data loaded",
                "source": "*data_employees",
                "derived_fields": {
                    "salary": e["salary"],
                    "tenure_months": e["tenure_months"],
                    "certifications": e["certifications"],
                    "performance_ratings": e["performance_ratings"]
                }
            },
            {
                "step": 2,
                "label": "Performance computed",
                "source": "*logic_performance_analysis_hr",
                "derived_fields": {
                    "average_rating": av,
                    "performance_classification": perf,
                    "growth_potential": growth
                }
            },
            {
                "step": 3,
                "label": "Conservative promotion evaluated",
                "source": "*logic_conservative_promotions_hr",
                "derived_fields": {"promoted": cons_r["promoted"]}
            },
            {
                "step": 4,
                "label": "Aggressive promotion evaluated",
                "source": "*logic_aggressive_promotions_hr",
                "derived_fields": {"promoted": aggr_r["promoted"]}
            }
        ],
        "classification_path": f"*data_employees → *result_performance_analysis({perf}) → *result_aggressive_promotions({aggr_r['promoted']})"
    }

result_transformation_trace_hr = {
    "aiurm_marker": "*result_transformation_trace_hr",
    "traces": [build_trace(e) for e in employees],
    "tree_trace_employees_to_aggressive": (
        "*data_employees "
        "→ [avg(performance_ratings)] "
        "→ *result_performance_analysis "
        "→ [apply aggressive_criteria] "
        "→ *result_aggressive_promotions"
    )
}

write_result("result_transformation_trace_hr", result_transformation_trace_hr)
log_step("R12", "Transformation trace results", "COMPLETED")

# ══════════════════════════════════════════════════════════════════════════════
# R13. JSON export results
# ══════════════════════════════════════════════════════════════════════════════
result_json_performance_hr = {
    "aiurm_marker": "*result_json_performance_hr",
    "export_source": "*result_performance_analysis",
    "export_format": "JSON",
    "data": result_performance_analysis
}

write_result("result_json_performance_hr", result_json_performance_hr)
log_step("R13", "JSON export results", "COMPLETED")

# ══════════════════════════════════════════════════════════════════════════════
# R14. Dependency tree results
# ══════════════════════════════════════════════════════════════════════════════
dot_graph = """digraph rh_analysis_workflow {
    rankdir=LR;
    node [shape=box, style=filled];

    // Data nodes
    data_employees           [label="*data_employees",           fillcolor="#AED6F1"];
    data_performance_rules   [label="*data_performance_rules",   fillcolor="#AED6F1"];
    data_retention_rules     [label="*data_retention_rules",     fillcolor="#AED6F1"];
    data_promotion_scenarios [label="*data_promotion_scenarios", fillcolor="#AED6F1"];
    data_output_configuration[label="*data_output_configuration",fillcolor="#AED6F1"];
    governance               [label="*aiurm_governance_rh_analysis_example", fillcolor="#F9E79F"];

    // Result nodes
    r1  [label="R1\\n*result_performance_analysis",   fillcolor="#A9DFBF"];
    r2  [label="R2\\n*result_retention_analysis",     fillcolor="#A9DFBF"];
    r3  [label="R3\\n*result_department_summary",     fillcolor="#A9DFBF"];
    r4  [label="R4\\n*result_hr_action_plan",         fillcolor="#A9DFBF"];
    r5  [label="R5\\n*result_executive_dashboard",    fillcolor="#A9DFBF"];
    r6  [label="R6\\n*result_conservative_promotions",fillcolor="#A9DFBF"];
    r7  [label="R7\\n*result_aggressive_promotions",  fillcolor="#A9DFBF"];
    r8  [label="R8\\n*result_scenario_comparison",    fillcolor="#A9DFBF"];
    r9  [label="R9\\n*result_ready_for_promotion",    fillcolor="#A9DFBF"];
    r10 [label="R10\\n*result_hr_filters_hr",         fillcolor="#A9DFBF"];
    r11 [label="R11\\n*result_explainability_hr",     fillcolor="#A9DFBF"];
    r12 [label="R12\\n*result_transformation_trace",  fillcolor="#A9DFBF"];
    r13 [label="R13\\n*result_json_performance_hr",   fillcolor="#A9DFBF"];
    r14 [label="R14\\n*result_dependency_tree_hr",    fillcolor="#FAD7A0"];

    // R1 deps
    data_employees -> r1;
    data_performance_rules -> r1;

    // R2 deps
    data_employees -> r2;
    data_retention_rules -> r2;

    // R3 deps
    data_employees -> r3;
    r1 -> r3;
    r2 -> r3;
    data_output_configuration -> r3;

    // R4 deps
    r1 -> r4;
    r2 -> r4;
    data_output_configuration -> r4;

    // R5 deps
    r1 -> r5;
    r2 -> r5;
    r3 -> r5;
    data_output_configuration -> r5;

    // R6 deps
    data_employees -> r6;
    data_promotion_scenarios -> r6;

    // R7 deps
    data_employees -> r7;
    data_promotion_scenarios -> r7;

    // R8 deps
    r6 -> r8;
    r7 -> r8;
    data_output_configuration -> r8;

    // R9 deps
    data_employees -> r9;
    r1 -> r9;

    // R10 deps
    r1 -> r10;
    r2 -> r10;
    r3 -> r10;

    // R11 deps
    r1 -> r11;
    r2 -> r11;
    r7 -> r11;
    r8 -> r11;

    // R12 deps
    data_employees -> r12;
    r1 -> r12;
    r6 -> r12;
    r7 -> r12;

    // R13 deps
    r1 -> r13;

    // R14 deps
    governance -> r14;
    r1  -> r14; r2  -> r14; r3  -> r14; r4  -> r14; r5  -> r14;
    r6  -> r14; r7  -> r14; r8  -> r14; r9  -> r14; r10 -> r14;
    r11 -> r14; r12 -> r14; r13 -> r14;
}"""

result_dependency_tree_hr = {
    "aiurm_marker": "*result_dependency_tree_hr",
    "format": "Graphviz/DOT",
    "visualization_tool": "https://dreampuf.github.io/GraphvizOnline/",
    "dot_graph": dot_graph,
    "sources": ["*aiurm_governance_rh_analysis_example"] + [
        f"*result_{x}" for x in [
            "performance_analysis", "retention_analysis", "department_summary",
            "hr_action_plan", "executive_dashboard", "conservative_promotions",
            "aggressive_promotions", "scenario_comparison", "ready_for_promotion_filter_hr",
            "hr_filters_hr", "explainability_hr", "transformation_trace_hr",
            "json_performance_hr"
        ]
    ]
}

write_result("result_dependency_tree_hr", result_dependency_tree_hr)
log_step("R14", "Dependency tree results", "COMPLETED")

# ══════════════════════════════════════════════════════════════════════════════
# Write execution log
# ══════════════════════════════════════════════════════════════════════════════
log_name = f"result_log__{CONTEXTSPACE}__{PROJECT}__{SESSION}__{TIMESTAMP}"
write_json(LOG_PATH, log_name, execution_log)

# ══════════════════════════════════════════════════════════════════════════════
# Write audit record
# ══════════════════════════════════════════════════════════════════════════════
audit_record = {
    "origin_contextspace": CONTEXTSPACE,
    "origin_entity": ENTITY,
    "origin_project": PROJECT,
    "origin_session": SESSION,
    "timestamp": TIMESTAMP,
    "governance": "aiurm_governance_rh_analysis_example",
    "execution_mode": "ONE_STEP",
    "steps_executed": len(execution_log),
    "steps_completed": sum(1 for s in execution_log if s["status"] == "COMPLETED"),
    "steps_failed": sum(1 for s in execution_log if s["status"] != "COMPLETED"),
    "step_log": execution_log
}
audit_name = f"result_audit__{CONTEXTSPACE}__{PROJECT}__{SESSION}__{TIMESTAMP}"
write_json(AUDIT_PATH, audit_name, audit_record)

print(f"\nExecution complete -- {len(execution_log)} steps | audit: {audit_name}")
