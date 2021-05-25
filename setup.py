import json

from models import Metro, District, Train


def setup(bot):
    with open("metro-config.json", encoding="utf8") as o:
        configs = json.loads(o.read())

    metro = configs["metro"]

    districts = [
        District(
            bot,
            d["cat_id"],
            d["role_id"],
            d["station_id"],
            configs["districts"],
            metro["trains"],
        )
        for d in configs["districts"]
    ]

    trains = [
        Train(
            bot,
            t["channel_id"],
            t["role_id"],
            t["direction"],
            t["start"],
            t["button"],
            metro["control_room"],
        )
        for t in metro["trains"]
    ]

    transit_id = metro["cat_id"]
    looped = metro["looped"]
    speed = metro["speed"]
    wait = metro["wait"]

    new_metro = Metro(districts, trains, transit_id, looped, speed, wait)

    return new_metro
