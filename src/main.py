import os
import logging
logging.basicConfig(level=logging.DEBUG)

import discord
from discord.ext import commands

# setup bot
bot = commands.Bot(command_prefix="$")
guild_ids = [947170492769521675]


@bot.event
async def on_ready():
    """Send a message when the bot has successfully connected

    :return:
    """
    print(f"Logged in as {bot.user}")

# finish setup
bot.load_extension("cogs.drive_import")
bot.load_extension("cogs.meeting_information")
bot.load_extension("cogs.dm_role")
bot.run(os.environ["DISCORD_TOKEN"])
