from typing import Optional
from discord.embeds import Embed
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord.ext.commands.core import guild_only
from SETUP import quick_flips_bot
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource


class HelpMenu(ListPageSource):
    def __init__(self, ctx: Context, data):
        self.ctx = ctx
        super().__init__(data, per_page=5)

    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        help_embed = Embed(
            title="Help",
            description=f"```{self.ctx.bot.PREFIX}command <argument>```",
            colour=self.ctx.author.colour,
        )
        help_embed.set_thumbnail(
            url=r"https://cdn.discordapp.com/attachments/879075886496899083/889219974206484500/dfaf229ee34edcf67791d91d1f5e07f1.png"
        )
        help_embed.set_author(name="QuickFlips Bot")
        help_embed.set_footer(
            text=f"{offset:,} - {min(len_data,offset+self.per_page-1):,} of {len_data:,} commands."
        )

        for name, value in fields:
            help_embed.add_field(name=name, value=value, inline=False)
        return help_embed

    async def format_page(self, menu, entries):
        fields = list()
        for entry in entries:
            fields.append((f"{entry}", f"{(entry.brief or 'No description')}"))
        return await self.write_page(menu, fields)


class Help(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.bot.remove_command("help")  # removing the standard 'help' cmd

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")
            self.guild = self.bot.get_guild(self.bot.guild)
            self.customer_role = self.guild.get_role(quick_flips_bot.customer_role_name)
            self.stdout = quick_flips_bot.stdout

        else:
            print("help cog loaded")

    @guild_only()
    async def cmd_help(self, ctx: Context, command):
        cmd_help_embed = Embed(title=f"`{command}`")

        cmd_help_embed.add_field(
            name="Command description", value=command.brief or "No description"
        )

        await ctx.send(embed=cmd_help_embed)

    @command(name="help", brief="shows the commands, their usage and syntax")
    @guild_only()
    async def show_help(self, ctx: Context, cmd: Optional[str]):
        if not cmd:
            menu = MenuPages(
                source=HelpMenu(ctx, list(self.bot.commands)),
                clear_reactions_after=True,
                timeout=180,
            )
            await menu.start(ctx)
        else:
            if command := get(self.bot.commands, name=cmd):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send("Command doesn't exist!")


def setup(bot):
    bot.add_cog(Help(bot))
