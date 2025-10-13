from amadeus_client import amadeus
#----SEARCHES FOR FLIGHT OPTIONS AND RETURNS PRICE, AIRLINE AND DEPARTURE/ARRIVAL TIMES----#
def search_flights(origin, destination, departure_date, adults=1):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=adults,
            max=5
        )
        flights = response.data
        results = []
        for flight in flights:
            offer = {
                "airline": flight['validatingAirlineCodes'][0],
                "price": flight['price']['total'],
                "departure": flight['itineraries'][0]['segments'][0]['departure']['at'],
                "arrival": flight['itineraries'][0]['segments'][0]['arrival']['at'],
                "link": flight.get('offerItems', [{}])[0].get('services', [{}])[0].get('segments', [{}])[0].get('flightOfferURL', '#')
            }
            results.append(offer)
        return results
    except Exception as e:
        print(f"Error searching flights: {e}")
        return []
