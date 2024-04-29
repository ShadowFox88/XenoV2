import datetime
import os
import time
from typing import List

import discord
import git
import psutil
from discord.ext import commands

from utils.bot import Xeno
from utils.context import XenoContext


class Information(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot
        self.process: psutil.Process = psutil.Process()

    def get_commits(self, count: int = 5) -> List[git.Commit]:
        repo = git.Repo(os.getcwd())
        return list(repo.iter_commits("master", max_count=count))

    def format_commit(self, commit: git.Commit) -> str:
        id = commit.hexsha[:7]
        message = (
            commit.message.split("\n")[0]
            if isinstance(commit.message, str)
            else "No message found."
        )  # to stop ugly red line
        time = datetime.datetime.fromtimestamp(commit.committed_date)

        time = round(time.timestamp())
        disc_dt = f"<t:{time}:R>"

        return f"[`{id}`](https://github.com/ShadowFox88/XenoV2/{commit.hexsha}) {message} ({disc_dt})"

    def strfdelta(self, tdelta: datetime.timedelta) -> str:
        years, remainder = divmod(
            tdelta.total_seconds(), 31536000
        )  # seconds in a year = 31536000.
        months, remainder = divmod(remainder, 2592000)  # seconds in a month = 2592000.
        weeks, remainder = divmod(remainder, 604800)  # seconds in a week = 604800.
        days, remainder = divmod(remainder, 86400)  # seconds in a day = 86400.
        hours, remainder = divmod(remainder, 3600)  # seconds in an hour = 3600.
        minutes, seconds = divmod(remainder, 60)
        intervals = [
            ("y", years),
            ("mo", months),
            ("w", weeks),
            ("d", days),
            ("h", hours),
            ("m", minutes),
            ("s", seconds),
        ]
        non_zero_intervals = [(name, value) for name, value in intervals if value != 0]
        if non_zero_intervals:
            result = ", ".join(
                f"{value:.0f}{name}" for name, value in non_zero_intervals
            )
            return result
        else:
            return "0s"

    @commands.command(alias=["stats", "botinfo"])
    async def info(self, ctx: XenoContext) -> None:
        """Tells you information about the bot itself."""

        commits = "\n".join(self.format_commit(c) for c in self.get_commits())
        memory = self.process.memory_info().rss / 1024**2
        total_memory = psutil.virtual_memory().total / 1024**3
        usage = (memory / 1024) / total_memory * 100
        uptime = self.strfdelta(discord.utils.utcnow() - self.bot.launch_time)

        embed = discord.Embed(description="Latest Commits:\n" + commits)
        embed.title = "Bot Information"
        embed.colour = discord.Color.teal()

        embed.set_author(name=self.bot.owner.name, icon_url=self.bot.owner.display_avatar.url)  # type: ignore

        embed.add_field(name="Guilds", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=len(self.bot.users))
        embed.add_field(name="Commands Run", value=self.bot.command_counter + 1)
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(
            name="Memory Usage (Process)",
            value=f"`{memory:.2f}` MiB / `{total_memory:.2f}` GiB (`{usage:.2f}%`)",
        )
        embed.add_field(
            name="CPU Usage",
            value=f"`{self.process.cpu_percent() / psutil.cpu_count():.2f}%`",
        )

        embed.set_footer(
            text="This section is dedicated to Runa.",
            icon_url="http://cds.vahin.dev/u/1FlYSp.png",
        )
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx: XenoContext) -> None:
        """Returns the latency of the bot."""

        discord_latency = round(self.bot.latency * 1000)

        start = time.perf_counter()
        message = await ctx.send("Pong!", reply=True)
        end = time.perf_counter()
        typing_latency = end - start

        start = time.perf_counter()
        await self.bot.db.execute("SELECT 1")
        end = time.perf_counter()
        db_latency = end - start

        embed = discord.Embed(title="Pong!", colour=discord.Color.green())
        embed.add_field(name="Discord Latency", value=f"`{discord_latency}ms`")
        embed.add_field(name="Typing Latency", value=f"`{typing_latency:.2f}ms`")
        embed.add_field(name="Database Latency", value=f"`{db_latency:.2f}ms`")

        await message.edit(embed=embed, content=None)


async def setup(bot: Xeno):
    cog = Information(bot)
    await bot.add_cog(cog)
