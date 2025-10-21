from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth.stealth import Stealth
import csv
import time

# --- Configuration and Constants ---
BASE_URL = "https://www.dubizzle.com.eg"
MAX_PAGES = 20
CSV_FILENAME = "dubizzle_products.csv"
CSV_COLUMNS = ["name", "description", "price", "location", "url", "page"]

def get_search_url(search_query) -> str:
    """Constructs the search URL."""
    url_friendly_query = search_query.replace(' ', '-')
    base_search_url = f"{BASE_URL}/en/mobile-phones-tablets-accessories-numbers/mobile-phones/q-{url_friendly_query}"
    print(f"Formatted Query: {url_friendly_query}")
    print(f"Base Search URL: {base_search_url}")
    return base_search_url

def scrape_page(page, url: str, page_number: int, search_query) -> list:
    """Scrapes a single page using Playwright."""
    print(f"\n📄 Scraping page {page_number}: {url}")
    data = []

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
    except PlaywrightTimeoutError:
        print(f"⚠️ Timeout while loading page {page_number}. Skipping...")
        return []

    try:
        page.wait_for_selector('li[aria-label="Listing"]', timeout=10000)
    except PlaywrightTimeoutError:
        print(f"⚠️ No listings found on page {page_number}.")
        return []

    # scroll to end
    for _ in range(3):
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(2)

    cards = page.locator('li[aria-label="Listing"]')
    count = cards.count()
    print(f"✅ Found {count} listings on page {page_number}")

    for i in range(count):
        try:
            desc = cards.nth(i).locator("h2").inner_text() if cards.nth(i).locator("h2").count() else "Not Available"
            price = cards.nth(i).locator('div[aria-label="Price"]').inner_text() if cards.nth(i).locator('div[aria-label="Price"]').count() else "Not Available"
            loc = cards.nth(i).locator('span[aria-label="Location"]').inner_text() if cards.nth(i).locator('span[aria-label="Location"]').count() else "Not Available"
            link = cards.nth(i).locator("a[href^='/en/ad/']").first.get_attribute("href")
            full_url = BASE_URL + link if link else "Not Available"

            data.append({
                "name": search_query,
                "description": desc.strip(),
                "price": price.strip(),
                "location": loc.strip(),
                "url": full_url,
                "page": page_number
            })
        except Exception as e:
            print(f"⚠️ Error extracting item {i+1} on page {page_number}: {e}")

    return data

def save_to_csv(data: list, filename: str, columns: list):
    """Saves the scraped data into a CSV file."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
        print(f"\n💾 Results successfully saved to {filename}")
    except Exception as e:
        print(f"\n❌ Error writing to CSV: {e}")

def main():
    """Main controller for the scraping flow."""
    search_query = input("Please enter phone or tablet name (e.g: iphone 13): ")
    base_search_url = get_search_url(search_query)
    all_data = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        for page_number in range(1, MAX_PAGES + 1):
            if page_number == 1:
                current_url = base_search_url
            else:
                current_url = f"{base_search_url}/?page={page_number}"

            page_data = scrape_page(page, current_url, page_number, search_query)

            if not page_data:
                print("🚫 No more listings or blocked by site. Stopping.")
                break

            all_data.extend(page_data)

        browser.close()

    save_to_csv(all_data, CSV_FILENAME, CSV_COLUMNS)

    print("\n--- Scraped Products Summary (First 5) ---")
    print(all_data[:5])
    if len(all_data) > 5:
        print(f"... and {len(all_data) - 5} more.")
    elif not all_data:
        print("No products were scraped.")

# --- Execution ---
if __name__ == "__main__":
    main()