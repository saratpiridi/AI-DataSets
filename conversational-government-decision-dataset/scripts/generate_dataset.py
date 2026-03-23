import csv
import json
import random
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


ROW_COUNT = 500

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

DOMAINS = {
    "finance": [
        "How should a city revise grant reporting guidance when quarterly expenditure totals do not match the approved budget narrative?",
        "What information should a county publish when a procurement threshold exception is requested for emergency repairs?",
        "Can a resident receive a clear explanation for why a municipal fee waiver request was not auto-approved?",
        "What factors should be disclosed when an automated tool flags duplicate vendor payment requests?",
        "How should a state finance office summarize the basis for delaying reimbursement of a public assistance claim?",
        "What data should support an automated recommendation to prioritize capital maintenance funding requests?",
        "How should an agency explain why a travel reimbursement exception was routed for manual review?",
        "What public-facing response should be provided when a local subsidy eligibility check returns an uncertain result?",
        "How should a finance chatbot answer questions about delayed grant disbursement approvals?",
        "What explanation should accompany an automated recommendation to reject a duplicate invoice submission?",
        "Can an agency explain which records were considered in a public budgeting inquiry response?",
        "How should a digital assistant respond when a citizen asks why a property tax relief request was escalated?",
        "What summary should accompany an automated municipal bond disclosure routing decision?",
        "How should a county system explain a review delay for a small business recovery payment request?",
        "What evidence should be referenced when an automated compliance check flags a spending report anomaly?",
    ],
    "healthcare": [
        "How should a public health chatbot explain a clinic eligibility response for a preventive care program?",
        "What information should a state health agency provide when an AI system routes a benefits question to human review?",
        "How should an automated assistant respond when a resident asks why a vaccination support request was deferred?",
        "What explanation should be given when a maternal health referral recommendation is marked high risk?",
        "How should a county health office summarize the basis for prioritizing inspection follow-up requests?",
        "What sources should support an AI response about environmental health complaint handling timelines?",
        "How should a digital health assistant explain uncertainty in a community services eligibility response?",
        "What policy-aligned response should be given when a citizen asks why a rural care subsidy decision was escalated?",
        "How should a health department assistant describe the basis for recommending manual review of a benefit enrollment query?",
        "What explanation should accompany an automated response about behavioral health transport assistance?",
        "How should an agency respond when a resident challenges a chatbot answer on mobile clinic coverage?",
        "What data should be cited when an AI assistant recommends follow-up review for a screening access complaint?",
        "How should a state public health office explain why a nutrition assistance question received a cautious response?",
        "What rationale should support a community care guidance answer generated under moderate confidence?",
        "How should a county system explain a manual override applied to a telehealth outreach eligibility result?",
    ],
    "justice": [
        "How should a court services chatbot explain why an expungement guidance request was sent for manual review?",
        "What information should be disclosed when an automated intake system classifies a legal aid request as high risk?",
        "How should a county justice assistant respond to a citizen asking why a records access question was escalated?",
        "What explanation should accompany an AI-generated response about community supervision reporting requirements?",
        "How should a public defender intake assistant explain uncertainty in a case routing recommendation?",
        "What data sources should support an automated answer about victim assistance program eligibility?",
        "How should a state justice portal explain why a fine relief inquiry was not automatically approved?",
        "What rationale should be given when a detention conditions complaint is flagged for human review?",
        "How should a chatbot answer questions about delayed processing of a restorative justice program request?",
        "What explanation should accompany an automated recommendation regarding legal records correction guidance?",
        "How should a digital assistant respond when a resident asks why a hearing accommodation query was escalated?",
        "What basis should support an AI answer about youth diversion intake criteria?",
        "How should an agency explain the standards applied to an automated justice information response?",
        "What policy-aligned explanation should be used when a case assistance query is marked medium risk?",
        "How should a county justice office summarize a manual override on a legal service referral response?",
    ],
    "environment": [
        "How should an environmental agency chatbot explain a permit status response with incomplete monitoring data?",
        "What information should support an automated answer about water quality complaint follow-up timelines?",
        "How should a county environmental assistant explain why a flood mitigation inquiry was escalated?",
        "What rationale should be given when a recycling compliance question receives a medium-confidence response?",
        "How should a state climate office summarize the basis for a resilience grant eligibility answer?",
        "What data sources should be cited when a resident asks why an air quality alert request was reviewed manually?",
        "How should a chatbot explain uncertainty in a hazardous waste pickup scheduling response?",
        "What explanation should accompany an AI recommendation to defer an environmental justice complaint answer?",
        "How should a local government assistant respond to questions about drought response eligibility checks?",
        "What policy-aligned response should be generated for a wetlands permit guidance query?",
        "How should an agency explain why a stormwater violation inquiry required human review?",
        "What justification should support an automated answer about energy rebate program eligibility?",
        "How should a county office describe the reasoning behind a manual override on a landfill complaint response?",
        "What explanation should accompany a conversational response on tree removal permit requirements?",
        "How should an environmental assistant summarize a high-risk policy interpretation request from a resident?",
    ],
    "education": [
        "How should a state education assistant explain why a school meal eligibility question was escalated?",
        "What information should support an automated answer about special program transportation assistance?",
        "How should a district-facing chatbot respond when a grant compliance inquiry has conflicting source records?",
        "What explanation should accompany a student services guidance response produced under moderate confidence?",
        "How should a county education office summarize the basis for a digital access support recommendation?",
        "What rationale should be given when an AI system routes a school enrollment policy question to human review?",
        "How should an agency explain a manual override applied to a tutoring assistance eligibility response?",
        "What data should support an answer about teacher stipend reimbursement timelines?",
        "How should an education assistant respond to a parent asking why a records correction request was deferred?",
        "What explanation should accompany an automated answer about after-school program eligibility?",
        "How should a public education chatbot explain uncertainty in a scholarship routing recommendation?",
        "What standards-aligned response should be used for a curriculum transparency inquiry?",
        "How should an agency explain why a childcare subsidy education-related request was marked high risk?",
        "What reasoning should support a district compliance response about reporting deadlines?",
        "How should a city education office summarize an escalated inquiry on adaptive learning device support?",
    ],
    "labor": [
        "How should a workforce agency assistant explain why a retraining grant question required manual review?",
        "What data sources should support an automated answer about unemployment documentation requirements?",
        "How should a labor department chatbot respond when a worker asks why a wage complaint was escalated?",
        "What explanation should accompany an AI-generated response about apprenticeship eligibility?",
        "How should a state labor office summarize the reasoning behind a benefits inquiry outcome?",
        "What policy-aligned answer should be given for a worker safety reporting guidance question?",
        "How should an assistant explain uncertainty in a public employment placement recommendation?",
        "What rationale should support a manual override on a temporary assistance for laid-off workers response?",
        "How should a county workforce office explain why a job center referral answer was reviewed and approved?",
        "What explanation should accompany an automated answer on paid leave documentation standards?",
        "How should a resident-facing assistant respond to a labor rights information query flagged medium risk?",
        "What evidence should support an AI response about contractor classification guidance from a public agency?",
        "How should a digital labor assistant explain a cautious response to an employer compliance inquiry?",
        "What basis should be cited when a worker transition support question is escalated?",
        "How should a workforce program chatbot summarize the policy basis for a rejected response recommendation?",
    ],
    "public safety": [
        "How should a city safety assistant explain why a non-emergency hazard report was routed for manual review?",
        "What information should support an automated answer about evacuation assistance eligibility?",
        "How should a county emergency management chatbot explain uncertainty in shelter guidance?",
        "What rationale should be provided when a public safety inquiry is escalated due to conflicting situational data?",
        "How should a resident-facing assistant explain the basis for a wildfire alert information response?",
        "What standards-aligned answer should be given for a community policing transparency question?",
        "How should an agency explain a manual override on an automated disaster recovery information response?",
        "What data sources should support a chatbot answer about road closure assistance programs?",
        "How should a public safety office summarize a reviewed and approved response on heat emergency resources?",
        "What explanation should accompany an AI-generated answer about neighborhood emergency preparedness grants?",
        "How should a city system respond when a resident challenges a safety inspection guidance answer?",
        "What basis should support an automated response about flood shelter accessibility services?",
        "How should an emergency services assistant explain why a hazardous conditions query was marked high risk?",
        "What reasoning should support an escalated response on disaster aid documentation requirements?",
        "How should a county public safety chatbot explain the review path for a resilience planning inquiry?",
    ],
}

