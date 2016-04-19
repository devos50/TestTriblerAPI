

class Torrent:

    def __init__(self, id, infohash, name, length, category):
        self.id = id
        self.infohash = infohash
        self.name = name
        self.length = length
        self.category = category
        self.files = []

    def get_json(self):
        return {"name": self.name, "infohash": self.infohash, "length": self.length, "category": self.category}
