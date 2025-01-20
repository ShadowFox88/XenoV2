from __future__ import annotations

import traceback

import discord
import mystbin
from discord.ext import commands

from utils import BlacklistedError, MaintenanceError, XenoCog, XenoContext

user_errors: dict[type[Exception], tuple[str, str]] = {
    BlacklistedError: (
        "You (or this guild) have been blacklisted from using the bot.",
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
        "You do not have permission to run this command.",
        "user_bad_permissions",
    ),
    commands.TooManyArguments: (
        "You have provided too many arguments for this command.",
        "too_many_arguments",
    ),
    commands.BadArgument: (
        "You have provided an invalid argument for this command.",
        "bad_argument",
    ),
    commands.BotMissingPermissions: (
        "I am missing the necessary permissions to run this command.",
        "missing_permissions",
    ),
    commands.MissingRequiredArgument: (
        "You are missing a required argument for this command.",
        "missing_argument",
    ),
    commands.MissingFlagArgument: (
        "You are missing a flag argument for this command.",
        "missing_flag_argument",
    ),
    commands.NotOwner: (
        "You must be the owner of the bot to run this command.",
        "not_owner",
    ),
    commands.MemberNotFound: (
        "I couldn't find that member.",
        "member_not_found",
    ),
    commands.errors.DisabledCommand: (
        "This command is currently disabled.",
        "command_disabled",
    ),
}

ignored_errors: tuple[type[discord.DiscordException], ...] = (
    commands.CommandNotFound,
    commands.PartialEmojiConversionFailure,
)


def _generate_error_embed(
    error: Exception, ctx: XenoContext, error_id: int
) -> discord.Embed:
    """
    Generate an error embed for the error handler to use.
    """
    if ctx.bot.is_owner(ctx.author):
        embed = discord.Embed(
            colour=discord.Color.red(),
            title="An unexpected error occurred while running this command, my developers are aware.",  # noqa: E501
            description=f"```py\n{''.join(traceback.format_exception(error))}```",
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f"Error ID: {error_id}")
    else:
        embed = discord.Embed(
            colour=discord.Color.red(),
            description="An unexpected error occurred while running this command, my developers have been informed",  # noqa: E501
        )
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(
            text=f"If you wish to talk to my developers about this, the error ID is: {error_id}"  # noqa: E501
        )

    return embed


def _generate_developer_embed(
    error: Exception, ctx: XenoContext, error_id: int
) -> discord.Embed:
    """
    Generate an error embed to send to the developer.
    """
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

    return developer_embed


class ErrorHandler(XenoCog):
    """
    A cog that handles errors that occur during command execution.
    """

    async def _is_known_error(self, error: Exception) -> bool:
        """
        Check if the error is a known error.
        """
        return bool(
            await self.bot.prisma.errors.find_first(where={"errorName": str(error)})
        )

    async def _is_error_fixed(self, error: Exception) -> bool:
        """
        Check if the error is fixed.
        """
        found_error = await self.bot.prisma.errors.find_first(
            where={"errorName": str(error)}
        )
        return False if not found_error else found_error.fixed

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: XenoContext, error: commands.CommandError
    ) -> None | discord.Message:
        """
        Handle errors that occur during command execution.
        """
        if (ctx.command and ctx.command.has_error_handler()) or (
            ctx.cog and ctx.cog.has_error_handler()
        ):
            return None
        if type(error) in ignored_errors:
            return None
        if type(error) in user_errors:
            error_message = user_errors[type(error)][0]

            embed = discord.Embed(colour=discord.Color.red())
            embed.timestamp = embed.timestamp or discord.utils.utcnow()
            embed.add_field(
                name="An error occurred while running this command.",
                value=error_message.format(error),
            )

            await ctx.message.add_reaction(self.bot.emoji_list["animated_red_cross"])

            return await ctx.reply(embed=embed, delete_after=30)

        # ============================
        # Checks if the error is known
        # ============================

        if (
            await self._is_known_error(error)
            and not await self._is_error_fixed(error)
            and "dev raise" not in ctx.message.content
        ):
            embed = discord.Embed(
                colour=discord.Color.red(),
                description="An unexpected error occurred while running this command, my developers are already aware and are working to fix this.",  # noqa: E501
            )
            embed.timestamp = discord.utils.utcnow()
            return await ctx.reply(embed=embed)

        # ==================================
        # Runs if error is not handled above
        # ==================================

        webhook = discord.Webhook.from_url(
            self.bot.error_webhook, session=self.bot.session
        )

        message = await webhook.send(embed=discord.Embed(title="Temporary"), wait=True)

        if await self._is_known_error(error) and await self._is_error_fixed(error):
            await self.bot.prisma.errors.update_many(
                where={"errorName": str(error)},
                data={"fixed": False, "errorMessageID": message.id},
            )
            generated_error = await self.bot.prisma.errors.find_first(
                where={"errorName": str(error)}
            )  # the error was fixed but now isn't, so we need to get the error again
        else:
            paste = await self.bot.mystbin.create_paste(
                files=[
                    mystbin.File(
                        filename="error.py",
                        content="".join(traceback.format_exception(error)),
                    )
                ]
            )
            await self.bot.prisma.pastes.create(
                data={
                    "ID": paste.id,
                    "ownerID": self.bot.owner_ids[0],
                    "safety": paste.security_token if paste.security_token else "",
                }
            )
            generated_error = await self.bot.prisma.errors.create(
                data={
                    "command": ctx.message.content,
                    "userID": ctx.author.id,
                    "guildID": ctx.guild.id if ctx.guild else None,
                    "traceback": "".join(traceback.format_exception(error)),
                    "errorMessageID": message.id,
                    "errorName": str(error),
                    "errorPasteID": paste.id,
                }
            )

        if not generated_error:
            msg = "An error occurred while reporting the error."
            raise commands.CommandError(msg)

        error_id = generated_error.ID

        embed = _generate_error_embed(error, ctx, error_id)
        developer_embed = _generate_developer_embed(error, ctx, error_id)

        await message.edit(embed=developer_embed)

        self.bot.logger.error(
            "Unexpected Error",
            exc_info=error,
            extra={"tags": {"type": "unexpected", "error": type(error).__name__}},
        )

        await ctx.message.add_reaction(self.bot.emoji_list["animated_red_cross"])

        try:
            await ctx.reply(embed=embed)
        except discord.errors.HTTPException:
            await ctx.send(
                message="I couldn't find your original message, was it deleted?",
                embed=embed,
                delete_after=30,
            )
