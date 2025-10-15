# Flight Price Tracker ✈️

A free web-based flight price tracker that scrapes **Kayak.com** to find the cheapest flights. No API keys needed!

## Features

- 🔍 **Real-time search** - Scrapes live data from Kayak.com
- 💰 **Price sorting** - Automatically sorted by price (cheapest first)
- 🔗 **Booking links** - Direct links to Kayak search results
- 🆓 **Completely free** - No API costs, no subscriptions!
- 💻 **Runs locally** - Full control over your data

## How It Works

The app uses Selenium to scrape flight data from Kayak.com, giving you real-time prices without needing expensive flight APIs.

## ⚠️ Important Limitations

- **LOCAL ONLY**: This app requires Selenium + Chrome and **cannot** be deployed to Streamlit Cloud or similar platforms
- Web scraping takes 15-30 seconds per search
- Booking links go to Kayak search pages (not direct booking to airlines)
- May break if Kayak changes their website structure

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
1. Enter origin airport code (e.g., YYZ for Toronto)
2. Enter destination airport code (e.g., LAX for Los Angeles)
3. Select departure date
4. Choose number of adults
5. Click "Search Flights"
6. Wait 15-20 seconds while Kayak is scraped
7. View results sorted by price
8. Click "Book Flight" to go to Kayak!

## Project Structure

```
Flight-Price-Tracker/
├── app.py                    # Main Streamlit application
├── flight_search.py          # Flight search interface
├── multi_scraper.py          # Kayak scraper wrapper
├── scraper_utils.py          # Shared scraper utilities (driver setup)
├── kayak_scraper.py          # Kayak web scraper
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Technologies Used

- **Streamlit** - Web interface
- **Selenium** - Web scraping automation
- **BeautifulSoup** - HTML parsing
- **Pandas** - Data processing
- **ChromeDriver** - Automated browser control

## Why Not Deploy to Streamlit Cloud?

Streamlit Cloud (and most cloud platforms) **do not support Selenium** because:
- They don't have Chrome/Chromium installed
- They don't allow installing browser drivers
- Web scraping requires a full browser environment

**This app must run locally on your machine.**

## Legal Note

This tool is for educational purposes. Please respect Kayak's terms of service and use responsibly.

## License

MIT License - feel free to use and modify!
