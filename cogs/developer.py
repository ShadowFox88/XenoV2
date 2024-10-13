import difflib
import time
from typing import Dict, Union

import discord
from discord.ext import commands

from utils.bot import Xeno
from utils.context import XenoContext
from utils.errors import DiscordExceptions
from utils.views import DismissView


class Developer(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.group(name="developer", aliases=["dev"], invoke_without_command=True)
    async def developer_group(self, ctx: XenoContext):
        await ctx.send_help(ctx.command)

    @developer_group.command()
    async def reload(self, ctx: XenoContext, extension: str = "all"):
        if extension == "all":
            extensions: Dict[str, bool | None | Exception] = {
                i: None for i in self.bot.extensions
            }
        else:
            extensions = {extension: None}

        async with ctx.typing():
            if extension == "all":
                for ext in extensions:
                    try:
                        await self.bot.reload_extension(ext)
                        extensions[ext] = True
                    except Exception:
                        pass
            else:
                try:
                    await self.bot.reload_extension(extension)
                    extensions[extension] = True
                except Exception as e:
                    extensions[extension] = e

            embed = discord.Embed(title="Reloaded Extensions")
            embed.colour = (
                discord.Colour.green()
                if all(extensions.values())
                else discord.Colour.red()
            )
            embed.add_field(
                name="Extensions",
                value="\n".join(
                    f"{self.bot.emoji_list['animated_green_tick'] if v else self.bot.emoji_list['animated_red_cross']} {k}"
                    for k, v in extensions.items()
                ),
            )

        await ctx.send(embed=embed, button=True)

    @developer_group.command(aliases=["purge"])
    async def purge_messages(
        self,
        ctx: XenoContext,
        arg1: Union[discord.Member, discord.User, discord.Role, int, bool] = None,
        arg2: Union[discord.Member, discord.User, int, bool] = None,
        arg3: Union[discord.Member, discord.User, int, bool] = None,
    ):

        target = None
        limit = 50
        manual_delete = False

        if isinstance(arg1, discord.Member) or isinstance(arg1, discord.User):
            target = arg1
        elif isinstance(arg2, discord.Member) or isinstance(arg2, discord.User):
            target = arg2
        elif isinstance(arg3, discord.Member) or isinstance(arg3, discord.User):
            target = arg3

        if isinstance(arg1, int):
            limit = arg1
        elif isinstance(arg2, int):
            limit = arg2
        elif isinstance(arg3, int):
            limit = arg3

        if isinstance(arg1, bool):
            manual_delete = arg1
        elif isinstance(arg2, bool):
            manual_delete = arg2
        elif isinstance(arg3, bool):
            manual_delete = arg3

        limit = limit + 1  # To include the command message

        embed = discord.Embed(title="Purged Messages")

        def check(message: discord.Message):
            if target is None:
                return message != ctx.message
            return message.author == target and message != ctx.message

        if not manual_delete:
            deleted_messages = await ctx.channel.purge(limit=limit, check=check)

            embed.title = "Purged Messages Successfully"
            embed.colour = discord.Colour.green()
            await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])

            message_statistics = {}

            for i in deleted_messages:
                if i.author not in message_statistics:
                    message_statistics[i.author] = 0
                message_statistics[i.author] += 1

            embed.add_field(
                name="Messages Deleted",
                value="\n".join(
                    [f"**{i}**: {j}" for i, j in message_statistics.items()]
                ),
            )

            return await ctx.reply(embed=embed)

        else:
            deleted_messages = []

            for i in ctx.channel.history(limit=limit):
                if i == ctx.message:
                    continue
                deleted_messages.append(i)
                await i.delete()

            embed.title = "Purged Messages Successfully"
            embed.colour = discord.Colour.green()
            await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])

            message_statistics = {}

            for i in deleted_messages:
                if i.author not in message_statistics:
                    message_statistics[i.author] = 0
                message_statistics[i.author] += 1

            embed.add_field(
                name="Messages Deleted",
                value="\n".join(
                    [f"**{i}**: {j}" for i, j in message_statistics.items()]
                ),
            )

            return await ctx.reply(embed=embed)

    @developer_group.command(aliases=["e"])
    async def error(self, ctx: XenoContext, id: int):
        data = await self.bot.db.fetch("SELECT * FROM errors WHERE id = $1", id)
        traceback = data[0]["traceback"]
        user_id = data[0]["user_id"]
        command = data[0]["command"]
        guild_id = data[0]["guild_id"]
        error_time = time.mktime(data[0]["error_time"].timetuple())

        embed = discord.Embed(
            title=f"Error Report: {id}",
            description=f"```py\n{traceback}```",
            colour=discord.Colour.red(),
        )

        additional_info = f"""User: {self.bot.get_user(user_id).name} ({user_id})
        Command: {command}
        Guild ID: {guild_id}
        Time: <t:{int(error_time)}:f>"""

        embed.add_field(name="Additional Info", value=additional_info)
        embed.timestamp = embed.timestamp or discord.utils.utcnow()

        await ctx.send(embed=embed, view=DismissView(id, ctx.author, self.bot))

    @developer_group.command(aliases=["re", "raise"])
    async def raise_error(self, ctx: XenoContext, error: str):

        cross: str = self.bot.emoji_list["animated_red_cross"]
        tick: str = self.bot.emoji_list["animated_green_tick"]

        matches = difflib.get_close_matches(error, DiscordExceptions().all_errors)

        if error in DiscordExceptions().all_errors:
            matches = [error]

        if len(matches) == 0:
            await ctx.message.add_reaction(cross)

            embed = discord.Embed(
                colour=discord.Colour.red(), description="No Matches Found"
            )

            return await ctx.send(embed=embed)
        elif len(matches) == 1:
            await ctx.message.add_reaction(tick)
            exec(f"raise {matches[0]}")

            return
        else:
            await ctx.message.add_reaction(cross)

            embed = discord.Embed(colour=discord.Colour.red())
            embed.add_field(
                name="Multiple Matches Found",
                value=", ".join([f"`{i}`" for i in matches]),
            )

            return await ctx.send(embed=embed)


async def setup(bot: Xeno):
    cog = Developer(bot)
    await bot.add_cog(cog)
