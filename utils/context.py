from __future__ import annotations

from typing import TYPE_CHECKING, Any

import discord
from discord import PartialEmoji as GetEmoji
from discord.ext import commands

from utils import views

if TYPE_CHECKING:
    from utils.bot import Xeno  # noqa: F401


class XenoEmojis:
    """
    Some useful emojis for the bot.
    """

    x = GetEmoji(name="AnimatedRedCross", id=789586505974022164)
    check = GetEmoji(name="AntimatedGreenTick", id=789586504950874132)
    slash = GetEmoji(name="greyTick", id=895688440690114560)


class XenoContext(commands.Context["Xeno"]):
    """
    Xeno's Custom Context Class.

    Inherits from commands.Context.
    """

    async def send(
        self,
        content: str | None = None,
        *,
        button: bool = False,
        reply: bool = False,
        **kwargs: any,
    ) -> discord.Message:
        """
        Send a message with the given content and kwargs.
        """
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
        return await super().send(content, **kwargs)

    async def confirm(  # noqa: PLR0913
        self,
        message: str | None = None,
        *,
        embed: discord.Embed | None = None,
        confirm_message: str = 'Press "yes" to accept, or press "no" to deny',
        timeout: int = 60,
        delete_message_after: bool = False,
        remove_view_after: bool = True,
        no_reply: bool = True,
        ephemeral: bool = True,
        **kwargs: any,
    ) -> bool | None:
        """
        Send a confirmation message to the user.
        """
        if delete_message_after and remove_view_after:
            raise ValueError(  # noqa: TRY003
                "Cannot have both delete_message_after and remove_view_after keyword arguments."  # noqa: E501, EM101
            )
        if embed:
            embed.description = (
                f"{embed.description}\n\n{confirm_message}"
                if embed.description
                else confirm_message
            )
        elif message:
            message = f"{message}\n\n{confirm_message}"
        view = views.ConfirmView(self.author, timeout=timeout)
        msg = await self.send(
            content=message,
            embed=embed,
            reply=no_reply,
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

    emoji = XenoEmojis()

    @discord.utils.cached_property
    def reference(self) -> discord.Message | None:
        """
        Return the message that the context references.
        """
        if not self.message:
            return None
        if not self.message.reference:
            return None
        message = self.message.reference.resolved

        if not isinstance(message, discord.Message):
            return None
        return message
