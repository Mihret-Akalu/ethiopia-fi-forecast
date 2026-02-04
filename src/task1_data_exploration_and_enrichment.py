import pandas as pd
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(".")
RAW_DATA_PATH = BASE_DIR / "data/raw/ethiopia_fi_unified_data.xlsx"
REF_CODES_PATH = BASE_DIR / "data/raw/reference_codes.xlsx"
OUTPUT_DATA_PATH = BASE_DIR / "data/processed/ethiopia_fi_enriched.csv"
LOG_PATH = BASE_DIR / "data/processed/data_enrichment_log.md"

OUTPUT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

# Load raw data
fi = pd.read_excel(RAW_DATA_PATH)
ref = pd.read_excel(REF_CODES_PATH)

print("Loaded unified dataset:", fi.shape)
print("Loaded reference codes:", ref.shape)

def create_base_record():
    return {col: None for col in fi.columns}

new_records = []
collection_date = datetime.today().strftime("%Y-%m-%d")

# --- Smartphone penetration (usage enabler) ---
smartphone_data = {
    2018: 12, 2019: 14, 2020: 16, 2021: 18, 2022: 21, 2023: 24
}

for year, value in smartphone_data.items():
    r = create_base_record()
    r.update({
        "record_id": f"OBS_SMARTPHONE_{year}",
        "record_type": "observation",
        "pillar": "USAGE",
        "indicator": "Smartphone penetration (% of adults)",
        "indicator_code": "SMARTPHONE_PENETRATION",
        "indicator_direction": "higher_better",
        "value_numeric": value,
        "value_type": "percentage",
        "unit": "%",
        "observation_date": f"{year}-12-31",
        "source_name": "GSMA Mobile Economy Sub-Saharan Africa",
        "source_type": "report",
        "source_url": "https://www.gsma.com/mobileeconomy/",
        "confidence": "medium",
        "collected_by": "Example_Trainee",
        "collection_date": collection_date,
        "notes": "Smartphone access is a key enabler of digital payments"
    })
    new_records.append(r)

# --- Fayda Digital ID Event ---
fayda_id = "EVT_FAYDA_2023"
fayda_event = create_base_record()
fayda_event.update({
    "record_id": fayda_id,
    "record_type": "event",
    "category": "policy",
    "event_name": "Fayda National Digital ID Rollout",
    "event_date": "2023-01-01",
    "source_name": "Government of Ethiopia (INSA)",
    "source_type": "government",
    "source_url": "https://www.insa.gov.et",
    "confidence": "high",
    "collected_by": "Example_Trainee",
    "collection_date": collection_date,
    "notes": "Digital ID rollout reduces KYC friction for account opening"
})
new_records.append(fayda_event)

# --- Impact Link ---
impact_link = create_base_record()
impact_link.update({
    "record_id": "IMPACT_FAYDA_ACCESS",
    "record_type": "impact_link",
    "parent_id": fayda_id,
    "pillar": "ACCESS",
    "related_indicator": "ACC_OWNERSHIP",
    "relationship_type": "causal",
    "impact_direction": "positive",
    "impact_magnitude": "medium",
    "lag_months": 12,
    "evidence_basis": "Comparable digital ID programs in India (Aadhaar) and Kenya"
})
new_records.append(impact_link)

# Append and save
enriched_fi = pd.concat([fi, pd.DataFrame(new_records)], ignore_index=True)
enriched_fi.to_csv(OUTPUT_DATA_PATH, index=False, encoding="utf-8")

# Write log safely
with open(LOG_PATH, "w", encoding="utf-8") as f:
    f.write(f"""
# Data Enrichment Log – Task 1

## Smartphone Penetration (2018–2023)
Source: GSMA Mobile Economy Sub-Saharan Africa  
Confidence: Medium  
Collected by: Example_Trainee  
Collection date: {collection_date}  

## Fayda Digital ID Rollout
Source: Government of Ethiopia (INSA)  
Confidence: High  
Collected by: Example_Trainee  
Collection date: {collection_date}  

## Impact Link
Fayda Digital ID -> Account Ownership (ACCESS pillar)  
Evidence: India Aadhaar, Kenya Huduma  
""")

print("✅ Task 1 completed successfully.")
print("Saved enriched data to:", OUTPUT_DATA_PATH)
print("Saved enrichment log to:", LOG_PATH)
