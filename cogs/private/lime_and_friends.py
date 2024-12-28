import datetime

import discord
from discord.ext import commands
from utils.bot import Xeno
from utils.context import XenoContext
from utils.views import ConfirmView


class Lime_And_Friends(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot

    async def cog_check(self, ctx):
        return (ctx.guild.id == 1265697842475831397) or ctx.bot.is_owner(ctx.author)

    @commands.command()
    async def unpin(self, ctx: XenoContext, message_id: int | None) -> None:
        if message_id and ctx.reference:
            raise AssertionError

        if message_id:
            message = await ctx.fetch_message(message_id)

        elif ctx.message.reference:
            message = ctx.reference

        else:
            await ctx.send("Please provide a message to unpin")
            return

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
    async def mass_slowmode(self, ctx: XenoContext, slowmode: int) -> None:
        for channel in ctx.guild.text_channels:
            await channel.edit(slowmode_delay=slowmode)

        embed = discord.Embed(
            description=f"Set slowmode to {slowmode} in all channels.",
            color=discord.Color.green(),
        )

        await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])
        await ctx.send(embed=embed)

    class TimeoutTime(commands.FlagConverter):
        seconds: int = 0
        minutes: int = 0
        hours: int = 0
        days: int = 0
        weeks: int = 0

    @commands.is_owner()
    @commands.command()
    async def timeout(
        self, ctx: XenoContext, user: commands.MemberConverter, *, times: TimeoutTime
    ) -> None:
        """
        Times out a user for a specific amount of time. Maximum time is 4 weeks.
        """
        time = {
            "seconds": times.seconds,
            "minutes": times.minutes,
            "hours": times.hours,
            "days": times.days,
            "weeks": times.weeks,
        }

        if datetime.timedelta(**time) > datetime.timedelta(weeks=4):
            raise commands.BadArgument(
                "You can only timeout a user for a maximum of 4 weeks."
            )

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

        confirm_message = await ctx.reply(embed=embed, view=view)

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
