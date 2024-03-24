import discord
from discord.ext import commands
from jishaku.models import copy_context_with

async def reload_command(ctx):
        alt_ctx = await copy_context_with(ctx, author=ctx.message.author, content="developer reload")
        a = str((await ctx.bot.get_prefix(alt_ctx))[2])
        alt_ctx = await copy_context_with(ctx, author=ctx.message.author, content=a + "developer reload")
        if alt_ctx.command is None:
          if alt_ctx.invoked_with is None:
            return await ctx.send(f'This bot has been hard-configured to ignore this user.')
          return await ctx.send(f'Command "{alt_ctx.invoked_with}" is not found')

        return await alt_ctx.command.invoke(alt_ctx)

class DefaultView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        if not ctx.author.id in ctx.bot.owner_ids:
            self.remove_item(self.reload)

    @discord.ui.button(
        emoji="\U0001f5d1", label="Delete", style=discord.ButtonStyle.danger, custom_id="delete"
    )
    async def delete(self, interaction, button):
        if interaction.user.id == self.ctx.author.id or interaction.user.id == 606648465065246750:
            return await interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )

    @discord.ui.button(
        label="Reload", style=discord.ButtonStyle.success, custom_id="reload"
    )
    async def reload(self, interaction, button):
        if interaction.user.id == self.ctx.author.id or interaction.user.id == 606648465065246750:
            await reload_command(self.ctx)
            return await interaction.response.send_message(
                f"Reloaded cogs!", 
                ephemeral=True
            )
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't run this!",
            ephemeral=True,
        )

class ReloadView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(
        emoji="\U0001f5d1", label="Delete", style=discord.ButtonStyle.danger, custom_id="delete"
    )
    async def delete(self, interaction, button):
        if interaction.user.id == self.ctx.author.id:
            return await interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )

    @discord.ui.button(
        label="Reload", style=discord.ButtonStyle.success, custom_id="reload"
    )
    async def reload(self, interaction, button):
        if interaction.user.id == self.ctx.message.author.id:
            await reload_command(self.ctx)
            return await interaction.response.send_message(
                f"Reloaded cogs!", 
                ephemeral=True
            )
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't run this!",
            ephemeral=True,
        )

class JoinSupportView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.remove_item(self.delete_button)
        self.add_item(discord.ui.Button(label="Support", url=self.ctx.bot.support_server))
        self.add_item(self.delete_button)
    
    @discord.ui.button(
        emoji="\U0001f5d1", custom_id="delete_short", style=discord.ButtonStyle.danger
    )
    async def delete_button(self, interaction, button):
        if interaction.user.id == self.ctx.author.id:
            return await interaction.message.delete()
        await interaction.response.send_message(
            f"This command was ran by {self.ctx.author.name}, so you can't delete it!",
            ephemeral=True,
        )