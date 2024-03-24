import discord
from utils import views
from discord import PartialEmoji as get_emoji
from discord.ext import commands


class XenoContext(commands.Context):
    async def send(self, *args, button: bool = False, **kwargs):
        embed = kwargs.get("embed")
        if embed:
            if not embed.color:
                embed.color = discord.Color.random()
            if not embed.footer:
                embed.set_footer(
                    text=f"Command ran by {self.author.name}",
                    icon_url=self.author.display_avatar,
                )
            if not embed.timestamp:
                embed.timestamp = discord.utils.utcnow()

        if button:
            kwargs["view"] = views.DefaultView(self)

        return await super().send(*args, **kwargs)

    async def reply(self, *args, **kwargs):
        kwargs["mention_author"] = kwargs.get("mention_author", False)

        return await super().reply(*args, **kwargs)

    async def add_reaction(self, value):
        return await self.message.add_reaction(value)

    class Emoji:
        x = get_emoji(name="AnimatedRedCross", id="789586505974022164")
        check = get_emoji(name="AntimatedGreenTick", id="789586504950874132")
        slash = get_emoji(name="greyTick", id="895688440690114560")

    emoji = Emoji()
