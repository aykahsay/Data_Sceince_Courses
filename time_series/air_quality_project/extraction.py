import requests
import pandas as pd

def get_air_quality(location_id, api_key):

    url = f"https://api.openaq.org/v3/locations/{location_id}"

    headers = {
        "X-API-Key": api_key
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    df = pd.json_normalize(data["results"])

    return df
