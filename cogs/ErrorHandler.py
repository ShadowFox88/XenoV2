from discord.ext import commands
from utils.bot import Xeno
from utils.context import XenoContext
from utils.errors import BlacklistedError, MaintenanceError

errors: dict[type[Exception], str] = {
    BlacklistedError: "You (or this guild) have been blacklisted from using the bot. I may remove this, but it's not likely. You may also have an expiry date on your blacklist.",
    MaintenanceError: "The bot is currently in maintenance mode, please wait.",
    commands.CommandOnCooldown: "You are on cooldown. Try this command again in {error.retry_after:.2f}s",
    commands.CheckFailure: "You do not have permission to run this command!"
}

class ErrorHandler(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx: XenoContext, error: commands.CommandError):
        ignoredErrors = (commands.CommandNotFound, commands.PartialEmojiConversionFailure)
        if isinstance(error, ignoredErrors):
            return
        if isinstance(error, tuple(errors.keys())):
            return await ctx.send(errors[type(error)])
        
        
async def setup(bot: Xeno):
    cog = ErrorHandler(bot)
    await bot.add_cog(cog)