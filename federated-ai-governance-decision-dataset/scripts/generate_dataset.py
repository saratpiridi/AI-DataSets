import csv
import json
import random
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


ROW_COUNT = 500

SCHEMA = [
    "id",
    "query",
    "cloud_environment",
    "deployment_model",
    "government_domain",
    "data_classification",
    "jurisdiction",
    "policy_framework",
    "governance_rule",
    "ai_action",
    "decision_explanation",
    "risk_level",
    "compliance_status",
    "human_override_required",
    "final_outcome",
    "identity_context",
    "security_control",
    "audit_trace",
    "timestamp",
    "agency_type",
    "region",
]

CLOUD_ENVIRONMENTS = ["Azure", "AWS", "On-Prem", "Hybrid", "Multi-Cloud"]
DEPLOYMENT_MODELS = [
    "Centralized model registry with federated policy enforcement",
    "Regional sovereign enclave with cross-cloud model routing",
    "Hybrid inference pipeline with local data residency controls",
    "Multi-cloud governance mesh with shared audit services",
    "Agency-managed on-prem orchestration with cloud failover",
]
GOVERNMENT_DOMAINS = [
    "healthcare",
    "justice",
    "finance",
    "education",
    "smart cities",
    "public safety",
    "defense",
]
DATA_CLASSIFICATIONS = ["Public", "Internal", "Sensitive", "Restricted", "Mission Critical"]
JURISDICTIONS = ["Federal", "State", "County", "City", "Cross-Border Public Sector Coalition"]
POLICY_FRAMEWORKS = [
    "NIST AI RMF 2023",
    "ISO/IEC 22989:2022",
    "NIST SP 800-207",
    "EU AI Act 2024",
    "NIST AI RMF 2023; NIST SP 800-207",
    "NIST AI RMF 2023; ISO/IEC 22989:2022",
    "EU AI Act 2024; ISO/IEC 22989:2022",
    "NIST AI RMF 2023; EU AI Act 2024; NIST SP 800-207",
]
GOVERNANCE_RULES = [
    "Cross-tenant inference is blocked unless identity provenance is verified and the audit chain is complete.",
    "Sensitive data movement requires sovereign routing and conditional approval under policy review.",
    "High-impact automated decisions require dual logging and human oversight before production release.",
    "Model invocation is restricted when zero-trust controls do not match jurisdictional access policy.",
    "Federated policy execution must preserve explainability artifacts for each approval or denial event.",
]
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
COMPLIANCE_STATUSES = ["Compliant", "Partially Compliant", "Non-Compliant", "Requires Review"]
AGENCY_TYPES = ["State Government", "Federal Government", "City Government", "County Government"]
REGIONS = [
    "US-East",
    "US-West",
    "US-Gov",
    "EU-Central",
    "EU-West",
    "National",
    "Statewide",
    "Metro Region",
    "Regional Sovereign Zone",
    "Cross-Cloud Oversight Region",
]
IDENTITY_CONTEXTS = [
    "Privileged analyst with conditional access and device trust attestation",
    "Agency operator using federated identity with region-bound claims",
    "Service principal request with workload identity and scoped token exchange",
    "Cross-agency reviewer with just-in-time access and session logging",
    "Automated orchestration identity awaiting secondary policy attestation",
]
SECURITY_CONTROLS = [
    "Zero Trust network segmentation with policy decision point validation",
    "Confidential compute requirement with region-bound key management",
    "Attribute-based access control with sovereign boundary enforcement",
    "Continuous audit logging with immutable retention policy",
    "Identity-aware proxy with workload attestation and token inspection",
]
DECISION_EXPLANATIONS = [
    "The decision was derived by comparing the request against identity posture, sovereignty requirements, governance controls, and the referenced policy framework before determining the permitted AI action.",
    "The governance engine selected this outcome because the request crossed one or more policy boundaries involving jurisdiction, access assurance, and auditability in a federated cloud environment.",
    "The explanation reflects a standards-aware control decision in which the deployment model, classification level, and security control posture were evaluated before approval, denial, or escalation.",
    "The response was generated after reviewing synthetic governance metadata, federated access conditions, and compliance thresholds associated with multi-cloud government AI operations.",
    "The policy result reflects identity verification, classification handling, and federated audit obligations required by the selected governance framework.",
]

