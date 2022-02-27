import discord
from discord import SlashCommandGroup, Option, message
from discord.ext import commands
from discord.commands import slash_command


class DMRoleCog(commands.Cog):
    """Cogs that manage the direct messaging of everyone with a role"""

    def __init__(self, bot):
        super(DMRoleCog, self).__init__(self)
        self.bot = bot

    @slash_command(name="dm_all_with_role")
    async def dm_all_with_role(self, ctx: discord.Bot,
                               role: Option(discord.Role, name="Role", description="Select a role")):
        """DM everyone with a role

        :param ctx: Message calling the command
        :param role: Role selected
        :return:
        """
        if message.content == "dm":
            await message.channel.send("Dming user")
            dm = await message.author.create_dm()  # Creates a dm channel with the user
            await dm.send("What you want to send")  # Sends the user the message


def setup(bot: commands.Bot):
    """
    Set up the bot
    :param bot:
    :return:
    """
    bot.add_cog(DMRoleCog(bot))
