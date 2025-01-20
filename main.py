import os
from asyncio import run
from typing import Literal

import discord
from discord.ext import commands

from utils import BlacklistedError, MaintenanceError, Xeno, XenoContext

bot = Xeno(intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    """
    Log the bot's information when it is ready.
    """
    if bot.user is not None:
        bot.logger.info("Logged in as %s (ID: %s)", bot.user, str(bot.user.id))

    owners = [bot.get_user(i) for i in bot.owner_ids]

    bot.owners = [i for i in owners if i is not None]


@bot.after_invoke
async def command_counter(ctx: XenoContext) -> None:
    """
    Increment the command counter after every command execution.
    """
    ctx.bot.command_counter += 1


@bot.check_once
async def blacklist(
    ctx: XenoContext,
) -> Literal[
    True
]:  # TODO(HypeShadowFox88): Check why this isn't working !!  # noqa: E501, FIX002, TD003
    """
    Check if a user is blacklisted from using commands.

    Prevent blacklisted users from executing any bot commands.
    """
    if not await bot.is_blacklisted(ctx) or ctx.author.id in bot.owner_ids:
        return True
    raise BlacklistedError


@bot.check_once
async def maintenance(ctx: XenoContext) -> Literal[True]:
    """
    Check if the bot is in maintenance mode.

    Prevent command execution when maintenance mode is active.
    """
    if not bot.maintenance or ctx.author.id in bot.owner_ids:
        return True
    raise MaintenanceError


@bot.check_once
async def cooldown(ctx: XenoContext) -> Literal[True]:
    """
    Check if the user has exceeded their command usage limit.

    Ensures users don't execute too many commands within a specific time frame.
    """
    if (
        ctx.author.id in bot.owner_ids
        or isinstance(ctx.author, discord.User)
        or ctx.channel.permissions_for(ctx.author).manage_messages
    ):
        return True

    bucket: commands.Cooldown | None = bot.cooldown.get_bucket(ctx.message)

    if not bucket:
        msg = "Cooldown Bucket does not exist!"
        raise RuntimeError(msg)

    retry_after: float | None = bucket.update_rate_limit()
    if retry_after:
        raise commands.CommandOnCooldown(
            bucket, retry_after, commands.BucketType.member
        )

    return True


@bot.listen()
async def on_message_edit(before: discord.Message, after: discord.Message) -> None:
    """
    Process commands when messages are edited.
    """
    if before.content == after.content:
        return
    await bot.process_commands(after)


async def main() -> None:
    """
    Start the bot with the given token.
    """
    async with bot:
        await bot.start(
            os.environ["TOKEN"]
            if os.getenv("TEST", "False").lower() not in ("true", "1", "t")
            else os.environ["TEST_TOKEN"]
        )


if __name__ == "__main__":
    run(main())
