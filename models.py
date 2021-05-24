import discord
import util
from emoji import clean_emoji


class District:
    def __init__(self, bot, cat_id, role_id, station_id):
        self.bot = bot  # discord.CLient

        self.cat_id = cat_id  # Snowflake
        self.role_id = role_id  # Snowflake
        self.station_id = station_id  # Snowflake

    async def validate(self):
        # TODO: Add stuff
        return True


class Train:
    def __init__(self, bot, channel_id, role_id, direction, start):
        self.bot = bot  # discord.CLient

        self.channel_id = channel_id  # Snowflake
        self.role_id = role_id  # Snowflake

        self.direction = direction  # int
        self.start = start  # int index

        self.current_station = None  # discord.CategoryChannel
        self.current_announcement = None  # discord.Message

    async def validate(self):
        # TODO: Add stuff
        if not self.direction in [-1, 1]:
            return False

        return True

    async def announce_movement(self, curr_ind, next_ind, curr, nxt, arriving):
        curr_channel = self.bot.working_guild.get_channel(curr.cat_id)
        nxt_channel = self.bot.working_guild.get_channel(nxt.cat_id)

        s_map = util.draw_map(
            curr_ind,
            next_ind,
            self.direction,
            len(self.bot.metro_state.metro.stations),
            not arriving,
            self.bot.metro_state.metro.looped,
        )

        curr_name = clean_emoji(curr_channel.name)
        nxt_name = clean_emoji(nxt_channel.name)

        msg = f"Arriving at: **{curr_name}**\nNext stop: **{nxt_name}**"
        if not arriving:
            msg = f"Departing: **{curr_name}**\nNext stop: **{nxt_name}**"

        msg = f"{s_map}\n\n{msg}"
        msg = discord.utils.escape_mentions(msg)

        await self.announce(msg)

    async def announce(self, message):
        if not self.current_announcement:
            channel = self.bot.working_guild.get_channel(self.channel_id)
            msg = await channel.send(message)
            self.current_announcement = msg
        else:
            try:
                await self.current_announcement.edit(content=message)
            except:
                self.current_announcement = None
                await self.announce(message)

    async def arrive(self, dest):
        channel = self.bot.working_guild.get_channel(self.channel_id)
        role = self.bot.working_guild.get_role(self.role_id)
        dest_cat = self.bot.working_guild.get_channel(dest.cat_id)

        self.current_station = dest_cat

        await channel.edit(category=dest_cat, position=0)
        await dest_cat.set_permissions(role, read_messages=True)

    async def depart(self, transit_id):
        channel = self.bot.working_guild.get_channel(self.channel_id)
        role = self.bot.working_guild.get_role(self.role_id)
        transit_cat = self.bot.working_guild.get_channel(transit_id)

        await self.current_station.set_permissions(role, overwrite=None)
        self.current_station = None
        await channel.edit(category=transit_cat)


class Metro:
    def __init__(self, stations, trains, cat_id, looped, speed, wait):
        self.stations = stations  # List<District>
        self.trains = trains  # List<Train>

        self.cat_id = cat_id  # Snowflake
        self.looped = looped  # boolean
        self.speed = speed  # int: How long it takes to go to the next station
        self.wait = wait  # int: How long to wait at a station

    async def validate(self):
        # TODO: Add stuff
        return True


class App:
    def __init__(self, metro):
        self.started = None  # datetime.datetime
        self.metro = metro  # Metro
