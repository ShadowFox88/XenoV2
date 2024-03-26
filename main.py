import os
from asyncio import run
from typing import Literal

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.bot import Xeno
from utils.context import XenoContext
from utils.errors import BlacklistedError, MaintenanceError

import traceback
import sys

load_dotenv()

bot = Xeno(intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    bot.owner = bot.get_user(606648465065246750)
    if bot.user is not None:
        print(f"Logged in as {bot.user} ({bot.user.id})")
    print(f"Launched at {bot.launch_time}")

@bot.after_invoke
async def command_counter(ctx: XenoContext) -> None:
    ctx.bot.command_counter += 1


@bot.check_once
async def blacklist(ctx: XenoContext) -> Literal[True]:
    "A check that gets applied before commands to make sure a blacklisted user can't use commands."
    if not bot.is_blacklisted(ctx) or ctx.author.id in bot.owner_ids:
        return True
    raise BlacklistedError


@bot.check_once
async def maintenance(ctx: XenoContext) -> Literal[True]:
    "A check that gets applied before commands to make sure that the bot isn't in maintenance."
    if not bot.maintenance or ctx.author.id in bot.owner_ids:
        return True
    raise MaintenanceError


@bot.check_once
async def cooldown(ctx: XenoContext) -> Literal[True]:
    "A check that gets applied before commands to make sure a user hasn't ran too many commands in X amount of time."
    if (
        ctx.author.id in bot.owner_ids
        or isinstance(ctx.author, discord.User)
        or ctx.channel.permissions_for(ctx.author).manage_messages
    ):
        return True

    bucket: commands.Cooldown | None = bot.cooldown.get_bucket(ctx.message)

    if not bucket:
        raise RuntimeError("Cooldown Bucket does not exist!")

    retry_after: float | None = bucket.update_rate_limit()
    if retry_after:
        raise commands.CommandOnCooldown(bucket, retry_after, commands.BucketType.member)

    return True


async def on_command_error(ctx: XenoContext, error: Exception):
    # Handle your errors here
    # All unhandled errors will print their original traceback
    print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
    await ctx.send(f"{error}, {type(error)}, {error.__traceback__}")
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

async def main() -> None:
    async with bot:
        await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    run(main())