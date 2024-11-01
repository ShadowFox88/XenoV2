import traceback
from typing import Tuple

import discord
from discord.ext import commands

from utils.bot import Xeno
from utils.context import XenoContext
from utils.errors import BlacklistedError, MaintenanceError

user_errors: dict[type[Exception], Tuple[str, str]] = {
    BlacklistedError: (
        "You (or this guild) have been blacklisted from using the bot. I may remove this, but it's not likely. You may also have an expiry date on your blacklist.",
        "blacklisted",
    ),
    MaintenanceError: (
        "The bot is currently in maintenance mode, please wait.",
        "in_maintenance",
    ),
    commands.CommandOnCooldown: (
        "You are on cooldown. Try this command again in {error.retry_after:.2f}s",
        "on_cooldown",
    ),
    commands.CheckFailure: (
        "You do not have permission to run this command!",
        "user_bad_permissions",
    ),
    commands.TooManyArguments: (
        "You have provided too many arguments for this command!",
        "too_many_arguments",
    ),
    commands.BadArgument: (
        "You have provided an invalid argument for this command!",
        "bad_argument",
    ),
    commands.BotMissingPermissions: (
        "I am missing the necessary permissions to run this command!",
        "missing_permissions",
    ),
    commands.MissingRequiredArgument: (
        "You are missing a required argument for this command!",
        "missing_argument",
    ),
}

ignoredErrors: Tuple[Exception] = (
    commands.CommandNotFound,
    commands.PartialEmojiConversionFailure,
)


class ErrorHandler(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: XenoContext, error: commands.CommandError):
        if isinstance(error, ignoredErrors):
            return
        if isinstance(error, tuple(user_errors.keys())):
            error_message = user_errors[type(error)][0]
            label = user_errors[type(error)][1]

            embed = discord.Embed(colour=discord.Color.red())
            embed.timestamp = embed.timestamp or discord.utils.utcnow()
            embed.add_field(
                name="An error occurred while running this command.",
                value=error_message.format(error),
            )

            emoji: str = self.bot.emoji_list["animated_red_cross"]
            await ctx.message.add_reaction(emoji)

            await ctx.send(embed=embed, reply=True, delete_after=30)

            self.bot.logger.exception(error, extra={"error": label})
            return

        if ctx.guild is not None:
            guild_id = ctx.guild.id
        else:
            guild_id = None
            
        webhook = discord.Webhook.from_url(
            self.bot.error_webhook, session=self.bot.session
        )
            
        message = await webhook.send(embed=discord.Embed(title="Temporary"), wait=True)

        await self.bot.db.execute(
            "INSERT INTO errors (command, user_id, guild_id, traceback, developer_message_id) VALUES ($1, $2, $3, $4, $5)",
            ctx.message.content,
            ctx.author.id,
            guild_id,
            "".join(traceback.format_exception(error)),
            message.id
        )
        
        data = await self.bot.db.fetch("SELECT id FROM errors ORDER BY id DESC LIMIT 1")
        error_id = data[0]["id"]

        embed = discord.Embed(
            colour=discord.Color.red(),
            title="An unexpected error occurred while running this command, my developers are aware.",
            description=f"```py\n{''.join(traceback.format_exception(error))}```",
        )
        embed.timestamp = embed.timestamp or discord.utils.utcnow()
        embed.set_footer(
            text=f"Should you wish to talk to the developer about this error, refer to it by its ID: {error_id}"
        )

        emoji = self.bot.emoji_list["animated_red_cross"]
        await ctx.message.add_reaction(emoji)
        await ctx.send(embed=embed, reply=True, delete_after=30)

        developer_embed = discord.Embed(
            colour=discord.Color.red(), title=f"Error Report: {error_id}"
        )
        developer_embed.timestamp = developer_embed.timestamp or discord.utils.utcnow()

        developer_embed.add_field(
            name="Exception",
            value=f"```py\n{''.join(traceback.format_exception_only(error))}```",
        )

        additional_info = f"""Error ID: {error_id}
        Command: {ctx.message.content}
        User: {ctx.author.mention} ({ctx.author.id})
        Guild ID: {ctx.guild.id if ctx.guild else None}"""

        developer_embed.add_field(name="Additional Information", value=additional_info)
        
        await message.edit(embed=developer_embed)

        self.bot.logger.exception(error, extra={"error": "unexpected"})


async def setup(bot: Xeno):
    cog = ErrorHandler(bot)
    await bot.add_cog(cog)
