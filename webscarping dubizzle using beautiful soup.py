# ###################This code was working before "20/10/2025" after that BeautifulSoup couldn't read the cards ( ads ) ###########################
# ###################so i decied to use playwright instead of it and also using stealth to get the ads ############################################
import requests
from bs4 import BeautifulSoup
import csv
BASE_URL = "https://www.dubizzle.com.eg"
MAX_PAGES = 20  # Maximum number of pages to scrape
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
CSV_FILENAME = "dubizzle_products.csv"
CSV_COLUMNS = ["name","describtion", "price", "location", "url", "page"]


def get_search_url(search_query) -> str:
    """Prompts the user for a search query and constructs the base search URL."""
    url_friendly_query = search_query.replace(' ', '-')
    
    print(f"Formatted Query: {url_friendly_query}")
    BASE_SEARCH_URL = f"{BASE_URL}/en/mobile-phones-tablets-accessories-numbers/mobile-phones/q-{url_friendly_query}"
    print(f"Base Search URL: {BASE_SEARCH_URL}")
    
    return BASE_SEARCH_URL

def scrape_page(url: str, page_number: int,search_query) -> list:
    """Fetches, parses, and extracts product data from a single URL."""
    products = []
    
    print(f"Scraping page {page_number}: {url}")
    
    try:
        page = requests.get(url, headers=HEADERS)
        page.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.HTTPError as http_err:
        print(f"Error: HTTP error on page {page_number} ({http_err}). Stopping.")
        return None # Return None to signal a critical error or end of search
    except requests.exceptions.RequestException as req_err:
        print(f"Error: Connection error on page {page_number} ({req_err}). Stopping.")
        return None # Return None to signal a critical error or end of search

    soup = BeautifulSoup(page.content, "lxml")
    # Selects the listing cards
    cards = soup.select('li[aria-label="Listing"]')

    if not cards:
        print(f"No listings found on page number {page_number}.")
        return [] # Return an empty list if no listings were found

    for card in cards:
        product = extract_product_data(card, page_number,search_query)
        if product:
            products.append(product)
            
    return products

def extract_product_data(card: BeautifulSoup, page_number: int,search_query) -> dict:
    """Extracts name, price, location, and URL from a single product card."""
    try:
        # Extract Name
        desc_element = card.select_one("h2")
        describtion = desc_element.text.strip() if desc_element else "Not Available"
        
        # Extract Price
        price_container = card.select_one('div[aria-label="Price"]')
        price = "Not Available"
        if price_container:
            price_element = price_container.select_one('span')
            price = price_element.text.strip() if price_element else "Not Available"
            
        # Extract Location
        location_element = card.select_one('span[aria-label="Location"]')
        location = location_element.text.strip() if location_element else "Not Available"
        location = location[:-1].strip()
        
        # Extract URL
        url_element = card.select_one("a")
        link_reference = url_element.get("href") if url_element else "Not Available"
        
        full_url = "Not Available"
        if link_reference != "Not Available":
            # Check if the URL is relative and prepend the base domain
            full_url = BASE_URL + link_reference
        
        return {
            "name": search_query,
            "describtion" : describtion,
            "price": price,
            "location": location,
            "url": full_url,
            "page": page_number
        }
        
    except Exception as e:
        print(f"Error while extracting data from a card on page {page_number}: {e}")
        return None # Return None if extraction fails for a specific card

def save_to_csv(data: list, filename: str, columns: list):
    """Saves the list of dictionaries to a CSV file."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
        print(f"\nResults successfully saved to {filename}")
    except Exception as e:
        print(f"\n Error while writing to CSV file: {e}")

def main():
    """Main function to control the scraping flow."""
    all_products = []
    search_query = input("Please enter phone or tablet name you want to scrap from (e.g: iphone 13): ")
    base_search_url = get_search_url(search_query)
    page_number = 1

    while page_number <= MAX_PAGES:
        # Construct the URL for the current page
        if page_number == 1:
            current_url = base_search_url
        else:
            current_url = f"{base_search_url}/?page={page_number}"
        
        # Scrape the current page
        products_on_page = scrape_page(current_url, page_number,search_query)

        # Handle different return values from scrape_page
        if products_on_page is None:
            # Critical error (HTTP or connection) - stop the loop
            break
        elif not products_on_page:
            # No cards found or only a few cards that failed extraction - stop the loop
            print("Finished scraping: No more listings or end of search results.")
            break
        else:
            # Successfully scraped data
            all_products.extend(products_on_page)
        
        page_number += 1

    # Save the collected data
    save_to_csv(all_products, CSV_FILENAME, CSV_COLUMNS)

    # Print the final list (optional, but requested in the original code)
    print("\n--- Scraped Products Summary (First 5) ---")
    print(all_products[:5])
    if len(all_products) > 5:
        print(f"... and {len(all_products) - 5} more.")
    elif not all_products:
         print("No products were scraped.")

# --- Execution ---
if __name__ == "__main__":
    main()