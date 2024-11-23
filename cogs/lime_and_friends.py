from discord.ext import commands

from utils.bot import Xeno
from utils.context import XenoContext


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


async def setup(bot: Xeno):
    cog = Lime_And_Friends(bot)
    await bot.add_cog(cog)
