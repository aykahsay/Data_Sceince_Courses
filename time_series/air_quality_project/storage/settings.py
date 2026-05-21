import os
from dotenv import load_dotenv
load_dotenv()

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")
BASE_URL = "https://api.openaq.org/v3"
LOCATION_ID = 5199863  # Kihumo Village || Antenna Array, Nairobi
