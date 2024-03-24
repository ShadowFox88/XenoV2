from typing import *
import discord
from discord.ext import commands
import asyncpg
import os
from utils.context import XenoContext
import re
import datetime

class Xeno(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(self.get_prefix, *args, **kwargs)
        self.emoji_list = {
            "animated_green_tick": "<a:AnimatedGreenTick:789586504950874132>",
            "animated_red_cross": "<a:AnimatedRedCross:789586505974022164>",
        }
        self.command_counter = 0
        self.maintenance = False

    async def get_prefix(self, message):
        return ["x-", "==", "<@737738422067658762>"]

    async def setup_hook(self):
        self.db: asyncpg.Pool[Any] | Any = await asyncpg.create_pool(
            host=os.environ["DATABASE_HOST"],
            user=os.environ["DATABASE_USER"],
            password=os.environ["DATABASE_PASSWORD"],
            database=os.environ["DATABASE"],
        )

        if not self.db:
            raise RuntimeError("Couldn't connect to database!")

        await self.load_extension("jishaku")

    def format_print(self, text):
        format = str(datetime.now().strftime("%x | %X") + f" | {text}")
        return format

    def get_message_emojis(self, message: discord.Message):
        regex = re.findall(
            "<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>",
            message.content,
        )
        emojis: list = []
        for animated, name, id in emojis:
            emojis += discord.PartialEmoji(animated=bool(animated), name=name, id=id)
        return emojis

    async def close(self):
        await super().close()
        await self.db.close()

    async def get_context(self, message, *, cls=XenoContext):
        # when you override this method, you pass your new Context
        # subclass to the super() method, which tells the bot to
        # use the new MyContext class
        # use the new MyContext class
        return await super().get_context(message, cls=cls)