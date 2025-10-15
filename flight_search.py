from multi_scraper import search_all_sources

#----SEARCHES FOR FLIGHT OPTIONS FROM MULTIPLE SOURCES----#
def search_flights(origin, destination, departure_date, adults=1):
    """
    Search for flights using multiple sources (Kayak, Skyscanner)
    Returns combined list of flights with specific booking links
    """
    try:
        flights = search_all_sources(origin, destination, departure_date, adults)
        return flights
    except Exception as e:
        print(f"Error searching flights: {e}")
        import traceback
        traceback.print_exc()
        return []
