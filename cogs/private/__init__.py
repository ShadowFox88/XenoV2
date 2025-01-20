"""
The private cog.

For commands and features available only in certain servers.
"""

from utils.bot import Xeno

from .lime_and_friends import LimeAndFriends

__all__ = ("LimeAndFriends",)


class Private(LimeAndFriends, name="Private"):
    """
    For commands and features available only in certain servers.
    """


async def setup(bot: Xeno) -> None:
    """
    Load the Private cog.
    """
    await bot.add_cog(Private(bot))
