import discord
from discord.ext import commands
from discord.commands import slash_command
from src.main import guild_ids


class DriveImportCommands(commands.Cog):
    def __init__(self, bot):
        super(DriveImportCommands, self).__init__(self)
        self.bot = bot

    @slash_command(guild_ids=guild_ids, name="Save Channel")
    async def save_channel(self, ctx: discord.Message):
        """Save a whole channel to a Google Docs document

        :param ctx:
        :return:
        """
        pass


def setup(bot: commands.Bot):
    bot.add_cog(DriveImportCommands(bot))
