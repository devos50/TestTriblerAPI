import json
from twisted.web import resource
import tribler_utils


class ChannelsEndpoint(resource.Resource):

    def getChild(self, path, request):
        if path == "subscribed":
            return ChannelsSubscribedEndpoint()
        elif path == "all":
            return ChannelsAllEndpoint()


class ChannelsSubscribedEndpoint(resource.Resource):

    isLeaf = True

    def render_GET(self, request):
        subscribed = []
        for channel_id in tribler_utils.tribler_data.subscribed_channels:
            subscribed.append(tribler_utils.tribler_data.channels[channel_id].get_json())
        return json.dumps({"subscribed": subscribed})


class ChannelsAllEndpoint(resource.Resource):

    isLeaf = True

    def render_GET(self, request):
        channels = []
        for channel in tribler_utils.tribler_data.channels:
            channels.append(channel.get_json())
        return json.dumps({"channels": channels}, ensure_ascii=False)
