from discord.ext import commands

from utils.bot import Xeno

class Music(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot



async def setup(bot: Xeno):
    cog = Music(bot)
    await bot.add_cog(cog)