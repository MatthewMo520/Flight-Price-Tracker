from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

def setup_driver(headless=True):
    """Initialize Chrome driver"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    return driver

def scrape_skyscanner_flights(origin, destination, departure_date, adults=1):
    """
    Scrape Skyscanner for flight information

    Args:
        origin: Origin airport code
        destination: Destination airport code
        departure_date: Date in YYYY-MM-DD format
        adults: Number of passengers

    Returns:
        List of flight dicts with airline, price, times, link, source
    """
    driver = None
    try:
        driver = setup_driver(headless=True)

        # Skyscanner URL format
        # https://www.skyscanner.com/transport/flights/yytz/lax/251115/
        date_formatted = departure_date.replace('-', '')[2:]  # 2025-11-15 -> 251115

        url = f"https://www.skyscanner.com/transport/flights/{origin.lower()}/{destination.lower()}/{date_formatted}/"

        print(f"[Skyscanner] Opening: {url}")
        driver.get(url)

        # Wait for results
        print("[Skyscanner] Waiting for flights to load...")
        time.sleep(15)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find flight cards
        flight_cards = soup.find_all('div', {'data-testid': lambda x: x and 'day-view-content' in str(x)})

        if not flight_cards:
            # Try alternative selector
            flight_cards = soup.find_all('div', class_=lambda x: x and 'FlightCard' in str(x))

        flights_data = []
        print(f"[Skyscanner] Found {len(flight_cards)} potential flights")

        for idx, card in enumerate(flight_cards[:5]):  # Limit to 5
            try:
                # Extract price
                price_elem = card.find('span', class_=lambda x: x and 'price' in str(x).lower())
                if price_elem:
                    price_text = re.sub(r'[^\d.]', '', price_elem.text)
                    try:
                        price = float(price_text)
                    except:
                        continue
                else:
                    continue

                # Extract airline
                airline_elem = card.find('div', class_=lambda x: x and 'carrier' in str(x).lower())
                airline = airline_elem.text.strip() if airline_elem else "Multiple Airlines"

                # Extract times
                times = card.find_all('span', class_=lambda x: x and 'time' in str(x).lower())
                departure_time = times[0].text.strip() if len(times) > 0 else "00:00"
                arrival_time = times[1].text.strip() if len(times) > 1 else "00:00"

                departure_datetime = f"{departure_date} {departure_time}"
                arrival_datetime = f"{departure_date} {arrival_time}"

                # Try to click and get specific link
                booking_link = url
                try:
                    clickable_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid*='day-view']")
                    if idx < len(clickable_elements):
                        clickable_elements[idx].click()
                        time.sleep(2)

                        # Look for booking button
                        booking_btns = driver.find_elements(By.XPATH, "//a[contains(@href, 'booking') or contains(text(), 'Select') or contains(text(), 'Book')]")
                        if booking_btns:
                            link = booking_btns[0].get_attribute('href')
                            if link and 'http' in link:
                                booking_link = link
                                print(f"  → Got specific booking link")
                except Exception as e:
                    print(f"  → Could not get specific link: {e}")

                flights_data.append({
                    "airline": airline,
                    "price": str(int(price)),
                    "departure": departure_datetime,
                    "arrival": arrival_datetime,
                    "link": booking_link,
                    "source": "Skyscanner"
                })

                print(f"[Skyscanner] Flight {idx + 1}: {airline} - ${int(price)}")

            except Exception as e:
                print(f"[Skyscanner] Error parsing flight {idx}: {e}")
                continue

        return flights_data

    except Exception as e:
        print(f"[Skyscanner] Error: {e}")
        import traceback
        traceback.print_exc()
        return []

    finally:
        if driver:
            driver.quit()
