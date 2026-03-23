# Dataset Card: Trustworthy Automation Decision Dataset (TADD)

## Overview

The Trustworthy Automation Decision Dataset (TADD) is a compact, structured dataset containing 100 synthetic records that model automation-assisted decision making across common workflow scenarios. Each record captures an automated recommendation, confidence and explainability signals, fairness and compliance risks, human override behavior, and a final operational outcome.

## Motivation

Many automation studies focus on predictive performance alone. TADD is designed to support research that also considers governance, human oversight, and decision accountability. The dataset emphasizes the interaction between automated recommendations and trust-related signals such as confidence, explainability, fairness risk, and compliance risk.

## Intended Use

TADD is intended for:

- academic research on responsible AI and human-in-the-loop systems
- teaching and coursework involving trustworthy automation
- prototyping data pipelines, dashboards, and validation tools
- benchmarking rule-based override policies
- exploratory analysis of governance-oriented decision features

## Not Intended Use

TADD is not intended for:

- production deployment without task-specific adaptation and validation
- training systems that make real legal, financial, employment, healthcare, or safety-critical decisions
- inferring real-world organizational behavior
- representing any real institution, platform, customer population, or individual

## Data Generation Process

The dataset is generated programmatically using a deterministic Python script with `random.seed(42)`. Records are created across ten scenario types with approximately equal representation. Each row is synthesized from:

- a scenario-specific task description
- controlled ranges for confidence and processing time
- categorical fairness and compliance risk assignments
- rule-based human override logic
- final decisions derived from automated recommendations and review conditions

The generation process includes constraints to ensure:

- no empty fields
- no duplicate rows
- valid schema ordering
- consistent override behavior
- realistic but synthetic variation across records

## Source Research

This dataset operationalizes concepts from the paper *Extending Microsoft Power Platform with Responsible AI: A Model for Trustworthy Automation* by Sarat Piridi, Nataraja Kumar Koduri, and Satyanarayana Asundi, presented at the 2025 5th Asian Conference on Innovation in Technology (ASIANCON).

The dataset design reflects research themes discussed in that paper, including:

- responsible AI in automation
- explainability
- fairness risk
- compliance risk
- human-in-the-loop oversight

Paper URL: https://ieeexplore.ieee.org/document/11281047

DOI: 10.1109/ASIANCON66527.2025.11281047

## Ethical Considerations

TADD is intentionally synthetic and does not contain personal data. This reduces privacy risk and makes the dataset safer for open publication. Even so, users should be careful not to overgeneralize from the synthetic distributions or treat the dataset as evidence about real populations, institutions, or operational harms.

The dataset includes fairness and compliance risk fields to support governance analysis, but these labels are synthetic abstractions rather than validated legal or sociotechnical assessments.

## Citation Guidance

Users should cite the dataset for direct use of the TADD records, schema, or derived repository releases.

Users should also cite the paper *Extending Microsoft Power Platform with Responsible AI: A Model for Trustworthy Automation* when referring to the conceptual framing, research motivation, or methodological foundation that informed the dataset design.

## Provenance

This dataset is a synthetic research asset derived from the conceptual framework described in the above paper. It does not contain or reproduce proprietary, confidential, or real-world organizational data.

## Limitations

- small dataset size relative to real enterprise-scale workflow logs
- synthetic distributions may not reflect real-world frequency or severity patterns
- rule-based generation can simplify edge cases found in live operations
- scenario descriptions are intentionally generic and may omit domain nuance
- final decisions are modeled outcomes, not observations from human operators

## Future Work

Potential extensions include:

- multi-turn case histories instead of single-row snapshots
- richer explanation artifacts or rationale fields
- temporal drift variants across versions
- benchmark splits for classification and policy-learning tasks
- annotation templates for simulating reviewer disagreement
