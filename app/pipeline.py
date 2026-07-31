import os
import pandas as pd
import numpy as np
import json
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date

# Define the federated FHIR Patient Schema Standard
class FHIRPatientResource(BaseModel):
    resourceType: str = "Patient"
    id: str = Field(..., description="Logical alphanumeric source system identifier")
    active: bool = True
    name: List[dict] # FHIR structured naming format
    gender: str # Must map strictly to administrative-gender value sets
    birthDate: Optional[date] = None
    
    @validator('gender', pre=True)
    def clean_fhir_gender(cls, v):
        if not v or pd.isna(v):
            return "unknown"
        v_clean = str(v).strip().lower()
        if v_clean in ['male', 'm']: return 'male'
        if v_clean in ['female', 'f']: return 'female'
        return 'unknown'

# Define the federated FHIR Observation Standard for Clinical Vitals
class FHIRObservationResource(BaseModel):
    resourceType: str = "Observation"
    status: str = "final"
    code: dict = {"coding": [{"system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure"}]}
    subject: dict # Reference link back to the parent Patient resource
    valueQuantity: dict
    
    @validator('valueQuantity')
    def validate_vitals_range(cls, v):
        val = v.get("value")
        if val is None or val < 30 or val > 300:
            raise ValueError(f"Physiologically impossible or critical validation outlier systolic value: {val}")
        return v

def run_interoperability_pipeline():
    print("Initializing FHIR Schema Compliance & Ingestion Pipeline...")
    raw_df = pd.read_csv("data/raw_ehr_export.csv")
    
    clean_fhir_bundle = []
    error_registry_logs = []
    
    total_records = len(raw_df)
    passed_validations = 0
    
    for idx, row in raw_df.iterrows():
        errors = []
        p_id = str(row['Internal_Patient_ID'])
        
        # 1. Enforce Primary Diagnostics constraints (ICD-10 check)
        diag = row['Primary_Diagnosis_ICD10']
        if not diag or pd.isna(diag) or diag == 'INVALID_CODE':
            errors.append(f"Clinical Taxonomy Fault: Malformed or missing ICD-10 identifier ({diag})")
            
        # 2. Extract and format dates safely
        dob_val = None
        if pd.notna(row['DOB']) and row['DOB']:
            try:
                dob_val = date.fromisoformat(str(row['DOB']))
            except Exception:
                errors.append("Structural Core Fault: Malformed ISO 8601 DOB layout string")
        else:
            errors.append("Demographic Core Fault: Null Patient DOB field detected")
            
        # 3. Process structural schema map through Pydantic borders
        try:
            patient_fhir = FHIRPatientResource(
                id=p_id,
                name=[{"use": "official", "family": str(row['Family_Name']), "given": [str(row['Given_Name'])]}],
                gender=str(row['Gender_Code']),
                birthDate=dob_val
            )
            
            # Map the vitals
            sys_val = float(row['Vitals_Systolic_mmHg'])
            vitals_fhir = FHIRObservationResource(
                subject={"reference": f"Patient/{p_id}"},
                valueQuantity={"value": sys_val, "unit": "mm[Hg]", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"}
            )
        except Exception as e:
            errors.append(f"Pydantic Validation Constraint Violation: {str(e)}")
            
        # If any errors accumulated, route to Data Quality Error Registry
        if errors:
            error_registry_logs.append({
                "Internal_Patient_ID": p_id,
                "Assigned_Given_Name": row['Given_Name'],
                "Assigned_Family_Name": row['Family_Name'],
                "Pipeline_Data_Fault_Descriptions": errors
            })
        else:
            passed_validations += 1
            # Bundle valid clinical assets into an interconnected transaction schema layout
            clean_fhir_bundle.append({
                "patient_resource": patient_fhir.dict(),
                "observation_resource": vitals_fhir.dict(),
                "mapped_icd10_code": diag
            })
            
    # Calculate Data Quality Health Index
    dq_health_index = (passed_validations / total_records) * 100
    
    # Save target production metrics outputs
    os.makedirs("data/production_output", exist_ok=True)
    
    with open("data/production_output/clean_fhir_bundle.json", "w") as f:
        json.dump(clean_fhir_bundle, f, indent=2, default=str)
        
    error_df = pd.DataFrame(error_registry_logs)
    error_df.to_csv("data/production_output/data_quality_error_registry.csv", index=False)
    
    print("\n=======================================================")
    print("       PIPELINE COMPLIANCE ENGINE AUDIT RUN METRICS     ")
    print("=======================================================")
    print(f"Total Raw EHR Records Processed : {total_records}")
    print(f"FHIR-Compliant Records Accepted : {passed_validations}")
    print(f"Non-Compliant Records Rejected  : {len(error_registry_logs)}")
    print(f"System Data Quality Health Index: {dq_health_index:.2f}%")
    print("=======================================================")
    print("Outputs successfully saved to 'data/production_output/' folder.")

if __name__ == "__main__":
    run_interoperability_pipeline()
