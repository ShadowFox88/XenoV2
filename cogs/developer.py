from discord.ext import commands
import discord
from typing import Dict

from utils.bot import Xeno
from utils.context import XenoContext

class Developer(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot

    @commands.is_owner()
    @commands.group(name="developer", aliases=["dev"], invoke_without_command=True)
    async def developer_group(self, ctx: XenoContext):
        await ctx.send_help(ctx.command)
        
    @developer_group.command()
    async def reload(self, ctx: XenoContext, extension: str = "all"):
        if extension == "all":
            extensions: Dict[str, bool | None | Exception] = {i: None for i in self.bot.extensions}
        else:
            extensions = {extension: None}
        
        async with ctx.typing(): 
            if extension == "all":
                for ext in extensions:
                    try:
                        await self.bot.reload_extension(ext)
                        extensions[ext] = True
                    except:
                        pass
            else:
                try:
                    await self.bot.reload_extension(extension)
                    extensions[extension] = True
                except Exception as e:
                    extensions[extension] = e
                    
            embed = discord.Embed(title="Reloaded Extensions")
            embed.colour = discord.Colour.green() if all(extensions.values()) else discord.Colour.red()
            embed.add_field(name="Extensions", value="\n".join(f"{k}: {'<:AnimatedGreenTick:789586504950874132>' if v else '<:AnimatedRedCross:789586505974022164>'}" for k, v in extensions.items()))
            
        await ctx.send(embed=embed, button=True)
        
    
    
    
async def setup(bot: Xeno):
    cog = Developer(bot)
    await bot.add_cog(cog)