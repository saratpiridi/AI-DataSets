import csv
import json
from collections import Counter
from pathlib import Path


EXPECTED_ROW_COUNT = 500
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

ALLOWED_CLOUDS = {"Azure", "AWS", "On-Prem", "Hybrid", "Multi-Cloud"}
ALLOWED_DOMAINS = {"healthcare", "justice", "finance", "education", "smart cities", "public safety", "defense"}
ALLOWED_RISK = {"Low", "Medium", "High", "Critical"}
ALLOWED_COMPLIANCE = {"Compliant", "Partially Compliant", "Non-Compliant", "Requires Review"}
ALLOWED_OVERRIDE = {"Yes", "No"}
ALLOWED_OUTCOME = {"Approved", "Denied", "Escalated", "Approved with Conditions"}
ALLOWED_ACTION = {"Allowed", "Blocked", "Escalated", "Restricted", "Logged"}
ALLOWED_AGENCIES = {"State Government", "Federal Government", "City Government", "County Government"}
POLICY_REFERENCES = {"NIST AI RMF 2023", "ISO/IEC 22989:2022", "NIST SP 800-207", "EU AI Act 2024"}


def load_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def validate():
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "data" / "fagdd_v1.csv"
    json_path = project_root / "data" / "fagdd_v1.json"
    issues = []

    if not csv_path.exists() or not json_path.exists():
        issues.append("Dataset files are missing.")
        return issues, Counter(), Counter(), Counter(), Counter()

    schema, rows = load_csv_rows(csv_path)
    if schema != SCHEMA:
        issues.append(f"Schema mismatch. Expected {SCHEMA}, found {schema}")
    if len(rows) != EXPECTED_ROW_COUNT:
        issues.append(f"CSV row count mismatch. Expected {EXPECTED_ROW_COUNT}, found {len(rows)}")

    with json_path.open(encoding="utf-8") as handle:
        json_rows = json.load(handle)
    if len(json_rows) != EXPECTED_ROW_COUNT:
        issues.append(f"JSON row count mismatch. Expected {EXPECTED_ROW_COUNT}, found {len(json_rows)}")

    seen_ids = set()
    seen_rows = set()
    cloud_counts = Counter()
    agency_counts = Counter()
    region_counts = Counter()
    domain_counts = Counter()

    for line_no, row in enumerate(rows, start=2):
        for field in SCHEMA:
            if row[field] == "":
                issues.append(f"Empty field '{field}' at CSV line {line_no}")

        if row["id"] in seen_ids:
            issues.append(f"Duplicate id '{row['id']}' at CSV line {line_no}")
        seen_ids.add(row["id"])

        signature = tuple(row[field] for field in SCHEMA[1:])
        if signature in seen_rows:
            issues.append(f"Duplicate row detected at CSV line {line_no}")
        seen_rows.add(signature)

        if row["cloud_environment"] not in ALLOWED_CLOUDS:
            issues.append(f"Invalid cloud_environment '{row['cloud_environment']}' at CSV line {line_no}")
        else:
            cloud_counts[row["cloud_environment"]] += 1

        if row["government_domain"] not in ALLOWED_DOMAINS:
            issues.append(f"Invalid government_domain '{row['government_domain']}' at CSV line {line_no}")
        else:
            domain_counts[row["government_domain"]] += 1

        if row["risk_level"] not in ALLOWED_RISK:
            issues.append(f"Invalid risk_level '{row['risk_level']}' at CSV line {line_no}")
        if row["compliance_status"] not in ALLOWED_COMPLIANCE:
            issues.append(f"Invalid compliance_status '{row['compliance_status']}' at CSV line {line_no}")
        if row["human_override_required"] not in ALLOWED_OVERRIDE:
            issues.append(f"Invalid human_override_required '{row['human_override_required']}' at CSV line {line_no}")
        if row["final_outcome"] not in ALLOWED_OUTCOME:
            issues.append(f"Invalid final_outcome '{row['final_outcome']}' at CSV line {line_no}")
        if row["ai_action"] not in ALLOWED_ACTION:
            issues.append(f"Invalid ai_action '{row['ai_action']}' at CSV line {line_no}")
        if row["agency_type"] not in ALLOWED_AGENCIES:
            issues.append(f"Invalid agency_type '{row['agency_type']}' at CSV line {line_no}")
        else:
            agency_counts[row["agency_type"]] += 1

        region_counts[row["region"]] += 1

        if not any(policy in row["policy_framework"] for policy in POLICY_REFERENCES):
            issues.append(f"policy_framework missing recognized reference at CSV line {line_no}")
        if not row["audit_trace"].startswith("Audit event "):
            issues.append(f"audit_trace format invalid at CSV line {line_no}")
        if "T" not in row["timestamp"]:
            issues.append(f"timestamp is not ISO-like at CSV line {line_no}")

    for cloud in sorted(ALLOWED_CLOUDS):
        if cloud_counts[cloud] < 90:
            issues.append(f"Cloud diversity too low for '{cloud}': found {cloud_counts[cloud]}")
    for agency in sorted(ALLOWED_AGENCIES):
        if agency_counts[agency] < 120:
            issues.append(f"Agency diversity too low for '{agency}': found {agency_counts[agency]}")
    for domain in sorted(ALLOWED_DOMAINS):
        if domain_counts[domain] < 70:
            issues.append(f"Domain diversity too low for '{domain}': found {domain_counts[domain]}")
    if len(region_counts) < 8:
        issues.append("Region diversity too low: fewer than 8 unique regions represented")

    return issues, cloud_counts, agency_counts, region_counts, domain_counts


def main():
    issues, cloud_counts, agency_counts, region_counts, domain_counts = validate()
    if issues:
        print("Validation failed.")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Validation passed.")
        print(f"- Row count is {EXPECTED_ROW_COUNT}")
        print(f"- Cloud distribution: {dict(cloud_counts)}")
        print(f"- Agency distribution: {dict(agency_counts)}")
        print(f"- Region distribution: {dict(region_counts)}")
        print(f"- Domain distribution: {dict(domain_counts)}")


if __name__ == "__main__":
    main()
