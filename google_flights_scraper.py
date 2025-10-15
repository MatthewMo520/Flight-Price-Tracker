from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
from scraper_utils import setup_driver

def scrape_google_flights(origin, destination, departure_date, adults=1):
    """
    Scrape Google Flights for flight information

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
        driver = setup_driver(headless=True)

        # Build Google Flights URL
        # Format: https://www.google.com/travel/flights?q=Flights%20from%20YYZ%20to%20LAX%20on%202025-11-20
        url = f"https://www.google.com/travel/flights?q=Flights%20from%20{origin}%20to%20{destination}%20on%20{departure_date}"

        print(f"[Google Flights] Opening: {url}")
        driver.get(url)

        # Wait longer for Google Flights to load
        print("[Google Flights] Waiting for flights to load...")
        time.sleep(25)  # Google Flights needs extra time

        # Try to wait for flight results
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li[class*='pIav']"))
            )
        except:
            print("[Google Flights] Timeout waiting for results, continuing anyway...")

        # Get page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find flight result items - Google uses dynamic class names
        flight_items = soup.find_all('li', class_=lambda x: x and 'pIav' in str(x))

        if not flight_items:
            # Try alternative selectors
            flight_items = soup.find_all('div', class_=lambda x: x and 'flight' in str(x).lower())

        flights_data = []
        print(f"[Google Flights] Found {len(flight_items)} flight results")

        for idx, flight_item in enumerate(flight_items[:10]):  # Limit to 10 flights
            try:
                # Extract airline - Google uses spans with specific classes
                airline_elem = flight_item.find('span', class_=lambda x: x and 'sSHqwe' in str(x))
                if not airline_elem:
                    airline_elem = flight_item.find('div', class_=lambda x: x and 'airline' in str(x).lower())
                airline = airline_elem.text.strip() if airline_elem else "Multiple Airlines"

                # Extract price
                price_elem = flight_item.find('span', class_=lambda x: x and 'YMlIz' in str(x))
                if not price_elem:
                    price_elem = flight_item.find('div', class_=lambda x: x and 'price' in str(x).lower())

                if price_elem:
                    price_text = re.sub(r'[^\d.]', '', price_elem.text)
                    try:
                        price = float(price_text)
                    except:
                        price = 0
                else:
                    price = 0

                # Extract times
                time_elems = flight_item.find_all('span', class_=lambda x: x and 'mv1WYe' in str(x) if x else False)
                if not time_elems:
                    time_elems = flight_item.find_all('span', class_=lambda x: x and 'time' in str(x).lower() if x else False)

                departure_time = ""
                arrival_time = ""

                # Look for time patterns
                for elem in time_elems[:4]:
                    text = elem.text.strip()
                    if re.search(r'\d{1,2}:\d{2}', text):
                        if not departure_time:
                            departure_time = text
                        elif not arrival_time:
                            arrival_time = text
                            break

                # Format times
                departure_datetime = f"{departure_date} {departure_time}" if departure_time else f"{departure_date} 00:00"
                arrival_datetime = f"{departure_date} {arrival_time}" if arrival_time else f"{departure_date} 00:00"

                # Try to get specific booking link by clicking into the flight
                booking_link = url  # Default fallback

                try:
                    # Find the clickable flight element
                    flight_elements = driver.find_elements(By.CSS_SELECTOR, "li[class*='pIav']")

                    if not flight_elements:
                        flight_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='button'][jsaction*='click']")

                    if idx < len(flight_elements):
                        # Scroll to element and click
                        driver.execute_script("arguments[0].scrollIntoView(true);", flight_elements[idx])
                        time.sleep(0.5)
                        flight_elements[idx].click()
                        time.sleep(3)  # Wait for booking options

                        # Look for "Book" or "View prices" buttons
                        booking_buttons = driver.find_elements(By.XPATH, "//a[contains(@href, 'booking.com') or contains(@href, 'expedia') or contains(text(), 'Book')]")

                        if booking_buttons:
                            # Get the first booking link
                            potential_link = booking_buttons[0].get_attribute('href')
                            if potential_link and 'http' in potential_link:
                                booking_link = potential_link
                                print(f"  → Got specific link")

                except Exception as e:
                    pass  # Silently fallback to main URL

                if price > 0:  # Only add if we got a price
                    flights_data.append({
                        "airline": airline,
                        "price": str(int(price)),
                        "departure": departure_datetime,
                        "arrival": arrival_datetime,
                        "link": booking_link,
                        "source": "Google Flights"
                    })

                    print(f"[Google Flights] Flight {idx + 1}: {airline} - ${int(price)}")

            except Exception as e:
                print(f"[Google Flights] Error parsing flight {idx}: {e}")
                continue

        return flights_data

    except Exception as e:
        print(f"[Google Flights] Error: {e}")
        import traceback
        traceback.print_exc()
        return []

    finally:
        if driver:
            driver.quit()
