import discord
from datetime import datetime, timezone, timedelta

from discord import SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command

from src.main import guild_ids
from src.db import create_meeting


class meeting_cogs(commands.Cog):
    """Cogs that manage the creation of a meeting"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        # create a slash command group
        meeting = SlashCommandGroup("meeting", "Manage and create meetings.", guild_ids=guild_ids)

        @meeting.command(guild_ids=guild_ids)
        async def new_meeting(ctx: discord.Message,
                              name: Option(str, name="name"),
                              month: Option(int, name="month", min_value=1, max_value=12, default=1),
                              day: Option(int, name="day", min_value=1, max_value=31, default=1),
                              year: Option(int, name="year", min_value=2000, max_value=9999, default=2022),
                              hour: Option(int, name="hour", min_value=1, max_value=12, default=1),
                              minute: Option(int, name="minute", min_value=0, max_value=59, default=0)):
            """Schedule a new meeting

            :param ctx: Context of the bot
            :param name: Name of the meeting
            :param month: MM of meeting
            :param day: DD of meeting
            :param year: YYYY of meeting
            :param hour: HH of meeting
            :param minute: MM of meeting
            :return:
            """
            # create datetime object
            time_obj = datetime(year, month, day, hour, minute, 0, 0, timezone(timedelta(0)))

            meeting_id = create_meeting(name, time_obj, str([ctx.author.id]))

            # create embed to send success message
            emb = discord.Embed(title="Meeting created!")
            emb.add_field(name="Meeting ID:", value=meeting_id)
            emb.add_field(name="Meeting Name:", value=name)
            emb.add_field(name="Time:", value=time_obj.strftime("%m/%d/%Y %H:%M:%S"))
            emb.set_footer(text="Meeting ID: " + meeting_id)

            await ctx.reply(embed=emb)


def setup(bot: commands.Bot):
    """Set up the bot

    :param bot:
    :return:
    """
    bot.add_cog(meeting_cogs(bot))
