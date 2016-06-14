import json
from twisted.web import http, resource
import tribler_utils


class DownloadsEndpoint(resource.Resource):

    def render_GET(self, request):
        return json.dumps({"downloads": [download.get_json() for download in tribler_utils.tribler_data.downloads]})

    def getChild(self, path, request):
        return DownloadEndpoint(path)


class DownloadEndpoint(resource.Resource):

    def __init__(self, infohash):
        resource.Resource.__init__(self)
        self.infohash = infohash

        self.putChild("remove", DownloadRemoveEndpoint(self.infohash))
        self.putChild("stop", DownloadStopEndpoint(self.infohash))
        self.putChild("resume", DownloadResumeEndpoint(self.infohash))
        self.putChild("forcerecheck", DownloadForceRecheckEndpoint(self.infohash))


class DownloadBaseEndpoint(resource.Resource):

    def __init__(self, infohash):
        resource.Resource.__init__(self)
        self.infohash = infohash

    @staticmethod
    def return_404(request, message="the download with given infohash does not exist"):
        """
        Returns a 404 response code if your channel has not been created.
        """
        request.setResponseCode(http.NOT_FOUND)
        return json.dumps({"error": message})


class DownloadRemoveEndpoint(DownloadBaseEndpoint):

    def render_DELETE(self, request):
        request.setHeader('Content-Type', 'text/json')
        download = tribler_utils.tribler_data.get_download_with_infohash(self.infohash)
        if download is None:
            DownloadRemoveEndpoint.return_404(request)

        parameters = http.parse_qs(request.content.read(), 1)
        if 'remove_data' not in parameters or len(parameters['remove_data']) == 0:
            request.setResponseCode(http.BAD_REQUEST)
            return json.dumps({"error": "remove_data parameter missing"})

        tribler_utils.tribler_data.downloads.remove(download)

        return json.dumps({"removed": True})


class DownloadResumeEndpoint(DownloadBaseEndpoint):

    def render_POST(self, request):
        request.setHeader('Content-Type', 'text/json')
        download = tribler_utils.tribler_data.get_download_with_infohash(self.infohash)
        if download is None:
            DownloadResumeEndpoint.return_404(request)

        download.status = 3

        return json.dumps({"resumed": True})


class DownloadStopEndpoint(DownloadBaseEndpoint):

    def render_POST(self, request):
        request.setHeader('Content-Type', 'text/json')
        download = tribler_utils.tribler_data.get_download_with_infohash(self.infohash)
        if download is None:
            DownloadRemoveEndpoint.return_404(request)

        download.status = 5

        return json.dumps({"stopped": True})


class DownloadForceRecheckEndpoint(DownloadBaseEndpoint):

    def render_POST(self, request):
        request.setHeader('Content-Type', 'text/json')
        download = tribler_utils.tribler_data.get_download_with_infohash(self.infohash)
        if download is None:
            DownloadRemoveEndpoint.return_404(request)

        download.status = 2

        return json.dumps({"forcedrecheck": True})
