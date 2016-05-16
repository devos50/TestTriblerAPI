from random import randint, uniform
from constants import DLSTATUS_STRINGS


class Download:

    def __init__(self, torrent):
        self.torrent = torrent
        self.status = randint(0, 8)
        self.peers = randint(0, 1000)
        self.seeds = randint(0, 1000)
        self.progress = uniform(0, 1)
        self.down_speed = randint(0, 1000000)
        self.up_speed = randint(0, 1000000)

    def get_json(self):
        return {"name": self.torrent.name, "infohash": self.torrent.infohash, "status": DLSTATUS_STRINGS[self.status],
                "peers": self.peers, "seeds": self.seeds, "progress": self.progress, "size": self.torrent.length,
                "speed_down": self.down_speed, "speed_up": self.up_speed, "eta": 1234}
