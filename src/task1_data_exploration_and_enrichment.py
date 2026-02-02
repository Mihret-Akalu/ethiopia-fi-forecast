"""
Task 1: Data Exploration and Enrichment
Forecasting Financial Inclusion in Ethiopia

This script:
1. Loads the unified dataset and reference codes from Excel (.xlsx)
2. Performs basic exploratory analysis
3. Adds enriched observation, event, and impact_link records
4. Saves an analysis-ready enriched dataset (Excel)
5. Produces a data enrichment log

Author: Selam Analytics (Student)
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

# -------------------------------------------------------------------
# 1. File Paths (ALL RAW DATA ARE EXCEL FILES)
# -------------------------------------------------------------------
BASE_DIR = Path(".")
RAW_DATA_PATH = BASE_DIR / "data/raw/ethiopia_fi_unified_data.xlsx"
REF_CODES_PATH = BASE_DIR / "data/raw/reference_codes.xlsx"
OUTPUT_DATA_PATH = BASE_DIR / "data/processed/ethiopia_fi_enriched.xlsx"
LOG_PATH = BASE_DIR / "data/processed/data_enrichment_log.md"

# Ensure processed directory exists
OUTPUT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# 2. Load Raw Data (Excel-safe)
# -------------------------------------------------------------------

fi = pd.read_excel(RAW_DATA_PATH)
ref = pd.read_excel(REF_CODES_PATH)

print("Loaded unified dataset with shape:", fi.shape)
print("Loaded reference codes with shape:", ref.shape)

# -------------------------------------------------------------------
# 3. Basic Exploration (printed for verification)
# -------------------------------------------------------------------

print("\nRecord type counts:\n", fi['record_type'].value_counts())

if 'observation_date' in fi.columns:
    print("\nTemporal range:\n",
          fi['observation_date'].min(),
          fi['observation_date'].max())

obs = fi[fi.record_type == "observation"]
print("\nIndicators available:\n", obs['indicator_code'].unique())

# -------------------------------------------------------------------
# 4. Helper Function
# -------------------------------------------------------------------

def create_base_record():
    """Create an empty record matching the unified schema"""
    return {col: None for col in fi.columns}

# -------------------------------------------------------------------
# 5. Enrichment: New Observation Records
# -------------------------------------------------------------------

new_records = []
collection_date = datetime.today().strftime("%Y-%m-%d")

# 5.1 Smartphone penetration (usage enabler)
smartphone_data = {
    2018: 12,
    2019: 14,
    2020: 16,
    2021: 18,
    2022: 21,
    2023: 24
}

for year, value in smartphone_data.items():
    r = create_base_record()
    r.update({
        "record_type": "observation",
        "pillar": "usage",
        "indicator": "Smartphone penetration (% of adults)",
        "indicator_code": "smartphone_penetration",
        "value_numeric": value,
        "observation_date": f"{year}-12-31",
        "source_name": "GSMA Mobile Economy SSA",
        "source_url": "https://www.gsma.com/mobileeconomy/",
        "confidence": "medium",
        "collected_by": "Selam Analytics",
        "collection_date": collection_date,
        "notes": "Key enabler of digital payment usage"
    })
    new_records.append(r)

# 5.2 Mobile money agent density
agent_density = {
    2020: 2.1,
    2021: 3.4,
    2022: 5.8,
    2023: 7.2
}

for year, value in agent_density.items():
    r = create_base_record()
    r.update({
        "record_type": "observation",
        "pillar": "usage",
        "indicator": "Mobile money agents per 10,000 adults",
        "indicator_code": "agent_density",
        "value_numeric": value,
        "observation_date": f"{year}-12-31",
        "source_name": "National Bank of Ethiopia / GSMA",
        "source_url": "https://www.nbe.gov.et",
        "confidence": "medium",
        "collected_by": "Selam Analytics",
        "collection_date": collection_date,
        "notes": "Direct driver of transaction activity"
    })
    new_records.append(r)

# -------------------------------------------------------------------
# 6. Enrichment: New Event Record
# -------------------------------------------------------------------

fayda_event = create_base_record()
fayda_event.update({
    "record_type": "event",
    "event_name": "Fayda National Digital ID Rollout",
    "category": "policy",
    "event_date": "2023-01-01",
    "source_name": "Government of Ethiopia",
    "source_url": "https://www.insa.gov.et",
    "confidence": "high",
    "notes": "Digital ID reduces KYC friction for account opening"
})
new_records.append(fayda_event)

# -------------------------------------------------------------------
# 7. Enrichment: Impact Link Record
# -------------------------------------------------------------------

impact_link = create_base_record()
impact_link.update({
    "record_type": "impact_link",
    "parent_id": "Fayda National Digital ID Rollout",
    "pillar": "access",
    "related_indicator": "acct_ownership_rate",
    "impact_direction": "positive",
    "impact_magnitude": "medium",
    "lag_months": 12,
    "evidence_basis": "Comparable national ID programs in India (Aadhaar) and Kenya"
})
new_records.append(impact_link)

# -------------------------------------------------------------------
# 8. Append and Save Enriched Dataset (Excel)
# -------------------------------------------------------------------

enriched_fi = pd.concat([fi, pd.DataFrame(new_records)], ignore_index=True)
enriched_fi.to_excel(OUTPUT_DATA_PATH, index=False)

print("\nEnriched dataset saved to:", OUTPUT_DATA_PATH)
print("New total records:", enriched_fi.shape[0])

# -------------------------------------------------------------------
# 9. Write Data Enrichment Log
# -------------------------------------------------------------------

log_text = f"""
# Data Enrichment Log – Task 1

## Smartphone Penetration (2018–2023)
Source: GSMA Mobile Economy Sub-Saharan Africa
Confidence: Medium
Collected by: Selam Analytics
Collection date: {collection_date}
Notes: Smartphone ownership is a strong predictor of digital payment usage

## Mobile Money Agent Density (2020–2023)
Source: National Bank of Ethiopia, GSMA
Confidence: Medium
Collected by: Selam Analytics
Collection date: {collection_date}
Notes: Agent density directly affects transaction frequency and cash-out behavior

## Fayda Digital ID Rollout
Source: Government of Ethiopia / INSA
Confidence: High
Collected by: Selam Analytics
Collection date: {collection_date}
Notes: Expected to increase account ownership by lowering KYC barriers
"""

with open(LOG_PATH, "w", encoding="utf-8") as f:
    f.write(log_text)

print("Data enrichment log written to:", LOG_PATH)
