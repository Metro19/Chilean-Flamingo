import os

import discord
from discord.ext import commands

# setup bot
bot = commands.Bot(command_prefix="$")
guild_ids = []


@bot.event
async def on_ready():
    """Send a message when the bot has successfully connected

    :return:
    """
    print(f"Logged in as {bot.user}")

# finish setup
bot.load_extension("cogs.DriveImport")
bot.run(os.environ["DISCORD_TOKEN"])
