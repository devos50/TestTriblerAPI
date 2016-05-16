import json
from twisted.web import resource
import tribler_utils


class DownloadsEndpoint(resource.Resource):

    def render_GET(self, request):
        download_details = []
        for download in tribler_utils.tribler_data.downloads:
            download_details.append(download.get_json())

        return json.dumps({"downloads": download_details})
