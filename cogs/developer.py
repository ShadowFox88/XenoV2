from discord.ext import commands
import discord
from typing import Dict, Union

from utils.bot import Xeno
from utils.context import XenoContext

class Developer(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot

    @commands.is_owner()
    @commands.group(name="developer", aliases=["dev"], invoke_without_command=True)
    async def developer_group(self, ctx: XenoContext):
        await ctx.send_help(ctx.command)
        
    @commands.is_owner()
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
            embed.add_field(name="Extensions", value="\n".join(f"{self.bot.emoji_list['animated_green_tick'] if v else self.bot.emoji_list['animated_red_cross']} {k}" for k, v in extensions.items()))
            
        await ctx.send(embed=embed, button=True)
        
    @commands.is_owner()
    @developer_group.command()
    async def purge_messages(self, ctx: XenoContext, target: Union[discord.Member, discord.User, int], manual_delete: bool = False):
        
        embed = discord.Embed(title="Purged Messages")
        
        if not isinstance(target, int):
            target = await self.bot.fetch_user(target)
            
        if not manual_delete:
            if isinstance(target, int):
                deleted_messages = await ctx.channel.purge(limit=int, check=lambda: m != ctx.message)
            else:
                deleted_messages = await ctx.channel.purge(limit=50, check=lambda m: m.author == target and m != ctx.message)
            
            embed.title = "Purged Messages Successfully"
            embed.colour = discord.Colour.green()
            await ctx.message.add_reaction(self.bot.emoji_list["animated_green_tick"])
            
            message_statistics = {}
            
            for i in deleted_messages:
                if i.author.id not in message_statistics:
                    message_statistics[i.author] = 0
                message_statistics[i.author] += 1
                
            embed.add_field(name="Messages Deleted", value="\n".join([f"**{i}**: {j}" for i, j in message_statistics.items()]))
            
            return await ctx.reply(embed=embed)
            
            
        limit = 50 if not isinstance(target, int) else target
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
            if i.author.id not in message_statistics:
                message_statistics[i.author] = 0
            message_statistics[i.author] += 1
                
        embed.add_field(name="Messages Deleted", value="\n".join([f"**{i}**: {j}" for i, j in message_statistics.items()]))
            
        return await ctx.reply(embed=embed)
            
            
        


    
    
    
async def setup(bot: Xeno):
    cog = Developer(bot)
    await bot.add_cog(cog)