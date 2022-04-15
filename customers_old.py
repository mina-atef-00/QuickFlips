from typing import Optional

from discord.embeds import Embed
from discord.ext.commands import Cog, command, has_permissions
from discord.ext.commands.context import Context
from discord.ext.commands.core import guild_only
from discord.utils import get

from SETUP import quick_flips_bot
from src.customer.customer_check import check_invoice_payment
from src.db.mongo import create_subscription, del_subscription, mongo_connect

# from pprint import pprint


class Customers(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("customers")
            self.guild = self.bot.get_guild(self.bot.guild)
            self.customer_role = get(
                self.guild.roles, name=quick_flips_bot.customer_role_name
            )
            # print(self.customer_role)
            self.stdout = self.bot.get_channel(quick_flips_bot.stdout)
            await mongo_connect()

        else:
            print("customers cog loaded")

    @guild_only()
    @has_permissions(administrator=True)
    @command(
        name="AddCustomers",
        aliases=["addcustomers", "add_customers", "add-customers"],
        brief=f"adds customers.\n`AddCustomers member_ids or mentions`",
        pass_context=True,
    )
    async def add_customers(self, ctx, members_text: Optional[str]):
        if not members_text:
            return await ctx.send(
                f"**You haven't provided member ids.**\nUse `{self.bot.PREFIX}RemoveCustomers member(s)_id`"
            )
        members_list = members_text.split(",")
        members = list(
            map(
                lambda member_id: get(self.guild.members, id=int(member_id)),
                members_list,
            )
        )

        if None in members:
            return await ctx.send(
                f"**You entered a wrong member id.**\nUse `{self.bot.PREFIX}RemoveCustomers member(s)_id`"
            )

        else:
            for member in members:
                if (
                    not ctx.guild.me.top_role.position > member.top_role.position
                    or not ctx.author.top_role.position > member.top_role.position
                ):
                    await ctx.message.add_reaction("🟥")
                    await ctx.send(
                        f"**{str(member)}'s top role is higher than mine/yours.**"
                    )
                    continue

                # ? ADD ROLES TO MEMBER
                try:
                    await member.add_roles(self.customer_role)
                    await ctx.message.add_reaction("🟩")
                except:
                    # return raise
                    return await ctx.send(
                        "**Maybe you have provided a wrong role_id.**"
                    )

    @guild_only()
    @has_permissions(administrator=True)
    @command(
        name="RemoveCustomers",
        aliases=["remcustomers", "remove_customers"],
        brief=f"removes customers.\n`RemoveCustomers member_ids or mentions`",
        pass_context=True,
    )
    async def remove_customers(self, ctx, members_text: Optional[str]):
        if not members_text:
            return await ctx.send(
                f"**You haven't provided member ids.**\nUse `{self.bot.PREFIX}RemoveCustomers member(s)_id`"
            )
        members_list = members_text.split(",")
        members = list(
            map(
                lambda member_id: get(self.guild.members, id=int(member_id)),
                members_list,
            )
        )
        if None in members:
            return await ctx.send(
                f"**You entered a wrong member id.**\nUse `{self.bot.PREFIX}RemoveCustomers member(s)_id`"
            )

        else:
            for member in members:
                # return print(member)
                if (
                    not ctx.guild.me.top_role.position > member.top_role.position
                    or not ctx.author.top_role.position > member.top_role.position
                ):
                    await ctx.message.add_reaction("🟥")
                    await ctx.send(
                        f"**{str(member)}'s top role is higher than mine/yours.**"
                    )
                    continue

                # ? REMOVE ROLES FROM MEMBER
                if not self.customer_role in member.roles:
                    await ctx.message.add_reaction("🟥")
                    await ctx.send(f"**{str(member)} is not a customer.**")
                    continue

                try:
                    await member.remove_roles(self.customer_role)
                    await ctx.message.add_reaction("🟩")
                except:
                    # return raise
                    return await ctx.send(
                        "**Maybe you have provided a wrong role_id.**"
                    )

    @guild_only()
    @has_permissions(administrator=True)
    @command(
        name="ShowCustomers",
        aliases=["show_customers"],
        brief=f"shows customers.\n`showCustomers member_ids or mentions`",
        pass_context=True,
    )
    async def show_customers(self, ctx: Context):
        return await ctx.send(
            "\n".join(
                [
                    f"{ind+1}- `{str(mem)}`"
                    for ind, mem in enumerate(self.customer_role.members)
                ]
            )
        )

    @command(
        name="VerifyPayment",
        aliases=["verify_payment"],
        brief="**Please Use this command in the bot DMs**\nfor the customer to verify their payment on paypal and get the customer role.\n`VerifyPayment invoice_id`",
    )
    async def verify_payment(self, ctx: Context, invoice_id: Optional[str]):
        member = get(self.guild.members, id=ctx.author.id)

        if not invoice_id:
            return await ctx.send("**You have not provided an invoice id.**")

        payment_check = await check_invoice_payment(invoice_id, live=True)
        # return pprint(payment_check, indent=3)  #!DEBUG
        if not payment_check:
            return await ctx.send(
                "**Either Your invoice id is wrong, or you haven't paid the specified amount, or there's a connection error so please try again later.**"
            )

        else:
            customer_embed = Embed(
                title="Congratulations You are now a Customer!",
                description=f"Please use `{self.bot.PREFIX}help` in the server to see the available commands.",
                colour=0x4AD26F,
            )

            # ? ADD ROLES TO MEMBER
            await member.add_roles(self.customer_role)
            await ctx.message.add_reaction("🟩")
            await ctx.author.send(embed=customer_embed)
            await self.stdout.send(f"`{str(ctx.author)}` is now a customer!")


def setup(bot):
    bot.add_cog(Customers(bot))
