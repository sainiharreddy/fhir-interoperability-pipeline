import pandas as pd
import numpy as np
import json

def generate_messy_ehr_data():
    np.random.seed(101)
    n_records = 1500
    
    # Generate raw, realistic data components
    patient_ids = [f"PAT-{np.random.randint(10000, 99999)}" for _ in range(n_records)]
    first_names = np.random.choice(['John', 'Mary', 'Srinivas', 'Sarah', 'Amit', 'Elena', 'Michael'], size=n_records)
    last_names = np.random.choice(['Smith', 'Reddy', 'Johnson', 'Rodriguez', 'Patel', 'Davis', 'Kim'], size=n_records)
    birth_dates = np.random.choice(['1974-05-12', '1994-08-29', '1965-11-23', '2001-02-14', None], size=n_records, p=[0.3, 0.3, 0.2, 0.15, 0.05])
    genders = np.random.choice(['male', 'female', 'MALE', 'F', 'unknown', None], size=n_records, p=[0.4, 0.4, 0.05, 0.05, 0.05, 0.05])
    icd10_codes = np.random.choice(['M81.0', 'C34.90', 'Z00.00', 'R69', 'INVALID_CODE', None], size=n_records, p=[0.3, 0.3, 0.2, 0.1, 0.05, 0.05])
    systolic_bp = np.random.choice([120, 140, 999, -50, 115], size=n_records, p=[0.5, 0.2, 0.05, 0.05, 0.2])
    
    data = {
        'Internal_Patient_ID': patient_ids,
        'Given_Name': first_names,
        'Family_Name': last_names,
        'DOB': birth_dates,
        'Gender_Code': genders,
        'Primary_Diagnosis_ICD10': icd10_codes,
        'Vitals_Systolic_mmHg': systolic_bp
    }
    
    df = pd.DataFrame(data)
    df.to_csv("data/raw_ehr_export.csv", index=False)
    print("Successfully generated 1,500 raw, unstandardized EHR records: saved to data/raw_ehr_export.csv")

if __name__ == "__main__":
    generate_messy_ehr_data()