QUERY_TEMPLATES = {
    "healthcare": [
        "Should a federated clinical triage model be allowed to query sensitive case summaries across sovereign clouds?",
        "Can a public health AI workflow route vaccination eligibility analytics from a regional cloud to a national oversight tenant?",
        "Should an agency permit cross-cloud retrieval of telehealth prioritization outputs for emergency surge planning?",
        "Can a hybrid care coordination assistant access restricted referral data when identity claims are partially missing?",
    ],
    "justice": [
        "Should a federated case-assistance model be blocked when audit continuity breaks across justice cloud environments?",
        "Can a legal services assistant use multi-cloud retrieval for sealed records review under conditional access?",
        "Should a justice analytics workflow be escalated when jurisdictional residency controls conflict with model routing?",
        "Can a regional court-support agent invoke an external policy model without full identity provenance?",
    ],
    "finance": [
        "Should a budget anomaly detection model be allowed to aggregate expenditure signals across agency clouds?",
        "Can a financial oversight assistant process restricted grant data in a hybrid deployment with partial compliance evidence?",
        "Should cross-cloud procurement scoring be restricted when sovereign controls differ by tenant?",
        "Can a fiscal transparency agent release summarized outputs before dual-policy validation is complete?",
    ],
    "education": [
        "Should a student support model be escalated when regional residency requirements differ across hosted environments?",
        "Can an education analytics assistant access restricted aid data from a multi-cloud orchestration layer?",
        "Should a district-facing tutoring allocation model be allowed under conditional identity claims only?",
        "Can a statewide education chatbot reuse prior decision traces from an external cloud enclave?",
    ],
    "smart cities": [
        "Should a traffic coordination model be allowed to federate telemetry across city and regional clouds?",
        "Can a smart-city services assistant access camera-derived event summaries under zero-trust restrictions?",
        "Should an urban planning model be logged only when non-sensitive sensor data crosses a sovereign boundary?",
        "Can a hybrid municipal operations agent run predictive maintenance scoring without full audit lineage?",
    ],
    "public safety": [
        "Should a public safety coordination model be blocked when identity federation is incomplete during incident response?",
        "Can a disaster management assistant retrieve restricted shelter analytics from a sovereign enclave?",
        "Should a cross-cloud emergency routing workflow be escalated under conflicting access policies?",
        "Can a regional hazard assessment service continue inference when an attestation control fails downstream?",
    ],
    "defense": [
        "Should a mission-support AI service be restricted when model governance controls differ across clouds?",
        "Can a defense logistics assistant access controlled deployment analytics under a partially compliant configuration?",
        "Should a federated intelligence-support model be denied when audit trace completeness cannot be proven?",
        "Can a hybrid defense planning workflow be approved with conditions under zero-trust and sovereignty constraints?",
    ],
}

QUERY_VARIANTS = [
    "The request originated from a cross-cloud review queue.",
    "The workflow requires a transparent explanation for supervisory approval.",
    "The decision must preserve sovereign routing and identity context evidence.",
    "The request includes policy-sensitive data handling constraints.",
    "The case requires a traceable governance decision for later audit.",
]


def target_counts(items, total):
    base = total // len(items)
    remainder = total % len(items)
    counts = {item: base for item in items}
    for item in items[:remainder]:
        counts[item] += 1
    return counts


CLOUD_TARGETS = target_counts(CLOUD_ENVIRONMENTS, ROW_COUNT)
DOMAIN_TARGETS = target_counts(GOVERNMENT_DOMAINS, ROW_COUNT)
AGENCY_TARGETS = target_counts(AGENCY_TYPES, ROW_COUNT)
REGION_TARGETS = target_counts(REGIONS, ROW_COUNT)


def choose_action_and_outcome(risk_level, compliance_status, row_index):
    if risk_level == "Critical":
        return ("Blocked" if row_index % 2 else "Escalated", "Denied" if compliance_status == "Non-Compliant" else "Escalated")
    if risk_level == "High":
        return ("Restricted" if row_index % 3 else "Escalated", "Approved with Conditions" if compliance_status == "Partially Compliant" else "Escalated")
    if risk_level == "Medium":
        return ("Logged" if row_index % 4 == 0 else "Allowed", "Approved with Conditions" if row_index % 3 else "Approved")
    return ("Allowed" if row_index % 5 else "Logged", "Approved")


def choose_compliance(risk_level, row_index):
    if risk_level == "Critical":
        return "Non-Compliant" if row_index % 2 else "Requires Review"
    if risk_level == "High":
        return "Requires Review" if row_index % 3 else "Partially Compliant"
    if risk_level == "Medium":
        return "Partially Compliant" if row_index % 4 else "Compliant"
    return "Compliant"


def choose_override(risk_level, ai_action, compliance_status):
    if risk_level in {"High", "Critical"}:
        return "Yes"
    if ai_action in {"Blocked", "Escalated", "Restricted"}:
        return "Yes"
    if compliance_status in {"Non-Compliant", "Requires Review"}:
        return "Yes"
    return "No"


def audit_trace_text(record_id, cloud_environment, ai_action, compliance_status, region):
    return (
        f"Audit event {record_id} recorded federated policy evaluation in {cloud_environment}; "
        f"region={region}; action={ai_action}; compliance={compliance_status}; "
        f"identity claims, governance rule check, and control evidence were archived."
    )


def iso_timestamp(base_dt, row_index):
    dt = base_dt + timedelta(hours=row_index * 4, minutes=(row_index * 11) % 60)
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def next_with_capacity(options, counts):
    for option in options:
        if counts[option] > 0:
            counts[option] -= 1
            return option
    raise ValueError("No remaining capacity for requested option set")


