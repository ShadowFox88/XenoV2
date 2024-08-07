from typing import TYPE_CHECKING, Any

import discord
from discord import PartialEmoji as get_emoji
from discord.ext import commands

from utils import views

if TYPE_CHECKING:
    from utils.bot import Xeno  # noqa: F401


class XenoContext(commands.Context["Xeno"]):
    async def send(
        self,
        content: str | None = None,
        button: bool = False,
        reply: bool = False,
        **kwargs: Any,                                                                  
    ):
        embeds = kwargs.get("embeds", [])
        for embed in embeds:
            embed.colour = embed.colour or self.author.color
            embed.timestamp = embed.timestamp or discord.utils.utcnow()
            if not embed.footer.text:
                embed.set_footer(
                    text=f"Command ran by {self.author.display_name}",
                    icon_url=self.author.display_avatar.url,
                )
        embed: discord.Embed | Any = kwargs.get("embed")
        if embed:
            embed.colour = embed.colour or self.author.color
            embed.timestamp = embed.timestamp or discord.utils.utcnow()
            if not embed.footer.text:
                embed.set_footer(
                    text=f"Command ran by {self.author.display_name}",
                    icon_url=self.author.display_avatar.url,
                )

        if (
            self.command
            and (self.command.root_parent or self.command).name == "jishaku"
        ):
            return await super().send(content, **kwargs)

        if button:
            kwargs["view"] = views.DeleteView(author=self.author)
        if reply:
            return await super().reply(content, **kwargs)
        else:
            return await super().send(content, **kwargs)

    async def confirm(
        self,
        message: str | None = None,
        *,
        embed: discord.Embed | None = None,
        confirm_message: str = 'Press "yes" to accept, or press "no" to deny',
        timeout: int = 60,
        delete_message_after: bool = False,
        remove_view_after: bool = True,
        no_reply: bool = False,
        ephemeral: bool = False,
        **kwargs: Any,
    ) -> bool | None:
        if delete_message_after and remove_view_after:
            raise ValueError(
                "Cannot have both delete_message_after and remove_view_after keyword arguments."
            )
        if embed:
            embed.description = (
                f"{embed.description}\n\n{confirm_message}"
                if embed.description
                else confirm_message
            )
        elif message:
            message = f"{message}\n\n{confirm_message}"
        view = views.ConfirmView(self.author)
        msg = await self.send(
            content=message,
            embed=embed,
            no_reply=no_reply,
            ephemeral=ephemeral,
            view=view,
            **kwargs,
        )
        await view.wait()
        if delete_message_after:
            await msg.delete()
        if remove_view_after:
            await msg.edit(view=None)
        return view.value

    class Emoji:
        x = get_emoji(name="AnimatedRedCross", id=789586505974022164)
        check = get_emoji(name="AntimatedGreenTick", id=789586504950874132)
        slash = get_emoji(name="greyTick", id=895688440690114560)

    emoji = Emoji()
