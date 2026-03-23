import csv
import json
from collections import Counter
from pathlib import Path


EXPECTED_ROW_COUNT = 500
SCHEMA = [
    "id",
    "query",
    "domain",
    "data_sources",
    "ai_response",
    "explanation",
    "policy_alignment",
    "risk_level",
    "confidence_score",
    "human_override_required",
    "final_outcome",
    "timestamp",
    "region",
    "agency_type",
]

ALLOWED_DOMAINS = {
    "finance",
    "healthcare",
    "justice",
    "environment",
    "education",
    "labor",
    "public safety",
}
ALLOWED_RISK = {"Low", "Medium", "High"}
ALLOWED_OVERRIDE = {"Yes", "No"}
ALLOWED_OUTCOME = {"Approved", "Reviewed and Approved", "Escalated", "Rejected"}
ALLOWED_AGENCY_TYPES = {
    "State Government",
    "Federal Government",
    "City Government",
    "County Government",
}
POLICY_KEYWORDS = {
    "NIST AI RMF 2023",
    "EU AI Act 2024",
    "ISO/IEC 42001:2023",
}


def load_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def validate():
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "data" / "cgdd_v1.csv"
    json_path = project_root / "data" / "cgdd_v1.json"
    issues = []

    if not csv_path.exists() or not json_path.exists():
        issues.append("Dataset files are missing")
        return issues, Counter(), Counter(), Counter()

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
    seen_signatures = set()
    domain_counts = Counter()
    region_counts = Counter()
    agency_counts = Counter()

    for line_no, row in enumerate(rows, start=2):
        for field in SCHEMA:
            if row[field] == "":
                issues.append(f"Empty field '{field}' at CSV line {line_no}")

        if row["id"] in seen_ids:
            issues.append(f"Duplicate id '{row['id']}' at CSV line {line_no}")
        seen_ids.add(row["id"])

        signature = tuple(row[field] for field in SCHEMA[1:])
        if signature in seen_signatures:
            issues.append(f"Duplicate row content at CSV line {line_no}")
        seen_signatures.add(signature)

        if row["domain"] not in ALLOWED_DOMAINS:
            issues.append(f"Invalid domain '{row['domain']}' at CSV line {line_no}")
        else:
            domain_counts[row["domain"]] += 1

        if row["risk_level"] not in ALLOWED_RISK:
            issues.append(f"Invalid risk_level '{row['risk_level']}' at CSV line {line_no}")
        if row["human_override_required"] not in ALLOWED_OVERRIDE:
            issues.append(f"Invalid human_override_required '{row['human_override_required']}' at CSV line {line_no}")
        if row["final_outcome"] not in ALLOWED_OUTCOME:
            issues.append(f"Invalid final_outcome '{row['final_outcome']}' at CSV line {line_no}")
        if row["agency_type"] not in ALLOWED_AGENCY_TYPES:
            issues.append(f"Invalid agency_type '{row['agency_type']}' at CSV line {line_no}")
        else:
            agency_counts[row["agency_type"]] += 1

        region_counts[row["region"]] += 1

        try:
            confidence_score = float(row["confidence_score"])
            if not (0.70 <= confidence_score <= 0.99):
                issues.append(f"confidence_score out of range at CSV line {line_no}")
        except ValueError:
            issues.append(f"Invalid confidence_score '{row['confidence_score']}' at CSV line {line_no}")

        if not any(keyword in row["policy_alignment"] for keyword in POLICY_KEYWORDS):
            issues.append(f"policy_alignment missing standard reference at CSV line {line_no}")

        if "T" not in row["timestamp"]:
            issues.append(f"timestamp is not ISO-like at CSV line {line_no}")

    for domain in sorted(ALLOWED_DOMAINS):
        if domain_counts[domain] < 70:
            issues.append(f"Domain diversity too low for '{domain}': found {domain_counts[domain]}")

    for agency_type in sorted(ALLOWED_AGENCY_TYPES):
        if agency_counts[agency_type] < 100:
            issues.append(f"Agency diversity too low for '{agency_type}': found {agency_counts[agency_type]}")

    if len(region_counts) < 8:
        issues.append("Region diversity too low: fewer than 8 regions represented")

    return issues, domain_counts, region_counts, agency_counts


def main():
    issues, domain_counts, region_counts, agency_counts = validate()
    if issues:
        print("Validation failed.")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Validation passed.")
        print(f"- Row count is {EXPECTED_ROW_COUNT}")
        print(f"- Schema matches expected field order")
        print(f"- Domains represented: {dict(domain_counts)}")
        print(f"- Regions represented: {dict(region_counts)}")
        print(f"- Agency types represented: {dict(agency_counts)}")


if __name__ == "__main__":
    main()
