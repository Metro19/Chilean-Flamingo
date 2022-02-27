import discord
from discord import SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command

from src.main import guild_ids


class dm_role_cog(commands.Cog):
    """Cogs that manage the direct messaging of everyone with a role"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @slash_command(name="dm_all_with_role", guild_ids=guild_ids)
    async def dm_all_with_role(self, ctx: discord.Message,
                               role: Option(discord.Role, name="role", description="Select a role"),
                               msg: Option(str, name="message", description="Message to send all users")):
        """DM everyone with a role

        :param msg:
        :param ctx: Message calling the command
        :param role: Role selected
        :return:
        """
        # looping through the members and messaging them
        count = 0
        for r in role.members:
            if not r.bot:
                count += 1
                await r.send(msg)
        await ctx.respond("Sent out " + str(count) + " messages")



def setup(bot: commands.Bot):
    """Set up the bot

    :param bot:
    :return:
    """
    bot.add_cog(dm_role_cog(bot))
