# Federated AI Governance Decision Dataset

## Overview

The Federated AI Governance Decision Dataset (FAGDD) is a synthetic, research-grade dataset created to support the white paper *Federated AI Governance Framework for Multi-Cloud Government Systems*.

The dataset models governance and compliance decisions across federated government AI deployments operating in Azure, AWS, on-premises, hybrid, and multi-cloud environments. Each record captures a policy-sensitive question, governance rule, AI action, risk rating, compliance disposition, human oversight requirement, and audit trail metadata suitable for research on sovereignty, explainability, identity-aware access, and multi-cloud control enforcement.

FAGDD is structured for direct publication through GitHub, Kaggle, and Zenodo. Zenodo is intended to serve as the primary archival source for the dataset, while Kaggle is intended as a distribution channel for broader download and discovery. This dataset provides a reproducible, standards-aligned benchmark for evaluating federated AI governance systems in national-scale digital government environments.

## 📄 Associated Publication (DOI)

Federated AI Governance Framework for Multi-Cloud Government Systems  
https://doi.org/10.17605/OSF.IO/2UW8X

## Highlights

- 500 synthetic, publication-ready records
- CSV and JSON formats for broad repository compatibility
- federated governance scenarios across multi-cloud and sovereign contexts
- standards-aligned policy metadata for compliance and oversight analysis
- deterministic regeneration using Python standard library only

## Use Cases

- benchmarking federated AI governance workflows
- studying explainability and compliance outcomes in multi-cloud government systems
- testing policy-aware routing, escalation, and approval logic
- evaluating identity-aware access and security control traces
- supporting teaching and research on sovereign AI governance architectures

## Dataset Contents

- `data/fagdd_v1.csv`: Tabular dataset with 500 synthetic records
- `data/fagdd_v1.json`: JSON version of the same dataset
- `scripts/generate_dataset.py`: Regenerates both dataset files
- `scripts/validate_dataset.py`: Validates schema, counts, duplicates, and diversity targets
- `dataset_card.md`: Structured dataset documentation
- `CITATION.cff`: Citation metadata for repository platforms
- `VERSION`: Release version marker
- `CHANGELOG.md`: Release history

## Schema

The dataset uses the following fields:

1. `id`: Unique record identifier
2. `query`: Synthetic governance or operational question
3. `cloud_environment`: Deployment environment such as Azure, AWS, On-Prem, Hybrid, or Multi-Cloud
4. `deployment_model`: Synthetic deployment pattern or operating model
5. `government_domain`: Sector domain
6. `data_classification`: Synthetic public-sector data sensitivity label
7. `jurisdiction`: Governing jurisdiction context
8. `policy_framework`: Referenced governance framework
9. `governance_rule`: Specific synthetic rule or control statement
10. `ai_action`: `Allowed`, `Blocked`, `Escalated`, `Restricted`, or `Logged`
11. `decision_explanation`: Explanation for the decision
12. `risk_level`: `Low`, `Medium`, `High`, or `Critical`
13. `compliance_status`: `Compliant`, `Partially Compliant`, `Non-Compliant`, or `Requires Review`
14. `human_override_required`: `Yes` or `No`
15. `final_outcome`: `Approved`, `Denied`, `Escalated`, or `Approved with Conditions`
16. `identity_context`: Identity and access posture context
17. `security_control`: Security control reference
18. `audit_trace`: Synthetic audit log summary
19. `timestamp`: ISO-formatted timestamp
20. `agency_type`: Public-sector institution type
21. `region`: Geographic or sovereign region example

## Standards Alignment

FAGDD references the following governance and AI control frameworks:

- `NIST AI RMF 2023`
- `ISO/IEC 22989:2022`
- `NIST SP 800-207`
- `EU AI Act 2024`

These references appear in `policy_framework` to support standards-aware analysis of federated AI decision making.

## Provenance

This dataset is fully synthetic and was created as a supporting research artifact for the white paper *Federated AI Governance Framework for Multi-Cloud Government Systems*. It does not contain real agency systems data, tenant telemetry, citizen records, classified materials, or proprietary cloud logs.

All decision traces, access contexts, security controls, and audit explanations were generated for research, benchmarking, and publication purposes.

## Publication Readiness

This project is organized for direct dataset publication:

- flat data files in `data/` for upload packaging
- markdown documentation for repository and catalog visibility
- deterministic generation for reproducibility
- citation metadata through `CITATION.cff`
- release metadata through `VERSION` and `CHANGELOG.md`
- permissive open-source licensing

## Dataset Availability

This dataset is available across multiple platforms:

- GitHub: https://github.com/saratpiridi/AI-DataSets/tree/main/federated-ai-governance-decision-dataset  
- Zenodo: intended primary archival source for the published dataset release  
- Kaggle: intended distribution source for dataset discovery and download  

Primary archival source: Zenodo  
Distribution channel: Kaggle

## Citation

If you use this dataset, please cite:

### Dataset

Piridi, S. (2026).  
*Federated AI Governance Decision Dataset (FAGDD) (v1.0)* [Data set].  
Zenodo (Primary), Kaggle (Distribution).

### Associated White Paper

Piridi, S. (2026).  
*Federated AI Governance Framework for Multi-Cloud Government Systems*.  
https://doi.org/10.17605/OSF.IO/2UW8X

BibTeX:

```bibtex
@dataset{piridi_fagdd_2026,
  author       = {Piridi, Sarat},
  title        = {Federated AI Governance Decision Dataset (FAGDD)},
  year         = {2026},
  version      = {1.0},
  publisher    = {Zenodo and Kaggle},
  note         = {Synthetic dataset for federated AI governance in multi-cloud government systems},
  url          = {https://github.com/saratpiridi/AI-DataSets/tree/main/federated-ai-governance-decision-dataset}
}

@article{piridi_federated_ai_2026,
  author       = {Piridi, Sarat},
  title        = {Federated AI Governance Framework for Multi-Cloud Government Systems},
  year         = {2026},
  doi          = {10.17605/OSF.IO/2UW8X}
}
```

## Associated White Paper

This dataset supports the white paper:

*Federated AI Governance Framework for Multi-Cloud Government Systems*

The dataset operationalizes research themes related to federated governance, multi-cloud compliance, sovereignty-aware access, explainability, auditability, and identity-aware policy enforcement in public-sector AI systems.

## Regeneration

From the project root:

```bash
python scripts/generate_dataset.py
python scripts/validate_dataset.py
```

The script writes:

- `data/fagdd_v1.csv`
- `data/fagdd_v1.json`

## Licensing

This project is released under the MIT License. Review the `LICENSE` file for details.
