# TechDeals - Amazon Affiliate Scraper

TechDeals is a Python-based Amazon affiliate product scraper and posting bot designed to help you find and share the best tech deals on Amazon India. It automates the process of searching for popular tech products, scraping product details, and posting deals to social media channels.

## Features

- Scrapes Amazon product details (title, price, image, URL) using Google search results.
- Automatically appends your Amazon affiliate tag to product URLs.
- Posts deals to Telegram channels and Instagram accounts using bots.
- Supports a wide range of tech product keywords including smartphones, laptops, smartwatches, gaming gear, and more.
- Generates a JSON file (`products.json`) with the scraped product data.
- Includes a simple React-based frontend to display featured deals and blog posts.

## Folder Structure

- `scraper.py`: Main script to search and scrape Amazon products.
- `bot_post_amazone.py`: Telegram bot script to post deals to a Telegram channel.
- `instabot.py`: Instagram bot script to post deals to an Instagram account.
- `products.json`: Output JSON file containing scraped product data.
- `index.html`: React frontend to display deals and blog posts.
- `config/`: Configuration files and logs for the bots.

## Setup and Usage

### Prerequisites

- Python 3.7 or higher
- Required Python packages (install via pip):

```bash
pip install requests beautifulsoup4 googlesearch-python python-telegram-bot instagrapi schedule
```

### Configuration

- Update your Amazon affiliate tag in `scraper.py` (`AFFILIATE_TAG` variable).
- Update bot tokens and channel usernames in `bot_post_amazone.py` and `instabot.py`.
- Ensure your Telegram bot is an admin in the target channel.
- Provide Instagram credentials in `instabot.py`.

### Running the Scraper

Run the scraper to fetch product data and save it to `products.json`:

```bash
python scraper.py
```

### Posting Deals

- To post deals on Telegram channel:

```bash
python bot_post_amazone.py
```

- To post deals on Instagram:

```bash
python instabot.py
```

### Frontend

Open `index.html` in a web browser to view the featured deals and blog posts.

## Notes

- The scraper uses Google search to find Amazon product pages, so ensure you have internet connectivity.
- Posting bots require valid API tokens and credentials.
- The affiliate tag is appended to product URLs to track referrals.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact [Your Name or Email].
