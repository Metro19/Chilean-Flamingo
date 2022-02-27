import time

import discord
import src.drive as drive
from discord.ext import commands
from discord.commands import slash_command
from src.main import guild_ids


class drive_import_cog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @slash_command(guild_ids=guild_ids, name="save_channel")
    async def save_channel(self, ctx: discord.Message):
        """Save a whole channel to a Google Docs document

        :param ctx:
        :return:
        """
        str_thing = ""
        messages = await ctx.channel.history(limit=500).flatten()
        bold_list = []
        ital_list = []

        for message in messages[::-1]:
            if not message.is_system() and not message.author.bot:
                inex = len(str_thing)
                str_thing += message.author.display_name
                bold_list.append((inex, len(str_thing)+1))
                index2 = len(str_thing)+1
                str_thing += " (" + time.strftime(format("%m/%d/%Y")) + ") " + \
                             message.created_at.strftime("%H:%M:%S")
                ital_list.append((index2, len(str_thing)))
                str_thing += " - "
                str_thing += message.content + "\n"

        drive.input_doc(str_thing, ctx.channel.name, bold_list, ital_list)
        await ctx.respond("Successfully Saved!")


def setup(bot: commands.Bot):
    bot.add_cog(drive_import_cog(bot))


