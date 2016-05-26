import base64
from random import randint
import binascii


class Torrent:

    def __init__(self, id, infohash, name, length, category):
        self.id = id
        self.infohash = binascii.a2b_base64(infohash).encode('hex')
        self.name = name
        self.length = length
        self.category = category
        self.files = []
        self.time_added = randint(1200000000, 1460000000)

    def get_json(self):
        return {"name": self.name, "infohash": self.infohash, "length": self.length, "category": self.category}
