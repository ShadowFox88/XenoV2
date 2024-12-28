"""
The meta cog.

For information relating to discord or the bot.
"""

from utils.bot import Xeno

from .info import Information

__all__ = ("Information",)


class Meta(Information, name="Meta"):
    """
    For information relating to discord or the bot.
    """


async def setup(bot: Xeno) -> None:
    """
    Load the Meta cog.
    """
    await bot.add_cog(Meta(bot))
