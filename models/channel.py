from random import randint
from utils import get_random_hex_string


class Channel:

    def __init__(self, id, name="", description=""):
        self.name = name
        self.description = description
        self.id = id
        self.channel_id = get_random_hex_string(40)
        self.votes = randint(0, 10000)
        self.spam_votes = randint(0, 10000)
        self.modified = randint(10, 10000)
        self.torrents = set()
        self.subscribed = False

    def add_torrent(self, torrent):
        self.torrents.add(torrent)

    def get_json(self):
        return {"id": self.id, "name": self.name, "description": self.description, "votes": self.votes,
                "torrents": len(self.torrents), "spam": self.spam_votes, "modified": self.modified,
                "sub": self.subscribed}
