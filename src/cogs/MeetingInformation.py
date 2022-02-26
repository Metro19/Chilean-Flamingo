import discord
from discord import SlashCommandGroup
from discord.ext import commands
from discord.commands import slash_command
from src.main import guild_ids
from src.db import create_meeting




class MeetingCogs(commands.Cog):
    """Cogs that manage the creation of a meeting"""
    def __init__(self, bot):
        super(MeetingCogs, self).__init__(self)
        self.bot = bot

        # create a slash command group
        meeting = SlashCommandGroup("Meeting", "Manage and create meetings.")


def setup(bot: commands.Bot):
    bot.add_cog(MeetingCogs(bot))
