import requests
import pandas as pd
from storage.settings import OPENAQ_API_KEY, BASE_URL

HEADERS = {"X-API-Key": OPENAQ_API_KEY}

def get_sensor_id(location_id, parameter="pm25"):
    url = f"{BASE_URL}/locations/{location_id}/sensors"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    sensors = r.json().get("results", [])
    for s in sensors:
        if s.get("parameter", {}).get("name", "").lower() == parameter.lower():
            return s["id"]
    available = [s.get("parameter", {}).get("name") for s in sensors]
    raise ValueError(f"Sensor '{parameter}' not found. Available: {available}")

def fetch_measurements(location_id, parameter="pm25", since=None, limit=1000):
    """
    Fetch newest records first (sort=desc), then drop anything
    at or before the checkpoint timestamp — so each run is truly incremental.
    """
    sensor_id = get_sensor_id(location_id, parameter)
    url = f"{BASE_URL}/sensors/{sensor_id}/measurements"

    params = {
        "limit": limit,
        "sort": "desc",          # ← newest records first
        "order_by": "datetime",  # ← sort key
    }
    if since:
        params["date_from"] = since  # belt-and-suspenders hint to the API

    print(f"📡 Fetching '{parameter}' data (newest first, since: {since or 'all'})")
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()

    results = r.json().get("results", [])
    df = pd.json_normalize(results)

    if df.empty:
        print("   → 0 records returned by API")
        return df

    # ── Client-side filter: drop records at or before the checkpoint ──────────
    TIME_COL = "period.datetimeFrom.utc"
    if since and TIME_COL in df.columns:
        df[TIME_COL] = pd.to_datetime(df[TIME_COL], utc=True)
        since_dt = pd.to_datetime(since, utc=True)
        before = len(df)
        df = df[df[TIME_COL] > since_dt].copy()
        print(f"   → {before} returned by API, {len(df)} new after checkpoint filter")
    else:
        print(f"   → {len(df)} records fetched (no checkpoint filter applied)")

    return df
