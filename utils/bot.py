import datetime
import os
import re
from typing import Any, List

import asyncpg
import discord
from discord.ext import commands

from utils.context import XenoContext
import aiohttp
import logging


class Xeno(commands.AutoShardedBot):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(command_prefix=self.get_prefix, *args, **kwargs, case_insensitive=True)  # type: ignore
        self.emoji_list = {
            "animated_green_tick": "<a:AnimatedGreenTick:789586504950874132>",
            "animated_red_cross": "<a:AnimatedRedCross:789586505974022164>",
        }

        self.cooldown: commands.CooldownMapping[discord.Message] = (
            commands.CooldownMapping.from_cooldown(1, 1.5, commands.BucketType.member) # type: ignore
        )
        self.command_counter = 0
        self.launch_time = discord.utils.utcnow()
        self.maintenance: bool = False
        self.owner_ids: List[int] = [606648465065246750]  # type: ignore
        self.owner: discord.User | None = None
        self.blacklisted: List[int] = []
        self.support_server: str = ""
        self.error_webhook: str = os.environ["ERROR_WEBHOOK"]
        self.DEFAULT_EXTENSIONS = ["cogs.info", "cogs.tasks", "cogs.ErrorHandler"]
        
    async def start(self, token: str, *, reconnect: bool = True) -> None:
        discord.utils.setup_logging(handler=logging.FileHandler("bot.log"))
        self.logger: logging.Logger = logging.getLogger("discord")
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.token = token
        await super().start(token)

    async def get_prefix(self, message: discord.Message):
        return commands.when_mentioned_or(*["x-", "=="])(self, message)

    async def setup_hook(self):
        self.db: asyncpg.Pool[Any] | Any = await asyncpg.create_pool(
            host=os.environ["DATABASE_HOST"],
            user=os.environ["DATABASE_USER"],
            password=os.environ["DATABASE_PASSWORD"],
            database=os.environ["DATABASE"],
        )

        if not self.db:
            raise RuntimeError("Couldn't connect to database!")

        with open("schema.sql") as file:
            await self.db.execute(file.read())
            
            
        record = await self.db.fetch("SELECT id FROM blacklist WHERE blacklist_active = true")
        
        for i in record:
            self.blacklisted.append(i["id"])
        
        await self.load_extension("jishaku")

        for i in self.DEFAULT_EXTENSIONS:
            try:
                await self.load_extension(i)
            except Exception as e:
                print(f"Failed to load extension {i} with error {e}")
                
    def get_error_webhook(self):
        return discord.Webhook.from_url(self.error_webhook, session=self.session, bot_token=self.token)

    def format_print(self, text: str) -> str:
        format = str(datetime.datetime.now().strftime("%x | %X") + f" | {text}")
        return format

    def get_message_emojis(self, message: discord.Message) -> List[discord.PartialEmoji]:
        regex = re.findall("<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>", message.content)
        emojis: List[discord.PartialEmoji] = []
        for animated, name, id in regex:
            emojis.append(
                discord.PartialEmoji(animated=bool(animated), name=name, id=id)
            )
        return emojis

    async def close(self):
        await super().close()
        await self.db.close()

    async def get_context(self, message: discord.Message | discord.Interaction[discord.Client], *, cls: Any = XenoContext) -> Any:
        return await super().get_context(message, cls=cls)

    def is_blacklisted(self, ctx: XenoContext):
        if ctx.guild:
            return (ctx.guild.id in self.blacklisted) or (ctx.author.id in self.blacklisted)
        return ctx.author.id in self.blacklisted
        # return user_id in self.blacklisted
