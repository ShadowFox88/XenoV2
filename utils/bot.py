from typing import Any, List
import discord
from discord.ext import commands
import asyncpg
import os
from utils.context import XenoContext
import re
import datetime

class Xeno(commands.AutoShardedBot):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(command_prefix=self.get_prefix, *args, **kwargs, case_insensitive=True) # type: ignore
        self.emoji_list = { 
            "animated_green_tick": "<a:AnimatedGreenTick:789586504950874132>",
            "animated_red_cross": "<a:AnimatedRedCross:789586505974022164>",
        }

        self.cooldown: commands.CooldownMapping[discord.Message] = commands.CooldownMapping.from_cooldown(1, 1.5, commands.BucketType.member)
        self.command_counter = 0
        self.launch_time = discord.utils.utcnow()
        self.maintenance = False
        self.owner_ids: List[int] = [606648465065246750] # type: ignore
        self.owner = self.get_user(self.owner_ids[0])
        self.blacklisted: List[int] = []
        self.support_server: str = ""

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

        await self.load_extension("jishaku")

    def format_print(self, text: str) -> str:
        format = str(datetime.datetime.now().strftime("%x | %X") + f" | {text}")
        return format

    def get_message_emojis(self, message: discord.Message) -> List[discord.PartialEmoji]:
        regex = re.findall(
            "<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>",
            message.content,
        )
        emojis: List[discord.PartialEmoji] = []
        for animated, name, id in regex:
            emojis.append(discord.PartialEmoji(animated=bool(animated), name=name, id=id))
        return emojis

    async def close(self):
        await super().close()
        await self.db.close()

    async def get_context(self, message: discord.Message | discord.Interaction[discord.Client], *, cls: Any = XenoContext) -> Any:
        # when you override this method, you pass your new Context
        # subclass to the super() method, which tells the bot to
        # use the new MyContext class
        # use the new MyContext class
        return await super().get_context(message, cls=cls)
    
    def is_blacklisted(self, ctx: XenoContext):
        if ctx.guild:
            return ctx.guild.id in self.blacklisted
        return ctx.author.id in self.blacklisted
        return False
        #return user_id in self.blacklisted

    
    
