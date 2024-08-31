from discord.ext import commands

from utils.bot import Xeno

class Logging(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
        
        
async def setup(bot: Xeno):
    cog = Logging(bot)
    await bot.add_cog(cog)