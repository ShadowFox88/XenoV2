from datetime import datetime

from discord.ext import tasks
from utils import XenoCog


class Tasks(XenoCog):
    """
    For tasks and events relating to the internal workings of the bot.
    """

    async def cog_unload(self) -> None:
        """
        Cancel the tasks when the cog is unloaded.
        """
        self.update_blacklist.cancel()

    @tasks.loop(hours=2.0)
    async def update_blacklist(self) -> None:
        """
        Update the blacklist every 2 hours.
        """
        self.bot.logger.info("Updating blacklist...")

        await self.bot.prisma.blacklist.delete_many(
            where={"expires": {"lt": datetime.datetime.now(tz=datetime.UTC)}}
        )

        self.bot.blacklisted.clear()
        self.bot.blacklisted = await self.bot.prisma.blacklist.find_many()

        self.bot.logger.info("Blacklist updated.")

    @update_blacklist.before_loop
    async def before(self) -> None:
        """
        Wait for the bot to be ready before starting the task.
        """
        await self.bot.wait_until_ready()
