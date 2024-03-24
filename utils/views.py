import discord
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.context import XenoContext

class DeleteView(discord.ui.View):
    def __init__(self, ctx: XenoContext):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(
        emoji="\U0001f5d1", label="Delete", style=discord.ButtonStyle.danger, custom_id="delete"
    )
    async def delete(self, interaction: discord.Interaction, _) -> None | discord.Interaction:
        if not interaction.message:
            return
        if interaction.user.id == self.ctx.author.id or interaction.user.id == 606648465065246750:
            return await interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )

class SupportView(discord.ui.View):
    def __init__(self, support_server: str) -> None:
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Support", url=f"discord://-/invite/{support_server}"))
        
class ConfirmView(discord.ui.View):
    def __init__(self, ctx: XenoContext):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.value: bool | None = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, _) -> None | discord.Interaction:
        if not interaction.message:
            return
        if interaction.user.id == self.ctx.author.id or interaction.user.id == 606648465065246750:
            self.value = True
            self.stop()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )
      
    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, _) -> None | discord.Interaction:
        if not interaction.message:
            return
        if interaction.user.id == self.ctx.author.id or interaction.user.id == 606648465065246750:
            self.value = True
            self.stop()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )  