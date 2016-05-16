from twisted.web import resource
from channels_endpoint import ChannelsEndpoint
from endpoints.channel_endpoint import ChannelEndpoint
from endpoints.downloads_endpoint import DownloadsEndpoint
from endpoints.events_endpoint import EventsEndpoint
from endpoints.mychannel_endpoint import MyChannelEndpoint
from endpoints.search_endpoint import SearchEndpoint
from endpoints.variables_endpoint import VariablesEndpoint
from settings_endpoint import SettingsEndpoint


class RootEndpoint(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)

        self.events_endpoint = EventsEndpoint()
        self.putChild("events", self.events_endpoint)

        self.search_endpoint = SearchEndpoint(self.events_endpoint)
        self.putChild("search", self.search_endpoint)

        self.mychannel_endpoint = MyChannelEndpoint()
        self.putChild("mychannel", self.mychannel_endpoint)

        self.channel_endpoint = ChannelEndpoint()
        self.putChild("channel", self.channel_endpoint)

        self.channels_endpoint = ChannelsEndpoint()
        self.putChild("channels", self.channels_endpoint)

        self.settings_endpoint = SettingsEndpoint()
        self.putChild("settings", self.settings_endpoint)

        self.variables_endpoint = VariablesEndpoint()
        self.putChild("variables", self.variables_endpoint)

        self.downloads_endpoint = DownloadsEndpoint()
        self.putChild("downloads", self.downloads_endpoint)

