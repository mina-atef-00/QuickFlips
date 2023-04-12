# QuickFlips

[![Python 3.9.6](https://img.shields.io/badge/python-3.9.6-blue)](https://www.python.org/downloads/release/python-396/)

QuickFlips is a powerful and intuitive Discord bot that enables users to search for eBay items that are listed under the average market price.

---

## Showcase

- I have a showcase server for the bots I make: <a href="https://discord.gg/vS5D4qWDAP"><img src="https://img.shields.io/badge/Discord-7289DA?logo=discord&logoColor=white"></a>
- you could also check the screenshots folder for more.

![Discord_vq5eWfHF62](https://user-images.githubusercontent.com/52796958/231370060-17bfcbf8-0738-4949-b47d-17310e96a1f4.gif)

---

## Features

- Advanced search - Quickly and easily search eBay for items below the average price, with typos, or that are about to expire.
- Sorting and filtering - Sorts all search results by price from low to high and provides filtering options such as categories and country to refine search results further.
- User-friendly interface - Easy-to-use commands with clear usage instructions:
  - `q!QuickFlip <item name>` - Fetches and displays items below the average price on eBay.
  - `q!TypoFlip <item name>` - Searches eBay for an item, with typos intentionally introduced in the search query to find deals.
  - `q!LastFlip <item name>` - Fetches and displays eBay items that are about to expire.
  - `q!help` - Displays all available commands along with their usage instructions.
- Efficient - Saves users time and effort in finding the best deals on eBay.

---

## How It's Made

- Python with enhanced-dpy library for Discord bot development.
- MongoDB for storing warned and muted users data
- To store data related to warned and muted users, I utilized MongoDB as my database management system. This allows store large amounts of data while ensuring optimal performance and scalability.
- To protect user anonymity, I hashed user IDs before they were stored in the database along with their confession messages links so that users that abuse this functionality get banned from using it.
- In order to enhance the functionality of the bot, I integrated a couple of APIs such as:
  - Unsplash for fetching random images
  - OpenWeatherMap for displaying weather information within the server
  - and Kanye West Quotes API for generating random quotes for the server.
- The bot is deployed on Heroku using a CI/CD pipeline for automatic deployment on every push to the main branch.

---

## Lessons Learned

- Learned how to use the enhanced-dpy library for Discord bot development.
- Gained experience in integrating SDKs such as eBay into a bot.
- Learned how to utilize MongoDB as a database management system to store user data.
- Gained experience in hosting bots on PaaSes and implementing CI/CD pipelines to streamline the development process.

---

## Installation

To install QuickFlips, follow these steps:

1. Visit the [discord developer portal](https://discord.com/developers/applications) and add a bot there (give it admin privileges).
2. Set up an eBay API account and obtain your developer credentials.
3. Clone the repository.
4. Install dependencies using `pip install -r requirements.txt`.
5. copy `env.template` to `.env` and fill the options (bot token,mongodb credentials, etc...).
6. fill the ebay appid in the `ebay.yaml` file.
7. Run the bot using `python pro_bot_x.py`.
