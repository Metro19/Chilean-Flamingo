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
                               role: Option(discord.Role, name="role", description="Select a role")):
        """DM everyone with a role

        :param ctx: Message calling the command
        :param role: Role selected
        :return:
        """
        await ctx.respond(role.name)


def setup(bot: commands.Bot):
    """Set up the bot

    :param bot:
    :return:
    """
    bot.add_cog(dm_role_cog(bot))