QUERY_VARIANTS = [
    "The request was submitted through a public self-service portal.",
    "The inquiry asks for a transparent explanation that can be shared with a resident or stakeholder.",
    "The available records include recent updates from the latest reporting cycle.",
    "The case involves a request for a traceable justification and data-source summary.",
    "The interaction is intended for a multilingual digital service channel.",
]

DATA_SOURCE_OPTIONS = {
    "finance": [
        "budget ordinance archive; grant reporting portal; internal expenditure summary",
        "procurement guidance bulletin; emergency spending policy; vendor review log",
        "public reimbursement rules; service eligibility checklist; transaction exception registry",
    ],
    "healthcare": [
        "public health eligibility guide; service directory; program enrollment rules",
        "clinic operations bulletin; resident assistance FAQ; intake review log",
        "community health policy manual; benefits coverage matrix; outreach case summary",
    ],
    "justice": [
        "court services guidance; public records policy; intake routing protocol",
        "legal aid program handbook; accessibility guidance; case review checklist",
        "justice information portal; complaint handling procedure; review escalation notes",
    ],
    "environment": [
        "permit guidance library; environmental monitoring summary; public complaint workflow",
        "climate adaptation program rules; resilience grant guidance; response protocol",
        "inspection bulletin; environmental services FAQ; case escalation register",
    ],
    "education": [
        "education services manual; eligibility checklist; district support guidance",
        "student assistance portal; grant compliance rules; review notes",
        "public education FAQ; family services handbook; case routing log",
    ],
    "labor": [
        "workforce services handbook; benefits rules; case routing summary",
        "labor compliance guide; worker support portal; review escalation log",
        "employment assistance FAQ; training program criteria; intake notes",
    ],
    "public safety": [
        "emergency operations guidance; resident safety FAQ; event response summary",
        "hazard reporting protocol; incident services directory; escalation notes",
        "preparedness program guidance; disaster assistance rules; review checklist",
    ],
}

