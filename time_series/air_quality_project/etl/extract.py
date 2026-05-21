import requests
import pandas as pd
from settings.settings import OPENAQ_API_KEY, BASE_URL

HEADERS  = {"X-API-Key": OPENAQ_API_KEY}
TIME_COL = "period.datetimeFrom.utc"

def get_sensor_id(location_id, parameter="pm25"):
    """Find the sensor ID for a given parameter at a location."""
    url = f"{BASE_URL}/locations/{location_id}/sensors"
    r   = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    sensors = r.json().get("results", [])
    for s in sensors:
        if s.get("parameter", {}).get("name", "").lower() == parameter.lower():
            return s["id"]
    available = [s.get("parameter", {}).get("name") for s in sensors]
    raise ValueError(f"Sensor '{parameter}' not found. Available: {available}")

def fetch_measurements(location_id, parameter="pm25", since=None, limit=1000):
    """
    Fetch latest 1000 records from API.

    First run  (since=None) → keep all 1000 records
    Later runs (since=<ts>) → keep only records AFTER checkpoint
                               so only new records get passed to load
    The load layer then APPENDS these to existing data.
    """
    sensor_id = get_sensor_id(location_id, parameter)
    url       = f"{BASE_URL}/sensors/{sensor_id}/measurements"
    params    = {"limit": limit}

    print(f"📡 Fetching latest {limit} '{parameter}' records from API...")
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()

    results = r.json().get("results", [])
    print(f"   → {len(results)} total records returned by API")

    if not results:
        return pd.DataFrame()

    df = pd.json_normalize(results)

    if TIME_COL not in df.columns:
        print(f"⚠️  Timestamp column missing. Got: {list(df.columns)}")
        return pd.DataFrame()

    # Parse and sort oldest → newest
    df[TIME_COL] = pd.to_datetime(df[TIME_COL], utc=True)
    df = df.sort_values(TIME_COL).reset_index(drop=True)

    if since:
        # Keep only records strictly AFTER the checkpoint
        since_dt       = pd.to_datetime(since, utc=True)
        before         = len(df)
        df             = df[df[TIME_COL] > since_dt].reset_index(drop=True)
        already_seen   = before - len(df)
        print(f"   → {already_seen} already-loaded records excluded (≤ {since})")
        print(f"   → {len(df)} new records to append")
    else:
        print(f"   → First run: all {len(df)} records will be loaded")

    return df
