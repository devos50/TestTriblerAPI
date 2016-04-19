from twisted.web import resource
from channels_endpoint import ChannelsEndpoint
from endpoints.channel_endpoint import ChannelEndpoint
from endpoints.events_endpoint import EventsEndpoint
from endpoints.search_endpoint import SearchEndpoint
from settings_endpoint import SettingsEndpoint


class RootEndpoint(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)

        self.search_endpoint = SearchEndpoint()
        self.putChild("search", self.search_endpoint)

        self.channel_endpoint = ChannelEndpoint()
        self.putChild("channel", self.channel_endpoint)

        self.channels_endpoint = ChannelsEndpoint()
        self.putChild("channels", self.channels_endpoint)

        self.settings_endpoint = SettingsEndpoint()
        self.putChild("settings", self.settings_endpoint)

        self.events_endpoint = EventsEndpoint()
        self.putChild("events", self.events_endpoint)
