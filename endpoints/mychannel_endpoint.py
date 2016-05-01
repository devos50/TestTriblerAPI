import json

from twisted.web import http, resource

import tribler_utils


class MyChannelEndpoint(resource.Resource):

    def getChild(self, path, request):
        if path == "overview":
            return MyChannelOverviewEndpoint()
        elif path == "torrents":
            return MyChannelTorrentsEndpoint()
        elif path == "rssfeeds":
            return MyChannelRssFeedsEndpoint()


class MyChannelOverviewEndpoint(resource.Resource):

    def render_GET(self, request):
            my_channel = tribler_utils.tribler_data.get_my_channel()
            if my_channel is None:
                request.setResponseCode(http.NOT_FOUND)
                return "your channel has not been created"

            request.setHeader('Content-Type', 'text/json')
            return json.dumps({'overview': {'identifier': my_channel.channel_id, 'name': my_channel.name,
                                            'description': my_channel.description}})


class MyChannelTorrentsEndpoint(resource.Resource):

    def render_GET(self, request):
        my_channel = tribler_utils.tribler_data.get_my_channel()
        if my_channel is None:
            request.setResponseCode(http.NOT_FOUND)
            return "your channel has not been created"

        request.setHeader('Content-Type', 'text/json')
        torrent_list = []
        for torrent in my_channel.torrents:
            torrent_list.append({'name': torrent.name, 'infohash': torrent.infohash, 'added': torrent.time_added})

        return json.dumps({"torrents": torrent_list})


class MyChannelRssFeedsEndpoint(resource.Resource):

    def render_GET(self, request):
        my_channel = tribler_utils.tribler_data.get_my_channel()
        if my_channel is None:
            request.setResponseCode(http.NOT_FOUND)
            return "your channel has not been created"

        request.setHeader('Content-Type', 'text/json')
        feeds_list = []
        for i in range(15):
            feeds_list.append({'url': 'http://test%d.com/feed.xml' % i})

        return json.dumps({"rssfeeds": feeds_list})
