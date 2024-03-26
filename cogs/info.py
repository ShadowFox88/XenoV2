import discord
from typing import List
from discord.ext import commands
from utils.context import XenoContext
from utils.bot import Xeno
import git
import psutil
import os
import datetime

class Information(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
        self.process: psutil.Process = psutil.Process()
        
    def get_commits(self, count: int = 5) -> List[git.Commit]:
        repo = git.Repo(os.getcwd())
        return list(repo.iter_commits("master", max_count=count))
        
    def format_commit(self, commit: git.Commit) -> str:
        id = commit.hexsha[:7]
        message = commit.message.split('\n')[0] if isinstance(commit.message, str) else "No message found." # to stop ugly red line
        time = datetime.datetime.fromtimestamp(commit.committed_date)
        
        time = round(time.timestamp())
        disc_dt = f"<t:{time}:R>"
        
        return f"[`{id}`](https://github.com/ShadowFox88/XenoV2{commit.hexsha}) {message} ({disc_dt})"
        

    @commands.command(alias=['stats', 'botinfo'])
    async def info(self, ctx: XenoContext):
        """Tells you information about the bot itself."""
        
        commits = '\n'.join(self.format_commit(c) for c in self.get_commits())
        memory = self.process.memory_info().rss / 1024 ** 2
        total_memory = psutil.virtual_memory().total / 1024 ** 3
        usage = memory / (total_memory / 1024) * 100
        
        embed = discord.Embed(description='Latest Commits:\n' + commits)
        embed.title = 'Bot Information'
        embed.colour = discord.Color.teal()
        
        embed.set_author(name=self.bot.owner.name, icon_url=self.bot.owner.display_avatar.url) # type: ignore
        
        embed.add_field(name='Guilds', value=len(self.bot.guilds))
        embed.add_field(name='Users', value=len(self.bot.users))
        embed.add_field(name='Commands Run', value=self.bot.command_counter)
        embed.add_field(name='Uptime', value=self.bot.format_print(str(discord.utils.utcnow() - self.bot.launch_time)))
        embed.add_field(name='Process', value=f'`Memory: \n{memory:.2f}` MiB / `{total_memory:.2f}` GiB ({usage:.2f}%)\n `CPU`: \n{self.process.cpu_percent() / psutil.cpu_count():.2f}%')
        
        embed.set_footer(text="This section is dedicated to Runa.", icon_url='http://cds.vahin.dev/u/1FlYSp.png')
        embed.timestamp = discord.utils.utcnow()
        
        await ctx.send(embed=embed, no_reply=False)
        
        
async def setup(bot: Xeno):
    cog = Information(bot)
    await bot.add_cog(cog)


