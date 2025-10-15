# Flight Price Tracker ✈️

A free web-based flight price tracker that scrapes Kayak.com to find the cheapest flights.

## Features

- 🔍 Search flights between any two airports
- 💰 Automatically sorted by price (cheapest first)
- 📊 Visual price comparison chart
- 🔗 Direct booking links to Kayak
- 🆓 **Completely free** - no API costs!

## How It Works

The app uses Selenium to scrape flight data from Kayak.com, giving you real-time prices without needing expensive flight APIs.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Flight-Price-Tracker.git
cd Flight-Price-Tracker
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Then:
1. Enter origin airport code (e.g., YYZ)
2. Enter destination airport code (e.g., LAX)
3. Select departure date
4. Click "Search Flights"
5. Wait 15-20 seconds for results
6. View cheapest flights with clickable booking links!

## Project Structure

```
Flight-Price-Tracker/
├── app.py                 # Main Streamlit application
├── flight_search.py       # Flight search interface
├── kayak_scraper.py       # Kayak web scraper using Selenium
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Technologies Used

- **Streamlit** - Web interface
- **Selenium** - Web scraping
- **BeautifulSoup** - HTML parsing
- **Pandas** - Data processing
- **Plotly** - Data visualization

## Limitations

- Search takes 15-20 seconds (web scraping vs instant API)
- Booking links go to Kayak search page (not direct booking)
- May break if Kayak changes their website structure

## Legal Note

This tool is for educational purposes. Please respect Kayak's terms of service and use responsibly.

## License

MIT License - feel free to use and modify!
