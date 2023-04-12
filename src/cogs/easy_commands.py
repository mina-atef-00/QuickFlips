import asyncio
from pprint import pprint
from typing import Optional

from discord import Embed, Guild, Member, Message, Reaction, User
from discord.ext.commands import Cog
from discord.utils import get
from flag import flag
from pytz import country_names
from SETUP import quick_flips_bot
from src.cogs.quick_search import create_item_embeds, send_pages
from src.searching.categories import get_categ_id
from src.searching.searches import fetch_items

emji_code_dict = {code: flag(f":{code}:") for code in country_names.keys()}

allowed_emjis = ("⬆️", "⬇️", "✅", *emji_code_dict.values())


class EasyCommands(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("easy_commands")
            self.guild: Guild = self.bot.get_guild(self.bot.guild)
            # print(self.guild)  #!DEBUG
            self.customer_role = get(
                self.guild.roles, name=quick_flips_bot.customer_role_name
            )
            self.stdout = self.bot.get_channel(quick_flips_bot.stdout)
            self.quickflip_chan, self.typoflip_chan, self.lastflip_chan = (
                get(self.guild.channels, name=channel_name)
                for channel_name in ("quickflip", "typoflip", "lastflip")
            )
            # print(self.quickflip_chan, self.typoflip_chan, self.lastflip_chan)

        else:
            print("easy_commands cog loaded")

    async def send_selection_embed(self, type, trgt: Member, query, categ_name=None):
        selection_embed = Embed(
            title="Would you like to narrow your search?",
            description=f"**- All options below are optional**\n\n* **React with a country flag** (like 🇺🇸) to select a country for the items.\n* **You can also order the items by their price** from the lowest to highest (by pressing on ⬆️) ,or vice-versa (⬇️).\n* **To confirm** your search press on ✅",
            colour=0x4AD26F,
        )
        selection_msg: Message = await trgt.send(embed=selection_embed)
        for emji in ("⬆️", "⬇️", "✅"):
            await selection_msg.add_reaction(emji)

        def check(reaction: Reaction, user: Optional[User] = None):
            return str(reaction.emoji) in allowed_emjis

        country = None
        sort_price = None
        categ_name = None
        categ_id = None

        while True:
            try:
                reaction = await self.bot.wait_for(
                    "raw_reaction_add", timeout=100.0, check=check,
                )
                if reaction.user_id == self.bot.user.id:
                    continue
                if str(reaction.emoji) == "⬆️":
                    sort_price = 1
                    # print(sort_price)
                elif str(reaction.emoji) == "⬇️":
                    sort_price = -1
                    # print(sort_price)

                elif str(reaction.emoji) in emji_code_dict.values():
                    country = list(emji_code_dict.keys())[
                        list(emji_code_dict.values()).index(str(reaction.emoji))
                    ]

                elif str(reaction.emoji) == "✅":
                    # break  #!DEBUG

                    if categ_name:
                        categ_id = get_categ_id(categ_name)
                        if not categ_id:
                            await trgt.send(
                                f"**Invalid Category.**\nUse `{self.bot.PREFIX}ShowCategories` for valid category names."
                            )
                            break

                    if type == 0:
                        data = await fetch_items(
                            query=query,
                            country=country,
                            category_id=categ_id,
                            sort_price=sort_price,
                        )
                    if type == 1:
                        data = await fetch_items(
                            query=query,
                            country=country,
                            category_id=categ_id,
                            fatfinger=True,
                            sort_price=sort_price,
                        )
                    if type == 2:
                        data = await fetch_items(
                            query=query,
                            country=country,
                            category_id=categ_id,
                            last_min=True,
                            sort_price=sort_price,
                        )
                        # pprint(data, indent=4)  #!DEBUG
                    if not data:
                        await trgt.send(
                            "**We couldn't find results for your search.**\nPlease try changing your search."
                        )
                        break

                    else:
                        avg_val = data["avg_val"]
                        avg_title = data["avg_title"]

                        try:

                            items_list = data["items_list"]
                            item_search_url = data["item_search_url"]
                        except:
                            break

                        item_embeds_list = create_item_embeds(
                            items_list,
                            item_search_url=item_search_url,
                            avg_title=avg_title,
                            avg_val=avg_val,
                        )

                        await send_pages(
                            trgt=trgt,
                            embeds_list=item_embeds_list,
                            items_or_categs="items",
                            cog=self,
                        )
                        break

            except asyncio.TimeoutError:
                break
            except:
                raise  #!DEBUG
                return await trgt.send("Please add a valid reaction")

    @Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.bot:
            if (not message.content.startswith(self.bot.PREFIX)) and (
                self.customer_role in message.author.roles
            ):
                # print("True Man")  #!DEBUG
                input_list = message.content.strip().split("+")
                query = input_list[0].strip()
                categ_name = input_list[1].strip() if len(input_list) > 1 else None

                if message.channel == self.quickflip_chan:
                    # print(True)  #!DEBUG
                    await self.send_selection_embed(
                        trgt=message.author, categ_name=categ_name, query=query, type=0
                    )

                if message.channel == self.typoflip_chan:
                    await self.send_selection_embed(
                        trgt=message.author, categ_name=categ_name, type=1, query=query
                    )

                if message.channel == self.lastflip_chan:
                    await self.send_selection_embed(
                        trgt=message.author, categ_name=categ_name, type=2, query=query
                    )


def setup(bot):
    bot.add_cog(EasyCommands(bot))
