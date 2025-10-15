import React, { useState } from 'react';
import './App.css';

// Set your backend URL here - change this when deploying
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    date: '',
    adults: 1
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [flights, setFlights] = useState([]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const searchFlights = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setFlights([]);

    try {
      const response = await fetch(`${API_URL}/api/search-flights`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to search flights');
      }

      setFlights(data.flights);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>✈️ Flight Price Tracker</h1>
        <p>Find the cheapest flights from Kayak.com</p>
      </header>

      <div className="container">
        <form onSubmit={searchFlights} className="search-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="origin">Origin Airport</label>
              <input
                type="text"
                id="origin"
                name="origin"
                placeholder="e.g., YYZ"
                maxLength="3"
                value={formData.origin}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="destination">Destination Airport</label>
              <input
                type="text"
                id="destination"
                name="destination"
                placeholder="e.g., LAX"
                maxLength="3"
                value={formData.destination}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="date">Departure Date</label>
              <input
                type="date"
                id="date"
                name="date"
                value={formData.date}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="adults">Adults</label>
              <input
                type="number"
                id="adults"
                name="adults"
                min="1"
                max="10"
                value={formData.adults}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>

          <button type="submit" disabled={loading} className="search-btn">
            {loading ? 'Searching...' : 'Search Flights'}
          </button>
        </form>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Searching Kayak.com... This may take 15-20 seconds.</p>
          </div>
        )}

        {error && (
          <div className="error">
            <p>Error: {error}</p>
          </div>
        )}

        {flights.length > 0 && (
          <div className="results">
            <h2>Found {flights.length} Flights</h2>
            <div className="cheapest-info">
              💰 Cheapest: {flights[0].airline} - ${flights[0].price}
            </div>

            <div className="flights-table">
              <table>
                <thead>
                  <tr>
                    <th>Airline</th>
                    <th>Price</th>
                    <th>Departure</th>
                    <th>Arrival</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {flights.map((flight, index) => (
                    <tr key={index}>
                      <td>{flight.airline}</td>
                      <td className="price">${flight.price}</td>
                      <td>{flight.departure}</td>
                      <td>{flight.arrival}</td>
                      <td>
                        <a
                          href={flight.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="book-btn"
                        >
                          Book
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
