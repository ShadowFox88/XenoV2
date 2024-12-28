from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from prisma import Prisma
    from prisma.models import Entites


class DatabaseOperations:
    """
    Class for common database operations.
    """

    def __init__(self, prisma: Prisma) -> None:
        """
        Initialize the class with the prisma instance.
        """
        self.prisma = prisma

    async def create_guild(self, guild_id: int) -> None:
        """
        Create a guild in the database.
        """
        await self.prisma.entities.create(data={"ID": guild_id, "type": "GUILD"})

    async def create_user(self, user_id: int) -> None:
        """
        Create a user in the database.
        """
        await self.prisma.entities.create(data={"ID": user_id, "type": "USER"})

    async def delete_user(self, user_id: int) -> None:
        """
        Delete a user from the database.
        """
        await self.prisma.entities.delete(where={"ID": user_id})

    async def delete_guild(self, guild_id: int) -> None:
        """
        Delete a guild from the database.
        """
        await self.prisma.entities.delete(where={"ID": guild_id})

    async def get_user(self, user_id: int) -> Entites:
        """
        Get a user from the database.
        """
        return await self.prisma.entities.find_first(where={"ID": user_id})

    async def get_guild(self, guild_id: int) -> Entites:
        """
        Get a guild from the database.
        """
        return await self.prisma.entities.find_first(where={"ID": guild_id})
