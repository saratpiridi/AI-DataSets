# Dataset Card: Conversational Government Decision Dataset (CGDD)

## Motivation

CGDD was created to support research on conversational AI in digital government environments where transparency, explainability, standards alignment, and policy-sensitive decision making are essential. The dataset provides a structured synthetic benchmark for studying how conversational systems handle public-sector questions while surfacing governance signals such as risk, confidence, and human oversight needs. Version `v1.0` contains 500 synthetic records covering finance, healthcare, justice, environment, education, labor, and public safety.

## Intended Uses

- research on explainable conversational AI in the public sector
- benchmarking governance-aware response generation systems
- experimentation with oversight rules, escalation logic, and approval workflows
- teaching digital government, responsible AI, and policy alignment concepts
- prototyping analytics and visualizations for public-sector AI transparency
- packaging as a public benchmark dataset for GitHub, Kaggle, and Zenodo

## Limitations

- the dataset is synthetic and does not represent actual government operations
- policy alignment labels are illustrative and not formal legal determinations
- the examples simplify real-world policy, procurement, and adjudication complexity
- the dataset is compact and not intended to represent production-scale deployment logs
- domain coverage is broad but not exhaustive across all public-sector functions

## Ethical Considerations

Although CGDD is synthetic, users should avoid treating it as evidence of real institutional practice or as a substitute for legal, administrative, or policy review. Public-sector AI systems operate in settings with accountability, equity, and due-process implications, and any real deployment would require domain-specific validation, governance, and human oversight.

The dataset includes risk levels and override indicators to support responsible AI analysis, but these values are synthetic annotations rather than certified compliance judgments.

## Synthetic Data Disclosure

CGDD is a fully synthetic dataset. It does not contain real citizen data, government case data, confidential records, or proprietary system outputs. All records were generated to be realistic in tone and structure while remaining safe for public release through open research channels such as GitHub, Kaggle, and Zenodo.

Kaggle DOI: https://doi.org/10.34740/kaggle/dsv/15339621
