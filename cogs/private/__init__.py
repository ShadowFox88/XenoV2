"""
The private cog.

For commands and features available only in certain servers.
"""

from utils.bot import Xeno

from .lime_and_friends import Lime_And_Friends

__all__ = ("Lime_And_Friends",)


class Private(Lime_And_Friends, name="Meta"):
    """
    For information relating to discord or the bot.
    """


async def setup(bot: Xeno) -> None:
    """
    Load the Meta cog.
    """
    await bot.add_cog(Private(bot))
