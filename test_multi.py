from flight_search import search_flights

flights = search_flights('YYZ', 'LAX', '2025-11-20', 1)
print(f"\n\nFinal Results: {len(flights)} flights")
for f in flights[:5]:
    print(f"{f['source']}: {f['airline']} ${f['price']}")
