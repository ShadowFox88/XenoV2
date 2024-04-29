from discord.ext import commands, tasks

from utils.bot import Xeno


class Tasks(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot

    async def cog_unload(self):
        self.update_blacklist.cancel()

    @tasks.loop(hours=2.0)
    async def update_blacklist(self):
        await self.bot.db.execute(
            "UPDATE blacklist SET blacklist_active = false WHERE blacklist_active = true AND blacklist_expiry < NOW()"
        )

    @update_blacklist.before_loop
    async def before(self):
        await self.bot.wait_until_ready()


async def setup(bot: Xeno):
    cog = Tasks(bot)
    await bot.add_cog(cog)
