### Some Notes ###
# 1- To run the bot, run quick_flips_main.py (python -m quick_flips_main)

# 2- To run the bot on heroku use this link: https://dashboard.heroku.com/apps/ebay-listing-bot/resources
# and then in the box with the "worker", press the pen button and turn the switch on

# 3- AFTER CHANGING ANYTHING IN THIS FILE, RESTART THE BOT BY TURNING THE SWITCH ON & OFF FROM HEROKU

from dataclasses import dataclass
from datetime import timedelta
from os import environ


@dataclass
class QuickBot:

    # ? Bot Thumbnail Picture link (have to be a web link, you can't add a local directory location)
    thumbnail_link: str

    # ?  bot password (DON'T SHARE) (can be changed normally if you have a developer account as long as you have the bot's source code) (it is accessible from https://dashboard.heroku.com/apps/quick-flips-discord-bot/settings, by pressing the reveal config vars button)
    token: str

    # ?  prefix that is before commands, like (!) for rhythm (!play)
    prefix: str

    # ?  payment link that users get redirected to if they are not customers yet
    payment_link: str

    # ?  the bot owner's user id (right click/hold on user and search for copy id after enabling developer options)(set to Quicky#7167 id by default)
    bot_owner_user_id: int

    # ?  the server id where the bot will work on (it can be found the same way as the owner id)
    server_id: int

    # ?  bot technical messages channel id (get it like the owner and server)
    stdout: int

    # ?  the role assigned to customers, without it they can't use the bot
    customer_role_name: str

    # ?  bot invite link to server
    invite_link: str

    # ? paypal api application token (can be accessed the same way as the bot token)
    paypal_token: str

    # ? mongo db username
    mongo_username: str

    # ? mongo db password
    mongo_password: str

    # ? Subscription renewal period
    sub_renew_period: timedelta


#! CHANGE THE CONFIGURATION HERE
quick_flips_bot = QuickBot(
    token=environ.get("quickflips_token"),
    prefix="q!",
    payment_link="https://www.google.com/",  #! change it
    customer_role_name="QuickFlippers",
    ############################################################ #? More Technical
    bot_owner_user_id=210800510175805440,
    server_id=888136007969562624,
    stdout=888136263364919316,
    paypal_token=environ.get("paypal_token"),
    mongo_password=environ.get("mongo_password"),
    mongo_username="quick-flips",
    thumbnail_link=(
        r"https://cdn.discordapp.com/attachments/879075886496899083/889219974206484500/dfaf229ee34edcf67791d91d1f5e07f1.png",
    ),
    invite_link=(
        r"https://discord.com/api/oauth2/authorize?client_id=890552186394791957&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D890552186394791957%26permissions%3D8%26redirect_uri%3Dhttps%253A%252F%252Fdiscord.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id%253D890552&scope=bot",
    ),
)

# ===============================================================

#! NOTE TO DEV server id (pushing: 888136007969562624) (testing: 892803998573277216)
#! NOTE TO DEV stdout (pushing: 888136263364919316) (testing: 892803998980112424)
