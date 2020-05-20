import discord
import util


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

    async def validate(self):
        # TODO: Add stuff
        if not self.direction in [-1, 1]:
            return False

        return True

    async def announce_arrival(self, dest, nxt):
        dest_channel = self.bot.working_guild.get_channel(dest.cat_id)
        nxt_channel = self.bot.working_guild.get_channel(nxt.cat_id)

        msg = f"Arriving at: **{dest_channel.name}**\nNext stop: **{nxt_channel.name}**"

        msg = discord.utils.escape_mentions(msg)
        msg = util.fancify(msg)

        await self.announce(msg)

    async def announce_departure(self, curr, dest):
        curr_channel = self.bot.working_guild.get_channel(curr.cat_id)
        dest_channel = self.bot.working_guild.get_channel(dest.cat_id)

        msg = f"Departing: **{curr_channel.name}**\nNext stop: **{dest_channel.name}**"

        msg = discord.utils.escape_mentions(msg)
        msg = util.fancify(msg)

        await self.announce(msg)

    async def announce(self, message):
        channel = self.bot.working_guild.get_channel(self.channel_id)

        await channel.send(message)

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
