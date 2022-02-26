import discord
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

        for message in messages[::-1]:
            print(message)
            str_thing += message.author.display_name + ": "
            str_thing += message.content + "\n"

        await ctx.send(str_thing)


def setup(bot: commands.Bot):
    bot.add_cog(drive_import_cog(bot))


