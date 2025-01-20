from __future__ import annotations

import datetime
import logging
import os
import re
import sys
from multiprocessing import Queue
from typing import TYPE_CHECKING, Any

import aiohttp
import asyncpg
import discord
import logging_loki
import mystbin
import redis.asyncio as redis
from discord.ext import commands

from prisma import Prisma

from .context import XenoContext
from .prisma import DatabaseOperations

if TYPE_CHECKING:
    from prisma.models import Blacklist


class RemoveUnnecessaryNoise(logging.Filter):
    """
    Remove unnecessary noise from the logs.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter the logs.
        """
        return not (
            record.levelno == logging.WARNING and "referencing an unknown" in record.msg
        )


class Xeno(commands.AutoShardedBot):
    """
    Xeno's Custom Bot Class.

    Inherits from commands.AutoShardedBot
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """
        Initialize the bot with the necessary attributes, and overwritten methods.
        """
        super().__init__(
            *args,
            **kwargs,
            case_insensitive=True,
            strip_after_prefix=True,
            command_prefix=[],
        )
        self.emoji_list = {
            "animated_green_tick": "<a:AnimatedGreenTick:789586504950874132>",
            "animated_red_cross": "<a:AnimatedRedCross:789586505974022164>",
        }

        self.cooldown: commands.CooldownMapping[discord.Message] = (
            commands.CooldownMapping.from_cooldown(1, 1.5, commands.BucketType.member)
        )
        self.command_counter = 0
        self.launch_time = discord.utils.utcnow()
        self.maintenance: bool = False
        self.owner_ids: list[int] = [606648465065246750]
        self.owners: list[discord.User] = []
        self.blacklisted: dict[int, Blacklist] = {}
        self.support_server: str = ""
        self.error_webhook: str = os.environ["ERROR_WEBHOOK"]
        self.DEFAULT_EXTENSIONS: list[str] = [
            "cogs.meta",
            "cogs.internals",
            "cogs.private",
        ]
        self.testing = os.getenv("TEST", "False").lower() in ("true", "1", "t")

    def setup_logging(self) -> None:
        """
        Set up the logging for the bot.
        """
        application_name = "Xeno" if not self.testing else "Xeno-Testy"
        logging_loki.emitter.LokiEmitter.level_tag = "level"  # pyright: ignore[reportAttributeAccessIssue] # this works.
        handler_loki = logging_loki.LokiQueueHandler(
            Queue(-1),  # pyright: ignore[reportArgumentType] # BEFORE ANYONE SAYS ANYTHING THE DOCS SAY DO IT THIS WAY
            url=os.environ["LOKI_URL"],
            tags={"application": application_name},
            auth=(os.environ["LOKI_USERNAME"], os.environ["LOKI_PASSWORD"]),
            version="1",
        )
        discord_handler_loki = logging_loki.LokiQueueHandler(
            Queue(-1),  # pyright: ignore[reportArgumentType] # BEFORE ANYONE SAYS ANYTHING THE DOCS SAY DO IT THIS WAY
            url=os.environ["LOKI_URL"],
            tags={"application": application_name},
            auth=(os.environ["LOKI_USERNAME"], os.environ["LOKI_PASSWORD"]),
            version="1",
        )
        http_handler_loki = logging_loki.LokiQueueHandler(
            Queue(-1),  # pyright: ignore[reportArgumentType] # BEFORE ANYONE SAYS ANYTHING THE DOCS SAY DO IT THIS WAY
            url=os.environ["LOKI_URL"],
            tags={"application": application_name},
            auth=(os.environ["LOKI_USERNAME"], os.environ["LOKI_PASSWORD"]),
            version="1",
        )
        state_handler_loki = logging_loki.LokiQueueHandler(
            Queue(-1),  # pyright: ignore[reportArgumentType] # BEFORE ANYONE SAYS ANYTHING THE DOCS SAY DO IT THIS WAY
            url=os.environ["LOKI_URL"],
            tags={"application": application_name},
            auth=(os.environ["LOKI_USERNAME"], os.environ["LOKI_PASSWORD"]),
            version="1",
        )

        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )
        file_handler = logging.FileHandler("bot.log", encoding="utf-8", mode="a")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        stdout_handler = logging.StreamHandler(sys.stdout)

        discord_logger = logging.getLogger("discord")
        discord_logger.setLevel(logging.INFO)
        discord_logger.addHandler(discord_handler_loki)
        discord_logger.addHandler(file_handler)
        discord_logger.addHandler(stdout_handler)

        http_logger = logging.getLogger("discord.http")
        http_logger.setLevel(logging.WARNING)
        http_logger.addHandler(http_handler_loki)
        http_logger.addHandler(file_handler)
        http_logger.addHandler(stdout_handler)

        state_logger = logging.getLogger("discord.state")
        state_logger.setLevel(logging.WARNING)
        state_logger.addHandler(state_handler_loki)
        state_logger.addHandler(file_handler)
        state_logger.addHandler(stdout_handler)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler_loki)
        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)

        self.logger = logger

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        """
        Start the bot.
        """
        self.setup_logging()
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.log_handler = None
        self.token = token
        await super().start(token, reconnect=reconnect)

    async def close(self) -> None:
        """
        Handle shutting down the bot.
        """
        await self.session.close()
        await self.database.close()
        await self.redis.aclose()
        await self.redis_pool.aclose()
        await super().close()
        await self.prisma.disconnect()

    async def get_prefix(self, message: discord.Message) -> list[str]:
        """
        Return the prefix for each user.
        """
        prefixes = ["x-", "=="] if not self.testing else ["t;"]
        return commands.when_mentioned_or(*prefixes)(self, message)

    async def setup_hook(self) -> None:
        """
        Set up the bot.
        """
        self.database: asyncpg.Pool = await asyncpg.create_pool(
            host=os.environ["DATABASE_HOST"],
            user=os.environ["DATABASE_USER"],
            password=os.environ["DATABASE_PASSWORD"],
            database=os.environ["DATABASE"],
        )  # only for use with jsk sql
        # TODO(ShadowFox88): Subclass jiskaku to use prisma  # noqa: FIX002, TD003

        if not self.database:
            raise RuntimeError("Couldn't connect to database!")  # noqa: EM101, TRY003

        await self.load_extension("jishaku")

        for i in self.DEFAULT_EXTENSIONS:
            try:
                await self.load_extension(i)
            except Exception:  # noqa: PERF203
                self.logger.exception("Failed to load extension %s", i)

        self.prisma = Prisma()
        await self.prisma.connect()

        self.blacklisted = {
            i.entityID: i for i in await self.prisma.blacklist.find_many()
        }

        self.database_operations = DatabaseOperations(self.prisma)
        self.mystbin = mystbin.Client(
            session=self.session, root_url="https://paste.vahin.dev"
        )
        self.redis_pool = redis.ConnectionPool.from_url(
            f"redis://:{os.environ['REDIS_PASSWORD']}@XenoRedis:6379/0"
        )
        self.redis = redis.Redis(connection_pool=self.redis_pool)

    def get_error_webhook(self) -> discord.Webhook:
        """
        Return the error webhook.
        """
        return discord.Webhook.from_url(
            self.error_webhook, session=self.session, bot_token=self.token
        )

    def format_print(self, text: str) -> str:
        """
        Format the text to be printed.
        """
        return str(
            datetime.datetime.now(tz=datetime.timezone.utc).strftime("%x | %X")
            + f" | {text}"
        )

    def get_message_emojis(
        self, message: discord.Message
    ) -> list[discord.PartialEmoji]:
        """
        Get the emojis from a message.
        """
        regex = re.findall(
            "<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>",
            message.content,
        )
        emojis: list[discord.PartialEmoji] = []
        for animated, name, emoji_id in regex:
            emojis.append(
                discord.PartialEmoji(animated=bool(animated), name=name, id=emoji_id)
            )
        return emojis

    async def get_context(
        self,
        message: discord.Message | discord.Interaction[discord.Client],
        *,
        cls: type[XenoContext] = XenoContext,
    ) -> XenoContext:
        """
        Get the context of the message.
        """
        return await super().get_context(message, cls=cls)

    async def is_blacklisted(self, ctx: XenoContext) -> bool:
        """
        Check if the user is blacklisted and delete if the blacklist has expired.
        """
        guild_blacklisted = user_blacklisted = None

        if ctx.guild:
            guild_blacklisted: Blacklist | None = self.blacklisted.get(ctx.guild.id)

        user_blacklisted: Blacklist | None = self.blacklisted.get(ctx.author.id)

        if (
            user_blacklisted
            and user_blacklisted.blacklistedUntil
            and user_blacklisted.blacklistedUntil < discord.utils.utcnow()
        ):
            await self.prisma.blacklist.delete(where={"entityID": ctx.author.id})
            self.blacklisted.pop(user_blacklisted.entityID)
            user_blacklisted = None

        if (
            guild_blacklisted
            and guild_blacklisted.blacklistedUntil
            and guild_blacklisted.blacklistedUntil < discord.utils.utcnow()
            and ctx.guild
        ):
            await self.prisma.blacklist.delete(where={"entityID": ctx.guild.id})
            self.blacklisted.pop(guild_blacklisted.entityID)
            guild_blacklisted = None

        return bool(guild_blacklisted or user_blacklisted)
