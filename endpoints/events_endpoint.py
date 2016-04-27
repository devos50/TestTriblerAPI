import json
from twisted.internet.task import LoopingCall
from twisted.web import server, resource
import tribler_utils


class EventsEndpoint(resource.Resource):

    isLeaf = True

    def __init__(self):
        resource.Resource.__init__(self)
        self.event_request = None

        # Schedule download status which is pushed every second
        lc = LoopingCall(self.upload_download_state).start(1)

    def upload_download_state(self):
        if self.event_request is None:
            return

        download_details = []
        for download in tribler_utils.tribler_data.downloads:
            download_details.append(download.get_json())
        self.event_request.write(json.dumps({"type": "downloads", "downloads": download_details}))

    def render_GET(self, request):
        self.event_request = request
        return server.NOT_DONE_YET
