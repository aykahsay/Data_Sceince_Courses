import os
import pandas as pd

PROJECT_ROOT   = "/content/Data_Sceince_Courses/time_series/air_quality_project"
DATA_DIR       = os.path.join(PROJECT_ROOT, "data")
RAW_PATH       = os.path.join(DATA_DIR, "raw.json")
PROCESSED_PATH = os.path.join(DATA_DIR, "processed.csv")

def save_raw(df):
    """
    Append newly fetched raw records to raw.json.
    Result = old records + new records (no duplicates).
    """
    if df.empty:
        print("⚠️  No raw data to save.")
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(RAW_PATH):
        existing = pd.read_json(RAW_PATH, orient="records")
        existing["period.datetimeFrom.utc"] = pd.to_datetime(
            existing["period.datetimeFrom.utc"], utc=True
        )
        combined = pd.concat([existing, df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["period.datetimeFrom.utc"])
        combined = combined.sort_values("period.datetimeFrom.utc").reset_index(drop=True)
        print(f"   → Appended: {len(existing)} old + {len(df)} new = {len(combined)} total raw records")
    else:
        combined = df
        print(f"   → First save: {len(combined)} raw records")

    combined.to_json(RAW_PATH, orient="records", indent=2)
    print(f"💾 raw.json → {RAW_PATH}")

def save_processed(df):
    """
    Append new hourly rows to processed.csv.
    Result = old hourly rows + new hourly rows (no duplicates).
    """
    if df.empty:
        print("⚠️  No processed data to save.")
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(PROCESSED_PATH):
        existing = pd.read_csv(PROCESSED_PATH)
        combined = pd.concat([existing, df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["timestamp"])
        combined = combined.sort_values("timestamp").reset_index(drop=True)
        print(f"   → Appended: {len(existing)} old + {len(df)} new = {len(combined)} total hourly rows")
    else:
        combined = df
        print(f"   → First save: {len(combined)} hourly rows")

    combined.to_csv(PROCESSED_PATH, index=False)
    print(f"💾 processed.csv → {PROCESSED_PATH}")
