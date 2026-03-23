[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19195085.svg)](https://doi.org/10.5281/zenodo.19195085)

# Conversational Government Decision Dataset

## Overview

The Conversational Government Decision Dataset (CGDD) is a synthetic, research-oriented dataset created to support the white paper *Conversational AI for Digital Government: A Standards-Aligned Framework for Data Transparency and Policy Decision-Making*.

The dataset models realistic public-sector conversational AI interactions in which a system responds to policy, service-delivery, compliance, and transparency-related questions. Each record includes the original query, supporting data sources, model response, explanation, standards-oriented policy alignment, risk rating, confidence score, human oversight requirement, and final outcome.

CGDD is designed for direct publication through GitHub, Kaggle, and Zenodo. The package includes ready-to-upload CSV and JSON files, structured documentation, a regeneration script, validation tooling, version metadata, and a permissive license.

## Highlights

- 500 synthetic, publication-ready records
- CSV and JSON formats for broad repository compatibility
- standards-aligned governance metadata for transparency analysis
- deterministic generation and validation scripts
- documentation optimized for GitHub, Kaggle, and Zenodo listing pages

## Use Cases

- benchmarking conversational AI systems used in digital government settings
- evaluating explainability and transparency in public-sector AI responses
- studying human oversight and escalation patterns in policy-sensitive workflows
- teaching responsible AI, governance, and data transparency concepts
- prototyping dashboards and analytics for standards-aligned AI decision support

## Dataset Contents

- `data/cgdd_v1.csv`: Tabular dataset with 500 synthetic records
- `data/cgdd_v1.json`: JSON version of the same dataset
- `scripts/generate_dataset.py`: Regenerates both dataset files
- `scripts/validate_dataset.py`: Validates schema, counts, value ranges, and diversity checks
- `dataset_card.md`: Structured dataset documentation
- `VERSION`: Release version marker
- `CHANGELOG.md`: Release history

## Schema

The dataset uses the following fields:

1. `id`: Unique record identifier
2. `query`: Synthetic government or citizen-facing question
3. `domain`: Policy or service domain
4. `data_sources`: Referenced synthetic or generic public data sources
5. `ai_response`: Concise professional response
6. `explanation`: Explanation of why the response was produced
7. `policy_alignment`: Standards-aligned governance reference
8. `risk_level`: `Low`, `Medium`, or `High`
9. `confidence_score`: Score between `0.70` and `0.99`
10. `human_override_required`: `Yes` or `No`
11. `final_outcome`: `Approved`, `Reviewed and Approved`, `Escalated`, or `Rejected`
12. `timestamp`: Realistic ISO timestamp
13. `region`: US state or national-level example
14. `agency_type`: `State Government`, `Federal Government`, `City Government`, or `County Government`

## Standards Alignment

CGDD is aligned to commonly referenced AI governance and management standards, including:

- `NIST AI RMF 2023`
- `EU AI Act 2024`
- `ISO/IEC 42001:2023`

These references appear in the `policy_alignment` field to support analysis of standards-aware public-sector AI decision making.

## Kaggle and Zenodo Readiness

This project is organized to support direct upload and publication workflows:

- flat data files in `data/` for straightforward asset packaging
- concise metadata and documentation for dataset landing pages
- deterministic regeneration for reproducibility
- validation tooling to confirm schema consistency and publication quality
- permissive licensing for open research distribution

## Provenance

This dataset is fully synthetic and was created as a supporting research artifact for the white paper *Conversational AI for Digital Government: A Standards-Aligned Framework for Data Transparency and Policy Decision-Making*. It does not contain real citizen records, agency case files, or operational government data.

All queries, explanations, data source references, and outcomes were generated for research, benchmarking, and publication purposes.

## Related Publication

This dataset supports the following white paper:

**Conversational AI for Digital Government – A Standards-Aligned Framework for Data Transparency and Policy Decision-Making**

DOI: https://doi.org/10.5281/zenodo.17383234

## Citation

If you use this dataset, please cite:

Piridi, S. (2026). Conversational Government Decision Dataset (CGDD) (v1.0). Zenodo. https://doi.org/10.5281/zenodo.19195085

If you use the conceptual framework, standards-aligned methodology, or research motivation that informed the dataset design, also cite the associated white paper:

*Conversational AI for Digital Government: A Standards-Aligned Framework for Data Transparency and Policy Decision-Making*

## Regeneration

From the project root:

```bash
python scripts/generate_dataset.py
python scripts/validate_dataset.py
```

The script writes:

- `data/cgdd_v1.csv`
- `data/cgdd_v1.json`

## Licensing

This project is released under the MIT License. Review the `LICENSE` file for details.
