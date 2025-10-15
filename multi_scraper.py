from kayak_scraper import scrape_kayak_flights
from expedia_scraper import scrape_expedia_flights
from google_flights_scraper import scrape_google_flights
import concurrent.futures

def search_all_sources(origin, destination, departure_date, adults=1):
    """
    Search multiple flight sources and combine results

    Args:
        origin: Origin airport code
        destination: Destination airport code
        departure_date: Date in YYYY-MM-DD format
        adults: Number of passengers

    Returns:
        Combined list of flights from all sources, sorted by price
    """
    print(f"\n{'='*60}")
    print(f"Searching flights from {origin} to {destination} on {departure_date}")
    print(f"Checking Kayak, Expedia, and Google Flights...")
    print(f"{'='*60}\n")

    all_flights = []

    # Run all three scrapers in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all three scrapers
        kayak_future = executor.submit(scrape_kayak_flights, origin, destination, departure_date, adults)
        expedia_future = executor.submit(scrape_expedia_flights, origin, destination, departure_date, adults)
        google_future = executor.submit(scrape_google_flights, origin, destination, departure_date, adults)

        # Get results
        try:
            kayak_flights = kayak_future.result(timeout=90)
            all_flights.extend(kayak_flights)
        except Exception as e:
            print(f"[Error] Kayak scraper failed: {e}")

        try:
            expedia_flights = expedia_future.result(timeout=90)
            all_flights.extend(expedia_flights)
        except Exception as e:
            print(f"[Error] Expedia scraper failed: {e}")

        try:
            google_flights = google_future.result(timeout=90)
            all_flights.extend(google_flights)
        except Exception as e:
            print(f"[Error] Google Flights scraper failed: {e}")

    # Remove duplicates (same price and airline)
    seen = set()
    unique_flights = []

    for flight in all_flights:
        key = (flight['airline'], flight['price'])
        if key not in seen:
            seen.add(key)
            unique_flights.append(flight)

    # Sort by price
    unique_flights.sort(key=lambda x: float(x['price']))

    print(f"\n{'='*60}")
    print(f"Total flights found: {len(unique_flights)}")
    if unique_flights:
        print(f"Cheapest: ${unique_flights[0]['price']} ({unique_flights[0]['source']})")
        print(f"Most expensive: ${unique_flights[-1]['price']} ({unique_flights[-1]['source']})")
    print(f"{'='*60}\n")

    return unique_flights
