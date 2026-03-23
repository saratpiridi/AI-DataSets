import csv
import random
from pathlib import Path


SCHEMA = [
    "record_id",
    "scenario_type",
    "task_description",
    "input_complexity",
    "ai_recommendation",
    "confidence_score",
    "explainability_score",
    "fairness_risk",
    "compliance_risk",
    "human_override",
    "override_reason",
    "final_decision",
    "outcome_status",
    "processing_time_seconds",
    "notes",
]

SCENARIO_DESCRIPTIONS = {
    "document_approval": [
        "Review a policy acknowledgment form with missing signature metadata.",
        "Assess a grant submission packet with one incomplete supporting attachment.",
        "Route a procurement memo that contains conflicting approval dates.",
        "Evaluate a travel exception request with manually entered cost estimates.",
        "Check a contract addendum requiring dual-approval verification.",
        "Process a quality assurance checklist uploaded in mixed file formats.",
        "Review a budget adjustment request flagged for unusual timing.",
        "Assess a supplier registration form with partially standardized fields.",
        "Validate a maintenance authorization packet containing handwritten notes.",
        "Examine a project closure document with unresolved checklist items.",
    ],
    "invoice_processing": [
        "Process a recurring service invoice with a changed line-item description.",
        "Review a shipment invoice that references an outdated purchase order code.",
        "Assess a multi-line facilities invoice with tax rounding discrepancies.",
        "Validate a training expense invoice submitted with a blurred receipt image.",
        "Check a consulting invoice that exceeds the expected monthly threshold.",
        "Process a hardware invoice with partially matched item quantities.",
        "Review a reimbursement invoice missing a secondary cost center tag.",
        "Assess a subscription invoice with duplicate-looking service periods.",
        "Validate an invoice containing a manual discount justification note.",
        "Check a logistics invoice tied to a delayed delivery event.",
    ],
    "customer_request_routing": [
        "Route a billing support request containing mixed refund and access questions.",
        "Classify a service complaint submitted in concise, ambiguous language.",
        "Triage a product inquiry that mentions urgent delivery and cancellation risk.",
        "Route a multilingual request that alternates between technical and billing topics.",
        "Classify a renewal question with inconsistent account reference details.",
        "Triage a feedback submission that includes a hidden request for escalation.",
        "Route a support message referencing multiple unresolved incidents.",
        "Classify a portal access complaint from a newly migrated user segment.",
        "Triage a contract clarification request with sparse historical context.",
        "Route a customer note that combines feature feedback and outage concerns.",
    ],
    "employee_onboarding": [
        "Review a starter checklist for a remote analyst with pending equipment needs.",
        "Assess an onboarding package with inconsistent role and department labels.",
        "Validate an orientation registration request submitted after the deadline window.",
        "Review a system setup request for a contractor with limited access duration.",
        "Assess a benefits enrollment packet missing one optional acknowledgement field.",
        "Validate a workstation request with overlapping hardware preferences.",
        "Review a background screening follow-up for a time-sensitive start date.",
        "Assess a relocation onboarding form with manually adjusted travel details.",
        "Validate a training assignment request for a cross-functional new hire.",
        "Review an onboarding checklist that includes role-specific policy exemptions.",
    ],
    "claims_review": [
        "Review a service reimbursement claim with one unsupported cost category.",
        "Assess a property repair claim submitted with low-resolution image evidence.",
        "Validate a travel disruption claim containing conflicting timeline entries.",
        "Review a wellness benefit claim with a missing provider classification.",
        "Assess a replacement claim for damaged equipment with duplicate serial text.",
        "Validate a claim packet that combines urgent review language with sparse detail.",
        "Review a claims submission with an unusually high manual adjustment request.",
        "Assess a resubmitted claim after a previous documentation rejection.",
        "Validate a claim including handwritten annotations on the primary form.",
        "Review a dependent support claim missing one verification timestamp.",
    ],
    "compliance_screening": [
        "Screen a vendor profile update that includes incomplete ownership details.",
        "Review a transaction note that triggers an elevated policy keyword match.",
        "Assess a registry screening result with partial identity overlap.",
        "Screen a partner onboarding record with conflicting jurisdiction fields.",
        "Review a flagged activity summary requiring secondary policy interpretation.",
        "Assess a due diligence packet with stale supporting documentation dates.",
        "Screen a payment release request with a nonstandard exception annotation.",
        "Review a policy monitoring alert tied to inconsistent classification labels.",
        "Assess a distribution request involving a restricted geography code.",
        "Screen a renewal package with missing beneficial control disclosures.",
    ],
    "case_prioritization": [
        "Prioritize an incident case with moderate impact but repeated reopen events.",
        "Rank a service interruption case affecting a low-volume but high-value channel.",
        "Prioritize a quality issue report with limited evidence and urgent language.",
        "Rank a field operations case that spans multiple unresolved dependencies.",
        "Prioritize a policy exception case with conflicting severity indicators.",
        "Rank a service backlog item linked to a time-sensitive regulatory milestone.",
        "Prioritize a technical fault report from a recently migrated workflow.",
        "Rank an operations complaint with vague impact and repeated follow-ups.",
        "Prioritize a high-visibility case with incomplete ownership assignment.",
        "Rank a resource contention issue involving several dependent teams.",
    ],
    "chatbot_escalation": [
        "Evaluate a support chat session where the user repeatedly asks for a specialist.",
        "Review a chatbot exchange that mixes billing confusion with emotional language.",
        "Assess a conversation containing contradictory self-service confirmations.",
        "Evaluate a chat transcript with repeated requests outside workflow scope.",
        "Review a session where the user rejects automated troubleshooting steps.",
        "Assess a conversation that includes an unresolved complaint and refund request.",
        "Evaluate a chat transcript with multiple topic changes in a short window.",
        "Review a self-service conversation containing low clarity intent signals.",
        "Assess a support chat involving accessibility-related assistance needs.",
        "Evaluate a chatbot conversation with a high-friction authentication loop.",
    ],
    "access_request_validation": [
        "Validate a role-based access request with mismatched business justification text.",
        "Review a temporary access request submitted without an end-date rationale.",
        "Assess a privileged access request with overlapping approval authority.",
        "Validate a shared workspace access form referencing an outdated team name.",
        "Review an emergency access request submitted during non-business hours.",
        "Assess a request to extend repository access beyond the standard review cycle.",
        "Validate a data-view permission request with incomplete training confirmation.",
        "Review a contractor access extension request missing one sponsor response.",
        "Assess a cross-functional access request with ambiguous least-privilege scope.",
        "Validate an application role request containing inconsistent environment labels.",
    ],
    "exception_handling": [
        "Review a workflow exception raised after a failed duplicate detection step.",
        "Assess a process exception involving a missing upstream status update.",
        "Validate an exception queue item with partial retry history metadata.",
        "Review a manually reopened automation exception with stale system notes.",
        "Assess a failed routing exception tied to inconsistent priority markers.",
        "Validate an exception case triggered by a malformed attachment bundle.",
        "Review a fallback processing exception for a time-sensitive transaction.",
        "Assess an exception item with conflicting timestamps from parallel events.",
        "Validate a workflow bypass request linked to repeated parsing failures.",
        "Review an exception case where the prior remediation record is incomplete.",
    ],
}

