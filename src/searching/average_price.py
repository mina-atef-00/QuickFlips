from re import search
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

# from asyncio import run


async def get_html(query: str) -> dict:
    search_url = f"https://averagefinder.com/averageFinder.php?Search={'%20'.join(query.split())}"
    with urlopen(search_url) as avg_price_finder_file:
        html = avg_price_finder_file.read().decode()

        return html


# print(run(get_html("playstation"))) #!DEBUG


async def avg_price(query: str) -> int:
    html = await get_html(query)
    soup = BeautifulSoup(html, "html.parser")

    avg_title = f"**Average price for [ {query} ] :**"
    # print(avg_title) #!DEBUG

    try:
        avg_val = str(
            "{0:.2f}".format(
                float(list(soup.body.find_all(re.compile("h2")))[4].text[1:])
                * 1.37
            )
        )
    except:
        avg_val = "N/A"

    # print(avg_val) #!DEBUG

    return {"avg_val": avg_val, "avg_title": avg_title}


# run(avg_price("playstation 5"))  #!DEBUG
