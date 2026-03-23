import csv
from collections import Counter
from pathlib import Path


def load_rows():
    project_root = Path(__file__).resolve().parents[1]
    dataset_path = project_root / "data" / "tadd_v1.csv"
    with dataset_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    rows = load_rows()
    scenario_counts = Counter(row["scenario_type"] for row in rows)
    outcome_counts = Counter(row["outcome_status"] for row in rows)
    override_count = sum(1 for row in rows if row["human_override"] == "Yes")
    average_confidence = sum(float(row["confidence_score"]) for row in rows) / len(rows)

    print("TADD Summary")
    print("============")
    print("Count per scenario_type:")
    for scenario_type in sorted(scenario_counts):
        print(f"- {scenario_type}: {scenario_counts[scenario_type]}")

    print("Outcome distribution:")
    for outcome, count in sorted(outcome_counts.items()):
        print(f"- {outcome}: {count}")

    print(f"Override percentage: {override_count / len(rows) * 100:.2f}%")
    print(f"Average confidence_score: {average_confidence:.3f}")


if __name__ == "__main__":
    main()
