from flight_search import search_flights

origin = "YYZ"
destination = "LAX"
departure_date = "2025-12-01"
adults = 1

flights = search_flights

for i, f in enumerate(flights, 1):
    print(f"Flight Option {i}:")
    print(f"  Airline: {f['airline']}")
    print(f"  Price: ${f['price']}")
    print(f"  Departure: {f['departure']}")
    print(f"  Arrival: {f['arrival']}")
    print()