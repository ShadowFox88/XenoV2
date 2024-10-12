from discord.ext import commands
import discord
from typing import Dict, Union

from utils.bot import Xeno
from utils.context import XenoContext

class Developer(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
    
    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)
    
    
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
                    except Exception:
                        pass
            else:
                try:
                    await self.bot.reload_extension(extension)
                    extensions[extension] = True
                except Exception as e:
                    extensions[extension] = e
                    
            embed = discord.Embed(title="Reloaded Extensions")
            embed.colour = discord.Colour.green() if all(extensions.values()) else discord.Colour.red()
            embed.add_field(name="Extensions", value="\n".join(f"{self.bot.emoji_list['animated_green_tick'] if v else self.bot.emoji_list['animated_red_cross']} {k}" for k, v in extensions.items()))
            
        await ctx.send(embed=embed, button=True)
        
        
    @developer_group.command(aliases=["purge"])
    async def purge_messages(self, ctx: XenoContext, arg1: Union[discord.Member, discord.User, discord.Role, int, bool] = None, arg2: Union[discord.Member, discord.User, int, bool] = None, arg3: Union[discord.Member, discord.User, int, bool] = None):
        
        target = None
        limit = 50
        manual_delete = False
        
        if isinstance(arg1, discord.Member) or isinstance(arg1, discord.User):
            target = arg1
        elif isinstance(arg2, discord.Member) or isinstance(arg2, discord.User):
            target = arg2
        elif isinstance(arg3, discord.Member) or isinstance(arg3, discord.User):
            target = arg3
            
        if isinstance(arg1, int):
            limit = arg1
        elif isinstance(arg2, int):
            limit = arg2
        elif isinstance(arg3, int):
            limit = arg3
        
        if isinstance(arg1, bool):
            manual_delete = arg1
        elif isinstance(arg2, bool):
            manual_delete = arg2
        elif isinstance(arg3, bool):
            manual_delete = arg3
            
        limit = limit + 1 # To include the command message
            
        embed = discord.Embed(title="Purged Messages")
        
        def check(message: discord.Message):
            if target is None:
                return message != ctx.message
            return message.author == target and message != ctx.message
        
        if not manual_delete:
            deleted_messages = await ctx.channel.purge(limit=limit, check=check)
            
            embed.title = "Purged Messages Successfully"
            embed.colour = discord.Colour.green()
            await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])
            
            message_statistics = {}
            
            for i in deleted_messages:
                if i.author not in message_statistics:
                    message_statistics[i.author] = 0
                message_statistics[i.author] += 1
                
            embed.add_field(name="Messages Deleted", value="\n".join([f"**{i}**: {j}" for i, j in message_statistics.items()]))
            
            return await ctx.reply(embed=embed)
        
        else:
            deleted_messages = []
        
            for i in ctx.channel.history(limit=limit):
                if i == ctx.message:
                    continue
                deleted_messages.append(i)
                await i.delete()
                
            embed.title = "Purged Messages Successfully"
            embed.colour = discord.Colour.green()
            await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])
                
            message_statistics = {}
                
            for i in deleted_messages:
                if i.author not in message_statistics:
                    message_statistics[i.author] = 0
                message_statistics[i.author] += 1
                    
            embed.add_field(name="Messages Deleted", value="\n".join([f"**{i}**: {j}" for i, j in message_statistics.items()]))
                
            return await ctx.reply(embed=embed)
    
    @developer_group.command(aliases=["e", "error"])
    async def error(self, ctx: XenoContext, id: int):
        ... # "SELECT * FROM errors WHERE id = $1"
    
async def setup(bot: Xeno):
    cog = Developer(bot)
    await bot.add_cog(cog)