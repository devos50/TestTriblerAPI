from random import randint
from models.channel import Channel
from models.torrent import Torrent


class TriblerData:

    def __init__(self):
        self.channels = []
        self.torrents = []
        self.torrent_files = {}
        self.subscribed_channels = set()

        self.read_torrent_files()
        self.generate_torrents()
        self.generate_channels()
        self.assign_subscribed_channels()
        self.assign_torrents_to_channels()

    # Generate channels from the random_channels file
    def generate_channels(self):
        # Read random channels file
        channel_name_desc_pairs = []
        with open("data/random_channels.dat") as random_channels_file:
            content = random_channels_file.readlines()
            for channel_name_desc in content:
                item_parts = channel_name_desc.split("\t")
                desc = ""
                if len(item_parts) == 2:
                    desc = item_parts[1]
                channel_name_desc_pairs.append((item_parts[0], desc))

        num_channels = randint(1000, len(channel_name_desc_pairs))
        for i in range(1, num_channels):
            rand_index = randint(0, len(channel_name_desc_pairs) - 1)
            pair = channel_name_desc_pairs[rand_index]
            del channel_name_desc_pairs[rand_index]
            self.channels.append(Channel(i, name=pair[0], description=pair[1]))

    def assign_subscribed_channels(self):
        # Make between 10 and 50 channels subscribed channels
        num_subscribed = randint(10, 50)
        for i in range(0, num_subscribed):
            channel_index = randint(0, len(self.channels) - 1)
            self.subscribed_channels.add(channel_index)
            self.channels[channel_index].subscribed = True

    def read_torrent_files(self):
        with open("data/torrent_files.dat") as torrent_files_file:
            content = torrent_files_file.readlines()
            for torrent_file_line in content:
                parts = torrent_file_line.split("\t")
                torrent_id = parts[0]
                if torrent_id not in self.torrent_files:
                    self.torrent_files[torrent_id] = []
                self.torrent_files[torrent_id].append({"path": parts[1], "length": parts[2]})

    def generate_torrents(self):
        # Create random torrents in channels
        with open("data/random_torrents.dat") as random_torrents:
            content = random_torrents.readlines()
            for random_torrent in content:
                random_torrent = random_torrent.rstrip()
                torrent_parts = random_torrent.split("\t")
                torrent = Torrent(*torrent_parts)
                if torrent_parts[0] in self.torrent_files:
                    torrent.files = self.torrent_files[torrent_parts[0]]
                self.torrents.append(torrent)

    def assign_torrents_to_channels(self):
        for channel in self.channels:
            num_torrents_in_channel = randint(0, len(self.torrents) - 1)
            for i in range(0, num_torrents_in_channel):
                channel.add_torrent(self.torrents[randint(0, len(self.torrents) - 1)])

    def get_channel_with_id(self, id):
        for channel in self.channels:
            if str(channel.id) == id:
                return channel
