import httpx
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.constants import ParseMode
from googlesearch import search
import asyncio
import json
import os
import re
import logging
import random

# === CONFIG ===
BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
CHANNEL_USERNAME = "USER_NAME"
AFFILIATE_TAG = "TAG"

SEARCH_KEYWORDS = {
    "Mobile Phones": ["nokia g42 5g", "realme narzo 70 pro", "oneplus 12r", "xiaomi 14", "samsung m15", "lava blaze curve", "motorola g73", "itel s23 plus"],
    
    "Laptops": ["asus vivobook s15", "msi modern 14", "dell inspiron 15", "acer swift go", "lenovo yoga slim 7", "hp pavilion x360", "infinix zerobook", "primebook 4g"],
    
    "Smart Watches": ["noise colorfit pro 5", "fire-boltt visionary", "boat wave sigma", "amazfit bip 5", "gizmore gizfit glow", "pebble cosmos luxe", "maxima max pro turbo"],
    
    "Bluetooth Earbuds": ["boat airdopes 141", "boult audio x10", "noise buds x", "fire-boltt fire pods", "pTron bassbuds duo", "lava probuds 22", "mivi duopods k7"],
    
    "Speakers": ["boat stone 352", "jbl go 3", "sony srs-xb13", "philips bt2003", "mivi roam 2", "claw swell"],
    
    "Gaming Gear": ["redragon k552 kumara", "ant esports mk1000", "cooler master mm711", "cosmic byte equinox", "zebronics zeb-transformer", "lenovo legion h300"],
    
    "Gaming": ["msi katana 15", "lenovo legion 5 pro", "asus rog strix g17", "acer nitro 5", "alienware m18", "xidax gaming desktop"],
    
    "Cameras": ["canon eos r10", "nikon z50", "sony alpha zv-e10", "panasonic lumix g7", "gopro hero 12", "djii osmo pocket 3"],
    
    "Audio": ["oneplus bullets wireless z2", "sony wh-ch520", "jbl tune 510bt", "skullcandy crusher evo", "noise tune active", "realme buds wireless 3 neo"],
    
    "Wearables": ["fire-boltt phoenix", "noise luna ring", "boat lunar call pro", "gizmore active band", "realme band 2", "cult sport smart ring"],
    
    "Home Appliances": ["air fryer", "geyser water heater", "microwave oven", "ceiling fan", "air purifier", "smart led bulb"],
    
    "Fitness & Health": ["yoga mat", "pull-up bar", "hand gripper", "steam vaporizer", "digital thermometer", "fitness tracker"],
    
    "Fashion": ["denim jacket men", "formal shoes women", "hiking shoes men", "blazer for men", "ethnic gown", "backpack for college girls"]
}


HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/14.0 Safari/605.1.15",
]

PRODUCTS_FILE = "products.json"

# === UTILS ===
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def save_product(product):
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump([product], f, indent=2)
    else:
        with open(PRODUCTS_FILE, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            if not any(p['title'] == product['title'] for p in data):
                data.append(product)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()

# === AMAZON SCRAPER ===
async def fetch_product_from_amazon(url, category):
    try:
        headers = {
            "User-Agent": random.choice(HEADERS_LIST),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.select_one("#productTitle")
            price = soup.select_one(".a-price .a-offscreen")
            image = soup.select_one("#imgTagWrapperId img")

            if title and image:
                return {
                    "title": title.get_text(strip=True),
                    "price": price.get_text(strip=True) if price else "N/A",
                    "image": image["src"],
                    "url": f"{url.split('?')[0]}?tag={AFFILIATE_TAG}",
                    "category": category
                }
    except Exception as e:
        print(f"⚠️ Failed to fetch: {url}\nError: {e}")
    return None

# === TELEGRAM POST ===
async def post_to_telegram(product):
    try:
        bot = Bot(token=BOT_TOKEN)
        title = escape_markdown(product["title"])
        price = escape_markdown(product["price"])
        url = product["url"]

        caption = f"*{title}*\n\n💰 Price: `{price}`\n👉 [Buy Now]({url})"

        await bot.send_photo(
            chat_id=CHANNEL_USERNAME,
            photo=product["image"],
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )
        print(f"✅ Posted: {product['title']}")
    except Exception as e:
        print(f"❌ Failed to post: {e}")

# === SEARCH AND POST ===
async def search_and_post():
    for category, keywords in SEARCH_KEYWORDS.items():
        for keyword in keywords:
            query = f"{keyword} site:amazon.in"
            print(f"🔍 Searching in [{category}]: {query}")
            try:
                results = search(query, num_results=5)
                for url in results:
                    if "amazon.in" not in url:
                        continue
                    product = await fetch_product_from_amazon(url, category)
                    if product:
                        save_product(product)
                        await post_to_telegram(product)
                        await asyncio.sleep(10)  # Delay to avoid spamming
                        break
                else:
                    print(f"⚠️ No valid Amazon products found for: {query}")
            except Exception as e:
                print(f"❌ Error during search/post: {e}")

# === SCHEDULED RUNNER ===
def start_scheduled_bot():
    logging.basicConfig(level=logging.INFO)
    print("⏳ Bot started. Will post every hour.")

    async def scheduler():
        while True:
            await search_and_post()
            await asyncio.sleep(3600)  # wait 1 hour

    asyncio.run(scheduler())

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    print("🔁 Running Amazon Deals Bot...")
    start_scheduled_bot()
