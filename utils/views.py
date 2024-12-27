from __future__ import annotations

from typing import TYPE_CHECKING, Self

import discord

if TYPE_CHECKING:
    from utils.bot import Xeno


class DeleteView(discord.ui.View):
    """
    A view that allows the author of a message to delete it.
    """

    def __init__(self, author: discord.Member | discord.User) -> None:
        """
        Initialize the view.
        """
        super().__init__(timeout=None)
        self.author = author

    async def on_timeout(self) -> None:
        """
        Remove the view after the timeout.
        """
        await self.message.edit(view=None)

    @discord.ui.button(
        emoji="\U0001f5d1",
        label="Delete",
        style=discord.ButtonStyle.danger,
        custom_id="delete",
    )
    async def delete(
        self, interaction: discord.Interaction, _: discord.ui.Button[Self]
    ) -> None | discord.Interaction:
        """
        Delete the message.
        """
        if not interaction.message:
            return None
        if interaction.user.id in (self.author.id, 606648465065246750):
            self.stop()
            return interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.author.name}, so you can't delete it!",
            ephemeral=True,
        )
        return None


class SupportView(discord.ui.View):
    """
    A view that allows anyone to join the support server.
    """

    def __init__(self, support_server: str) -> None:
        """
        Initialize the view.
        """
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(
                label="Support", url=f"discord://-/invite/{support_server}"
            )
        )


class ConfirmView(discord.ui.View):
    """
    A view that allows the author of a message to confirm something.
    """

    def __init__(
        self, author: discord.Member | discord.User, timeout: int | None = None
    ) -> None:
        """
        Initialize the view.
        """
        super().__init__(timeout=timeout)
        self.author = author
        self.value: bool | None = None

    async def on_timeout(self) -> None:
        """
        Remove the view after the timeout.
        """
        await self.message.edit(view=None)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(
        self, interaction: discord.Interaction, _: discord.ui.Button[Self]
    ) -> None | discord.Interaction:
        """
        Process the user's confirmation.
        """
        if not interaction.message:
            return
        if interaction.user.id in (self.author.id, 606648465065246750):
            self.value = True
            self.stop()
            return
        await interaction.response.send_message(
            f"This command was ran by {self.author.name}, so you can't respond to it!",
            ephemeral=True,
        )

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(
        self, interaction: discord.Interaction, _: discord.ui.Button[Self]
    ) -> None | discord.Interaction:
        """
        Process the user's denial.
        """
        if not interaction.message:
            return
        if interaction.user.id in (self.author.id, 606648465065246750):
            self.value = False
            self.stop()
            return
        await interaction.response.send_message(
            f"This command was ran by {self.author.name}, so you can't respond to it!",
            ephemeral=True,
        )


class DismissView(discord.ui.View):
    """
    A view that allows the developer of the bot to dismiss an error.
    """

    def __init__(
        self,
        error_id: int,
        author: discord.Member | discord.User,
        bot: Xeno,
        developer_message: discord.WebhookMessage | None,
    ) -> None:
        """
        Initialize the view.
        """
        super().__init__(timeout=None)
        self.author = author
        self.error_id = error_id
        self.bot = bot
        self.developer_message = developer_message

    async def on_timeout(self) -> None:
        """
        Remove the view after the timeout.
        """
        await self.message.edit(view=None)

    @discord.ui.button(label="Fixed/Ignored", style=discord.ButtonStyle.green)
    async def dismiss(
        self, interaction: discord.Interaction, _: discord.ui.Button[Self]
    ) -> None | discord.Interaction:
        """
        Dismiss the error.
        """
        if not interaction.message:
            return
        if interaction.user.id in self.bot.owner_ids:
            await self.bot.db.execute("DELETE FROM errors WHERE id = $1", self.error_id)
            await interaction.message.delete()
            await interaction.response.send_message(
                f"Error {self.error_id} has been dismissed!",
                ephemeral=True,
            )
            if self.developer_message is not None:
                await self.developer_message.delete()

            self.stop()
            return
        await interaction.response.send_message(
            f"This command was ran by {self.author.name}, so you can't respond to it!",
            ephemeral=True,
        )

    @discord.ui.button(
        label="Delete (Message)", style=discord.ButtonStyle.danger, custom_id="delete"
    )
    async def delete(
        self, interaction: discord.Interaction, _: discord.ui.Button[Self]
    ) -> None | discord.Interaction:
        """
        Delete the error message without dismissing it.
        """
        if not interaction.message:
            return None
        if interaction.user.id in self.bot.owner_ids:
            self.stop()
            return await interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.author.name}, so you can't delete it!",
            ephemeral=True,
        )
        return None
