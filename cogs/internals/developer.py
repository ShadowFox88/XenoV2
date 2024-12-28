from __future__ import annotations

import difflib
import time
from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from utils import DiscordExceptions, DismissView, XenoCog

if TYPE_CHECKING:
    from utils.context import XenoContext


class Developer(XenoCog):
    """
    Developer Commands for the bot.
    """

    async def cog_check(self, ctx: XenoContext) -> bool:
        """
        Ensure that the user is a bot owner.

        Applies to all commands in this cog.
        """
        return await self.bot.is_owner(ctx.author)

    @commands.group(name="developer", aliases=["dev"], invoke_without_command=True)
    async def developer_group(self, ctx: XenoContext) -> None:
        """
        Developer Commands for the bot.

        This command is a group command.
        """
        await ctx.send_help(ctx.command)

    @developer_group.command()
    async def reload(self, ctx: XenoContext, extension: str = "all") -> None:
        """
        Reload an extension or all extensions.

        No idea why I have this - I use docker, but its legacy code so who cares.
        """
        if extension == "all":
            extensions: dict[str, bool | None | Exception] = {
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
                    except Exception:  # noqa: BLE001, PERF203, S110
                        pass
            else:
                try:
                    await self.bot.reload_extension(extension)
                    extensions[extension] = True
                except Exception as e:  # noqa: BLE001
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
                    f"{(self.bot.emoji_list['animated_green_tick']
                        if v else
                        self.bot.emoji_list['animated_red_cross'])} {k}"
                    for k, v in extensions.items()
                ),
            )

        await ctx.send(embed=embed, button=True)

    @developer_group.command()
    async def purge(  # noqa: C901, PLR0912
        self,
        ctx: XenoContext,
        arg1: discord.Member | discord.User | discord.Role | int | bool = None,
        arg2: discord.Member | discord.User | int | bool = None,
        arg3: discord.Member | discord.User | int | bool = None,
    ) -> None | discord.Message:
        """
        Purges messages from a channel.
        """
        target = None
        limit = 50
        manual_delete = False

        if isinstance(arg1, (discord.Member, discord.User)):
            target = arg1
        elif isinstance(arg2, (discord.Member, discord.User)):
            target = arg2
        elif isinstance(arg3, (discord.Member, discord.User)):
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

        def check(message: discord.Message) -> bool:
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
            value="\n".join([f"**{i}**: {j}" for i, j in message_statistics.items()]),
        )

        return await ctx.reply(embed=embed)

    @developer_group.command(aliases=["e"])
    async def error(
        self,
        ctx: XenoContext,
        error_id: int,
        fixed: bool | None = False,  # noqa: FBT002
    ) -> None | discord.Embed:
        """
        View an error report.
        """
        error = await self.bot.prisma.errors.find_first(where={"ID": error_id})

        if not error:
            embed = discord.Embed(
                description="Error Report Not Found",
                colour=discord.Colour.red(),
            )
            return await ctx.send(embed=embed, reply=True, delete_after=30)

        traceback = error.traceback
        user_id = error.userID
        command = error.command
        guild_id = error.guildID
        message_id = error.errorMessageID
        error_time = time.mktime(error.errorTime.timetuple())

        webhook = discord.Webhook.from_url(
            self.bot.error_webhook, session=self.bot.session
        )
        try:
            developer_message = await webhook.fetch_message(message_id)
        except discord.errors.NotFound:
            developer_message = None

        if fixed:
            await self.bot.prisma.errors.update(
                where={"ID": error_id},
                data={"fixed": True},
            )
            await developer_message.delete()

            embed = discord.Embed(
                description=f"Error {error_id} Fixed",
                colour=discord.Colour.green(),
            )
            return await ctx.send(embed=embed, reply=True, delete_after=30)

        embed = discord.Embed(
            title=f"Error Report: {error_id}",
            description=f"```py\n{traceback}```",
            colour=discord.Colour.red(),
        )

        additional_info = f"""User: {self.bot.get_user(user_id).name or "Not Found"} ({user_id})
        Command: {command}
        Guild ID: {guild_id}
        Time: <t:{int(error_time)}:f>"""  # noqa: E501

        embed.add_field(name="Additional Info", value=additional_info)
        embed.timestamp = embed.timestamp or discord.utils.utcnow()

        await ctx.send(
            embed=embed,
            view=DismissView(error_id, ctx.author, self.bot, developer_message),
            delete_after=60,
        )

        return None

    @developer_group.command(aliases=["ec", "ce"])
    async def clear_errors(self, ctx: XenoContext) -> None:
        """
        Clear all error reports.
        """
        errors = await self.bot.prisma.errors.find_many(where={"fixed": False})

        webhook = discord.Webhook.from_url(
            self.bot.error_webhook, session=self.bot.session
        )

        for i in errors:
            try:
                developer_message = await webhook.fetch_message(i.errorMessageID)
            except discord.errors.NotFound:
                developer_message = None

            if developer_message:
                await developer_message.delete()

        await self.bot.prisma.errors.update_many(where={}, data={"fixed": True})

        embed = discord.Embed(
            description=f"Cleared {len(errors)} Error{'s' if len(errors) != 1 else ''}",
            colour=discord.Colour.green(),
        )

        await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])
        await ctx.send(embed=embed, reply=True)

    @developer_group.command(aliases=["re", "raise"])
    async def raise_error(self, ctx: XenoContext, error: str) -> discord.Message | None:
        """
        Raise and error for debugging.
        """
        cross: str = self.bot.emoji_list["animated_red_cross"]
        tick: str = self.bot.emoji_list["animated_green_tick"]

        errors = DiscordExceptions().errors

        matches = difflib.get_close_matches(error, list(errors.keys()))
        msg = f"{matches[0]}: Testing"

        errors_matched = [errors[i] for i in matches]

        if len(errors_matched) == 0:
            await ctx.message.add_reaction(cross)

            embed = discord.Embed(
                colour=discord.Colour.red(), description="No Matches Found"
            )

            return await ctx.send(embed=embed)
        if len(errors_matched) == 1:
            await ctx.message.add_reaction(tick)

            # All of the errors are given as base classes,
            # and aren't called yet. We call the error here
            # with our message to distinguish it from the other errors.
            self.bot.dispatch("command_error", ctx, errors_matched[0](msg))

            return None
        await ctx.message.add_reaction(cross)

        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(
            name="Multiple Matches Found",
            value=", ".join([f"`{i}`" for i in matches]),
        )
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(
                discord.Colour.red(), description="Too many matches to display"
            )
