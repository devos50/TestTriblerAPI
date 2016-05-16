import json
from twisted.internet.task import LoopingCall
from twisted.web import server, resource
import tribler_utils


class EventsEndpoint(resource.Resource):

    isLeaf = True

    def __init__(self):
        resource.Resource.__init__(self)
        self.event_request = None

    def on_search_results_channels(self, results):
        for result in results:
            self.event_request.write(json.dumps({"type": "search_result_channel", "result": result}) + '\n')

    def on_search_results_torrents(self, results):
        for result in results:
            self.event_request.write(json.dumps({"type": "search_result_torrent", "result": result}) + '\n')

    def render_GET(self, request):
        self.event_request = request

        request.write(json.dumps({"type": "events_start"}))

        return server.NOT_DONE_YET
