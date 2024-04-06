from discord.ext import commands
from utils.bot import Xeno
from utils.context import XenoContext
from utils.errors import BlacklistedError, MaintenanceError

class ErrorHandler(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx: XenoContext, error: commands.CommandError):
        ignoredErrors = (commands.CommandNotFound, commands.PartialEmojiConversionFailure)
        if isinstance(error, ignoredErrors):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You are on cooldown. Try this command again in {error.retry_after:.2f}s")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to run this command!")
        elif isinstance(error, BlacklistedError):
            await ctx.send("You (or this guild) have been blacklisted from using the bot. I may remove this, but it's not likely. You may also have an expiry date on your blacklist.")
        elif isinstance(error, MaintenanceError):
            await ctx.send("The bot is currently in maintenance mode, please wait.")
        
        
async def setup(bot: Xeno):
    cog = ErrorHandler(bot)
    await bot.add_cog(cog)