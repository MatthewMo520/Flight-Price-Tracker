from kayak_scraper import scrape_kayak_flights

def search_all_sources(origin, destination, departure_date, adults=1):
    print(f"\n{'='*60}")
    print(f"Searching flights from {origin} to {destination} on {departure_date}")
    print(f"Checking Kayak.com...")
    print(f"{'='*60}\n")

    try:
        flights = scrape_kayak_flights(origin, destination, departure_date, adults)
        if flights:
            print(f"[OK] Found {len(flights)} flights")
        else:
            print(f"[WARN] No flights found")
    except Exception as e:
        print(f"[FAIL] Kayak scraper failed: {e}")
        flights = []

    flights.sort(key=lambda x: float(x['price']))

    print(f"\n{'='*60}")
    print(f"Total flights found: {len(flights)}")
    if flights:
        print(f"Cheapest: ${flights[0]['price']}")
        print(f"Most expensive: ${flights[-1]['price']}")
    print(f"{'='*60}\n")

    return flights
