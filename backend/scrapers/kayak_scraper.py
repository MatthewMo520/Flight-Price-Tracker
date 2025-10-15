from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
from scraper_utils import setup_driver

def scrape_kayak_flights(origin, destination, departure_date, adults=1):
    """
    Scrape Kayak for flight information
    """
    driver = None
    try:
        driver = setup_driver(headless=True)

        url = f"https://www.kayak.com/flights/{origin}-{destination}/{departure_date}?sort=price_a&adults={adults}"

        print(f"[Kayak] Opening: {url}")
        driver.get(url)

        # Wait for page to load
        print("[Kayak] Waiting for results to load...")
        time.sleep(20)  # Give Kayak time to load

        # Try to find flights using multiple selectors
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Try different selectors
        flight_containers = []

        # Method 1: data-resultid
        flight_containers = soup.find_all('div', {'data-resultid': True})
        print(f"[Kayak] Method 1 (data-resultid): Found {len(flight_containers)} results")

        # Method 2: Common class patterns
        if not flight_containers:
            flight_containers = soup.find_all('div', class_=re.compile(r'.*result.*item.*', re.I))
            print(f"[Kayak] Method 2 (result item): Found {len(flight_containers)} results")

        # Method 3: Look for price elements and work backwards
        if not flight_containers:
            price_elements = soup.find_all('div', class_=re.compile(r'.*price.*', re.I))
            print(f"[Kayak] Method 3 (price elements): Found {len(price_elements)} price elements")
            # Get parent containers
            flight_containers = [elem.find_parent('div', class_=re.compile(r'.*')) for elem in price_elements[:10]]
            flight_containers = [c for c in flight_containers if c]

        flights_data = []

        for idx, container in enumerate(flight_containers[:10]):
            try:
                # Extract price - try multiple methods
                price = 0
                price_elem = container.find(string=re.compile(r'\$\d+'))
                if price_elem:
                    price_text = re.findall(r'\d+', price_elem)[0]
                    price = int(price_text)
                else:
                    # Try finding price in attributes or nested divs
                    price_elem = container.find('div', class_=re.compile(r'.*price.*', re.I))
                    if price_elem:
                        price_text = re.findall(r'\d+', price_elem.get_text())
                        if price_text:
                            price = int(price_text[0])

                if price == 0:
                    continue  # Skip if no price found

                # Extract airline
                airline = "Unknown Airline"
                airline_elem = container.find('div', class_=re.compile(r'.*airline.*', re.I))
                if airline_elem:
                    airline = airline_elem.get_text(strip=True)
                else:
                    # Look for airline logo alt text
                    img = container.find('img', alt=True)
                    if img:
                        airline = img['alt']

                # Extract times
                time_elements = container.find_all(string=re.compile(r'\d{1,2}:\d{2}'))
                departure_time = time_elements[0] if len(time_elements) > 0 else "12:00"
                arrival_time = time_elements[1] if len(time_elements) > 1 else "12:00"

                flights_data.append({
                    "airline": airline,
                    "price": str(price),
                    "departure": f"{departure_date} {departure_time}",
                    "arrival": f"{departure_date} {arrival_time}",
                    "link": url,
                    "source": "Kayak"
                })

                print(f"[Kayak] Flight {idx + 1}: {airline} - ${price}")

            except Exception as e:
                print(f"[Kayak] Error parsing flight {idx}: {e}")
                continue

        return flights_data

    except Exception as e:
        print(f"[Kayak] Error: {e}")
        import traceback
        traceback.print_exc()
        return []

    finally:
        if driver:
            driver.quit()
