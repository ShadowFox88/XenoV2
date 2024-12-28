from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from bot import Xeno

__all__ = ("XenoCog",)


class XenoCog(commands.Cog):
    """
    Xeno's Custom Cog Class.
    """

    bot: Xeno

    def __init__(self, bot: Xeno) -> None:
        """
        Initialize the base cog to automatically set the bot.
        """
        self.bot = bot
