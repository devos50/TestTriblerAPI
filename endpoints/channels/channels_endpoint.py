import json
from random import sample

from twisted.web import http, resource

import tribler_utils


class BaseChannelsEndpoint(resource.Resource):

    @staticmethod
    def return_404(request, message="the channel with the provided cid is not known"):
        """
        Returns a 404 response code if your channel has not been created.
        """
        request.setResponseCode(http.NOT_FOUND)
        return json.dumps({"error": message})


class ChannelsEndpoint(BaseChannelsEndpoint):

    def __init__(self):
        BaseChannelsEndpoint.__init__(self)

        child_handler_dict = {"subscribed": ChannelsSubscribedEndpoint, "discovered": ChannelsDiscoveredEndpoint,
                              "popular": ChannelsPopularEndpoint}
        for path, child_cls in child_handler_dict.iteritems():
            self.putChild(path, child_cls())


class ChannelsSubscribedEndpoint(resource.Resource):

    def getChild(self, path, request):
        return ChannelsModifySubscriptionEndpoint(path)

    def render_GET(self, request):
        subscribed = []
        for channel_id in tribler_utils.tribler_data.subscribed_channels:
            subscribed.append(tribler_utils.tribler_data.channels[channel_id].get_json())
        return json.dumps({"subscribed": subscribed})


class ChannelsModifySubscriptionEndpoint(BaseChannelsEndpoint):

    def __init__(self, cid):
        BaseChannelsEndpoint.__init__(self)
        self.cid = cid

    def render_PUT(self, request):
        request.setHeader('Content-Type', 'text/json')

        channel = tribler_utils.tribler_data.get_channel_with_cid(self.cid)
        if channel is None:
            return ChannelsModifySubscriptionEndpoint.return_404(request)

        if channel.subscribed:
            request.setResponseCode(http.CONFLICT)
            return json.dumps({"error": "you are already subscribed to this channel"})

        tribler_utils.tribler_data.subscribed_channels.add(channel.id)
        channel.subscribed = True

        return json.dumps({"subscribed": True})

    def render_DELETE(self, request):
        request.setHeader('Content-Type', 'text/json')

        channel = tribler_utils.tribler_data.get_channel_with_cid(self.cid)
        if channel is None:
            return ChannelsModifySubscriptionEndpoint.return_404(request)

        if not channel.subscribed:
            return ChannelsModifySubscriptionEndpoint.return_404(request,
                                                                 message="you are not subscribed to this channel")

        tribler_utils.tribler_data.subscribed_channels.remove(channel.id)
        channel.subscribed = False

        return json.dumps({"unsubscribed": True})


class ChannelsDiscoveredEndpoint(resource.Resource):

    def getChild(self, path, request):
        return ChannelsDiscoveredSpecificEndpoint(path)

    def render_GET(self, request):
        channels = []
        for channel in tribler_utils.tribler_data.channels:
            channels.append(channel.get_json())
        return json.dumps({"channels": channels}, ensure_ascii=False)


class ChannelsDiscoveredSpecificEndpoint(BaseChannelsEndpoint):

    def __init__(self, cid):
        BaseChannelsEndpoint.__init__(self)

        child_handler_dict = {"torrents": ChannelTorrentsEndpoint, "playlists": ChannelPlaylistsEndpoint}
        for path, child_cls in child_handler_dict.iteritems():
            self.putChild(path, child_cls(cid))


class ChannelTorrentsEndpoint(BaseChannelsEndpoint):

    def __init__(self, cid):
        BaseChannelsEndpoint.__init__(self)
        self.cid = cid

    def render_GET(self, request):
        channel = tribler_utils.tribler_data.get_channel_with_cid(self.cid)
        if channel is None:
            return ChannelsModifySubscriptionEndpoint.return_404(request)

        results_json = []
        for torrent in channel.torrents:
            results_json.append(torrent.get_json())

        return json.dumps({"torrents": results_json})


class ChannelPlaylistsEndpoint(BaseChannelsEndpoint):

    def __init__(self, cid):
        BaseChannelsEndpoint.__init__(self)
        self.cid = cid

    def render_GET(self, request):
        channel = tribler_utils.tribler_data.get_channel_with_cid(self.cid)
        if channel is None:
            return BaseChannelsEndpoint.return_404(request)

        playlists = []
        for playlist in channel.playlists:
            playlists.append(playlist.get_json())

        return json.dumps({"playlists": playlists})


class ChannelsPopularEndpoint(BaseChannelsEndpoint):

    def render_GET(self, request):
        results_json = [channel.get_json() for channel in sample(tribler_utils.tribler_data.channels, 20)]
        return json.dumps({"channels": results_json})
