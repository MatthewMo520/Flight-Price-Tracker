from kayak_scraper import scrape_kayak_flights

#----SEARCHES FOR FLIGHT OPTIONS AND RETURNS PRICE, AIRLINE AND DEPARTURE/ARRIVAL TIMES----#
def search_flights(origin, destination, departure_date, adults=1):
    """
    Search for flights using Kayak web scraping
    Returns list of flights with booking links
    """
    try:
        print(f"Searching for flights from {origin} to {destination} on {departure_date}")
        flights = scrape_kayak_flights(origin, destination, departure_date, adults)
        return flights
    except Exception as e:
        print(f"Error searching flights: {e}")
        import traceback
        traceback.print_exc()
        return []
