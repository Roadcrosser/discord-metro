import discord
import asyncio
import setup
import json
import datetime

from models import App

with open("bot-config.json", encoding="utf8") as o:
    botconfigs = json.loads(o.read())


bot = discord.Client(
    intents=discord.Intents(
        guilds=True, guild_messages=True, guild_reactions=True, members=True
    )
)
metro = setup.setup(bot)

# All extra attributes defined here
bot.metro_state = App(metro)
bot.working_guild = None


@bot.event
async def on_ready():
    print(f"Running on {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
    working_guild = bot.get_guild(botconfigs["working-guild"])

    if not working_guild:
        raise ValueError("Working Guild not found!")

    bot.working_guild = working_guild

    if bot.metro_state.started == None:
        bot.metro_state.started = datetime.datetime.utcnow()
        for t in bot.metro_state.metro.trains:
            bot.loop.create_task(train_loop(t))


# Here's an idea, the train channels are voice channels instead because thats totally more immersive. Do think about it.
async def train_loop(train):
    metro = bot.metro_state.metro
    stations = metro.stations
    curr_ind = train.start
    curr_ind = curr_ind % len(stations)
    next_ind = curr_ind + train.direction
    next_ind = next_ind % len(stations)
    while True:
        current_station = stations[curr_ind]
        next_station = stations[next_ind]

        await train.announce_movement(
            curr_ind, next_ind, current_station, next_station, True
        )
        await train.arrive(current_station)

        await asyncio.sleep(metro.wait)

        await train.announce_movement(
            curr_ind, next_ind, current_station, next_station, False
        )
        await train.depart(metro.cat_id)

        await asyncio.sleep(metro.speed)

        curr_ind = next_ind
        next_ind += train.direction

        if (not metro.looped) and (next_ind < 0 or next_ind >= len(stations)):
            train.direction *= -1
            next_ind = curr_ind + train.direction

        next_ind = next_ind % len(stations)


bot.run(botconfigs["token"])
