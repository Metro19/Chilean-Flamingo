import asyncio
import operator

import discord
from datetime import datetime, timezone, timedelta

from discord import SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command

from src.main import guild_ids
from src.db import meeting, channel
import src.db as db


def meeting_sort(mtgs: list[meeting]) -> list[meeting]:
    """Organize meetings by start time

    :param mtgs: List of unorganized meetings
    :return: Organized list of meetings
    """
    return sorted(mtgs, key=operator.attrgetter("time"), reverse=True)


def create_meeting_embed(message: str, mtg: meeting) -> discord.Embed:
    """Create a meeting embed for after a meeting operation

    :param message: Message to accompany embed
    :param mtg: Meeting object modified
    :return: Embed message with meeting information
    """

    # create the embed
    emb = discord.Embed(title=message)
    emb.add_field(name="Meeting ID:", value=mtg.id, inline=False)
    emb.add_field(name="Meeting Name:", value=mtg.name, inline=False)
    emb.add_field(name="Time:", value=mtg.time.strftime("%m/%d/%Y %H:%M:%S"), inline=False)
    emb.add_field(name="Users", value=str(len(mtg.id)) + " user(s) associated.", inline=False)
    emb.set_footer(text="Meeting ID: " + mtg.id)

    return emb


def allocate_meetings(meetings: list[meeting], channels: list[channel]):
    """Allocate meetings to channel"""
    mtg_copy = meetings.copy()

    # unallocated all channels
    for chnl in channels:
        chnl.allocated = []

    # check for zero channels
    if len(channels) > 0:
        # assign to each channel one at a time
        count = 0
        while len(mtg_copy) > 0:
            channels[count % len(channels)].allocated.append(mtg_copy.pop())
            count += 1


def upcoming_meeting_embed(mtg: meeting) -> discord.Embed:
    """Generate an embed for an upcoming meeting

    :param mtg: Meeting to send information about
    :return: Completed embed
    """
    # format datetime
    current_time = datetime.now()
    diff_time: timedelta = mtg.time - current_time
    diff_time_string = str(diff_time.days) + "D " + str(diff_time.seconds) + "S"

    # create embed
    emb = discord.Embed(title="Upcoming Meeting:")
    emb.add_field(name="Meeting Name:", value=mtg.name, inline=False)
    emb.add_field(name="Time:", value=mtg.time.strftime("%m/%d/%Y %H:%M:%S"), inline=False)
    emb.add_field(name="In:", value=diff_time_string, inline=False)
    emb.add_field(name="Users", value=str(len(mtg.users)) + " user(s) associated.", inline=False)
    emb.set_footer(text="Meeting ID: " + str(mtg.id))
    return emb


class meeting_cogs(commands.Cog):
    """Cogs that manage the creation of a meeting"""

    def __init__(self, bot):
        super().__init__()
        self.bot: discord.Bot = bot
        self.channels: list[channel] = db.load_all_channels()
        self.meetings: list[meeting] = meeting_sort(db.load_all_meetings())

    # create a slash command group
    meeting = SlashCommandGroup("meeting", "Manage and create meetings.", guild_ids=guild_ids)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        # setup meetings
        print(self.meetings)
        allocate_meetings(self.meetings, self.channels)
        await self.send_upcoming_meeting(self.channels)

    async def send_upcoming_meeting(self, chnl) -> list[channel]:
        """Add upcoming meeting information to the channels

        :param chnl: Channels to add allocate
        :return:
        """

        # iter through channels
        for c in chnl:
            # check if channel is out of control
            if c.status:
                # create channel object
                print(c.id)
                channel_loc = await self.bot.fetch_channel(c.id)
                print(channel_loc)

                # clear channel
                await channel_loc.purge()

                # print all meeting information
                for mtg in c.allocated:
                    await channel_loc.send(embed=upcoming_meeting_embed(mtg))

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

    @meeting.command(guild_ids=guild_ids, name="new_meeting_channel")
    async def new_meeting_channel(self, ctx):
        self.channels.append(db.create_channel(ctx.channel.id, True))

        # reset all allocations
        allocate_meetings()
        send_upcoming_meeting(self.channels)

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
        for meet in self.meetings:
            if meet.id == id:
                meet.time = time_obj

                # pass to db
                db.adjust_meeting(meet)

                await ctx.respond(embed=create_meeting_embed("Time adjusted!", meet))

        await ctx.respond("Meeting ID not found!")

    @meeting.command(guild_ids=guild_ids, name="view_meeting")
    async def view_meeting(self, ctx,
                           id: Option(str, name="meeting_id")):
        """View the information about a meeting

        :param ctx: Message context
        :param id: Message id
        :return:
        """

        # find meeting
        for meet in self.meetings:
            if meet.id == id:
                await ctx.respond(embed=create_meeting_embed("Meeting:", meet))

        # meeting not found
        await ctx.respond("Meeting ID not found!")

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
        for meet in self.meetings:
            if meet.id == id:
                meet.name = name

                # pass to db
                db.adjust_meeting(meet)

                await ctx.respond(embed=create_meeting_embed("Name adjusted!", meet))

        await ctx.respond("Meeting ID not found!")


def setup(bot: commands.Bot):
    """Set up the bot

    :param bot:
    :return:
    """
    bot.add_cog(meeting_cogs(bot))
