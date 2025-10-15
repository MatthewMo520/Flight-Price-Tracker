from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scrapers'))

from multi_scraper import search_all_sources

app = Flask(__name__)
CORS(app)

#----- API ROUTES -----#

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Flight Price Tracker API is running"})

@app.route('/api/search-flights', methods=['POST'])
def search_flights():
    try:
        data = request.get_json()

        required_fields = ['origin', 'destination', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        origin = data['origin'].upper()
        destination = data['destination'].upper()
        date = data['date']
        adults = data.get('adults', 1)

        if len(origin) != 3 or len(destination) != 3:
            return jsonify({"error": "Airport codes must be 3 letters"}), 400

        print(f"[API] Searching flights: {origin} -> {destination} on {date}")

        flights = search_all_sources(origin, destination, date, adults)

        print(f"[API] Found {len(flights)} flights")

        return jsonify({
            "success": True,
            "count": len(flights),
            "flights": flights
        })

    except Exception as e:
        print(f"[API] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