POLICY_ALIGNMENTS = [
    "NIST AI RMF 2023",
    "EU AI Act 2024",
    "ISO/IEC 42001:2023",
    "NIST AI RMF 2023; ISO/IEC 42001:2023",
    "NIST AI RMF 2023; EU AI Act 2024",
    "EU AI Act 2024; ISO/IEC 42001:2023",
    "NIST AI RMF 2023; EU AI Act 2024; ISO/IEC 42001:2023",
]

REGIONS = [
    "National",
    "California",
    "Texas",
    "New York",
    "Florida",
    "Illinois",
    "Washington",
    "Virginia",
    "Colorado",
    "Georgia",
    "Arizona",
]

AGENCY_TYPES = [
    "State Government",
    "Federal Government",
    "City Government",
    "County Government",
]

RESPONSE_TEMPLATES = [
    "The request can be answered using the available public guidance, but review conditions have been noted where policy sensitivity is elevated.",
    "The response is based on the referenced public records and current program guidance, with a recommendation for additional review when risk indicators are present.",
    "The available sources support a provisional answer that emphasizes transparency, traceability, and policy-aware handling.",
    "The answer reflects the most relevant public guidance currently associated with the request and identifies whether human review is warranted.",
    "The response prioritizes transparency by identifying the governing rules, the supporting public records, and the rationale for any review step.",
]

EXPLANATION_TEMPLATES = [
    "The answer was produced by matching the query to the most relevant synthetic policy references, service rules, and procedural guidance while prioritizing transparent reasoning.",
    "The system selected this response because the referenced public-sector records and workflow rules aligned with the request context and supported an explainable outcome.",
    "The response was generated after comparing the request against synthetic guidance materials, domain-specific criteria, and oversight thresholds tied to risk and confidence.",
    "The explanation reflects a standards-aware decision path in which source relevance, policy sensitivity, and confidence level were evaluated before issuing the answer.",
    "The response combines source matching, policy review logic, and traceability criteria to support transparent public-sector decision support.",
]


def target_counts(items, total):
    base = total // len(items)
    remainder = total % len(items)
    counts = {item: base for item in items}
    for item in items[:remainder]:
        counts[item] += 1
    return counts


DOMAIN_TARGETS = target_counts(list(DOMAINS.keys()), ROW_COUNT)
REGION_TARGETS = target_counts(REGIONS, ROW_COUNT)
AGENCY_TARGETS = target_counts(AGENCY_TYPES, ROW_COUNT)


