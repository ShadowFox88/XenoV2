from discord.ext import commands
from utils.bot import Xeno


class ErrorHandler(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
