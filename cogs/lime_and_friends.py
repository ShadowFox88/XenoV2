from discord.ext import commands

from utils.bot import Xeno

class Lime_And_Friends(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot

    
    @commands.command()
    async def unpin(self, ctx, message_id: int | None) -> None:
        assert not (message_id and ctx.message.reference)
        assert ctx.guild.id == 1265697842475831397
        
        if message_id:
            message = await ctx.fetch_message(message_id)

        elif ctx.message.reference:
            message = await ctx.fetch_message(
                ctx.message.reference.message_id
            )

        else:
            await ctx.send('Please provide a message to unpin')
            return
        
        assert message.pinned
        await message.unpin()

    @commands.command()
    async def pin(self, ctx, message_id: int | None) -> None:
        assert not (message_id and ctx.message.reference)
        assert ctx.guild.id == 1265697842475831397
        if message_id:
            message = await ctx.fetch_message(message_id)

        elif ctx.message.reference:
            message = await ctx.fetch_message(
                ctx.message.reference.message_id
            )

        else:
            await ctx.send('Please provide a message to pin')
            return
        
        await message.pin()


async def setup(bot: Xeno):
    cog = Lime_And_Friends(bot)
    await bot.add_cog(cog)