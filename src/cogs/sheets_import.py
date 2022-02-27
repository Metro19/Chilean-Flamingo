import discord
from discord import SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command

from src.main import guild_ids
import src.sheets as sheets


class sheets_import_cog(commands.Cog):
    """Cogs that manage the direct messaging of everyone with a role"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @slash_command(name="pull_discordids_from_sheets", guild_ids=guild_ids)
    async def pull_discordids_from_sheets(self, ctx):
        """Pull the discordIDs from sheets

                :param ctx:
                :return:
                """
        # pulling the column of the google sheet
        string_id_array = sheets.pull_column()

        # looping through the DiscordIds and printing them to the chat one by one
        for x in string_id_array:
            x = x.value.strip()
            name, discrim = x.split("#")
            await ctx.respond(discord.utils.get(self.bot.get_all_members(), name=name, discriminator=discrim))


def setup(bot: commands.Bot):
    """Set up the bot

    :param bot:
    :return:
    """
    bot.add_cog(sheets_import_cog(bot))
