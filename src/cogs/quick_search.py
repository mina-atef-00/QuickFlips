from typing import Optional
from discord.channel import DMChannel
from discord.embeds import Embed
from discord.ext.commands import Cog, command, has_role
from discord.ext.commands.context import Context
from discord.member import Member
from pytz import country_names
from src.searching.searches import fetch_items
from src.searching.categories import (
    get_categ_id,
    create_categ_embeds,
    showing_categ_list,
)
from re import findall
from SETUP import quick_flips_bot
from DiscordUtils.Pagination import CustomEmbedPaginator
from src.searching.pages_dms import CustomEmbedPaginatorDM


async def format_input(self, input_list: list, ctx: Context) -> tuple:
    if len(input_list) == 1:
        query = input_list[0]
        country, categ_id = None, None

    elif len(input_list) == 2:
        query = input_list[0]

        if input_list[1].startswith("-"):
            categ_name = input_list[1][1:]
            categ_id = get_categ_id(categ_name)
            if not categ_id:
                return await ctx.send(
                    f"**Invalid Category.**\nUse `{self.bot.PREFIX}ShowCategories` for valid category names."
                )
            country = None

        elif len(input_list[1]) == 2:
            country = input_list[1]
            categ_id = None

        elif input_list[1] not in country_names.keys():
            return await ctx.send(
                "**Please enter a valid country code.**\ne.g.: `US`,`GB`"
            )

        else:
            return await ctx.send(
                f"**You have entered the command wrong.**\nuse: `{self.bot.PREFIX}LastFlip search_query,country_code,-category_name`"
            )

    elif len(input_list) == 3:
        query = input_list[0]

        if len(input_list[1]) == 2:
            country = input_list[1]
        elif input_list[1] not in country_names.keys():
            return await ctx.send(
                "**Please enter a valid country code.**\ne.g.: `US`,`GB`"
            )

        if input_list[2].startswith("-"):
            categ_name = input_list[2][1:]
            categ_id = get_categ_id(categ_name)
            if not categ_id:
                return await ctx.send(
                    f"**Invalid Category.**\nUse `{self.bot.PREFIX}ShowCategories` for valid category names."
                )
        else:
            return await ctx.send(
                f"**You have entered the command wrong.**\nuse: `{self.bot.PREFIX}LastFlip search_query,country_code,-category_name`"
            )

    elif len(input_list) > 3:
        return await ctx.send(
            f"**You have entered the command wrong.**\nuse: `{self.bot.PREFIX}LastFlip search_query,country_code,-category_name`"
        )

    return (query, country, categ_id)


def format_time_left(time_str: str):
    time_re_list = findall(r"\d+", time_str)

    time_dict = {
        "days": time_re_list[0],
        "hours": time_re_list[1],
        "minutes": time_re_list[2],
        "seconds": time_re_list[3],
    }
    return f"`{time_dict['days']}` days| `{time_dict['hours']}` hrs| `{time_dict['minutes']}` mins| `{time_dict['seconds']}` secs"


async def send_pages(
    embeds_list,
    items_or_categs,
    cog: Cog,
    private: bool = True,
    ctx: Context = None,
    trgt: Member = None,
):

    paginator = (
        CustomEmbedPaginator(ctx, remove_reactions=True, timeout=180)
        if not trgt
        else CustomEmbedPaginatorDM(
            trgt=trgt, remove_reactions=True, timeout=180, cog=cog
        )
    )
    pag_reacts = [
        ("⏮️", "first"),
        ("⏪", "back"),
        ("🔐", "lock"),
        ("⏩", "next"),
        ("⏭️", "last"),
    ]
    for emj, cmd in pag_reacts:
        paginator.add_reaction(emoji=emj, command=cmd)

    if trgt:
        await paginator.run(embeds_list, send_to=trgt)

    try:
        await ctx.message.add_reaction("🟩")
        if not isinstance(ctx.channel, DMChannel) and items_or_categs == "items":
            await ctx.send(
                f"The Items have been sent to you on DMs. {ctx.author.mention}"
            )
        await paginator.run(embeds_list, send_to=ctx.author if private else ctx)
    except:
        if private:
            return
            await ctx.author.send(
                f"{ctx.author.mention} **Can't send the {'Items' if items_or_categs=='items' else 'Categories'} to you on DMs!**\nPlease enable receiving DMs from members."
            )
        elif not private:
            await ctx.send(
                f"{ctx.author.mention} **Can't send the {'Items' if items_or_categs=='items' else 'Categories'} to you on DMs!**\nPlease enable receiving DMs from members."
            )


