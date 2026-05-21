import os
import pandas as pd

RAW_PATH = "storage/raw.json"
PROCESSED_PATH = "storage/processed.csv"

def save_raw(df):
    """Append new raw records to raw.json (avoid duplicates)."""
    if df.empty:
        print("⚠️  No raw data to save.")
        return

    if os.path.exists(RAW_PATH):
        existing = pd.read_json(RAW_PATH, orient="records")
        combined = pd.concat([existing, df], ignore_index=True).drop_duplicates()
    else:
        combined = df

    combined.to_json(RAW_PATH, orient="records", indent=2)
    print(f"💾 Raw data saved: {len(combined)} total records in {RAW_PATH}")

def save_processed(df):
    """Append new hourly rows to processed.csv (avoid duplicates)."""
    if df.empty:
        print("⚠️  No processed data to save.")
        return

    if os.path.exists(PROCESSED_PATH):
        existing = pd.read_csv(PROCESSED_PATH)
        combined = pd.concat([existing, df], ignore_index=True).drop_duplicates(subset=["timestamp"])
        combined = combined.sort_values("timestamp")
    else:
        combined = df

    combined.to_csv(PROCESSED_PATH, index=False)
    print(f"💾 Processed data saved: {len(combined)} total rows in {PROCESSED_PATH}")
