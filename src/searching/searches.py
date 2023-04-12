from typing import Optional
from ebaysdk.finding import Connection
from ebaysdk.exception import ConnectionError
from asyncio import run
from src.searching.typos import typoing  #!src.typos
from src.searching.average_price import avg_price  #!src.average_price

# from pprint import pprint


async def fetch_items(
    query: str,
    country: Optional[str] = None,
    category_id: Optional[str] = None,
    last_min: bool = False,
    fatfinger: bool = False,
    sort_price: Optional[int] = None,
):
    try:
        avg_dict = await avg_price(query=query)
        avg_val = float(avg_dict["avg_val"])
        avg_title = avg_dict["avg_title"]
    except:
        avg_val = None
        avg_title = "No average price found"

    try:
        api = Connection(
            config_file=r"src/searching/ebay.yaml",
            siteid="EBAY-US",
            debug=False,
        )  #!src/ebay.yaml

        if last_min:
            sort_order = "EndTimeSoonest"
        elif sort_price == 1:
            sort_order = "PricePlusShippingLowest"
        elif sort_price == -1:
            sort_order = "PricePlusShippingHighest"
        else:
            sort_order = ""

        request = {
            "keywords": query if not fatfinger else typoing(query),
            # "categoryId": category_id,
            "descriptionSearch": False,
            "itemFilter": [
                {"name": "LocatedIn", "value": country} if country else None,
                {"name": "MaxPrice", "value": avg_val} if avg_val else None,
            ],
            "sortOrder": "EndTimeSoonest" if last_min else "",
            "sortOrder": sort_order,  # "EndTimeSoonest" if last_min else ""] #!DEBUG
        }
        if category_id:
            request["categoryId"] = category_id

        response = api.execute("findItemsAdvanced", request)
        data = response.dict()
        # return data  #!DEBUG

        try:
            if len(data["searchResult"]["item"]) < 1:
                return None
        except:
            return None

        try:
            for item in data["searchResult"]["item"]:
                for attr in (
                    "listingInfo",
                    "returnsAccepted",
                    "condition",
                    "primaryCategory",
                    "shippingInfo",
                    "sellingStatus",
                    "galleryURL",
                ):
                    if not attr in item.keys():
                        item[f"{attr}"] = r"N/A"

            return {
                "items_list": data["searchResult"]["item"],
                "item_search_url": data["itemSearchURL"],
                "avg_title": avg_title,
                "avg_val": avg_val,
            }
        except:
            return None

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        return None
    #!COMMENT THE BELOW CODE FOR DEBUGGING
    except:
        return None


#########! DEBUGGING
# bruh = typoing("playstation")

# bruh = run(
#     fetch_items(
#         query=typoing("bible"),
#         country="GB",
#         last_min=True,
#         category_id="139973",
#     )
# )

# print(bruh)


# for mwah in bruh["searchResult"]["item"]:
#     pprint(
#         mwah["primaryCategory"]["categoryName"], indent=3
#     )  #!bruh["primaryCategory"]["categoryName"]

# TODO
# SEE HOW TO FILTER BY CATEGORY, IT IS NOT FILTERING BY CATEGORY AT ALLLLLLLLL