def create_item_embeds(
    items_list: list,
    item_search_url: str,
    avg_val,
    avg_title,
) -> list:

    item_embeds_list = list()
    for item in items_list:
        item_embed = Embed(
            title=item["title"],
            colour=0x4AD26F,
            description=f"{avg_title} `{avg_val}` {item['sellingStatus']['convertedCurrentPrice']['_currencyId']}",
        )
        item_embed.set_thumbnail(
            url=r"https://cdn.discordapp.com/attachments/879075886496899083/889219974206484500/dfaf229ee34edcf67791d91d1f5e07f1.png"
        )

        if not item["galleryURL"] == "N/A":
            item_embed.set_image(url=item["galleryURL"])

        item_embed.set_author(
            name="results from ebay.com",
            url=r"https://ebay.com",
            # icon_url=r"https://icons.iconarchive.com/icons/limav/flat-gradient-social/256/ebay-icon.png",
        )
        item_embed.set_footer(
            text=f"{items_list.index(item)+1} of {len(items_list)} items"
        )

        try:
            fields = [
                ("Item", f"[Link]({item['viewItemURL']})", True),
                ("Search", f"[URL]({item_search_url})", True),
                (
                    "Price",
                    f"`{item['sellingStatus']['convertedCurrentPrice']['value']}` {item['sellingStatus']['convertedCurrentPrice']['_currencyId']}",
                    True,
                ),
                ("Country", item["country"], True),
                ("Condition", item["condition"]["conditionDisplayName"], True),
                (
                    "Time Left",
                    format_time_left(item["sellingStatus"]["timeLeft"]),
                    True,
                ),
                (
                    "Returns",
                    (
                        "Accepted"
                        if item["returnsAccepted"] == "true"
                        else "Not Accepted"
                    ),
                    True,
                ),
                (
                    "Shipping Type",
                    item["shippingInfo"]["shippingType"],
                    True,
                ),
                ("Category", item["primaryCategory"]["categoryName"], True),
            ]
        except:
            continue

        for name, content, inline in fields:
            item_embed.add_field(name=name, value=content, inline=inline)

        item_embeds_list.append(item_embed)

    return item_embeds_list


