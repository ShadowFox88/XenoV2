import discord
from utils import views
from discord import PartialEmoji as get_emoji
from discord.ext import commands
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from utils.bot import Xeno  # noqa: F401


class XenoContext(commands.Context["Xeno"]):
    async def send(self, content: str | None = None, button: bool = False, no_reply: bool = True, **kwargs: Any):
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
        if no_reply:
            return await super().send(content, **kwargs)
        else:
            return await super().reply(content, **kwargs)
    
    async def confirm(self, message: str | None = None, *, embed: discord.Embed | None = None, confirm_messsage: str = 'Press "yes" to accept, or press "no" to deny',
            timeout: int = 60, delete_message_after: bool = False, remove_view_after: bool = True,
            no_reply: bool = False, ephemeral: bool = False, **kwargs: Any) -> bool | None:
        if delete_message_after and remove_view_after:
            raise ValueError("Cannot have both delete_message_after and remove_view_after keyword arguments.")
        if embed:
            embed.description = f"{embed.description}\n\n{confirm_messsage}" if embed.description else confirm_messsage
        elif message:
            message = f"{message}\n\n{confirm_messsage}"
        view = views.ConfirmView(self.author)
        msg = await self.send(content=message, embed=embed, no_reply=no_reply, ephemeral=ephemeral, view=view, **kwargs)
        await view.wait()
        if delete_message_after:
            await self.message.delete()
        if remove_view_after:
            await msg.edit(view=None)
        return view.value        
        

    class Emoji:
        x = get_emoji(name="AnimatedRedCross", id=789586505974022164)
        check = get_emoji(name="AntimatedGreenTick", id=789586504950874132)
        slash = get_emoji(name="greyTick", id=895688440690114560)

    emoji = Emoji()
