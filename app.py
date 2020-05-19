import discord
import setup
import models
import json
import datetime

with open("bot-config.json", encoding="utf8") as o:
    botconfigs = json.loads(o.read())

metro = setup.setup()

bot = discord.Client()
bot._metro_state = models.App(metro)


@bot.event
async def on_ready():
    print(f"Running on {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
    await bot.user.edit(avatar=open("icon.png", "rb").read())

    if bot._metro_state.started == None:
        bot._metro_state.started = datetime.datetime.utcnow()


bot.run(botconfigs["token"])
