# Trustworthy Automation Decision Dataset (TADD)

TADD is a fully synthetic, research-oriented dataset for studying trustworthy automation decisions in operational workflows. It is designed for academic experiments, benchmarking, interpretability studies, and responsible AI evaluations involving human oversight, model confidence, explainability, fairness risk, and compliance risk.

The dataset is inspired by themes from the research paper *Extending Microsoft Power Platform with Responsible AI: A Model for Trustworthy Automation*, while keeping all records generic, non-proprietary, and suitable for open-source publication.

## Synthetic Data Statement

This repository contains **100% synthetic data**. It does not include real organizations, customers, employees, transactions, or personal data. All scenarios, descriptions, and outcomes were generated for research and educational use only.

## Motivation

Trustworthy automation systems often need more than a single model recommendation. They also need:

- confidence-aware decision support
- explainability signals
- fairness and compliance risk indicators
- human override pathways
- auditable final outcomes

TADD provides a compact benchmark for analyzing how automated recommendations interact with governance-oriented controls and human review.

## Repository Structure

```text
trustworthy-automation-decision-dataset/
├── README.md
├── dataset_card.md
├── LICENSE
├── .gitignore
├── data/
│   └── tadd_v1.csv
└── scripts/
    ├── generate_tadd.py
    ├── validate_tadd.py
    └── summarize_tadd.py
```

## Schema

The dataset uses the following columns in strict order:

1. `record_id`: Unique record identifier.
2. `scenario_type`: One of ten workflow scenario categories.
3. `task_description`: Short synthetic description of the automation case.
4. `input_complexity`: Qualitative input complexity level.
5. `ai_recommendation`: Initial automated recommendation.
6. `confidence_score`: Model confidence score from `0.50` to `0.99`.
7. `explainability_score`: Integer score from `1` to `5`.
8. `fairness_risk`: `Low`, `Medium`, or `High`.
9. `compliance_risk`: `Low`, `Medium`, or `High`.
10. `human_override`: `Yes` or `No`.
11. `override_reason`: `None` when there is no override, otherwise a meaningful explanation.
12. `final_decision`: Final disposition after automation and review.
13. `outcome_status`: One of `Approved`, `Rejected`, `Escalated`, or `Deferred`.
14. `processing_time_seconds`: Synthetic processing duration from `5` to `120`.
15. `notes`: Additional neutral context for research use.

## Example Usage

```python
import csv
from collections import Counter

with open("data/tadd_v1.csv", newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

print(f"Rows: {len(rows)}")
print("Scenario counts:", Counter(row["scenario_type"] for row in rows))
```

## How To Regenerate The Dataset

From the repository root:

```bash
python scripts/generate_tadd.py
python scripts/validate_tadd.py
python scripts/summarize_tadd.py
```

The generator uses `random.seed(42)` to ensure deterministic output.

## Research Reference

Reference paper:

- *Extending Microsoft Power Platform with Responsible AI: A Model for Trustworthy Automation*

This dataset is a synthetic research artifact inspired by that paper's high-level themes around responsible AI and trustworthy automation. The dataset itself does not include proprietary workflows, vendor-specific terminology, or source data from the paper.

## Suggested Uses

- benchmarking human-in-the-loop decision policies
- teaching responsible AI governance concepts
- testing validation pipelines for structured decision datasets
- prototyping explainability-aware workflow analytics
- studying override behavior under varying risk conditions

## Citation

If you publish work using this dataset, cite the repository and optionally reference the motivating paper in your related work section.
