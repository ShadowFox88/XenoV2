from discord.ext import commands

from utils.bot import Xeno
from utils.context import XenoContext

class Developer(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot

    @commands.is_owner()
    @commands.group(name="developer", aliases=["dev"], invoke_without_command=True)
    async def developer_group(self, ctx: XenoContext):
        await ctx.send_help(ctx.command)
        
    @developer_group.command(name="load")
    async def reload(self, ctx: XenoContext, extension: str = "all"):
        await self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded {extension}")
    
    
    
async def setup(bot: Xeno):
    cog = Developer(bot)
    await bot.add_cog(cog)