class QuickSearch(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("quick_search")
            self.guild = self.bot.get_guild(self.bot.guild)
            self.customer_role = self.guild.get_role(quick_flips_bot.customer_role_name)

    @has_role(quick_flips_bot.customer_role_name)
    @command(
        name="QuickFlip",
        aliases=["quickflip"],
        brief=f"Searches for items that are below the average price on ebay.\n`{quick_flips_bot.prefix}QuickFlip search_keyword,country_code,-category`",
    )
    async def quick_flip(
        self,
        ctx: Context,
        *,
        input_text: Optional[str],
        # country: Optional[str],
        # category: Optional[str] = None,
    ):

        with ctx.channel.typing():
            if not input_text:
                return await ctx.send(
                    f"**You haven't searched for anything.**\nUse: `{self.bot.PREFIX}`QuickFlip"
                )

            input_list = input_text.split(",")
            query, country, categ_id = await format_input(
                self, ctx=ctx, input_list=input_list
            )

            data = await fetch_items(query=query, country=country, category_id=categ_id)
            if not data:
                await ctx.send(
                    "**We couldn't find results for your search.**\nPlease try changing your search."
                )
            else:
                avg_val = data["avg_val"]
                avg_title = data["avg_title"]

                try:
                    items_list = data["items_list"]
                    item_search_url = data["item_search_url"]
                except:
                    return

                item_embeds_list = create_item_embeds(
                    items_list,
                    # ctx=ctx,
                    item_search_url=item_search_url,
                    avg_title=avg_title,
                    avg_val=avg_val,
                )

                await send_pages(
                    ctx=ctx,
                    embeds_list=item_embeds_list,
                    items_or_categs="items",
                    cog=self,
                )

    @has_role(quick_flips_bot.customer_role_name)
    @command(
        name="TypoFlip",
        aliases=["typoflip"],
        brief=f"Searches for items by adding typos to the search keywords. All items are below the average price on ebay.\n`{quick_flips_bot.prefix}TypoFlip search_keyword,country_code,-category`",
    )
    async def typo_flip(
        self,
        ctx: Context,
        *,
        input_text: Optional[str],
        # country: Optional[str],
        # category: Optional[str] = None,
    ):

        with ctx.channel.typing():
            if not input_text:
                return await ctx.send(
                    f"**You haven't searched for anything.**\nUse: `{self.bot.PREFIX}`TypoFlip"
                )

            input_list = input_text.split(",")
            query, country, categ_id = await format_input(
                self, ctx=ctx, input_list=input_list
            )

            data = await fetch_items(
                query=query, country=country, category_id=categ_id, fatfinger=True
            )
            if not data:
                await ctx.send(
                    "**We couldn't find results for your search.**\nPlease try changing your search."
                )
            else:
                avg_val = data["avg_val"]
                avg_title = data["avg_title"]

                try:
                    items_list = data["items_list"]
                    item_search_url = data["item_search_url"]
                except:
                    return

                item_embeds_list = create_item_embeds(
                    items_list,
                    # ctx=ctx,
                    item_search_url=item_search_url,
                    avg_title=avg_title,
                    avg_val=avg_val,
                )

                await send_pages(
                    ctx=ctx,
                    embeds_list=item_embeds_list,
                    items_or_categs="items",
                    cog=self,
                )

    @has_role(quick_flips_bot.customer_role_name)
    @command(
        name="LastFlip",
        aliases=["lastflip"],
        brief=f"Searches for items that are going to expire soon.\n`{quick_flips_bot.prefix}LastFlip search_keyword,country_code,-category`",
    )
    async def last_flip(
        self,
        ctx: Context,
        *,
        input_text: Optional[str],
        # country: Optional[str],
        # category: Optional[str] = None,
    ):

        with ctx.channel.typing():
            if not input_text:
                return await ctx.send(
                    f"**You haven't searched for anything.**\nUse: `{self.bot.PREFIX}`LastFlip"
                )

            input_list = input_text.split(",")
            query, country, categ_id = await format_input(
                self, ctx=ctx, input_list=input_list
            )

            data = await fetch_items(
                query=query, country=country, category_id=categ_id, last_min=True
            )
            if not data:
                await ctx.send(
                    "**We couldn't find results for your search.**\nPlease try changing your search."
                )
            else:
                avg_val = data["avg_val"]
                avg_title = data["avg_title"]

                try:
                    items_list = data["items_list"]
                    item_search_url = data["item_search_url"]
                except:
                    return

                item_embeds_list = create_item_embeds(
                    items_list,
                    # ctx=ctx,
                    item_search_url=item_search_url,
                    avg_title=avg_title,
                    avg_val=avg_val,
                )

                await send_pages(
                    ctx=ctx,
                    embeds_list=item_embeds_list,
                    items_or_categs="items",
                    cog=self,
                )

    @has_role(quick_flips_bot.customer_role_name)
    @command(
        name="ShowCategories",
        aliases=["show_categories", "categories", "showcategories"],
        brief="Shows ebay search categories, and shows a link that has all ebay categories.",
    )
    async def show_categories(self, ctx: Context):
        await send_pages(
            ctx=ctx,
            embeds_list=create_categ_embeds(categs_list=showing_categ_list),
            items_or_categs="categs",
            private=False,
            cog=self,
        )


def setup(bot):
    bot.add_cog(QuickSearch(bot))