def choose_risk_and_outcome(confidence_score, row_index):
    if confidence_score < 0.76:
        return "High", "Yes", "Escalated"
    if confidence_score < 0.83:
        return "Medium", "Yes", "Reviewed and Approved" if row_index % 2 else "Escalated"
    if row_index % 17 == 0:
        return "High", "Yes", "Rejected"
    if row_index % 5 == 0:
        return "Medium", "Yes", "Reviewed and Approved"
    return "Low", "No", "Approved"


def iso_timestamp(base_date, offset_index, rng):
    dt = base_date + timedelta(days=offset_index, hours=rng.randint(8, 17), minutes=rng.randint(0, 59))
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def make_query(base_query, variant):
    return f"{base_query[:-1]} {variant}" if base_query.endswith("?") else f"{base_query} {variant}"


def next_with_capacity(options, counts):
    for option in options:
        if counts[option] > 0:
            counts[option] -= 1
            return option
    raise ValueError("No remaining capacity for requested options")


def generate_rows():
    rng = random.Random(42)
    base_date = datetime(2025, 1, 6, 8, 0, 0)
    rows = []
    seen_signatures = set()
    row_id = 1
    region_counts = REGION_TARGETS.copy()
    agency_counts = AGENCY_TARGETS.copy()

    for domain, target in DOMAIN_TARGETS.items():
        query_pool = [make_query(query, variant) for query in DOMAINS[domain] for variant in QUERY_VARIANTS]
        rng.shuffle(query_pool)
        generated_for_domain = 0
        query_index = 0

        while generated_for_domain < target:
            query = query_pool[query_index % len(query_pool)]
            data_sources = DATA_SOURCE_OPTIONS[domain][query_index % len(DATA_SOURCE_OPTIONS[domain])]
            ai_response = RESPONSE_TEMPLATES[(query_index + generated_for_domain) % len(RESPONSE_TEMPLATES)]
            explanation = EXPLANATION_TEMPLATES[(query_index + row_id) % len(EXPLANATION_TEMPLATES)]
            policy_alignment = POLICY_ALIGNMENTS[(query_index + generated_for_domain) % len(POLICY_ALIGNMENTS)]
            confidence_score = round(0.70 + ((row_id * 13) % 30) / 100, 2)
            risk_level, human_override_required, final_outcome = choose_risk_and_outcome(confidence_score, row_id)
            region = next_with_capacity(REGIONS, region_counts)
            agency_type = next_with_capacity(AGENCY_TYPES, agency_counts)

            row = {
                "id": f"CGDD-{row_id:03d}",
                "query": query,
                "domain": domain,
                "data_sources": data_sources,
                "ai_response": ai_response,
                "explanation": explanation,
                "policy_alignment": policy_alignment,
                "risk_level": risk_level,
                "confidence_score": f"{confidence_score:.2f}",
                "human_override_required": human_override_required,
                "final_outcome": final_outcome,
                "timestamp": iso_timestamp(base_date, row_id * 2, rng),
                "region": region,
                "agency_type": agency_type,
            }

            signature = (row["query"], row["domain"], row["region"], row["agency_type"])
            if signature not in seen_signatures:
                seen_signatures.add(signature)
                rows.append(row)
                row_id += 1
                generated_for_domain += 1
            else:
                region_counts[region] += 1
                agency_counts[agency_type] += 1

            query_index += 1

    return rows


def write_csv(rows, output_path):
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows, output_path):
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)


def summarize(rows):
    print(f"Rows: {len(rows)}")
    print("Domain distribution:", dict(Counter(row["domain"] for row in rows)))
    print("Region distribution:", dict(Counter(row["region"] for row in rows)))
    print("Agency distribution:", dict(Counter(row["agency_type"] for row in rows)))


def main():
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    rows = generate_rows()
    write_csv(rows, data_dir / "cgdd_v1.csv")
    write_json(rows, data_dir / "cgdd_v1.json")
    print(f"Wrote {len(rows)} records to {data_dir / 'cgdd_v1.csv'}")
    print(f"Wrote {len(rows)} records to {data_dir / 'cgdd_v1.json'}")
    summarize(rows)


if __name__ == "__main__":
    main()
