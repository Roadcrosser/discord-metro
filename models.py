class District:
    def __init__(self, cat_id, role_id, station_id):
        self.cat_id = cat_id  # Snowflake
        self.role_id = role_id  # Snowflake
        self.station_id = station_id  # Snowflake

class Train:
    def __init__(self, channel_id, role_id, direction, start):
        self.channel_id = channel_id  # Snowflake
        self.role_id = role_id  # Snowflake

        self.direction = direction  # int
        self.start = start  # int index


class Metro:
    def __init__(self, stations, trains, looped, speed, wait):
        self.stations = stations  # List<District>
        self.trains = trains  # List<Train>
        self.looped = looped  # boolean
        self.speed = speed  # int: How long it takes to go to the next station
        self.wait = wait  # int: How long to wait at a station


class App:
    def __init__(self, metro):
        self.started = None  # datetime.datetime
        self.metro = metro  # Metro
