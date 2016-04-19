import json

from twisted.web import resource

import tribler_utils


class ChannelEndpoint(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        return ChannelDetailEndpoint(path)


class ChannelDetailEndpoint(resource.Resource):

    def __init__(self, channel_id):
        resource.Resource.__init__(self)

        self.channel_torrents_endpoint = ChannelTorrentsEndpoint(channel_id)
        self.putChild("torrents", self.channel_torrents_endpoint)


class ChannelTorrentsEndpoint(resource.Resource):

    isLeaf = True

    def __init__(self, channel_id):
        resource.Resource.__init__(self)
        self.channel_id = channel_id

    def render_GET(self, request):
        results_json = []
        channel = tribler_utils.tribler_data.get_channel_with_id(self.channel_id)
        for torrent in channel.torrents:
            results_json.append(torrent.get_json())

        return json.dumps({"torrents": results_json})