def build_query(domain, sequence_index):
    templates = QUERY_TEMPLATES[domain]
    base = templates[sequence_index % len(templates)]
    variant = QUERY_VARIANTS[(sequence_index // len(templates)) % len(QUERY_VARIANTS)]
    return f"{base[:-1]} {variant}" if base.endswith("?") else f"{base} {variant}"


def generate_rows():
    rows = []
    seen_signatures = set()
    base_dt = datetime(2025, 1, 7, 8, 0, 0)
    cloud_counts = CLOUD_TARGETS.copy()
    domain_counts = DOMAIN_TARGETS.copy()
    agency_counts = AGENCY_TARGETS.copy()
    region_counts = REGION_TARGETS.copy()

    row_id = 1
    domain_sequence = {domain: 0 for domain in GOVERNMENT_DOMAINS}

    while row_id <= ROW_COUNT:
        domain = next_with_capacity(GOVERNMENT_DOMAINS, domain_counts)
        cloud_environment = next_with_capacity(CLOUD_ENVIRONMENTS, cloud_counts)
        agency_type = next_with_capacity(AGENCY_TYPES, agency_counts)
        region = next_with_capacity(REGIONS, region_counts)

        query = build_query(domain, domain_sequence[domain])
        domain_sequence[domain] += 1

        policy_framework = POLICY_FRAMEWORKS[(row_id - 1) % len(POLICY_FRAMEWORKS)]
        deployment_model = DEPLOYMENT_MODELS[(row_id - 1) % len(DEPLOYMENT_MODELS)]
        data_classification = DATA_CLASSIFICATIONS[(row_id - 1) % len(DATA_CLASSIFICATIONS)]
        jurisdiction = JURISDICTIONS[(row_id - 1) % len(JURISDICTIONS)]
        governance_rule = GOVERNANCE_RULES[(row_id - 1) % len(GOVERNANCE_RULES)]
        risk_level = RISK_LEVELS[(row_id * 3) % len(RISK_LEVELS)]
        compliance_status = choose_compliance(risk_level, row_id)
        ai_action, final_outcome = choose_action_and_outcome(risk_level, compliance_status, row_id)
        human_override_required = choose_override(risk_level, ai_action, compliance_status)
        identity_context = IDENTITY_CONTEXTS[(row_id - 1) % len(IDENTITY_CONTEXTS)]
        security_control = SECURITY_CONTROLS[(row_id - 1) % len(SECURITY_CONTROLS)]
        decision_explanation = DECISION_EXPLANATIONS[(row_id - 1) % len(DECISION_EXPLANATIONS)]
        record_id = f"FAGDD-{row_id:03d}"
        audit_trace = audit_trace_text(record_id, cloud_environment, ai_action, compliance_status, region)

        signature = (query, cloud_environment, deployment_model, agency_type, region)
        if signature in seen_signatures:
            cloud_counts[cloud_environment] += 1
            domain_counts[domain] += 1
            agency_counts[agency_type] += 1
            region_counts[region] += 1
            continue

        seen_signatures.add(signature)
        rows.append(
            {
                "id": record_id,
                "query": query,
                "cloud_environment": cloud_environment,
                "deployment_model": deployment_model,
                "government_domain": domain,
                "data_classification": data_classification,
                "jurisdiction": jurisdiction,
                "policy_framework": policy_framework,
                "governance_rule": governance_rule,
                "ai_action": ai_action,
                "decision_explanation": decision_explanation,
                "risk_level": risk_level,
                "compliance_status": compliance_status,
                "human_override_required": human_override_required,
                "final_outcome": final_outcome,
                "identity_context": identity_context,
                "security_control": security_control,
                "audit_trace": audit_trace,
                "timestamp": iso_timestamp(base_dt, row_id),
                "agency_type": agency_type,
                "region": region,
            }
        )
        row_id += 1

    return rows


def write_csv(rows, path):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows, path):
    with path.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)


def summarize(rows):
    print(f"Rows: {len(rows)}")
    print("Cloud distribution:", dict(Counter(row["cloud_environment"] for row in rows)))
    print("Agency distribution:", dict(Counter(row["agency_type"] for row in rows)))
    print("Region distribution:", dict(Counter(row["region"] for row in rows)))
    print("Domain distribution:", dict(Counter(row["government_domain"] for row in rows)))


def main():
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    rows = generate_rows()
    write_csv(rows, data_dir / "fagdd_v1.csv")
    write_json(rows, data_dir / "fagdd_v1.json")
    print(f"Wrote {len(rows)} records to {data_dir / 'fagdd_v1.csv'}")
    print(f"Wrote {len(rows)} records to {data_dir / 'fagdd_v1.json'}")
    summarize(rows)


if __name__ == "__main__":
    main()
