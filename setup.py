import json

from models import Metro, District, Train


def setup(bot):
    with open("metro-config.json", encoding="utf8") as o:
        configs = json.loads(o.read())

    districts = [
        District(bot, d["cat_id"], d["role_id"], d["station_id"])
        for d in configs["districts"]
    ]

    metro = configs["metro"]
    trains = [
        Train(bot, t["channel_id"], t["role_id"], t["direction"], t["start"])
        for t in metro["trains"]
    ]

    transit_id = metro["cat_id"]
    looped = metro["looped"]
    speed = metro["speed"]
    wait = metro["wait"]

    new_metro = Metro(districts, trains, transit_id, looped, speed, wait)

    return new_metro
