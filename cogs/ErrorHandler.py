from discord.ext import commands
from utils.bot import Xeno
from utils.context import XenoContext
from typing import Dict
from utils.errors import BlacklistedError, MaintenanceError


errors: Dict[type[Exception], str] = {
    BlacklistedError: "You have been blacklisted from using the bot until {self.bot.blacklisted}",
    MaintenanceError: "The bot is currently in maintenance mode, please wait.",
    commands.CheckFailure: "You do not have permission to run this command!",
    commands.CommandOnCooldown: "You are on cooldown. Try this command again in {error.retry_after:.2f}s",
}

class ErrorHandler(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx: XenoContext, error: commands.CommandError):
        ignoredErrors = (commands.CommandNotFound, commands.PartialEmojiConversionFailure)
        if isinstance(error, ignoredErrors):
            return
        