import discord
from datetime import datetime, timezone, timedelta

from discord import SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command

from src.main import guild_ids
from src.db import meeting
import src.db as db





# initial vars
channels = {}
meetings: list[meeting] = []


def create_meeting_embed(message: str, mtg: meeting) -> discord.Embed:
    """Create a meeting embed for after a meeting operation

    :param message: Message to accompany embed
    :param mtg: Meeting object modified
    :return: Embed message with meeting information
    """

    # create the embed
    emb = discord.Embed(title="Meeting created!")
    emb.add_field(name="Meeting ID:", value=mtg.id, inline=False)
    emb.add_field(name="Meeting Name:", value=mtg.name, inline=False)
    emb.add_field(name="Time:", value=mtg.time.strftime("%m/%d/%Y %H:%M:%S"), inline=False)
    emb.set_footer(text="Meeting ID: " + mtg.id)

    return emb


class meeting_cogs(commands.Cog):
    """Cogs that manage the creation of a meeting"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    # create a slash command group
    meeting = SlashCommandGroup("meeting", "Manage and create meetings.", guild_ids=guild_ids)

    @meeting.command(guild_ids=guild_ids, name="new_meeting")
    async def new_meeting(self, ctx,
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

        mtg = db.create_meeting(name, time_obj, [ctx.author.id])

        # create embed to send success message
        emb = create_meeting_embed("Meeting Created!", mtg)

        await ctx.respond(embed=emb)

    @meeting.command(guild_ids=guild_ids, name="change_time")
    async def change_time(self, ctx,
                          id: Option(str, name="meeting_id"),
                          month: Option(int, name="month", min_value=1, max_value=12, default=1),
                          day: Option(int, name="day", min_value=1, max_value=31, default=1),
                          year: Option(int, name="year", min_value=2000, max_value=9999, default=2022),
                          hour: Option(int, name="hour", min_value=1, max_value=12, default=1),
                          minute: Option(int, name="minute", min_value=0, max_value=59, default=0)):
        """Change the time of a meeting

        :param ctx: Context of the message
        :param id: Message id
        :param month: Month of meeting
        :param day: Day of meeting
        :param year: Year of meeting
        :param hour: Hour of meeting
        :param minute: Minute of meeting
        :return:
        """

        # create datetime object
        time_obj = datetime(year, month, day, hour, minute, 0, 0, timezone(timedelta(0)))

        # find meeting
        for meet in meetings:
            if meet.id == id:
                meet.time = time_obj

                # pass to db
                db.adjust_meeting(meet)

                ctx.respond(embed=create_meeting_embed("Time adjusted!", meet))

        ctx.respond("Meeting ID not found!")

    @meeting.command(guild_ids=guild_ids, name="view_meeting")
    async def view_meeting(self, ctx,
                           id: Option(str, name="meeting_id")):
        """View the information about a meeting

        :param ctx: Message context
        :param id: Message id
        :return:
        """

        # find meeting
        for meet in meetings:
            if meet.id == id:
                ctx.respond(embed=create_meeting_embed("Meeting:", meet))

        # meeting not found
        ctx.respond("Meeting ID not found!")

    @meeting.command(guild_ids=guild_ids, name="change_name")
    async def change_name(self, ctx,
                          id: Option(str, name="meeting_id"),
                          name: Option(str, name="name")):
        """Change the name on a meeting

        :param id: Meeting id
        :param ctx: Context of the message
        :param name: Name of the meeting
        :return:
        """

        # find meeting
        for meet in meetings:
            if meet.id == id:
                meet.name = name

                # pass to db
                db.adjust_meeting(meet)

                ctx.respond(embed=create_meeting_embed("Name adjusted!", meet))

        ctx.respond("Meeting ID not found!")





def setup(bot: commands.Bot):
    """Set up the bot

    :param bot:
    :return:
    """
    bot.add_cog(meeting_cogs(bot))