SCENARIO_COMPLEXITY = {
    "document_approval": ["Low", "Medium", "Medium", "High"],
    "invoice_processing": ["Low", "Medium", "Medium", "High"],
    "customer_request_routing": ["Medium", "Medium", "High"],
    "employee_onboarding": ["Low", "Medium", "High"],
    "claims_review": ["Medium", "High", "High"],
    "compliance_screening": ["Medium", "High", "High"],
    "case_prioritization": ["Low", "Medium", "High"],
    "chatbot_escalation": ["Low", "Medium", "High"],
    "access_request_validation": ["Medium", "High"],
    "exception_handling": ["Medium", "High", "High"],
}

LOW_CONFIDENCE_REASONS = [
    "Low model confidence triggered mandatory human review.",
    "Confidence fell below the autonomous decision threshold.",
    "Reviewer intervened because the prediction confidence was insufficient.",
]

HIGH_COMPLIANCE_REASONS = [
    "High compliance risk required reviewer sign-off before completion.",
    "Policy-sensitive conditions forced manual review by a compliance reviewer.",
    "Human review was required due to elevated compliance exposure.",
]

HIGH_FAIRNESS_REASONS = [
    "Potential fairness concerns required a human equity check.",
    "High fairness risk triggered a manual bias review.",
    "Reviewer intervened to inspect a possible disparate impact pattern.",
]

LOW_EXPLAINABILITY_REASONS = [
    "The recommendation explanation was too weak for automated handling.",
    "Low explainability score required human interpretation of the result.",
    "Reviewer intervened because the rationale transparency was insufficient.",
]

NOTES_POOL = [
    "Synthetic record for trustworthy automation benchmarking.",
    "Generated for open research on human-in-the-loop governance.",
    "Represents a generic operational workflow decision scenario.",
    "Designed to support analysis of risk-aware automation behavior.",
    "Suitable for reproducible experiments with synthetic decision data.",
]


def determine_ai_recommendation(confidence_score, fairness_risk, compliance_risk, explainability_score):
    if compliance_risk == "High":
        return "Escalate for compliance review"
    if fairness_risk == "High":
        return "Defer pending fairness review"
    if confidence_score < 0.62:
        return "Defer for additional evidence"
    if explainability_score <= 2:
        return "Escalate for interpretability review"
    if confidence_score >= 0.84 and fairness_risk == "Low" and compliance_risk == "Low":
        return "Approve automatically"
    if confidence_score <= 0.72 and (fairness_risk == "Medium" or compliance_risk == "Medium"):
        return "Escalate for manual assessment"
    if confidence_score <= 0.69:
        return "Defer for additional evidence"
    return "Approve with monitoring"


