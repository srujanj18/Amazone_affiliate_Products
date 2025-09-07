import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json
import re
import logging

# === CONFIG ===
AFFILIATE_TAG = 'AMAZONE_AFFILIATE_TAG'  # Replace with your Amazon affiliate tag
SEARCH_KEYWORDS = [
    "iphone 11", "iphone 12", "iphone 13", "iphone 15 pro max", "iphone 16", 
    "samsung phones", "redmi 11", "redmi 12", "vivo phones", "realme phones", 
    "motorola phones", "hp laptop", "asus TUF", "dell laptop", "asus laptop", 
    "acer laptop", "lenovo laptop", "smartwatch", "led strip light", 
    "gaming mouse", "bluetooth speaker", "sony speaker", "boat speaker"
]
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}
OUTPUT_FILE = "products.json"

# === ESCAPE MARKDOWN ===
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# === SCRAPE PRODUCT ===
def fetch_product_from_amazon(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.select_one("#productTitle")
        price = soup.select_one(".a-price .a-offscreen")
        image = soup.select_one("#landingImage")

        if title and image:
            return {
                "title": title.get_text(strip=True),
                "price": price.get_text(strip=True) if price else "N/A",
                "image": image["src"],
                "url": f"{url.split('?')[0]}?tag={AFFILIATE_TAG}"
            }
    except Exception as e:
        print(f"⚠️ Failed to fetch product: {e}")
    return None

# === SEARCH AND SAVE ===
def search_and_save():
    products = []
    for keyword in SEARCH_KEYWORDS:
        query = f"{keyword} site:amazon.in"
        print(f"🔍 Searching Google for: {query}")
        try:
            results = list(search(query, num_results=5))
            found = False
            for url in results:
                if "amazon.in" in url:
                    product = fetch_product_from_amazon(url)
                    if product:
                        products.append(product)
                        found = True
                        break  # One product per keyword
            if not found:
                print(f"⚠️ No links found for: {query}")
        except Exception as e:
            print(f"❌ Error while searching: {e}")

    # Save to JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(products, f, indent=2)
    print(f"✅ Saved {len(products)} products to {OUTPUT_FILE}")

# === MAIN ===
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    search_and_save()
