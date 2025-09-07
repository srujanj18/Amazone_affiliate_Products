import os
import re
import time
import logging
import schedule
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.constants import ParseMode
from googlesearch import search
from instagrapi import Client

# === CONFIG ===
BOT_TOKEN = 'BOT_TOKEN'
CHANNEL_USERNAME = 'TELEGRAM_CHANNEL_NAME'  # Bot must be admin in this channel
AFFILIATE_TAG = 'AFFILIATE_TAG'

INSTA_USERNAME = 'INSTA_USER_NAME'
INSTA_PASSWORD = 'INSTA_PASSWORD'

SEARCH_KEYWORDS = [
    # Smartphones - Popular Models and Brands
    "iphone 15", "iphone 14", "iphone 13", "iphone 12", "iphone 11",
    "samsung s24 ultra", "samsung galaxy m14", "samsung a15", "samsung phones",
    "redmi note 13", "redmi 12", "redmi phones",
    "vivo v27", "vivo t2", "vivo phones",
    "realme narzo", "realme c55", "realme phones",
    "motorola edge", "moto g73", "motorola phones",
    "oneplus nord", "oneplus 11r", "oneplus phones",
    "nothing phone 2", "nothing phone",

    # Laptops - All brands
    "hp laptop", "dell laptop", "asus laptop", "acer laptop", "lenovo laptop", "msi gaming laptop",
    "macbook air m2", "macbook pro m3",

    # Smartwatches & Bands
    "smartwatch under 2000", "noise smartwatches", "boat smartwatch", "fire boltt smartwatch", "oneplus watch", "samsung galaxy watch",

    # Headphones / Earphones / Audio
    "boat airdopes", "noise earbuds", "oneplus bullets wireless", "sony headphones", "jbl headphones", "wired earphones", "bluetooth earphones",

    # Speakers
    "bluetooth speaker", "sony speaker", "boat stone speaker", "jbl portable speaker", "soundbar under 5000",

    # Gaming Gear
    "gaming mouse", "rgb keyboard", "gaming headset", "gaming controller", "xbox controller", "ps5 controller", "gaming monitor", "gaming chair",

    # Storage & Peripherals
    "pendrive 128gb", "external hard disk", "ssd 1tb", "memory card 64gb",

    # Smart Home Devices
    "smart bulb", "smart plug", "alexa echo dot", "google nest", "smart tv 43 inch",

    # Home & Kitchen Appliances
    "air fryer", "microwave oven", "water purifier", "washing machine", "refrigerator under 20000", "vacuum cleaner", "ceiling fan", "electric kettle", "iron box",

    # Trending Gadgets
    "neckband under 1000", "mobile stand", "tripod for mobile", "ring light", "usb fan", "cable organizer", "power bank 10000mah",

    # Daily Essentials
    "face wash", "trimmer", "electric toothbrush", "shaving kit", "hair dryer"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def fetch_product(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")

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
        print(f"⚠️ Error fetching product: {e}")
    return None


def post_to_instagram(product):
    try:
        cl = Client()
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)

        img_path = "product.jpg"
        img_data = requests.get(product["image"]).content
        with open(img_path, "wb") as f:
            f.write(img_data)

        hashtags = "#AmazonDeals #TechDeals #BudgetBuys #BestDeals #IndiaDeals #OnlineShopping #GadgetOfTheDay #DailyDeals #AmazonFinds #AffordableTech #TrendingProducts"

        caption = f"{product['title']}\n\nPrice: ₹{product['price']}\nBuy now: {product['url']}\n\n{hashtags}"

        cl.photo_upload(img_path, caption)
        print(f"✅ Instagram Posted: {product['title']}")
        os.remove(img_path)
    except Exception as e:
        print(f"❌ Instagram post failed: {e}")

def search_and_post():
    for keyword in SEARCH_KEYWORDS:
        query = f"{keyword} site:amazon.in"
        print(f"🔍 Searching: {query}")
        try:
            links = list(search(query, num_results=5))
            for url in links:
                if "amazon.in" in url:
                    product = fetch_product(url)
                    if product:

                        post_to_instagram(product)
                        time.sleep(15)
                        break
        except Exception as e:
            print(f"❌ Error while searching: {e}")

def start_bot():
    logging.basicConfig(level=logging.INFO)
    print("⏳ Bot started. Running hourly.")
    schedule.every(1).hours.do(search_and_post)
    search_and_post()
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    start_bot()
