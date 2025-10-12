import os
from amadeus import Client
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY and API_SECRET must be set in environment variables")

amadeus = Client(
    client_id=API_KEY,
    client_secret=API_SECRET
)