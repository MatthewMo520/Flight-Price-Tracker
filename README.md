# Flight Price Tracker ✈️

A free web-based flight price tracker that scrapes **multiple flight websites** to find the cheapest flights. Compares prices from Kayak, Expedia, and Google Flights in parallel!

## Features

- 🔍 **Multi-source search** - Scrapes Kayak, Expedia, and Google Flights simultaneously
- 💰 **Smart price comparison** - Automatically sorted by price (cheapest first)
- 📊 **Visual charts** - Interactive price comparison visualization
- 🔗 **Direct booking links** - Click to book specific flights at displayed prices
- ⚡ **Parallel scraping** - All sources checked at once for faster results
- 🏷️ **Source tracking** - See which website has the best deal
- 🆓 **Completely free** - no API costs, no subscriptions!

## How It Works

The app uses Selenium to scrape flight data from three major flight booking websites in parallel, giving you comprehensive real-time price comparisons without needing expensive flight APIs.

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
6. Wait 20-30 seconds while all three sources are scraped in parallel
7. View results sorted by price with source labels
8. Click "Book Flight" to go to the specific booking page!

## Project Structure

```
Flight-Price-Tracker/
├── app.py                    # Main Streamlit application
├── flight_search.py          # Flight search interface
├── multi_scraper.py          # Combines all scrapers with parallel execution
├── scraper_utils.py          # Shared scraper utilities (driver setup)
├── kayak_scraper.py          # Kayak web scraper
├── expedia_scraper.py        # Expedia web scraper
├── google_flights_scraper.py # Google Flights web scraper
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Technologies Used

- **Streamlit** - Web interface and data visualization
- **Selenium** - Web scraping automation
- **BeautifulSoup** - HTML parsing
- **Pandas** - Data processing and analysis
- **Plotly** - Interactive charts
- **ThreadPoolExecutor** - Parallel scraping for faster results

## How the Multi-Source Scraping Works

1. **Parallel Execution** - All three scrapers run simultaneously using Python's ThreadPoolExecutor
2. **Click-Through Detection** - Each scraper clicks into individual flights to extract specific booking links
3. **Deduplication** - Removes duplicate flights (same airline + price combo)
4. **Smart Sorting** - Results sorted by price, showing cheapest options first
5. **Source Attribution** - Each flight tagged with its source (Kayak, Expedia, or Google Flights)

## Limitations

- Search takes 20-30 seconds (web scraping vs instant API, but checks 3 sources!)
- Booking links attempt to get specific flight URLs, may fallback to search pages
- May break if websites change their structure (will need CSS selector updates)
- Some sites may have bot detection (e.g., Skyscanner has captcha, so we use Expedia instead)

## Legal Note

This tool is for educational purposes. Please respect the terms of service of Kayak, Expedia, and Google Flights. Use responsibly and avoid excessive scraping.

## License

MIT License - feel free to use and modify!
