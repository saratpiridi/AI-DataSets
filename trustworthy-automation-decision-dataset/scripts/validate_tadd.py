import csv
from collections import Counter
from pathlib import Path


EXPECTED_SCHEMA = [
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

ALLOWED_SCENARIOS = {
    "document_approval",
    "invoice_processing",
    "customer_request_routing",
    "employee_onboarding",
    "claims_review",
    "compliance_screening",
    "case_prioritization",
    "chatbot_escalation",
    "access_request_validation",
    "exception_handling",
}
ALLOWED_COMPLEXITY = {"Low", "Medium", "High"}
ALLOWED_RISK = {"Low", "Medium", "High"}
ALLOWED_OVERRIDE = {"Yes", "No"}
ALLOWED_OUTCOMES = {"Approved", "Rejected", "Escalated", "Deferred"}


def expected_override(confidence_score, fairness_risk, compliance_risk, explainability_score):
    return (
        confidence_score < 0.70
        or compliance_risk == "High"
        or fairness_risk == "High"
        or explainability_score <= 2
    )


def validate():
    project_root = Path(__file__).resolve().parents[1]
    dataset_path = project_root / "data" / "tadd_v1.csv"
    issues = []

    if not dataset_path.exists():
        issues.append(f"Dataset file not found: {dataset_path}")
        return issues

    with dataset_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        schema = reader.fieldnames
        rows = list(reader)

    if schema != EXPECTED_SCHEMA:
        issues.append(f"Schema mismatch. Expected {EXPECTED_SCHEMA}, found {schema}")

    if len(rows) != 100:
        issues.append(f"Row count mismatch. Expected 100, found {len(rows)}")

    scenario_counts = Counter()
    seen_rows = set()
    seen_ids = set()

    for row_number, row in enumerate(rows, start=2):
        row_signature = tuple(row[column] for column in EXPECTED_SCHEMA)
        if row_signature in seen_rows:
            issues.append(f"Duplicate row detected at CSV line {row_number}")
        seen_rows.add(row_signature)

        record_id = row["record_id"]
        if record_id in seen_ids:
            issues.append(f"Duplicate record_id '{record_id}' at CSV line {row_number}")
        seen_ids.add(record_id)

        for field in EXPECTED_SCHEMA:
            if row[field] == "":
                issues.append(f"Empty value in field '{field}' at CSV line {row_number}")

        scenario_type = row["scenario_type"]
        if scenario_type not in ALLOWED_SCENARIOS:
            issues.append(f"Invalid scenario_type '{scenario_type}' at CSV line {row_number}")
        else:
            scenario_counts[scenario_type] += 1

        if row["input_complexity"] not in ALLOWED_COMPLEXITY:
            issues.append(f"Invalid input_complexity '{row['input_complexity']}' at CSV line {row_number}")
        if row["fairness_risk"] not in ALLOWED_RISK:
            issues.append(f"Invalid fairness_risk '{row['fairness_risk']}' at CSV line {row_number}")
        if row["compliance_risk"] not in ALLOWED_RISK:
            issues.append(f"Invalid compliance_risk '{row['compliance_risk']}' at CSV line {row_number}")
        if row["human_override"] not in ALLOWED_OVERRIDE:
            issues.append(f"Invalid human_override '{row['human_override']}' at CSV line {row_number}")
        if row["final_decision"] not in ALLOWED_OUTCOMES:
            issues.append(f"Invalid final_decision '{row['final_decision']}' at CSV line {row_number}")
        if row["outcome_status"] not in ALLOWED_OUTCOMES:
            issues.append(f"Invalid outcome_status '{row['outcome_status']}' at CSV line {row_number}")

        try:
            confidence_score = float(row["confidence_score"])
            if not (0.50 <= confidence_score <= 0.99):
                issues.append(f"confidence_score out of range at CSV line {row_number}")
        except ValueError:
            issues.append(f"Invalid confidence_score '{row['confidence_score']}' at CSV line {row_number}")
            continue

        try:
            explainability_score = int(row["explainability_score"])
            if not (1 <= explainability_score <= 5):
                issues.append(f"explainability_score out of range at CSV line {row_number}")
        except ValueError:
            issues.append(f"Invalid explainability_score '{row['explainability_score']}' at CSV line {row_number}")
            continue

        try:
            processing_time_seconds = int(row["processing_time_seconds"])
            if not (5 <= processing_time_seconds <= 120):
                issues.append(f"processing_time_seconds out of range at CSV line {row_number}")
        except ValueError:
            issues.append(f"Invalid processing_time_seconds '{row['processing_time_seconds']}' at CSV line {row_number}")

        should_override = expected_override(
            confidence_score,
            row["fairness_risk"],
            row["compliance_risk"],
            explainability_score,
        )
        actual_override = row["human_override"] == "Yes"
        if should_override != actual_override:
            issues.append(f"Override logic mismatch at CSV line {row_number}")
        if actual_override and row["override_reason"] == "None":
            issues.append(f"Override reason missing at CSV line {row_number}")
        if not actual_override and row["override_reason"] != "None":
            issues.append(f"Override reason should be 'None' at CSV line {row_number}")
        if row["final_decision"] != row["outcome_status"]:
            issues.append(f"final_decision and outcome_status mismatch at CSV line {row_number}")

    for scenario in sorted(ALLOWED_SCENARIOS):
        count = scenario_counts[scenario]
        if count != 10:
            issues.append(f"Scenario distribution mismatch for '{scenario}': expected 10, found {count}")

    return issues


def main():
    issues = validate()
    if issues:
        print("Validation failed.")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Validation passed.")
        print("- Schema is correct")
        print("- Row count is 100")
        print("- Scenario distribution is balanced")
        print("- Allowed values and score ranges are valid")
        print("- Override logic is consistent")


if __name__ == "__main__":
    main()
