import json
from random import randint, sample

import time
from twisted.web import resource

import tribler_utils


class SearchEndpoint(resource.Resource):

    isLeaf = True

    def __init__(self, events_endpoint):
        resource.Resource.__init__(self)
        self.events_endpoint = events_endpoint

    def render_GET(self, request):
        # Just ignore the query and return some random channels/torrents
        num_channels = len(tribler_utils.tribler_data.channels)
        num_torrents = len(tribler_utils.tribler_data.torrents)

        picked_channels = sample(range(0, num_channels - 1), randint(0, num_channels - 1))
        picked_torrents = sample(range(0, num_torrents - 1), randint(0, num_channels - 1))

        channels_json = []
        for index in picked_channels:
            channels_json.append(tribler_utils.tribler_data.channels[index].get_json())

        self.events_endpoint.on_search_results_channels(channels_json)

        torrents_json = []
        for index in picked_torrents:
            torrents_json.append(tribler_utils.tribler_data.torrents[index].get_json())

        self.events_endpoint.on_search_results_torrents(torrents_json)

        return json.dumps({"queried": True})
