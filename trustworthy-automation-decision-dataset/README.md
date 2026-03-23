# Trustworthy Automation Decision Dataset (TADD)

TADD is a fully synthetic, research-oriented dataset for studying trustworthy automation decisions in operational workflows. It is designed for academic experiments, benchmarking, interpretability studies, and responsible AI evaluations involving human oversight, model confidence, explainability, fairness risk, and compliance risk.

The dataset is derived from concepts presented in the research paper *Extending Microsoft Power Platform with Responsible AI: A Model for Trustworthy Automation*, while keeping all records generic, non-proprietary, and suitable for open-source publication.

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
|-- README.md
|-- dataset_card.md
|-- CITATION.cff
|-- zenodo_metadata_notes.md
|-- LICENSE
|-- .gitignore
|-- data/
|   `-- tadd_v1.csv
`-- scripts/
    |-- generate_tadd.py
    |-- validate_tadd.py
    `-- summarize_tadd.py
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

## Related Research

This dataset is derived from concepts presented in the conference paper:

- Piridi, Sarat, Nataraja Kumar Koduri, and Satyanarayana Asundi. *Extending Microsoft Power Platform with Responsible AI: A Model for Trustworthy Automation*. 2025 5th Asian Conference on Innovation in Technology (ASIANCON), 2025.
- Paper URL: https://ieeexplore.ieee.org/document/11281047
- DOI: 10.1109/ASIANCON66527.2025.11281047

TADD operationalizes research themes from that paper, including responsible AI in automation, explainability-aware decisions, fairness risk, compliance risk, and human-in-the-loop oversight. This repository is an independent synthetic dataset project and does not reproduce proprietary workflows or source data from the paper.

## Suggested Uses

- benchmarking human-in-the-loop decision policies
- teaching responsible AI governance concepts
- testing validation pipelines for structured decision datasets
- prototyping explainability-aware workflow analytics
- studying override behavior under varying risk conditions

## How to Cite

If you use the dataset directly, cite the dataset or repository release associated with your work.

If you use the conceptual framework, methodological framing, or research basis that informed the dataset design, also cite the paper *Extending Microsoft Power Platform with Responsible AI: A Model for Trustworthy Automation*.

Paper citation BibTeX:

```bibtex
@inproceedings{piridi2025trustworthyautomation,
  author    = {Sarat Piridi and Nataraja Kumar Koduri and Satyanarayana Asundi},
  title     = {Extending Microsoft Power Platform with Responsible AI: A Model for Trustworthy Automation},
  booktitle = {2025 5th Asian Conference on Innovation in Technology (ASIANCON)},
  year      = {2025},
  doi       = {10.1109/ASIANCON66527.2025.11281047},
  url       = {https://ieeexplore.ieee.org/document/11281047}
}
```

Dataset citation placeholder BibTeX:

```bibtex
@dataset{piridi_tadd_2026,
  author = {Sarat Piridi},
  title  = {Trustworthy Automation Decision Dataset (TADD)},
  year   = {2026},
  doi    = {TO_BE_ADDED},
  url    = {TO_BE_ADDED}
}
```

## Zenodo Metadata Notes

For Zenodo upload, add the paper as a related identifier:

- Identifier: https://ieeexplore.ieee.org/document/11281047
- Relation: Is derived from
- DOI: 10.1109/ASIANCON66527.2025.11281047