def determine_override(confidence_score, fairness_risk, compliance_risk, explainability_score):
    return (
        confidence_score < 0.70
        or compliance_risk == "High"
        or fairness_risk == "High"
        or explainability_score <= 2
    )


def determine_override_reason(confidence_score, fairness_risk, compliance_risk, explainability_score, rng):
    reasons = []
    if confidence_score < 0.70:
        reasons.append(rng.choice(LOW_CONFIDENCE_REASONS))
    if compliance_risk == "High":
        reasons.append(rng.choice(HIGH_COMPLIANCE_REASONS))
    if fairness_risk == "High":
        reasons.append(rng.choice(HIGH_FAIRNESS_REASONS))
    if explainability_score <= 2:
        reasons.append(rng.choice(LOW_EXPLAINABILITY_REASONS))
    return " ".join(reasons) if reasons else "None"


def determine_final_decision(
    ai_recommendation,
    human_override,
    confidence_score,
    fairness_risk,
    compliance_risk,
    explainability_score,
    rng,
):
    if human_override == "No":
        if ai_recommendation.startswith("Approve"):
            return "Approved"
        if "Defer" in ai_recommendation:
            return "Deferred"
        return "Escalated"

    if compliance_risk == "High":
        return "Rejected" if confidence_score < 0.66 or explainability_score <= 2 else "Escalated"
    if fairness_risk == "High":
        return "Deferred" if confidence_score < 0.68 else "Escalated"
    if confidence_score < 0.60:
        return "Rejected"
    if confidence_score < 0.70:
        return "Deferred" if rng.random() < 0.55 else "Escalated"
    if explainability_score <= 2:
        if fairness_risk == "Low" and compliance_risk == "Low" and confidence_score >= 0.82:
            return "Approved"
        return "Escalated"
    return "Escalated"


def determine_processing_time(complexity, human_override, compliance_risk, rng):
    base_ranges = {
        "Low": (5, 35),
        "Medium": (20, 75),
        "High": (45, 120),
    }
    low, high = base_ranges[complexity]
    time_value = rng.randint(low, high)
    if human_override == "Yes":
        time_value = min(120, time_value + rng.randint(8, 18))
    if compliance_risk == "High":
        time_value = min(120, time_value + rng.randint(4, 12))
    return max(5, min(120, time_value))


def build_record(record_index, scenario_type, task_description, rng):
    confidence_score = round(rng.uniform(0.50, 0.99), 2)
    explainability_score = rng.randint(1, 5)
    fairness_risk = rng.choices(["Low", "Medium", "High"], weights=[0.58, 0.27, 0.15], k=1)[0]
    compliance_risk = rng.choices(["Low", "Medium", "High"], weights=[0.52, 0.31, 0.17], k=1)[0]
    input_complexity = rng.choice(SCENARIO_COMPLEXITY[scenario_type])
    ai_recommendation = determine_ai_recommendation(
        confidence_score, fairness_risk, compliance_risk, explainability_score
    )
    human_override = "Yes" if determine_override(
        confidence_score, fairness_risk, compliance_risk, explainability_score
    ) else "No"
    override_reason = determine_override_reason(
        confidence_score, fairness_risk, compliance_risk, explainability_score, rng
    )
    final_decision = determine_final_decision(
        ai_recommendation,
        human_override,
        confidence_score,
        fairness_risk,
        compliance_risk,
        explainability_score,
        rng,
    )
    processing_time_seconds = determine_processing_time(
        input_complexity, human_override, compliance_risk, rng
    )

    return {
        "record_id": f"TADD-{record_index:03d}",
        "scenario_type": scenario_type,
        "task_description": task_description,
        "input_complexity": input_complexity,
        "ai_recommendation": ai_recommendation,
        "confidence_score": f"{confidence_score:.2f}",
        "explainability_score": str(explainability_score),
        "fairness_risk": fairness_risk,
        "compliance_risk": compliance_risk,
        "human_override": human_override,
        "override_reason": override_reason,
        "final_decision": final_decision,
        "outcome_status": final_decision,
        "processing_time_seconds": str(processing_time_seconds),
        "notes": rng.choice(NOTES_POOL),
    }


def generate_dataset():
    rng = random.Random(42)
    rows = []
    record_index = 1
    for scenario_type, descriptions in SCENARIO_DESCRIPTIONS.items():
        for task_description in descriptions:
            rows.append(build_record(record_index, scenario_type, task_description, rng))
            record_index += 1
    return rows


def write_dataset(rows):
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "data" / "tadd_v1.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def main():
    rows = generate_dataset()
    output_path = write_dataset(rows)
    print(f"Wrote {len(rows)} records to {output_path}")


if __name__ == "__main__":
    main()
