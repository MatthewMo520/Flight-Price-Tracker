import os
from amadeus import Client

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

amadeus = Client(
    client_id=API_KEY,
    client_secret=API_SECRET
)