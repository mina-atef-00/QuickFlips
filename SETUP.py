### Some Notes ###
# 1- To run the bot, run quick_flips_main.py (python -m quick_flips_main)

# 2- To run the bot on heroku use this link: https://dashboard.heroku.com/apps/ebay-listing-bot/resources
# and then in the box with the "worker", press the pen button and turn the switch on

# 3- AFTER CHANGING ANYTHING IN THIS FILE, RESTART THE BOT BY TURNING THE SWITCH ON & OFF FROM HEROKU

from dataclasses import dataclass
import dotenv
import os

env_file_path: str = ".env"
dotenv.load_dotenv(".env")


@dataclass
class QuickBot:
    thumbnail_link: str
    token: str
    prefix: str
    payment_link: str
    bot_owner_user_id: int
    server_id: int
    stdout: int
    customer_role_name: str
    invite_link: str
    paypal_token: str
    mongo_username: str
    mongo_password: str
    mongo_hostname: str
    mongo_clustername: str


quick_flips_bot = QuickBot(
    token=os.getenv("token"),
    prefix=os.getenv("prefix"),
    payment_link=os.getenv("payment_link"),
    customer_role_name=os.getenv("customer_role_name"),
    bot_owner_user_id=int(os.getenv("bot_owner_user_id")),
    server_id=int(os.getenv("server_id")),
    stdout=int(os.getenv("stdout")),
    invite_link=os.getenv("invite_link"),
    paypal_token=os.getenv("paypal_token"),
    thumbnail_link=os.getenv("thumbnail_link"),
    mongo_password=os.getenv("mongo_password"),
    mongo_username=os.getenv("mongo_username"),
    mongo_hostname=os.getenv("mongo_hostname"),
    mongo_clustername=os.getenv("mongo_clustername"),
)
