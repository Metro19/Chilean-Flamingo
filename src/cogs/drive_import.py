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
        # empty string that will be the files to print
        str_message = ""
        # getting the entire channel dialog
        messages = await ctx.channel.history(limit=500).flatten()
        bold_list = []
        ital_list = []

        # looping through the messages in reverse to print in correct order
        for message in messages[::-1]:
            # only adding if it was a message from a user.
            # messages from bots and the system are skipped

            if not message.is_system() and not message.author.bot:
                inex = len(str_message)
                str_message += message.author.display_name
                bold_list.append((inex, len(str_message) + 1))
                index2 = len(str_message) + 1
                str_message += " (" + time.strftime(format("%m/%d/%Y")) + ") " + \
                               message.created_at.strftime("%H:%M:%S")
                ital_list.append((index2, len(str_message) + 1))
                str_message += " - "

                for attachment in message.attachments:
                    str_message += attachment.proxy_url
                str_message += message.content + "\n"

        # calling the creation of the doc
        drive.input_doc(str_message, ctx.channel.name, bold_list, ital_list)

        # code has run successfully
        print("Hello")
        await ctx.respond("Successfully Saved!")


def setup(bot: commands.Bot):
    bot.add_cog(drive_import_cog(bot))
