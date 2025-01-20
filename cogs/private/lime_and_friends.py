# type: ignore  # noqa: PGH003
# fmt: off

from __future__ import annotations

import datetime
import inspect

import discord
from discord.ext import commands

from utils import ConfirmView, IncompatibleOptionsProvided, XenoCog, XenoContext

LIME_AND_FRIENDS_GUILD = 1265697842475831397


class TimeoutTime(commands.FlagConverter):
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0
    weeks: int = 0


class LimeAndFriends(XenoCog):
    """
    Commands for the Lime and Friends private guild.
    """

    async def cog_check(self, ctx: XenoContext) -> bool:  # pyright: ignore[reportIncompatibleMethodOverride]
        """
        Ensure the command is only available in the Lime and Friends guild.
        """
        return (
            ctx.guild.id == LIME_AND_FRIENDS_GUILD if ctx.guild else False
        ) or await self.bot.is_owner(ctx.author)

    @commands.command()
    async def unpin(self, ctx: XenoContext, message_id: int | None) -> None:
        if message_id and ctx.reference:
            msg = "You can only provide a message ID or a reference, not both."
            raise IncompatibleOptionsProvided(msg)

        if message_id:
            message = await ctx.fetch_message(message_id)

        if ctx.message.reference:
            message = ctx.reference
            if not message:
                msg = "The message you are replying to was not found."
                raise commands.MessageNotFound(msg)

        else:
            raise commands.MissingRequiredArgument(
                commands.parameters.Parameter(
                    name="message_id", kind=inspect.Parameter.POSITIONAL_ONLY
                )
            )

        if not message.pinned:
            raise AssertionError
        await message.unpin()

    @commands.command()
    async def pin(self, ctx: XenoContext, message_id: int | None) -> None:
        if message_id and ctx.reference:
            raise AssertionError

        if message_id:
            message = await ctx.fetch_message(message_id)

        elif ctx.reference:
            message = ctx.reference

        else:
            await ctx.send("Please provide a message to pin")
            return

        await message.pin()

    @commands.is_owner()
    @commands.command()
    @commands.guild_only()
    async def mass_slowmode(self, ctx: XenoContext, slowmode: int) -> None:
        """
        Set the slowmode of everything.
        """
        if not ctx.guild:
            return
        for channel in ctx.guild.text_channels:
            await channel.edit(slowmode_delay=slowmode)

        embed = discord.Embed(
            description=f"Set slowmode to {slowmode} in all channels.",
            color=discord.Color.green(),
        )

        await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def timeout(
        self, ctx: XenoContext, user: commands.MemberConverter, *, times: TimeoutTime
    ) -> None:
        """
        Time out a user for a specific amount of time. Maximum time is 4 weeks.
        """
        time = {
            "seconds": times.seconds,
            "minutes": times.minutes,
            "hours": times.hours,
            "days": times.days,
            "weeks": times.weeks,
        }

        if datetime.timedelta(**time) > datetime.timedelta(weeks=4):
            msg = "You can only timeout a user for a maximum of 4 weeks."
            raise commands.BadArgument(msg)

        if not any(time.values()) or datetime.timedelta(**time) < datetime.timedelta(
            seconds=0
        ):
            embed = discord.Embed(
                description="Are you sure you want to remove any timeout the user has?",
                color=discord.Color.orange(),
            )
        else:
            embed = discord.Embed(
                description=f"Are you sure you want to timeout {user.mention} until {discord.utils.format_dt(datetime.datetime.utcnow() + datetime.timedelta(**time))}?",
                color=discord.Color.orange(),
            )

        view = ConfirmView(ctx.author)

        confirm_message = view.message = await ctx.reply(embed=embed, view=view)

        await view.wait()
        if view.value is None:
            embed = discord.Embed(
                description="You took too long. This operation was cancelled.",
                color=discord.Color.red(),
            )
            await confirm_message.edit(embed=embed, view=None)

        if not view.value:
            embed = discord.Embed(
                description="Operation cancelled.", color=discord.Color.red()
            )
            await confirm_message.edit(embed=embed, view=None)
            return

        await user.timeout(datetime.timedelta(**time))

        if not any(time.values()) or datetime.timedelta(**time) < datetime.timedelta(
            seconds=0
        ):
            embed = discord.Embed(
                description=f"Removed timeout from {user.mention}",
                color=discord.Color.green(),
            )
        else:
            until_time = discord.utils.format_dt(
                datetime.datetime.now(tz=datetime.datetime.utc)
                + datetime.timedelta(**time)
            )
            embed = discord.Embed(
                description=f"Timed out {user.mention} until {until_time}",
                color=discord.Color.green(),
            )

        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(
            text=f"Command ran by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])
        await confirm_message.edit(embed=embed, view=None)
