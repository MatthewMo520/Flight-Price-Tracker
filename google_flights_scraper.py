from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

def setup_driver(headless=True):
    """Initialize Chrome driver with anti-detection measures"""
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")  # Use new headless mode

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--lang=en-US")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Modify navigator.webdriver flag
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    return driver

def scrape_kayak_flights(origin, destination, departure_date, adults=1):
    """
    Scrape Kayak for flight information including booking links

    Args:
        origin: Origin airport code (e.g., 'YYZ')
        destination: Destination airport code (e.g., 'LAX')
        departure_date: Departure date in YYYY-MM-DD format
        adults: Number of adult passengers

    Returns:
        List of flight dictionaries with airline, price, times, and booking link
    """
    driver = None
    try:
        # Setup driver
        driver = setup_driver(headless=True)

        # Build Kayak URL
        # Format: https://www.kayak.com/flights/YYZ-LAX/2025-11-15?sort=bestflight_a
        url = f"https://www.kayak.com/flights/{origin}-{destination}/{departure_date}?sort=price_a"

        print(f"Opening Kayak: {url}")
        driver.get(url)

        # Wait for flights to load
        print("Waiting for flights to load...")
        time.sleep(15)  # Kayak loads slowly

        # Get page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find flight result divs (Kayak uses div with data-resultid)
        flight_divs = soup.find_all('div', {'data-resultid': True})

        flights_data = []
        print(f"Found {len(flight_divs)} flight results")

        for idx, flight_div in enumerate(flight_divs[:10]):  # Limit to 10 flights
            try:
                # Extract airline
                airline_elem = flight_div.find('div', class_='codeshares-airline-names')
                if not airline_elem:
                    airline_elem = flight_div.find('div', class_=lambda x: x and 'airline' in str(x).lower())
                airline = airline_elem.text.strip() if airline_elem else "Multiple Airlines"

                # Extract price
                price_elem = flight_div.find('div', class_=lambda x: x and 'price' in str(x).lower())
                if price_elem:
                    price_text = re.sub(r'[^\d.]', '', price_elem.text)
                    try:
                        price = float(price_text)
                    except:
                        price = 0
                else:
                    price = 0

                # Extract times - try multiple selectors
                time_elems = flight_div.find_all('span', class_=lambda x: x and ('time' in str(x).lower()))

                # Parse times from the text
                departure_time = ""
                arrival_time = ""

                # Look for time patterns (e.g., "6:00 am", "18:00")
                for elem in time_elems[:4]:  # Check first 4 time elements
                    text = elem.text.strip()
                    # Match time patterns like "6:00a", "18:00", "6:00 am"
                    if re.search(r'\d{1,2}:\d{2}', text):
                        if not departure_time:
                            departure_time = text
                        elif not arrival_time:
                            arrival_time = text
                            break

                # Format times - use placeholder if not found
                departure_datetime = f"{departure_date} {departure_time}" if departure_time else f"{departure_date} 00:00"
                arrival_datetime = f"{departure_date} {arrival_time}" if arrival_time else f"{departure_date} 00:00"

                # Get booking link - Kayak uses data-resultid or has a link to booking page
                link_elem = flight_div.find('a', href=True)
                if link_elem and 'http' in link_elem['href']:
                    booking_link = link_elem['href']
                else:
                    # Use Kayak search URL
                    booking_link = url

                if price > 0:  # Only add if we got a price
                    flights_data.append({
                        "airline": airline,
                        "price": str(int(price)),
                        "departure": departure_datetime,
                        "arrival": arrival_datetime,
                        "link": booking_link
                    })

                    print(f"Flight {idx + 1}: {airline} - ${int(price)}")

            except Exception as e:
                print(f"Error parsing flight {idx}: {e}")
                continue

        return flights_data

    except Exception as e:
        print(f"Error scraping Kayak: {e}")
        import traceback
        traceback.print_exc()
        return []

    finally:
        if driver:
            driver.quit()

# Test function
if __name__ == "__main__":
    flights = scrape_kayak_flights("YYZ", "LAX", "2025-11-15", 1)
    print(f"\nFound {len(flights)} flights:")
    for flight in flights:
        print(f"{flight['airline']}: ${flight['price']} - {flight['link'][:80]}...")
