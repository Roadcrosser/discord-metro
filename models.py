import discord
import util
from emoji import clean_emoji


class District:
    def __init__(self, bot, cat_id, role_id, station_id, stations, trains):
        self.bot = bot  # discord.CLient

        self.cat_id = cat_id  # Snowflake
        self.role_id = role_id  # Snowflake
        self.station_id = station_id  # Snowflake

        self.current_announcement = None  # discord.Message

        self.station_list = stations  # List<Dict>
        self.train_list = trains  # List<Dict>

    async def validate(self):
        # I don't think there's anything *to* validate here.
        return True

    async def reset_perms(self):
        cat = self.bot.working_guild.get_channel(self.cat_id)
        for t in self.train_list:
            train_role = self.bot.working_guild.get_role(t["role_id"])
            if not cat.overwrites_for(train_role).is_empty():
                await cat.set_permissions(train_role, overwrite=None)

    async def announce_platform(self):
        category = self.bot.working_guild.get_channel(self.cat_id)
        msg = f"You are at: {clean_emoji(category.name)}\n"

        station_index = 0
        for s in self.station_list:
            if self.cat_id == s["cat_id"]:
                break
            station_index += 1

        # TODO: Add more comprehensive station naming
        for t in self.train_list:
            next_station_index = (station_index + t["direction"]) % len(
                self.station_list
            )
            next_station = self.station_list[next_station_index]
            next_station_cat = self.bot.working_guild.get_channel(
                next_station["cat_id"]
            )

            msg += f"\n{t['button']}: {clean_emoji(next_station_cat.name)}"

        msg += "\n\nReact below to board the next train."

        await self.announce(msg)

    async def announce(self, message):
        if not self.current_announcement:
            channel = self.bot.working_guild.get_channel(self.station_id)
            # Get last message. We have to do this instead of deleting/resending because of caching issues.
            async for msg in channel.history(oldest_first=False):
                if msg.author.id == self.bot.user.id:
                    self.current_announcement = msg
                    break

            # If loop turns up empty, send a message
            if not self.current_announcement:
                msg = await channel.send(message)
                for t in self.train_list:
                    await msg.add_reaction(t["button"])
                self.current_announcement = await channel.fetch_message(
                    msg.id
                )  # Grab the message again so we get reaction info
                return

        try:
            await self.current_announcement.edit(content=message)
        except:
            self.current_announcement = None
            await self.announce(message)


class Train:
    def __init__(
        self, bot, channel_id, role_id, direction, start, button, control_room
    ):
        self.bot = bot  # discord.CLient

        self.channel_id = channel_id  # Snowflake
        self.role_id = role_id  # Snowflake

        self.direction = direction  # int
        self.start = start  # int index

        self.button = button  # str emoji

        self.current_station = None  # District
        self.current_station_cat = None  # discord.CategoryChannel
        self.current_announcement = None  # discord.Message

        self.control_room = control_room

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

        msg = f"{s_map}\n\n{msg}\n\nReact below to disembark at the {'current' if arriving else 'next'} stop."
        msg = discord.utils.escape_mentions(msg)

        await self.announce(msg)

    async def announce(self, message):
        if not self.current_announcement:
            channel = self.bot.working_guild.get_channel(self.channel_id)
            # Get last message. We have to do this instead of deleting/resending because of caching issues.
            async for msg in channel.history(oldest_first=False):
                if msg.author.id == self.bot.user.id:
                    self.current_announcement = msg
                    break

            # If loop turns up empty, send a message
            if not self.current_announcement:
                msg = await channel.send(message)
                await msg.add_reaction(util.EJECT_SYMBOL)
                self.current_announcement = await channel.fetch_message(
                    msg.id
                )  # Grab the message again so we get reaction info
                return

        try:
            await self.current_announcement.edit(content=message)
        except:
            self.current_announcement = None
            await self.announce(message)

    async def arrive(self, dest):
        channel = self.bot.working_guild.get_channel(self.channel_id)
        train_role = self.bot.working_guild.get_role(self.role_id)
        dest_cat = self.bot.working_guild.get_channel(dest.cat_id)

        self.current_station = dest
        self.current_station_cat = dest_cat

        await dest_cat.set_permissions(train_role, read_messages=True)
        await channel.edit(category=dest_cat, position=0)

        if not (self.current_announcement):
            return

        # Disembark scheduled passengers
        self.current_announcement = await channel.fetch_message(
            self.current_announcement.id
        )
        reaction = self.current_announcement.reactions[0]
        async for user in reaction.users():
            if user.bot:
                continue
            await reaction.remove(user)
            await self.disembark(user)

    async def depart(self, transit_id):
        channel = self.bot.working_guild.get_channel(self.channel_id)
        train_role = self.bot.working_guild.get_role(self.role_id)
        transit_cat = self.bot.working_guild.get_channel(transit_id)

        self.current_station.current_announcement = await self.bot.working_guild.get_channel(
            self.current_station.station_id
        ).fetch_message(
            self.current_station.current_announcement.id
        )
        platform_message = self.current_station.current_announcement
        if not platform_message:
            return

        for reaction in platform_message.reactions:
            if reaction.emoji != self.button:
                continue

            async for user in reaction.users():
                if user.bot:
                    continue
                await reaction.remove(user)
                await self.embark(user)

        await self.current_station_cat.set_permissions(train_role, overwrite=None)
        await channel.edit(category=transit_cat)
        self.current_station = None
        self.current_station_cat = None

    async def disembark(self, user):
        train_role = self.bot.working_guild.get_role(self.role_id)
        dest_role = self.bot.working_guild.get_role(self.current_station.role_id)

        member = self.bot.working_guild.get_member(user.id)
        if not member:
            return

        if util.has_role(member, train_role):
            await member.remove_roles(train_role)
            if not util.has_role(member, dest_role):
                await member.add_roles(dest_role)
                await self.log_user_movement(member, self.current_station_cat, False)

    async def embark(self, user):
        train_role = self.bot.working_guild.get_role(self.role_id)
        station_role = self.bot.working_guild.get_role(self.current_station.role_id)

        member = self.bot.working_guild.get_member(user.id)
        if not member:
            return

        # prevent members from getting on two trains at once
        if util.has_role(member, station_role):
            await member.remove_roles(station_role)
            if not util.has_role(member, train_role):
                await member.add_roles(train_role)
                await self.log_user_movement(member, self.current_station_cat, True)

    async def log_user_movement(self, user, station, boarding):
        control_room_channel = self.bot.working_guild.get_channel(self.control_room)
        await control_room_channel.send(
            "{} **{}**#**{}** {} <#{}> {} {}".format(
                "📥" if boarding else "📤",
                clean_emoji(user.name),
                user.discriminator,
                "boarded" if boarding else "disembarked",
                self.channel_id,
                "from" if boarding else "to",
                clean_emoji(station.name),
            )
        )


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
