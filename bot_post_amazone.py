import logging
from telegram import Bot, ParseMode
from time import sleep

# === CONFIG ===
BOT_TOKEN = '7506933533:AAFANaQg00Y13bsRRTsggd_ARq0z8YnFac0'
CHANNEL_USERNAME = '@BestDeals_2_0'  # example: @amazondealsindia

# Sample affiliate product list (replace with actual ones)
product_list = [
    {
        'title': '🔥 One-Plus 13s at ₹54,998',
        'description': 'OnePlus 13s | Snapdragon® 8 Elite | Best Battery Life Ever on a Compact Phone | Lifetime Display Warranty | 12GB+256GB | Green Silk',
        'url': 'https://amzn.to/4o6p1Jl',
        'image_url': 'https://m.media-amazon.com/images/I/61BTIyv+XdL._SL1500_.jpg'
    },
    {
        'title': '💡 LED Light Strip under ₹299',
        'description': 'Perfect for room decor or gaming setup!',
        'url': 'https://amzn.to/your-affiliate-link2',
        'image_url': 'https://m.media-amazon.com/images/I/71lA5ygXN1L._SL1500_.jpg'
    }
]


def post_deals():
    bot = Bot(token=BOT_TOKEN)

    for product in product_list:
        caption = f"*{product['title']}*\n\n{product['description']}\n👉 [Buy Now]({product['url']})"
        bot.send_photo(
            chat_id=CHANNEL_USERNAME,
            photo=product['image_url'],
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )
        print(f"Posted with image: {product['title']}")
        sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    post_deals()
