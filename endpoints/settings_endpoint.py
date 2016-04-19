import json
from twisted.web import resource


class SettingsEndpoint(resource.Resource):

    isLeaf = True

    def render_GET(self, request):
        return json.dumps({"video": {"port": "1337"}})
