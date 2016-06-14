from random import randint, sample
from models.channel import Channel
from models.download import Download
from models.playlist import Playlist
from models.torrent import Torrent


CREATE_MY_CHANNEL = False


class TriblerData:

    def __init__(self):
        self.channels = []
        self.torrents = []
        self.torrent_files = {}
        self.subscribed_channels = set()
        self.downloads = []
        self.my_channel = -1
        self.rss_feeds = []

        self.read_torrent_files()
        self.generate_torrents()
        self.generate_channels()
        self.assign_subscribed_channels()
        self.assign_torrents_to_channels()
        self.generate_downloads()
        self.generate_rss_feeds()
        self.generate_playlists()

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

        num_channels = randint(300, len(channel_name_desc_pairs))
        for i in range(0, num_channels):
            rand_index = randint(0, len(channel_name_desc_pairs) - 1)
            pair = channel_name_desc_pairs[rand_index]
            del channel_name_desc_pairs[rand_index]
            self.channels.append(Channel(i, name=pair[0], description=pair[1]))

        if CREATE_MY_CHANNEL:
            # Pick one of these channels as your channel
            self.my_channel = randint(0, len(self.channels))

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

    def generate_rss_feeds(self):
        for i in range(randint(10, 30)):
            self.rss_feeds.append('http://test%d.com/feed.xml' % i)

    def assign_torrents_to_channels(self):
        for channel in self.channels:
            num_torrents_in_channel = randint(0, len(self.torrents) - 1)
            for i in range(0, num_torrents_in_channel):
                channel.add_torrent(self.torrents[randint(0, len(self.torrents) - 1)])

    def get_channel_with_id(self, id):
        for channel in self.channels:
            if str(channel.id) == id:
                return channel

    def get_channel_with_cid(self, cid):
        for channel in self.channels:
            if str(channel.cid) == cid:
                return channel

    def get_my_channel(self):
        if self.my_channel == -1:
            return None
        return self.channels[self.my_channel]

    def get_download_with_infohash(self, infohash):
        for download in self.downloads:
            if download.torrent.infohash == infohash:
                return download

    def generate_downloads(self):
        random_torrents = sample(self.torrents, randint(10, 30))
        for torrent in random_torrents:
            self.downloads.append(Download(torrent))

    def generate_playlists(self):
        for channel in self.channels:
            num_playlists = randint(1, 5)
            for i in range(num_playlists):
                playlist = Playlist(i, "Test playlist %d" % randint(1, 40), "This is a description")

                picked_torrents = sample(channel.torrents, randint(0, min(20, len(channel.torrents))))
                for torrent in picked_torrents:
                    playlist.add_torrent(torrent)

                channel.add_playlist(playlist)
