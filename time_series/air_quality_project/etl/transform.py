import pandas as pd

TIME_COL = "period.datetimeFrom.utc"

def clean(df):
    """Parse timestamps, sort, drop duplicates, keep useful columns."""
    if df.empty:
        print("⚠️  Empty dataframe — nothing to clean.")
        return df

    if TIME_COL not in df.columns:
        raise ValueError(f"Missing '{TIME_COL}'. Got: {list(df.columns)}")

    df[TIME_COL] = pd.to_datetime(df[TIME_COL], utc=True)
    df = df.sort_values(TIME_COL).drop_duplicates(subset=[TIME_COL]).reset_index(drop=True)

    keep = [TIME_COL, "value", "parameter.name", "parameter.units"]
    df   = df[[c for c in keep if c in df.columns]].copy()

    print(f"   → {len(df)} records after cleaning")
    print(f"   → Range: {df[TIME_COL].min()}  →  {df[TIME_COL].max()}")
    return df

def aggregate_hourly(df):
    """Resample cleaned data to hourly mean."""
    if df.empty:
        return df

    df      = df.set_index(TIME_COL)
    hourly  = df["value"].resample("1h").mean().reset_index()
    hourly.columns = ["timestamp", "pm25"]
    hourly["timestamp"] = hourly["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"   → {len(hourly)} hourly buckets aggregated")
    return hourly
