import discord
from utils import views
from discord import PartialEmoji as get_emoji
from discord.ext import commands
from typing import Any
from utils.bot import Xeno  # noqa: F401


class XenoContext(commands.Context["Xeno"]):
    async def send(self, content: str | None = None, button: bool = False, **kwargs: Any):
        for embed in kwargs.get("embeds", []):
            embed.colour = embed.colour or self.author.color
            embed.timestamp = embed.timestamp or discord.utils.utcnow()
            if not embed.footer.text:
                embed.set_footer(
                    text=f"Command ran by {self.author.display_name}",
                    icon_url=self.author.display_avatar.url,
                )

        if self.command and (self.command.root_parent or self.command).name == "jishaku":
            return await super().send(content, **kwargs)
        
        if button:
            kwargs["view"] = views.DeleteView(author = self.author)

        return await super().send(content, **kwargs)

    async def reply(self, *args: Any, **kwargs: Any):
        kwargs["mention_author"] = kwargs.get("mention_author", False)

        return await super().reply(*args, **kwargs)

    class Emoji:
        x = get_emoji(name="AnimatedRedCross", id=789586505974022164)
        check = get_emoji(name="AntimatedGreenTick", id=789586504950874132)
        slash = get_emoji(name="greyTick", id=895688440690114560)

    emoji = Emoji()
