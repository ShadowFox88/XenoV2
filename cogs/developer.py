from discord.ext import commands

from utils.bot import Xeno

class Developer(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot


async def setup(bot: Xeno):
    cog = Developer(bot)
    await bot.add_cog(cog)