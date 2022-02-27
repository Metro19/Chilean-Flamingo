import os
import logging
import discord
from discord.ext import commands
from src.config import GUILD_IDS, DISCORD_TOKEN

# setup logging
logging.basicConfig(level=logging.DEBUG)

# setup bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)
guild_ids = GUILD_IDS


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
bot.load_extension("cogs.sheets_import")
bot.run(DISCORD_TOKEN)
