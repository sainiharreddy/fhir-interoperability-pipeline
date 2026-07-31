# fhir-interoperability-pipeline
# US Healthcare Interoperability & Data Quality Governance Engine

An enterprise-grade, rule-driven clinical data extraction, transformation, and load (ETL) compliance pipeline designed to ingest unstandardized Electronic Health Record (EHR) registries, enforce rigid structural schema boundaries, and map flat patient variables into federated **HL7 FHIR (Fast Healthcare Interoperability Resources)** JSON data structures.

This engine directly addresses the ONC Cures Act and CMS interoperability mandates by establishing an automated **Data Quality Firewall**. It detects, standardizes, and strips out dangerous clinical data defects (such as invalid ICD-10 codes, missing demographic markers, or impossible vital-sign telemetry outliers) before they can propagate down to high-stakes clinical decision systems or trigger severe insurance claim rejections.

---

## 🚀 Core Architectural Features
- **US Core FHIR Ingestion Gateway:** Designed strict object mapping layouts to convert legacy flat-file patient and vitals logs into interconnected, standardized JSON schemas (`Patient` and `Observation` profiles).
- **Perimeter Schema Enforcement:** Built runtime data-integrity perimeters using **Pydantic v2 Core**, intercepting malformed payloads, formatting ISO 8601 timestamps, and mapping unstructured demographic variances into strict administrative value sets.
- **Dynamic Data Quality Auditing:** Implemented a system compliance monitoring module that evaluates raw system logs, computes an aggregate **Data Quality Health Index**, and routes defective patient entries into an isolated registry log to facilitate targeted database cleaning.

---

## 📁 Repository Structure
```text
fhir-interoperability-pipeline/
│
├── app/
│   └── pipeline.py         # FHIR Schema mapping, Pydantic type-casting, and auditing logic
│
├── data/
│   └── production_output/
│       ├── clean_fhir_bundle.json            # Interoperable, transaction-ready JSON records
│       └── data_quality_error_registry.csv  # Detailed audit logs of rejected data defects
│
├── generate_raw_ehr.py    # Multi-defect 1,500-sample raw clinical registry simulator
├── requirements.txt        # Enterprise environment dependency manifest
└── README.md               # Production architecture documentation
```

---

## 🛡️ Ingestion Governance & Validation Safeguards
The pipeline screens raw input vectors against three strict regulatory and clinical health rules:
1. **Clinical Taxonomy Verification:** Validates primary diagnoses against correct ICD-10 configurations; isolates rows flagged with missing or unmapped medical coding tags.
2. **Physiologically Impossible Outliers:** Intercepts out-of-bounds telemetry (e.g., blood pressure reading inputs outside a strict 30–300 mmHg threshold) to prevent dirty field data from crashing downstream dashboards.
3. **Demographic Completeness Bounds:** Mandates strict ISO 8601 formatting for patient dates of birth, enforcing a critical identity-matching baseline for multi-system health network integrations.

---

## 📊 Live Pipeline Performance Run Audit Metrics

### Ingestion Metrics Table

| Performance Metrics Parameter | Value Summary Outcome |
| :--- | :--- |
| **Total Raw EHR Records Processed** | 1,500 |
| **FHIR-Compliant Records Accepted** | 1,173 |
| **Non-Compliant Records Rejected** | 327 |
| **System Data Quality Health Index** | **78.20%** |

---

## 🩺 Mapped Production Output Example (FHIR Transaction Resource)
```json
{
  "patient_resource": {
    "resourceType": "Patient",
    "id": "PAT-74291",
    "active": true,
    "name": [
      {
        "use": "official",
        "family": "Smith",
        "given": ["John"]
      }
    ],
    "gender": "male",
    "birthDate": "1994-08-29"
  },
  "observation_resource": {
    "resourceType": "Observation",
    "status": "final",
    "code": {
      "coding": [
        {
          "system": "http://loinc.org",
          "code": "8480-6",
          "display": "Systolic blood pressure"
        }
      ]
    },
    "subject": {
      "reference": "Patient/PAT-74291"
    },
    "valueQuantity": {
      "value": 120.0,
      "unit": "mm[Hg]",
      "system": "http://unitsofmeasure.org",
      "code": "mm[Hg]"
    }
  },
  "mapped_icd10_code": "M81.0"
}
```

---

## 🛠️ Technology Stack & Engineering Libraries
- **Language:** Python 3.11+
- **Data Architectures & Schemas:** Pydantic Core v2, JSON Standard Libraries
- **Data Engineering Core:** Pandas, NumPy
- **Healthcare Standards Framework:** HL7 FHIR US Core Implementation Profiles
