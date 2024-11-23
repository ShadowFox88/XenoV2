from discord.ext import commands
import discord

from utils.bot import Xeno
from utils.context import XenoContext
import datetime


class Lime_And_Friends(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
        
    async def cog_check(self, ctx):
        return ctx.guild.id == 1265697842475831397

    @commands.command()
    async def unpin(self, ctx: XenoContext, message_id: int | None) -> None:
        assert not (message_id and ctx.reference)

        if message_id:
            message = await ctx.fetch_message(message_id)

        elif ctx.message.reference:
            message = ctx.reference

        else:
            await ctx.send("Please provide a message to unpin")
            return

        assert message.pinned
        await message.unpin()

    @commands.command()
    async def pin(self, ctx: XenoContext, message_id: int | None) -> None:
        assert not (message_id and ctx.reference)

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
            color=discord.Color.green()
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
    async def timeout(self, ctx: XenoContext, user: commands.MemberConverter, *, times: TimeoutTime) -> None:
        
        time = {
                "seconds": times.seconds,
                "minutes": times.minutes,
                "hours": times.hours,
                "days": times.days,
                "weeks": times.weeks
        }
                
        if not any(time.values()):
            raise commands.BadArgument("Please provide a time to timeout the user for.")
              
        await user.timeout(datetime.timedelta(**time))
                
        embed = discord.Embed(
            description=f"Timed out {user.mention} until {discord.utils.format_dt(datetime.datetime.utcnow() + datetime.timedelta(**time))}",
            color=discord.Color.green()
        )
                
        
        await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])
        await ctx.send(embed=embed)
        

async def setup(bot: Xeno):
    cog = Lime_And_Friends(bot)
    await bot.add_cog(cog)
