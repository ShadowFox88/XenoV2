"""
The internal cog.

For tasks and events relating to the internal workings of the bot.
"""

from utils.bot import Xeno

from .developer import Developer
from .error_handler import ErrorHandler
from .logging import Logging
from .tasks import Tasks

__all__ = ("Developer", "ErrorHandler", "Logging", "Tasks")


class Internals(ErrorHandler, Logging, Tasks, Developer, name="Internals"):
    """
    For tasks and events relating to the internal workings of the bot.
    """


async def setup(bot: Xeno) -> None:
    """
    Load the Internals cog.
    """
    await bot.add_cog(Internals(bot))
