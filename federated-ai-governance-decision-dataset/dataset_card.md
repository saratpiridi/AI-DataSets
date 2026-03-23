# Dataset Card: Federated AI Governance Decision Dataset (FAGDD)

## Motivation

FAGDD was created to support research on federated AI governance across multi-cloud government systems where sovereignty, explainability, compliance, identity-aware access, and auditability are central design requirements. The dataset provides a structured synthetic benchmark for analyzing governance decisions in heterogeneous public-sector cloud environments. Version `v1.0` contains 500 synthetic records balanced across cloud environments, regions, agency types, and government domains.

## Intended Uses

- research on federated AI governance and compliance enforcement
- benchmarking multi-cloud policy decision and escalation workflows
- experimentation with sovereignty-aware access control and oversight logic
- teaching standards-aligned AI governance in government systems
- prototyping analytics for auditability, traceability, and policy transparency

## Limitations

- the dataset is synthetic and does not represent live government cloud environments
- governance outcomes are illustrative and not legal, regulatory, or certification judgments
- the examples simplify operational complexity found in production-scale sovereign cloud systems
- control mappings are research-oriented abstractions rather than validated compliance attestations
- domain coverage is broad but not exhaustive across all government workloads

## Ethical Considerations

Although FAGDD is synthetic, it touches on high-stakes governance themes such as defense, justice, and public safety. Users should not treat the dataset as a substitute for real compliance review, identity governance, security accreditation, or legal assessment. Real deployments require domain-specific validation, human oversight, and rigorous operational controls.

The dataset includes risk, compliance, and audit fields to support governance analysis, but these are synthetic annotations intended for research use only.

## Synthetic Data Disclosure

FAGDD is a fully synthetic dataset. It does not contain real cloud tenant data, government case records, classified data, confidential configurations, or proprietary system outputs. All records were generated to be realistic in tone and structure while remaining safe for open publication through GitHub, Kaggle, and Zenodo.

External links:

- GitHub: `https://github.com/saratpiridi/AI-DataSets/tree/main/federated-ai-governance-decision-dataset`
- Zenodo: `TO_BE_ADDED`
- Kaggle: `TO_BE_ADDED`
