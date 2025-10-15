import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from datetime import datetime

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

#----SEARCHES FOR FLIGHT OPTIONS AND RETURNS PRICE, AIRLINE AND DEPARTURE/ARRIVAL TIMES----#
def search_flights(origin, destination, departure_date, adults=1):
    try:
        # SerpAPI parameters for Google Flights
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": departure_date,
            "adults": adults,
            "currency": "USD",
            "hl": "en",
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        flights_data = []

        # Check if we have best flights data
        if "best_flights" in results:
            flights_list = results["best_flights"]
        elif "other_flights" in results:
            flights_list = results["other_flights"]
        else:
            print("No flights found in response")
            return []

        # Extract flight information
        for flight in flights_list[:10]:  # Limit to 10 flights
            # Get first flight segment for departure/arrival times
            first_flight = flight.get("flights", [{}])[0]
            last_flight = flight.get("flights", [{}])[-1]

            # Extract airline (from first segment)
            airline = first_flight.get("airline", "Unknown")

            # Extract price
            price = flight.get("price", 0)

            # Extract departure and arrival times
            departure_time = first_flight.get("departure_airport", {}).get("time", "")
            arrival_time = last_flight.get("arrival_airport", {}).get("time", "")

            # Convert times to full datetime format (YYYY-MM-DD HH:MM)
            if departure_time:
                departure_datetime = f"{departure_date} {departure_time}"
            else:
                departure_datetime = ""

            # For arrival, we need to handle potential next-day arrivals
            # For now, use same date (can be improved with flight duration)
            if arrival_time:
                arrival_datetime = f"{departure_date} {arrival_time}"
            else:
                arrival_datetime = ""

            # Get booking token for deep link
            booking_token = flight.get("booking_token", "")

            # Generate booking link
            if booking_token:
                # Create deep link using booking token
                booking_link = f"https://www.google.com/travel/flights/booking?booking_token={booking_token}"
            else:
                # Fallback to general search
                booking_link = f"https://www.google.com/flights?hl=en#flt={origin}.{destination}.{departure_date}"

            flights_data.append({
                "airline": airline,
                "price": str(price),
                "departure": departure_datetime,
                "arrival": arrival_datetime,
                "link": booking_link
            })

        return flights_data

    except Exception as e:
        print(f"Error searching flights with SerpAPI: {e}")
        import traceback
        traceback.print_exc()
        return []
